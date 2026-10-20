# Prepared from the actual installed starsector_minimal.bat, never invoked by the lab.
param([string]$GameHome='H:\Games\Starsector')
$ErrorActionPreference='Stop'
$labRoot=Split-Path $PSScriptRoot -Parent
$runRoot=Join-Path $labRoot 'outputs\idris\game-run'
$modsPath=Join-Path $labRoot 'outputs\idris\export'
$corePath=Join-Path $GameHome 'starsector-core'
$javaPath=Join-Path $GameHome 'jre\bin\java.exe'
if (-not (Test-Path -LiteralPath (Join-Path $modsPath 'idris_lab\mod_info.json'))) { throw 'Run the lab export command first.' }
foreach ($folderName in @('saves','screenshots','logs')) { New-Item -ItemType Directory -Force -Path (Join-Path $runRoot $folderName) | Out-Null }
$line=Get-Content -Raw -LiteralPath (Join-Path $corePath 'starsector_minimal.bat')
$tokens=[regex]::Matches($line,'"[^"]*"|\S+') | ForEach-Object { $_.Value.Trim('"') }
$javaArgs=@($tokens | Select-Object -Skip 1 | ForEach-Object {
    if ($_ -match '^-Dcom\.fs\.starfarer\.settings\.paths\.(saves|screenshots|logs|mods)=') {
        $key=$Matches[1]
        $value=if ($key -eq 'mods') { $modsPath } else { Join-Path $runRoot $key }
        "-Dcom.fs.starfarer.settings.paths.$key=$value"
    } elseif ($_ -match '^-Xm[xs]') { if ($_ -like '-Xmx*') { '-Xmx4096m' } else { '-Xms1024m' } }
    else { $_ }
})
Write-Output "Launching the isolated lab mission. Saves/logs/screenshots: $runRoot"
Push-Location $corePath
try { & $javaPath @javaArgs } finally { Pop-Location }
