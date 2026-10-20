# Always invoke the retained local executable; never resolve a registry package.
$ErrorActionPreference = 'Stop'
$tool = Join-Path (Split-Path $PSScriptRoot -Parent) 'node_modules/workspace-template-win32-x64/bin/workspace-template.exe'
if (-not (Test-Path -LiteralPath $tool -PathType Leaf)) {
    throw 'Local workspace-template is missing. Run: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup.ps1'
}
& $tool @args
exit $LASTEXITCODE
