# Instagram TUE — instalação única do executor de música no Android

**Objetivo:** editar a faixa de música no **mesmo carrossel já publicado**. Nada é reenviado. A música aprovada no catálogo é **Thriller — Michael Jackson**, carrossel `https://www.instagram.com/p/DfNVlLDmC8P/`.

## Estado real, sem promessas

- Postagem com 8 fotos: já publicada, `media_id=18107496023215107`.
- Música: **não verificada nem salva**. Registro continua em `awaiting_native_music`.
- Autenticação via Instagram WEB foi confirmada, mas ela **não é sessão Android**.
- Não há um telefone Android/ADB vinculado ao GitHub Actions, e este chat não tem acesso direto ao Windows nem às configurações do celular. Logo, não é possível executar essa edição daqui sem o primeiro pareamento legítimo.
- **O GitHub não executa a tarefa no seu PC apenas porque há um arquivo `.ps1` no repositório.** É necessário executar a instalação uma vez em seu Windows.
- Windows e Android precisam estar na **mesma rede Wi-Fi privada** e o Android deve estar desbloqueado durante o trabalho. O dispositivo tem que permitir uma autorização explícita pelo sistema Android (Wireless debugging / ADB).
- Não existe promessa de operação 24/7 se o PC estiver desligado. Não foi contratado serviço nem fornecida credencial de Instagram.

## Comando de instalação (executar uma única vez no Windows)

Em um clone atualizado do repositório `gabrielslinhares12-sudo/instagram-skills`, abra PowerShell e rode:

```powershell
git pull --ff-only origin main
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup_instagram_android.ps1 -Install
```

O instalador baixa o **ADB oficial do Google** se não estiver no Windows, explica como localizar os dados de pareamento em **Opções do desenvolvedor → Depuração por Wi-Fi → Parear dispositivo com código**, e recebe o endereço e código **somente no terminal local**. Não envie o código nem cookies para ChatGPT ou GitHub. O instalador grava **somente o IP e porta privados do Android** em `%LOCALAPPDATA%\InstagramTUE\wireless-debugging.json` e instala a tarefa **Instagram TUE - Musica Android** no Windows.

O agendador tenta reconectar e executar discretamente a cada dez minutos, uma publicação por vez. Nenhum clique em publicar um novo carrossel é feito por este executor. A seleção **exata** de título e artista é obrigatória; não substitui Thriller por remix ou cover. Se não encontrar os controles de música ou uma confirmação inequívoca, bloqueia a edição repetida e mantém o recibo pendente.

## Diagnóstico / remoção

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup_instagram_android.ps1 -Diagnose
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_instagram_music_watch.ps1 -Uninstall
```

A tarefa Windows é executada **sem janela de CMD**. A instalação exige **apenas a primeira autorização de pareamento no dispositivo**; a seleção de música não fica a cargo do proprietário a cada publicação.

## O que ainda requer um teste de produção

A tela do Instagram pode expor ou não seus controles no Android `uiautomator`. O bridge interrompe de modo conservador quando não consegue identificar a conta, a faixa ou o botão de salvar. O sucesso dos testes de lógica no GitHub **não prova** que o editor real já foi automatizado. O usuário não deve ser instruído a editar manualmente a publicação como substituto do teste real.

Fontes: [Android Developers: depuração Wi-Fi e pareamento](https://developer.android.com/studio/run/device) e [ADB](https://developer.android.com/tools/adb).
