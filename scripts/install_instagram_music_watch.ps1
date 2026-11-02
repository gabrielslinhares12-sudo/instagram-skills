param([switch]$Install, [switch]$Uninstall)
$ErrorActionPreference = 'Stop'
$name = 'Instagram TUE - Musica Android'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if ($Install -and $Uninstall) { throw 'Escolha instalar OU desinstalar.' }
if ($Uninstall) {
  $task = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
  if ($null -ne $task) { Unregister-ScheduledTask -TaskName $name -Confirm:$false }
  exit 0
}
if (-not $Install) {
  Write-Host 'Nada foi instalado: o executor precisa ser ativado uma vez no Windows.'
  exit 0
}
$python = (Get-Command python -ErrorAction Stop).Source
$adb = (Get-Command adb -ErrorAction Stop).Source
if (!(Test-Path (Join-Path $root 'content\music-assignments.json'))) {
  throw 'Faltam as faixas aprovadas.'
}
# ADB may be temporarily disconnected. Install the dormant task without
# opening Instagram or sending credentials; worker skips until phone ready.
$taskScript = Join-Path $root 'scripts\run_instagram_music_task.ps1'
$quoted = '"' + $taskScript.Replace('"', '') + '"'
$action = New-ScheduledTaskAction -Execute 'powershell.exe' `
  -Argument ('-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File ' + $quoted) `
  -WorkingDirectory $root
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
  -RepetitionInterval (New-TimeSpan -Minutes 10) `
  -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew `
  -ExecutionTimeLimit (New-TimeSpan -Minutes 6) -StartWhenAvailable
Register-ScheduledTask -TaskName $name -Action $action -Trigger $trigger `
  -Settings $settings -Description 'Instagram TUE: aplicar musica aprovada apenas em carrossel existente, sem repostar' -Force | Out-Null
Write-Host 'Executor local instalado sem janela CMD. Música é aplicada só com Android ADB autorizado e faixa previamente aprovada.'
Write-Host 'Não há serviço 24/7 em nuvem: o Windows precisa estar ligado.'
