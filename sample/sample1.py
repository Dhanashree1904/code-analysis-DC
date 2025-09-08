import os
import sys
import base64
import socket
import platform
from pathlib import Path

key = "aHR0cDovL2V4YW1wbGUuY29tOjgwODAvY2hlY2s="  # http://example.com:8080/check
cmd = "Y21kIC9jICJwaW5nIC1uIDEyNy4wLjAuMSI="       # cmd /c "ping -n 127.0.0.1"

def decode_payload(encoded):
    return base64.b64decode(encoded.encode("ascii")).decode("utf-8")

def check_vm():
    markers = ["VIRTUALBOX", "VMWARE", "HYPER-V"]
    sysinfo = platform.platform().upper()
    for m in markers:
        if m in sysinfo:
            return True
    return False

def persistence():
    try:
        f = Path("./system_init.log")
        f.write_text("init")
    except Exception:
        pass

def network():
    try:
        url = decode_payload(key)
        host = "example.com"
        port = 8080
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect((host, port))
        # s.send(b"ping")
        # s.close()
        return url
    except Exception:
        return None

def execute():
    c = decode_payload(cmd)
    print("Would execute:", c)

def main():
    if check_vm():
        sys.exit(0)
    persistence()
    target = network()
    execute()
    print("Target:", target)

if __name__ == "__main__":
    main()
