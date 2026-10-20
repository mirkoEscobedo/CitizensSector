$ErrorActionPreference = 'Stop'
& (Join-Path $PSScriptRoot 'lab.ps1') check
exit $LASTEXITCODE
