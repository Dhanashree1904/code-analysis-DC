#include <windows.h>
#include <stdio.h>

int main() {
    HKEY hKey;
    const char *keyPath = "Software\\Microsoft\\Windows\\CurrentVersion\\Run";
    const char *valName = "Updater";
    const char *valData = "C:\\\\Users\\\\Public\\\\updater.exe";

    // Registry persistence simulation
    RegCreateKeyExA(HKEY_CURRENT_USER, keyPath, 0, NULL, 0, KEY_WRITE, NULL, &hKey, NULL);
    RegSetValueExA(hKey, valName, 0, REG_SZ, (const BYTE*)valData, strlen(valData) + 1);
    RegCloseKey(hKey);

    // Fake CreateProcess for lateral movement
    STARTUPINFOA si = { sizeof(si) };
    PROCESS_INFORMATION pi;
    CreateProcessA("C:\\\\Windows\\\\System32\\\\cmd.exe", "/c echo test",
                   NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);

    printf("Registry entry set and process created.\n");
    return 0;
}
