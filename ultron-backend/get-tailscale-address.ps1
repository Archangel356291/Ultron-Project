# get-tailscale-address.ps1
#
# Prints this machine's Tailscale address in the format the dashboard's
# Settings -> Connection panel expects, so you don't have to piece it
# together by hand from `tailscale status`.
#
# NOTE: this script could not be run against a real Tailscale installation
# while it was written (no Windows machine, no Tailscale account available
# in that environment) — it's built from documented `tailscale` CLI output
# formats, not verified against a live install. Sanity-check the output
# against what you see in the Tailscale tray icon / admin console the
# first time you run it.
#
# Run from PowerShell (no admin rights needed):
#   .\get-tailscale-address.ps1

$ErrorActionPreference = "Stop"

function Test-TailscaleInstalled {
    $cmd = Get-Command tailscale -ErrorAction SilentlyContinue
    return $null -ne $cmd
}

if (-not (Test-TailscaleInstalled)) {
    Write-Host "Tailscale CLI not found on PATH." -ForegroundColor Red
    Write-Host "Install it from https://tailscale.com/download/windows, or if it's" -ForegroundColor Red
    Write-Host "already installed, the CLI is usually at:" -ForegroundColor Red
    Write-Host "  C:\Program Files\Tailscale\tailscale.exe" -ForegroundColor Red
    exit 1
}

try {
    $ip = (tailscale ip -4 2>$null | Select-Object -First 1).Trim()
} catch {
    $ip = $null
}

if ([string]::IsNullOrWhiteSpace($ip)) {
    Write-Host "Could not get a Tailscale IP. Is Tailscale running and signed in?" -ForegroundColor Red
    Write-Host "Check the Tailscale icon in the system tray - it should say 'Connected'." -ForegroundColor Red
    exit 1
}

$backendPort = 5000
$suggestedUrl = "http://${ip}:${backendPort}"

Write-Host ""
Write-Host "Tailscale IPv4 address for this machine:" -ForegroundColor Cyan
Write-Host "  $ip"
Write-Host ""
Write-Host "Paste this into the dashboard's Settings -> Connection -> Backend URL:" -ForegroundColor Cyan
Write-Host "  $suggestedUrl"
Write-Host ""
Write-Host "Prefer a stable hostname over the raw IP? Check the MagicDNS name in" -ForegroundColor DarkGray
Write-Host "the Tailscale tray icon or https://login.tailscale.com/admin/machines" -ForegroundColor DarkGray
Write-Host "-- it looks like http://<device-name>.tailXXXX.ts.net:$backendPort and" -ForegroundColor DarkGray
Write-Host "won't change if this device's IP ever does." -ForegroundColor DarkGray
Write-Host ""

$healthUrl = "$suggestedUrl/api/health"
Write-Host "Quick check that the backend is actually reachable at this address:" -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 5
    if ($response.ok -eq $true) {
        Write-Host "  OK - $healthUrl responded correctly." -ForegroundColor Green
    } else {
        Write-Host "  Reached $healthUrl but got an unexpected response:" -ForegroundColor Yellow
        Write-Host "  $($response | ConvertTo-Json -Compress)"
    }
} catch {
    Write-Host "  Could not reach $healthUrl" -ForegroundColor Yellow
    Write-Host "  Is app.py running? (this only checks from THIS machine - it" -ForegroundColor Yellow
    Write-Host "  doesn't prove remote access works, just that the backend is up)" -ForegroundColor Yellow
}
