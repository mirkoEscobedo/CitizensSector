$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$python = Join-Path $root 'ship-sprite-lab/.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    throw 'Lab environment is missing. From the repository root run: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ship-sprite-lab\scripts\setup.ps1'
}
Push-Location (Join-Path $root 'ship-sprite-lab')
try {
    & $python -m sprite_lab @args
    $code = $LASTEXITCODE
} finally { Pop-Location }
exit $code
