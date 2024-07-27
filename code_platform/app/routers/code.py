from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import docker
from docker.errors import ContainerError, ImageNotFound, APIError
import tempfile
import os

router = APIRouter()

client = docker.from_env()

class CodeExecution(BaseModel):
    code: str
    language: str

@router.post("/execute")
async def execute_code_endpoint(execution: CodeExecution):
    image_name = "code_platform_sandbox:latest"
    container = None
    temp_filename = None
    try:
        # Проверка наличия образа
        client.images.get(image_name)
    except ImageNotFound:
        # Попытка создать образ, если он не найден
        try:
            client.images.build(path="./sandbox", tag=image_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error building image: {e}")

    try:
        # Создание временного файла для кода
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{execution.language}") as temp_file:
            temp_file.write(execution.code.encode())
            temp_filename = temp_file.name
        
        # Монтирование временного каталога в контейнер
        volume_bindings = {os.path.dirname(temp_filename): {'bind': '/mnt/tmp', 'mode': 'rw'}}
        
        # Запуск Docker контейнера с кодом *обезательно не забыть пересобрать еге ! 
        container = client.containers.run(
            image_name,
            f"/mnt/tmp/{os.path.basename(temp_filename)} {execution.language}",
            detach=True,
            remove=False,  # Не удалять сразу, чтобы получить логи иначе будет пустота в ответе
            stdout=True,
            stderr=True,
            network_disabled=True,  # Отключение сети для безопасности
            mem_limit="128m",  # Ограничение памяти *В теории можно делить на 2*
            cpu_period=100000, #Ограничение на время выполнение
            cpu_quota=50000,  # Ограничение ЦПУ
            volumes=volume_bindings  # Монтирование томов что бы был доступ к временному файлу
        )
        
        
        
        # Ожидание завершения выполнения
        container.wait()
        logs = container.logs().decode("utf-8")
        return {"output": logs}
    
    #TODO:
    # Переписать типы ошибок нормально
    
    except ContainerError as e:
        raise HTTPException(status_code=500, detail=f"Container error: {e}")
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"Docker API error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        if container:
            container.remove(v=True, force=True)
        # Удаление временного файла
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)