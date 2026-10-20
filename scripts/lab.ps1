$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$python = Join-Path $root 'ship-sprite-lab/.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    throw 'Lab environment is missing. Run scripts/setup.ps1 first.'
}
Push-Location (Join-Path $root 'ship-sprite-lab')
try {
    & $python -m sprite_lab @args
    $code = $LASTEXITCODE
} finally { Pop-Location }
exit $code
