import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found. Please add it to .env")

# OpenRouter API endpoint
URL = "https://openrouter.ai/api/v1/chat/completions"

def analyze_with_deepseek(code, filename):
    prompt_content = f"""
You are a malware code analyst.
Analyze this source code from {filename}.

1. What is the purpose of this code? (high-level summary in plain words)
2. Which specific lines or functions are suspicious or malicious? (with line numbers + reasoning)
3. What coding patterns indicate malware behavior? (e.g., process injection, persistence setup, API misuse)
4. What external libraries, APIs, or system calls are used, and why might they be suspicious?
5. Does the code perform file system operations? (read/write/delete, suspicious paths, temp files)
6. Does it contain network-related code? (sockets, HTTP requests, DNS lookups, hardcoded IPs/domains)
7. Does the code manipulate processes or services? (process creation, privilege escalation, service installation)
8. Does it interact with system resources? (registry, drivers, scheduled tasks, kernel functions)
9. Does it use obfuscation or evasion techniques? (encoded strings, encryption, anti-VM, anti-debug tricks)
10. Does it attempt data collection or exfiltration? (credentials, keystrokes, clipboard, environment variables)
11. Which parts of the code look incomplete, obfuscated, or intentionally misleading?
12. What MITRE ATT&CK techniques apply to this code? (list T-codes + explanation)
13. What is the overall risk rating of this code? (Low / Medium / High)
14. What recommendations should an analyst consider? (further dynamic analysis, sandbox execution, YARA rules, detection strategies)
15. Is there any part of the code that you could not understand/interpret?
16. Can you give a brief summary about this code in points.
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek/deepseek-r1",  # reasoning model
        "messages": [
            {"role": "system", "content": "You are a malware code analyst."},
            {"role": "user", "content": prompt_content + "\n\nCode:\n" + code},
        ],
    }

    response = requests.post(URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        raise RuntimeError(f"Request failed: {response.status_code} - {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]
