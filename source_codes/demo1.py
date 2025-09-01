# SAFE DEMO: This script is inert and does not perform harmful actions.
# It only simulates patterns often seen in malicious code for static analysis testing.

import os
import sys
import base64
import socket
import platform
from pathlib import Path

# --- Obfuscated strings (demo) ---
# Typical malware might hide C2 or commands; here we store a harmless placeholder.
ENCODED_C2 = base64.b64encode(b"http://example.com:8080/api").decode("ascii")  # "obfuscated"
ENCODED_CMD = "cGluZyAtYyAidGVzdCI="  # base64("ping -c \"test\"") as a harmless placeholder

def decode_strings():
    c2 = base64.b64decode(ENCODED_C2.encode("ascii")).decode("utf-8")
    cmd = base64.b64decode(ENCODED_CMD.encode("ascii")).decode("utf-8")
    return c2, cmd

# --- Anti-VM / environment checks (demo) ---
def anti_vm_check():
    suspicious_markers = ["VIRTUALBOX", "VMWARE"]
    sysinfo = platform.platform().upper()
    for marker in suspicious_markers:
        if marker in sysinfo:
            # Demo: would normally alter behavior; here we just note it.
            return True
    return False

# --- Persistence (demo) ---
def setup_persistence_demo():
    """
    Simulate a persistence idea WITHOUT actually modifying the system.
    Real malware might add Run keys / launch agents / services.
    Here we only write to a temp file in the current directory as a placeholder.
    """
    try:
        placeholder_path = Path("./.persistence_demo.txt")
        placeholder_path.write_text("This is a harmless placeholder for persistence simulation.\n")
        # Example (commented, DO NOT RUN): Windows registry Run key
        # import winreg; k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
        # winreg.SetValueEx(k, "DemoApp", 0, winreg.REG_SZ, "C:\\Path\\To\\Demo.exe")
        return True
    except Exception as e:
        return False

# --- Network communication (demo) ---
def connect_c2_demo():
    """
    Demonstrate how code might prepare a socket.
    This function does NOT actually connect anywhere; it builds the tuple then exits.
    """
    c2, _ = decode_strings()
    # Parse host/port safely (no connect)
    # e.g., "http://example.com:8080/api"
    try:
        host = "example.com"
        port = 8080
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.settimeout(2.0)
        # s.connect((host, port))   # <-- intentionally NOT executed in this demo
        # s.close()
        return (host, port)
    except Exception:
        return None

# --- Data collection / exfil (demo) ---
def collect_data_demo():
    """
    Pretend to collect some system info (harmless).
    """
    return {
        "cwd": os.getcwd(),
        "pid": os.getpid(),
        "platform": platform.platform(),
    }

def main():
    vm = anti_vm_check()
    _ = setup_persistence_demo()
    _ = connect_c2_demo()
    info = collect_data_demo()

    # Output to stdout so your analyzer can quote lines/behavior.
    print("SAFE DEMO START")
    print(f"Anti-VM triggered? {vm}")
    print(f"Decoded C2 (placeholder): {decode_strings()[0]}")
    print(f"System info: {info}")
    print("SAFE DEMO END")

if __name__ == "__main__":
    # Do not perform any network/system modification. This is safe to run.
    main()
