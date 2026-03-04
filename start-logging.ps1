# ===== Studio_System Engineering Logger =====

$projectPath = $PSScriptRoot
$logDir = Join-Path $projectPath "logs"
$logPath = Join-Path $logDir "engineering.log"

# Ensure logs directory exists
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null
}

Set-Location $projectPath

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "   ENGINEERING LOGGING: ACTIVE" -ForegroundColor Green
Write-Host "   Path: $projectPath" -ForegroundColor White
Write-Host "   Log:  logs\engineering.log" -ForegroundColor Yellow
Write-Host "   CLI:  python -m src.studio.cli" -ForegroundColor Magenta
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Start-Transcript -Path $logPath -Append
