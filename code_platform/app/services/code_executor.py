import subprocess
import sys

def execute_code(code: str, language: str) -> str:
    if language == "python":
        result = subprocess.run(["python3", "-c", code], capture_output=True, text=True)
    elif language == "javascript":
        result = subprocess.run(["node", "-e", code], capture_output=True, text=True)
    else:
        return "Unsupported language"

    return result.stdout if result.returncode == 0 else result.stderr

if __name__ == "__main__":
    code = sys.argv[1]
    language = sys.argv[2]
    print(execute_code(code, language))
