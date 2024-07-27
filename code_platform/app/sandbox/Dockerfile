FROM python:3.9-slim

# Установка Node.js для JavaScript, если это необходимо
RUN apt-get update && apt-get install -y nodejs npm

# Копирование файлов в контейнер
COPY code_executor.py /app/code_executor.py

WORKDIR /app

ENTRYPOINT ["python", "/app/code_executor.py"]
