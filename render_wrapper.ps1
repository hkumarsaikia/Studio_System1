<#
.SYNOPSIS
    PowerShell Logging Wrapper for Studio System Batch Renderer.
    Execute this to start the rendering process with full engineering logging.

.DESCRIPTION
    Wraps the Python render_all.py script, logging start/stop times, arguments,
    and exit codes directly into logs/engineering.log. Ensures that every 
    production batch run is tracked for accountability.

.PARAMETER Limit
    Optional. Limits the render run to N videos. Maps to --limit in python script.

.PARAMETER Force
    Optional switch. Forces re-render even if videos exist. Maps to --force.
#>

param (
    [int]$Limit = 0,
    [switch]$Force
)

$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$logsDir = Join-Path $rootDir "logs"
$logFile = Join-Path $logsDir "engineering.log"

if (!(Test-Path $logsDir)) {
    New-Item -ItemType Directory -Force -Path $logsDir | Out-Null
}

$timestampStr = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$argsLog = ""
if ($Limit -gt 0) { $argsLog += "--limit $Limit " }
if ($Force) { $argsLog += "--force " }

$startMsg = "[$timestampStr] [START] Initiating Batch Render Request. Args: [$argsLog]"
Add-Content -Path $logFile -Value $startMsg
Write-Host -ForegroundColor Cyan $startMsg

# Launch the python script explicitly
$pythonCmd = "python"
$scriptPath = Join-Path $rootDir "automation\render_all.py"

$pythonArgs = @($scriptPath)
if ($Limit -gt 0) { $pythonArgs += "--limit", $Limit }
if ($Force) { $pythonArgs += "--force" }

# Capture the Start Time
$startTime = Get-Date

try {
    # Run process directly 
    $process = Start-Process -FilePath $pythonCmd -ArgumentList $pythonArgs -Wait -NoNewWindow -PassThru
    $exitCode = $process.ExitCode
} catch {
    $exitCode = -1
    $errMsg = "[$timestampStr] [ERROR] powershell caught exception: $_"
    Add-Content -Path $logFile -Value $errMsg
    Write-Host -ForegroundColor Red $errMsg
}

# Capture End Time
$endTime = Get-Date
$duration = New-TimeSpan -Start $startTime -End $endTime

$timestampStrEnd = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$durationStr = "{0:hh\:mm\:ss}" -f $duration

if ($exitCode -eq 0) {
    $endMsg = "[$timestampStrEnd] [SUCCESS] Batch Render completed successfully in $durationStr"
    Write-Host -ForegroundColor Green $endMsg
} else {
    $endMsg = "[$timestampStrEnd] [FAILURE] Batch Render failed (Exit: $exitCode) in $durationStr"
    Write-Host -ForegroundColor Red $endMsg
}

Add-Content -Path $logFile -Value $endMsg
Add-Content -Path $logFile -Value "--------------------------------------------------------"
