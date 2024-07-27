import sys

def execute_code(file_path, language):
    with open(file_path, 'r') as file:
        code = file.read()

    if language == "python":
        exec(code)
    elif language == "javascript":
        import subprocess
        result = subprocess.run(["node", "-e", code], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    else:
        print("Unsupported language")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: code_executor.py <file_path> <language>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    language = sys.argv[2]
    execute_code(file_path, language)
