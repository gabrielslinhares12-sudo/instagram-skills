# Invocado pelo agendador Windows, sem CMD. Use apenas Android já autorizado.
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$state = Join-Path $env:LOCALAPPDATA 'InstagramTUE\wireless-debugging.json'
$adb = Join-Path $env:LOCALAPPDATA 'InstagramTUE\platform-tools\adb.exe'
if (!(Test-Path -LiteralPath $adb)) {
  $command = Get-Command adb -ErrorAction SilentlyContinue
  if ($null -eq $command) { exit 0 }
  $adb = $command.Source
}
if (Test-Path -LiteralPath $state) {
  try {
    $config = Get-Content -Raw -LiteralPath $state | ConvertFrom-Json
    $endpoint = [string]$config.connect_address
    if ($endpoint -notmatch '^(10\\.|192\\.168\\.|172\\.(1[6-9]|2[0-9]|3[01])\\.)\\d{1,3}\\.\\d{1,3}:\\d{1,5}$') { exit 0 }
    # Trusted pairing remains bound to a private IP. If Android rotates its
    # debugging port, mDNS can discover the new _adb-tls-connect endpoint
    # on the SAME private IP; never connect to any other device automatically.
    $trustedIp = $endpoint.Split(':')[0]
    $discovered = @()
    try {
      $services = @(& $adb mdns services 2>$null)
      foreach ($service in $services) {
        if (($service -match '_adb-tls-connect\\._tcp') -and
            ($service -match '(?<ip>(?:\\d{1,3}\\.){3}\\d{1,3}):(?<port>\\d{1,5})')) {
          if ($Matches.ip -eq $trustedIp) {
            $discovered += ($Matches.ip + ':' + $Matches.port)
          }
        }
      }
    } catch { }
    $discovered = @($discovered | Select-Object -Unique)
    if ($discovered.Count -eq 1) { $endpoint = $discovered[0] }
    & $adb connect $endpoint | Out-Null
  } catch { exit 0 }
}
$env:PATH = (Split-Path -Path $adb -Parent) + [IO.Path]::PathSeparator + $env:PATH
$env:INSTAGRAM_ANDROID_MUSIC_ENABLED = 'true'
Set-Location $root
$python = (Get-Command python -ErrorAction SilentlyContinue)
if ($null -eq $python) { exit 0 }
& $python.Source (Join-Path $root 'scripts\instagram_music_watch.py') --execute
exit $LASTEXITCODE
