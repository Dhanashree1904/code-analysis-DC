$encUrl = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("http://example.com:9090/api"))
$decUrl = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($encUrl))

function Get-EnvironmentInfo {
    $user = $env:USERNAME
    $os = (Get-WmiObject Win32_OperatingSystem).Caption
    return @{ User=$user; OS=$os }
}

function Set-Persistence {
    $path = "$PSScriptRoot\\run_key.txt"
    "autorun" | Out-File -FilePath $path -Encoding utf8
}

function Invoke-Network {
    $uri = [Uri]$decUrl
    return @{ Host=$uri.Host; Port=$uri.Port; Path=$uri.AbsolutePath }
}

$info = Get-EnvironmentInfo
Set-Persistence
$net = Invoke-Network

Write-Output "User: $($info.User)"
Write-Output "OS: $($info.OS)"
Write-Output "Contact: $($net.Host):$($net.Port)$($net.Path)"
