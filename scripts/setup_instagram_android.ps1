#requires -version 5.1
<#
.SYNOPSIS
  Configure a single authorized Android for Instagram TUE music editing.
.DESCRIPTION
  Runs ONLY on the owner's Windows PC (not GitHub cloud). Installs official
  Google SDK Platform-Tools (no third-party APK) in LocalAppData if missing,
  pairs via Android's on-device wireless debugging consent, stores only
  a private-network endpoint, and registers the already-developed local worker.
  No Instagram password, session token, or pairing PIN is stored in GitHub.
#>
param(
  [switch]$Install,
  [switch]$Diagnose
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$stateDir = Join-Path $env:LOCALAPPDATA 'InstagramTUE'
$toolsDir = Join-Path $stateDir 'platform-tools'
$adbPath = Join-Path $toolsDir 'adb.exe'
$endpointPath = Join-Path $stateDir 'wireless-debugging.json'

function Assert-PrivateEndpoint([string]$value) {
  if ($value -notmatch '^(?<ip>(?:\d{1,3}\.){3}\d{1,3}):(?<port>\d{1,5})$') {
    throw 'Use somente IP IPv4 local e porta, como 192.168.1.20:37099.'
  }
  $ip = [System.Net.IPAddress]::Parse($Matches.ip)
  $octets = $ip.GetAddressBytes()
  $port = [int]$Matches.port
  if (($port -lt 1) -or ($port -gt 65535)) { throw 'Porta ADB inválida.' }
  $private = ($octets[0] -eq 10) -or
             (($octets[0] -eq 172) -and ($octets[1] -ge 16) -and ($octets[1] -le 31)) -or
             (($octets[0] -eq 192) -and ($octets[1] -eq 168))
  if (-not $private) { throw 'Pareamento ADB só é permitido na rede privada local.' }
  return "$($ip.ToString()):$port"
}

function Get-Adb() {
  if (Test-Path -LiteralPath $adbPath) { return $adbPath }
  $known = Get-Command adb -ErrorAction SilentlyContinue
  if ($null -ne $known) { return $known.Source }
  New-Item -ItemType Directory -Force -Path $stateDir | Out-Null
  $zipPath = Join-Path $stateDir 'platform-tools-windows.zip'
  $uri = 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip'
  Write-Host 'Instalando Android Platform-Tools oficiais do Google, sem privilégios de administrador...'
  Invoke-WebRequest -Uri $uri -OutFile $zipPath -UseBasicParsing
  try {
    Expand-Archive -LiteralPath $zipPath -DestinationPath $stateDir -Force
    if (!(Test-Path -LiteralPath $adbPath)) { throw 'A instalação ADB oficial falhou.' }
  } finally {
    Remove-Item -LiteralPath $zipPath -Force -ErrorAction SilentlyContinue
  }
  return $adbPath
}

function Get-AuthorizedDeviceCount([string]$adb) {
  $list = @(& $adb devices)
  $found = @($list | Where-Object { $_ -match '^\S+\s+device\s*$' })
  return $found.Count
}

if (-not $Install -and -not $Diagnose) {
  Write-Host 'Modo seguro. Use -Install para parear seu Android uma vez e ativar o executor.'
  exit 0
}
if ($Install -and $Diagnose) { throw 'Escolha -Install OU -Diagnose.' }
if ($Diagnose -and !(Test-Path -LiteralPath $endpointPath)) {
  Write-Host 'Android ainda não pareado com o executor local.'
  exit 0
}
$adb = Get-Adb
$env:PATH = (Split-Path -Path $adb -Parent) + [IO.Path]::PathSeparator + $env:PATH
& $adb start-server | Out-Null
$python = (Get-Command python -ErrorAction SilentlyContinue)
if ($null -eq $python) {
  throw 'Python não está instalado no Windows ou não está no PATH.'
}
if ($Diagnose) {
  $config = Get-Content -Raw -LiteralPath $endpointPath | ConvertFrom-Json
  $target = Assert-PrivateEndpoint ([string]$config.connect_address)
  & $adb connect $target | Out-Null
  $count = Get-AuthorizedDeviceCount $adb
  Write-Host ("Dispositivos Android autorizados: {0}. Nada foi publicado ou editado." -f $count)
  exit 0
}

Write-Host ''
Write-Host 'No Android (mesmo Wi-Fi do PC):'
Write-Host 'Configurações > Opções do desenvolvedor > Depuração por Wi-Fi >'
Write-Host 'Parear dispositivo com código de pareamento.'
Write-Host 'Use somente endereços exibidos no seu celular. Não compartilhe o código no chat.'
Write-Host ''
$pair = Assert-PrivateEndpoint (Read-Host 'Digite IP:PORTA DE PAREAMENTO exibidos no celular')
Write-Host 'O adb solicitará o código diretamente neste terminal local. O código não será salvo.'
& $adb pair $pair
if ($LASTEXITCODE -ne 0) { throw 'Pareamento não foi autorizado pelo Android.' }
$connect = Assert-PrivateEndpoint (Read-Host 'Digite IP:PORTA DE DEPURAÇÃO (no topo da tela Depuração por Wi-Fi)')
& $adb connect $connect
if ($LASTEXITCODE -ne 0) { throw 'Não foi possível conectar ao Android.' }
if ((Get-AuthorizedDeviceCount $adb) -ne 1) {
  throw 'É necessário exatamente um Android autorizado. Nenhum agendamento instalado.'
}
$packages = @(& $adb shell pm list packages com.instagram.android)
if ($packages -notcontains 'package:com.instagram.android') {
  throw 'O aplicativo oficial Instagram não está instalado nesse Android.'
}
New-Item -ItemType Directory -Force -Path $stateDir | Out-Null
@{ version = 1; connect_address = $connect; app = 'com.instagram.android' } |
  ConvertTo-Json | Set-Content -LiteralPath $endpointPath -Encoding UTF8
# Store endpoint only, never authentication code, Android storage or cookies.
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'install_instagram_music_watch.ps1') -Install
if ($LASTEXITCODE -ne 0) { throw 'O agendador de música não foi instalado.' }
Write-Host ''
Write-Host 'Pareamento concluído e executor instalado; as músicas serão selecionadas pelo Android quando o PC e o celular estiverem disponíveis.'
Write-Host 'O telefone precisa continuar desbloqueado e na mesma rede Wi-Fi durante a edição.'
