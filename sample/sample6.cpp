#include <windows.h>
#include <tlhelp32.h>
#include <iostream>

DWORD findProcessId(const std::wstring& processName) {
    PROCESSENTRY32 pe32;
    pe32.dwSize = sizeof(PROCESSENTRY32);
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

    if (Process32First(hSnapshot, &pe32)) {
        do {
            if (!_wcsicmp(pe32.szExeFile, processName.c_str())) {
                CloseHandle(hSnapshot);
                return pe32.th32ProcessID;
            }
        } while (Process32Next(hSnapshot, &pe32));
    }
    CloseHandle(hSnapshot);
    return 0;
}

int main() {
    DWORD pid = findProcessId(L"explorer.exe");
    if (pid == 0) {
        std::wcout << L"Process not found.\n";
        return 1;
    }

    HANDLE hProc = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (!hProc) {
        std::wcout << L"Failed to open process.\n";
        return 1;
    }

    char payload[] = "injected_payload";
    LPVOID addr = VirtualAllocEx(hProc, NULL, sizeof(payload), MEM_COMMIT, PAGE_READWRITE);
    WriteProcessMemory(hProc, addr, payload, sizeof(payload), NULL);

    std::wcout << L"Injected payload into explorer.exe (simulation).\n";

    CloseHandle(hProc);
    return 0;
}
