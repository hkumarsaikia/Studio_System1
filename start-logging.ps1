# ===== Studio_System Engineering Logger =====

# This sets the path to the folder where the script is currently located
$projectPath = $PSScriptRoot 
$logPath = Join-Path $projectPath "engineering.log"

Set-Location $projectPath

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   ENGINEERING LOGGING: ACTIVE" -ForegroundColor Green
Write-Host "   Path: $projectPath" -ForegroundColor White
Write-Host "   Log:  engineering.log" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Starts recording everything in the terminal to the log file
Start-Transcript -Path $logPath -Append