# PowerShell script to set up Redis and Celery as Windows Services

# Ensure running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Please run this script as Administrator!"
    exit 1
}

# Configuration
$REDIS_VERSION = "6.2.6"
$NSSM_VERSION = "2.24"
$PROJECT_ROOT = Split-Path -Parent $PSScriptRoot
$VENV_PATH = Join-Path $PROJECT_ROOT "venv"
$PYTHON_PATH = Join-Path $VENV_PATH "Scripts\python.exe"
$CELERY_PATH = Join-Path $VENV_PATH "Scripts\celery.exe"

# Download and install NSSM if not present
$NSSM_PATH = "C:\nssm\nssm.exe"
if (-not (Test-Path $NSSM_PATH)) {
    Write-Host "Downloading and installing NSSM..."
    $NSSM_URL = "https://nssm.cc/release/nssm-2.24.zip"
    $NSSM_ZIP = Join-Path $env:TEMP "nssm.zip"
    Invoke-WebRequest -Uri $NSSM_URL -OutFile $NSSM_ZIP
    Expand-Archive -Path $NSSM_ZIP -DestinationPath "C:\nssm" -Force
    Move-Item "C:\nssm\nssm-2.24\win64\nssm.exe" "C:\nssm\" -Force
    Remove-Item "C:\nssm\nssm-2.24" -Recurse -Force
    Remove-Item $NSSM_ZIP -Force
}

# Download and install Redis if not present
$REDIS_PATH = "C:\Redis\redis-server.exe"
if (-not (Test-Path $REDIS_PATH)) {
    Write-Host "Downloading and installing Redis..."
    $REDIS_URL = "https://github.com/microsoftarchive/redis/releases/download/win-$REDIS_VERSION/Redis-x64-$REDIS_VERSION.msi"
    $REDIS_MSI = Join-Path $env:TEMP "redis.msi"
    Invoke-WebRequest -Uri $REDIS_URL -OutFile $REDIS_MSI
    Start-Process msiexec.exe -ArgumentList "/i $REDIS_MSI /qn" -Wait
    Remove-Item $REDIS_MSI -Force
}

# Create Redis Service
Write-Host "Setting up Redis Service..."
& $NSSM_PATH install "InventoryManager95-Redis" $REDIS_PATH
& $NSSM_PATH set "InventoryManager95-Redis" AppDirectory "C:\Redis"
& $NSSM_PATH set "InventoryManager95-Redis" Description "Redis server for InventoryManager95"
& $NSSM_PATH set "InventoryManager95-Redis" Start SERVICE_AUTO_START

# Create Celery Worker Service
Write-Host "Setting up Celery Worker Service..."
$WORKER_SCRIPT = @"
@echo off
cd /d $PROJECT_ROOT
call $VENV_PATH\Scripts\activate.bat
celery -A InventoryManagement95 worker -l info
"@
$WORKER_SCRIPT_PATH = Join-Path $PROJECT_ROOT "scripts\start_worker.bat"
$WORKER_SCRIPT | Out-File -FilePath $WORKER_SCRIPT_PATH -Encoding ASCII

& $NSSM_PATH install "InventoryManager95-CeleryWorker" $WORKER_SCRIPT_PATH
& $NSSM_PATH set "InventoryManager95-CeleryWorker" AppDirectory $PROJECT_ROOT
& $NSSM_PATH set "InventoryManager95-CeleryWorker" Description "Celery Worker for InventoryManager95"
& $NSSM_PATH set "InventoryManager95-CeleryWorker" DependOnService "InventoryManager95-Redis"
& $NSSM_PATH set "InventoryManager95-CeleryWorker" Start SERVICE_AUTO_START

# Create Celery Beat Service
Write-Host "Setting up Celery Beat Service..."
$BEAT_SCRIPT = @"
@echo off
cd /d $PROJECT_ROOT
call $VENV_PATH\Scripts\activate.bat
celery -A InventoryManagement95 beat -l info
"@
$BEAT_SCRIPT_PATH = Join-Path $PROJECT_ROOT "scripts\start_beat.bat"
$BEAT_SCRIPT | Out-File -FilePath $BEAT_SCRIPT_PATH -Encoding ASCII

& $NSSM_PATH install "InventoryManager95-CeleryBeat" $BEAT_SCRIPT_PATH
& $NSSM_PATH set "InventoryManager95-CeleryBeat" AppDirectory $PROJECT_ROOT
& $NSSM_PATH set "InventoryManager95-CeleryBeat" Description "Celery Beat for InventoryManager95"
& $NSSM_PATH set "InventoryManager95-CeleryBeat" DependOnService "InventoryManager95-Redis InventoryManager95-CeleryWorker"
& $NSSM_PATH set "InventoryManager95-CeleryBeat" Start SERVICE_AUTO_START

# Start Services
Write-Host "Starting services..."
Start-Service "InventoryManager95-Redis"
Start-Service "InventoryManager95-CeleryWorker"
Start-Service "InventoryManager95-CeleryBeat"

Write-Host "Services setup complete! The following services have been created and started:"
Write-Host "- InventoryManager95-Redis"
Write-Host "- InventoryManager95-CeleryWorker"
Write-Host "- InventoryManager95-CeleryBeat"
Write-Host "`nThese services will start automatically with Windows."
