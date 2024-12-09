# PowerShell script to remove Redis and Celery Windows Services

# Ensure running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Please run this script as Administrator!"
    exit 1
}

$NSSM_PATH = "C:\nssm\nssm.exe"

# Stop and remove services
$SERVICES = @(
    "InventoryManager95-Redis",
    "InventoryManager95-CeleryWorker",
    "InventoryManager95-CeleryBeat"
)

foreach ($SERVICE in $SERVICES) {
    Write-Host "Removing service: $SERVICE"
    if (Get-Service $SERVICE -ErrorAction SilentlyContinue) {
        Stop-Service $SERVICE -Force
        & $NSSM_PATH remove $SERVICE confirm
    }
}

# Clean up script files
$PROJECT_ROOT = Split-Path -Parent $PSScriptRoot
Remove-Item (Join-Path $PROJECT_ROOT "scripts\start_worker.bat") -ErrorAction SilentlyContinue
Remove-Item (Join-Path $PROJECT_ROOT "scripts\start_beat.bat") -ErrorAction SilentlyContinue

Write-Host "Services have been removed successfully!"
