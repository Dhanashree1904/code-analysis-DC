import os, hashlib

def load_code_files(folder):
    code_files = []
    for root, _, files in os.walk(folder):
        for f in files:
            path = os.path.join(root, f)
            if path.endswith((".c", ".cpp", ".py", ".js", ".ps1", ".go", ".java")):
                try:
                    with open(path, "r", errors="ignore") as file:
                        content = file.read()
                    sha = hashlib.sha256(content.encode()).hexdigest()
                    code_files.append({
                        "path": path,
                        "hash": sha,
                        "content": content
                    })
                except Exception as e:
                    print(f"Error reading {path}: {e}")
    return code_files
