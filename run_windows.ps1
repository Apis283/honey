[CmdletBinding()]
param(
    [int]$Episodes = 100,
    [switch]$Quiet,
    [switch]$SkipInstall,
    [switch]$Help
)

$ErrorActionPreference = "Stop"

if ($Help) {
    Write-Host "Usage: .\run_windows.ps1 [-Episodes <int>] [-Quiet] [-SkipInstall]"
    Write-Host "Example: .\run_windows.ps1 -Episodes 1000 -Quiet"
    exit 0
}

if ($Episodes -lt 1) {
    throw "Episodes must be >= 1"
}

Set-Location $PSScriptRoot

$pythonBootstrap = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonBootstrap) {
    throw "Python is not available on PATH. Install Python 3 and retry."
}

if (-not (Test-Path ".venv")) {
    & $pythonBootstrap.Source -m venv .venv
}

$pythonCmd = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonCmd)) {
    throw "Could not find virtual environment Python at .venv\\Scripts\\python.exe"
}

if (-not $SkipInstall) {
    & $pythonCmd -m pip install --upgrade pip
    & $pythonCmd -m pip install -r requirements.txt
}

$argsList = @("main.py", "--episodes", $Episodes)
if ($Quiet) {
    $argsList += "--quiet"
}

& $pythonCmd @argsList
