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

1. What is the high-level purpose of this code? Is it benign, suspicious, or malicious?
2. What programming language and style does the code use? (any hints of auto-generated or obfuscated code)
3. Does the code appear complete, or is it a fragment that relies on other modules?
4. Are there hardcoded file names, extensions, or paths? If yes, are they suspicious?
5. Does the code drop, create, or modify additional files on the system?
6. What forensic artifacts (files, registry keys, processes, logs, or network traffic) would this code likely leave behind?
7. What libraries, APIs, or system calls does this code use?
8. Are any of these APIs or libraries commonly abused in malware?
9. Are there suspicious command executions (e.g., os.system, subprocess, cmd.exe, powershell.exe)?
10. Are there suspicious strings (IPs, domains, registry keys, commands, encoded/obfuscated text)?
11. Does the code use obfuscation or packing techniques (base64, XOR, string manipulation)?
12. Are there cryptographic functions (hashing, encryption, decryption)? If yes, what are they used for?
13. Are there hardcoded credentials, API keys, or authentication bypass logic?
14. Does the code interact with the operating system (registry, services, drivers, or OS configuration)?
15.Does it attempt process injection, privilege escalation, or persistence mechanisms?
16. Does it try to disable or bypass security features (firewall rules, antivirus processes, EDR tools)?
17. Does the code collect environment/system information (e.g., username, OS version, IP, installed programs)?
18. Does the code contain network-related functionality (sockets, HTTP requests, DNS lookups, hardcoded IPs/domains)?
19. What protocols (HTTP, DNS, raw sockets, custom protocols) are used for communication?
20. Does it attempt to exfiltrate data or connect to a Command-and-Control (C2) server?
21. Does it suggest lateral movement techniques (e.g., network scanning, remote service abuse)?
22. Does the code perform file system operations (read/write/delete/encrypt)?
23. Does it attempt to steal or log sensitive data (keystrokes, clipboard, credentials, browser data)?
24. Does it compress, encode, or prepare data for exfiltration?
25. Does the code use any anti-analysis or evasion techniques (VM checks, debugger detection, sandbox evasion)?
26. Are there timers, delays, or sleep functions to evade sandbox execution?
27. Are there signs of polymorphism or self-modifying behavior (code generation, dynamic imports)?
28. Which specific lines or functions in the code are most suspicious or malicious? (include line numbers and reasoning)
29. Are there dead code sections, misleading code, or intentionally obfuscated logic?
30. Which MITRE ATT&CK techniques (with T-codes) apply to this code, and why?
31. What is the potential impact if this code is executed (e.g., data theft, persistence, lateral movement)?
32. What is the overall risk rating of this code (Low / Medium / High)?
33. What should an analyst do next? (sandbox execution, YARA rules, detection strategies, network blocking)
34. Which parts of the code are unclear or require dynamic analysis to fully understand?
35. Can you summarize the analysis in concise bullet points?
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
