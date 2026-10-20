[CmdletBinding()]
param([string]$Python = 'python')
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Push-Location $root
try {
    if ([Environment]::OSVersion.Platform -ne 'Win32NT') { throw 'Setup requires Windows x64.' }
    $nodeVersion = & node --version
    if ($LASTEXITCODE -ne 0 -or $nodeVersion -notmatch '^v24\.') { throw 'Install Node.js 24 LTS (with npm), then rerun setup.' }
    $nodeArchitecture = & node -p process.arch
    if ($LASTEXITCODE -ne 0 -or $nodeArchitecture -ne 'x64') { throw 'Install the Windows x64 build of Node.js 24.' }
    $archive = Join-Path $root 'vendor/workspace-template-win32-x64-0.9.0-alpha.0.tgz'
    if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash -ne '95c61b973fd68204289f257fae957589a921d4ff4331f552c11b72015d1d38f5') {
        throw 'Retained archive SHA-256 mismatch. Restore it from Git; do not substitute a same-version build.'
    }
    & npm.cmd ci --offline --include=dev --ignore-scripts --no-audit --no-fund --update-notifier=false --cache .onboarding-cache/npm
    if ($LASTEXITCODE -ne 0) { throw 'Offline tooling install failed; check the retained archive and package-lock.json.' }
    $tool = Join-Path $root 'node_modules/workspace-template-win32-x64/bin/workspace-template.exe'
    if (-not (Test-Path -LiteralPath $tool -PathType Leaf)) { throw 'Installed workspace-template.exe is missing.' }
    if ((Get-FileHash -LiteralPath $tool -Algorithm SHA256).Hash -ne '00e272fdf9a406fc15619c1c7fecec36c39ebea04a184c5d9f725a3ce83213d0') {
        throw 'Installed workspace-template.exe SHA-256 mismatch.'
    }
    foreach ($toolArgs in @(@('version'), @('doctor', '.'), @('skills', 'list'))) {
        & $tool @toolArgs
        if ($LASTEXITCODE -ne 0) { throw "workspace-template $toolArgs failed." }
    }
    & (Join-Path $root 'ship-sprite-lab/scripts/setup.ps1') -Python $Python
    if ($LASTEXITCODE -ne 0) { throw 'Lab setup failed.' }
    & (Join-Path $root 'scripts/check.ps1')
    if ($LASTEXITCODE -ne 0) { throw 'Lab software checks failed.' }
    Write-Output 'Setup complete. See README.md for agent loading, issue ownership, and optional art/game checks.'
} finally { Pop-Location }
