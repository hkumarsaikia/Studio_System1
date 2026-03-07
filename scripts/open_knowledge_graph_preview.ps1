param(
    [int]$Port = 4173
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ServerScript = Join-Path $RepoRoot 'scripts\serve_knowledge_graph_preview.py'
$GeneratorScript = Join-Path $RepoRoot 'scripts\generate_repo_knowledge_graph.py'
$LogsDir = Join-Path $RepoRoot 'logs'
$PreviewProfile = Join-Path $RepoRoot '.codex\chrome-dev-knowledge-graph'
$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$ServerStdOutLog = Join-Path $LogsDir ("knowledge_graph_preview_server_{0}.out.log" -f $Timestamp)
$ServerStdErrLog = Join-Path $LogsDir ("knowledge_graph_preview_server_{0}.err.log" -f $Timestamp)
$Url = "http://127.0.0.1:$Port/tools/knowledge-graph-viewer/"

New-Item -ItemType Directory -Force $LogsDir | Out-Null
New-Item -ItemType Directory -Force $PreviewProfile | Out-Null

function Get-ChromeDevPath {
    $appPathKeys = @(
        'HKLM:\Software\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe',
        'HKCU:\Software\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'
    )

    foreach ($key in $appPathKeys) {
        try {
            $value = (Get-ItemProperty -Path $key -ErrorAction Stop).'(default)'
            if ($value -and (Test-Path $value) -and $value -match 'Chrome Dev') {
                return $value
            }
        } catch {
        }
    }

    $fallback = 'C:\Program Files\Google\Chrome Dev\Application\chrome.exe'
    if (Test-Path $fallback) {
        return $fallback
    }

    throw 'Google Chrome Dev was not found in Windows App Paths or the default install location.'
}

Write-Host "[1/4] Regenerating knowledge graph suite..."
python $GeneratorScript
if ($LASTEXITCODE -ne 0) {
    throw 'Graph generation failed.'
}

$serverHealthy = $false
try {
    $probe = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
    if ($probe.StatusCode -eq 200) {
        $serverHealthy = $true
    }
} catch {
    $serverHealthy = $false
}

if (-not $serverHealthy) {
    Write-Host "[2/4] Starting static preview server on port $Port ..."
    Start-Process -FilePath python -ArgumentList @($ServerScript, '--port', $Port) -WorkingDirectory $RepoRoot -RedirectStandardOutput $ServerStdOutLog -RedirectStandardError $ServerStdErrLog -WindowStyle Normal | Out-Null

    $started = $false
    for ($i = 0; $i -lt 20; $i++) {
        Start-Sleep -Milliseconds 500
        try {
            $probe = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
            if ($probe.StatusCode -eq 200) {
                $started = $true
                break
            }
        } catch {
        }
    }

    if (-not $started) {
        throw "The knowledge graph preview server did not respond on $Url. Check $ServerStdOutLog and $ServerStdErrLog"
    }
} else {
    Write-Host "[2/4] Reusing existing preview server on port $Port ..."
}

$ChromeDev = Get-ChromeDevPath
Write-Host "[3/4] Opening Google Chrome Dev: $ChromeDev"
Start-Process -FilePath $ChromeDev -ArgumentList @(
    "--user-data-dir=$PreviewProfile",
    '--new-window',
    '--auto-open-devtools-for-tabs',
    $Url
) | Out-Null

Write-Host "[4/4] Preview ready at $Url"
Write-Host "Server stdout log: $ServerStdOutLog"
Write-Host "Server stderr log: $ServerStdErrLog"
