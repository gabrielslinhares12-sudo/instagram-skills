# Invocado apenas pelo agendador Windows. Nenhuma credencial salva aqui.
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$env:INSTAGRAM_ANDROID_MUSIC_ENABLED = 'true'
Set-Location $root
$py = (Get-Command python -ErrorAction Stop).Source
& $py (Join-Path $root 'scripts\instagram_music_watch.py') --execute
exit $LASTEXITCODE
