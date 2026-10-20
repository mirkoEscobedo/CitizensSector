$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if (-not (Test-Path '.venv/Scripts/python.exe')) {
    $bundledPython = 'C:\Users\escob\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path -LiteralPath $bundledPython) {
        & $bundledPython -m venv --system-site-packages --without-pip .venv
    } else {
        python -m venv .venv
        & ./.venv/Scripts/python.exe -m pip install -e .
    }
}
& ./.venv/Scripts/python.exe -m sprite_lab doctor
