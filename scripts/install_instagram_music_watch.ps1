param([switch]$Install, [switch]$Uninstall)
$ErrorActionPreference = 'Stop'
$name = 'Instagram TUE - Musica Android'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if ($Install -and $Uninstall) { throw 'Escolha instalar OU desinstalar.' }
if ($Uninstall) {
  schtasks.exe /Delete /TN $name /F
  exit $LASTEXITCODE
}
if (-not $Install) {
  Write-Host 'Modo seguro: nada foi instalado. Use -Install somente com Android ADB autorizado.'
  exit 0
}
$python = (Get-Command python -ErrorAction Stop).Source
$adb = (Get-Command adb -ErrorAction Stop).Source
& $adb devices
$script = Join-Path $root 'scripts\instagram_music_watch.py'
$taskCommand = "cmd.exe /D /C `"cd /D `"`"$root`"`" && set INSTAGRAM_ANDROID_MUSIC_ENABLED=true && `"`"$python`"`" `"`"$script`"`" --execute`""
schtasks.exe /Create /F /SC MINUTE /MO 10 /TN $name /TR $taskCommand
if ($LASTEXITCODE -ne 0) { throw 'Falha no Task Scheduler.' }
Write-Host 'Task agendada a cada 10 minutos SOMENTE enquanto o Windows estiver ligado.'
Write-Host 'E necessario um unico telefone Android desbloqueado, conectado via ADB, com Instagram logado.'
Write-Host 'Nada sera feito sem faixa e artista exatos aprovados em content/schedule.json.'
