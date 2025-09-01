# SAFE DEMO: Inert PowerShell script for static analysis testing only.

# --- Obfuscated strings (demo) ---
$encUrl = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("http://example.com:8080/heartbeat"))
$decUrl = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($encUrl))

function Get-AntiVM {
    # Demo: check common VM process names (no action taken)
    $vmHints = @("vboxservice", "vmtoolsd")
    $found = @()
    foreach ($p in Get-Process | Select-Object -ExpandProperty Name -ErrorAction SilentlyContinue) {
        if ($vmHints -contains $p.ToLower()) { $found += $p }
    }
    return $found
}

function Set-PersistenceDemo {
    <#
    Demo only: show what a persistence command might look like (COMMENTED OUT)
    DO NOT UNCOMMENT OR RUN ON PRODUCTION SYSTEMS.
    #>
    # reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v DemoApp /d "C:\Demo\demo.exe" /f
    "$PSScriptRoot\.persistence_demo.txt" | Out-File -Encoding utf8
}

function Invoke-NetworkDemo {
    # Build a request but do not send it (no network I/O)
    $uri = [Uri]$decUrl
    return @{
        Host = $uri.Host
        Port = $uri.Port
        Path = $uri.AbsolutePath
    }
}

# MAIN
$vm = Get-AntiVM
Set-PersistenceDemo | Out-Null
$net = Invoke-NetworkDemo
Write-Output "SAFE DEMO (PowerShell)"
Write-Output ("Anti-VM hits: " + ($vm -join ", "))
Write-Output ("Decoded URL: " + $decUrl)
Write-Output ("Parsed network target: " + ($net | ConvertTo-Json -Compress))
