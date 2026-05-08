$ErrorActionPreference = "Stop"

$ctxHome = Split-Path -Parent $MyInvocation.MyCommand.Path
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ([string]::IsNullOrWhiteSpace($userPath)) {
    $paths = @()
} else {
    $paths = $userPath -split ";"
}

$alreadyInstalled = $paths | Where-Object {
    $_.TrimEnd("\") -ieq $ctxHome.TrimEnd("\")
}

if (-not $alreadyInstalled) {
    $newPath = if ([string]::IsNullOrWhiteSpace($userPath)) {
        $ctxHome
    } else {
        "$userPath;$ctxHome"
    }
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "[ok] Added ContextDrop to your user PATH."
    Write-Host "Close and reopen PowerShell, then run: ctx --help"
} else {
    Write-Host "[ok] ContextDrop is already on your user PATH."
}

Write-Host ""
Write-Host "You can also use it immediately in this terminal with:"
Write-Host "  .\ctx.cmd --help"
