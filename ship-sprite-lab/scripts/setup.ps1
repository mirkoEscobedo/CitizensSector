[CmdletBinding()]
param([string]$Python = 'python')
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    if (-not (Test-Path -LiteralPath '.venv/Scripts/python.exe')) {
        & $Python -c 'import sys; assert sys.version_info >= (3,12), "Python 3.12+ is required"'
        if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.12+ with venv/pip, or pass -Python C:\path\to\python.exe.' }
        & $Python -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'Could not create the local lab virtual environment.' }
    }
    $venvPython = Join-Path $PWD '.venv/Scripts/python.exe'
    if ((Get-Content -LiteralPath '.venv/pyvenv.cfg') -match '^include-system-site-packages\s*=\s*true') {
        throw 'Legacy shared-runtime .venv detected. Move ship-sprite-lab/.venv aside, then rerun setup to create an isolated local environment.'
    }
    & $venvPython -c 'import sys; assert sys.version_info >= (3,12), "Recreate .venv with Python 3.12+"'
    if ($LASTEXITCODE -ne 0) { throw 'Existing .venv requires Python 3.12+.' }
    # Also repairs an interrupted install; all packages remain inside this venv.
    & $venvPython -m pip --require-virtualenv install --disable-pip-version-check -e .
    if ($LASTEXITCODE -ne 0) { throw 'Lab dependency install failed. First setup needs Python package downloads; see README.md.' }
    & $venvPython -m pip check
    if ($LASTEXITCODE -ne 0) { throw 'Lab dependency check failed.' }
    & $venvPython -m sprite_lab doctor
    if ($LASTEXITCODE -ne 0) { throw 'Lab doctor failed.' }
} finally { Pop-Location }
