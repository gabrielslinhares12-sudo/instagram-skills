# Instagram TUE — automação de música após publicar carrossel (Android oficial)

## Música especificamente escolhida pelo proprietário: Thriller — Michael Jackson

- Atribuição oficial para o carrossel de Halloween em `content/music-assignments.json`.
- Post existente `18107496023215107` — https://www.instagram.com/p/DfNVlLDmC8P/ .
- **Não altera** a legenda, a ordem das oito fotos, o `due_at` nem a assinatura `fingerprint` do recibo de publicação.
- O aplicativo deve encontrar exatamente **Thriller — Michael Jackson**, não um cover, remix, instrumental ou áudio não identificado. A disponibilidade na biblioteca da conta ainda não foi confirmada; se não for encontrada, parar e manter `awaiting_native_music`.
- A atribuição significa **faixa escolhida/autorizada**, não música já salva. Sem ADB conectado a Android autenticado, não houve edição do Instagram.
- Com a aprovação específica, `python scripts/instagram_mobile_music.py` agora retorna `exact_song_configured=true` e o watcher opcional terá um post elegível. A instalação/agendamento da tarefa Windows continua **desativada**, até testar no aparelho.


## Status e evidências em 01/11/2026

O proprietário confirmou com captura do **aplicativo Android oficial** que a publicação `https://www.instagram.com/p/DfNVlLDmC8P/` oferece **Editar informações > Adicionar música**. O mesmo post já está publicado pela Meta, com recibo `18107496023215107`, e no ledger consta `awaiting_native_music`.

**Isso confirma a presença do recurso no app, NÃO prova que alguma música já foi escolhida ou salva.**

A API oficial Meta Graph NÃO oferece editar música nativa de carrossel já publicado. `instagrapi` documenta `album_upload_with_music()` para publicar um carrossel **novo** com música, mas `media_edit()` não documenta adicionar música a um post existente. A versão WEB da edição foi inspecionada e não apresenta a opção. Assim, para concluir automaticamente sem republicar nem autenticar a API privada, é preciso controlar o aplicativo Android **já autenticado**.

## Implementação preparada

- `scripts/instagram_mobile_music.py` — ponte opcional via ADB para abrir o permalink já publicado no app oficial, verificar `@temumaexplicacao`, abrir o editor, procurar **a faixa e o artista exatos previamente aprovados**, salvar, reabrir o mesmo link e confirmar o rótulo de música, e registrar `published` com evidências caso a confirmação apareça. **Nenhum post novo é enviado.**
- `scripts/test_instagram_mobile_music.py` e `.github/workflows/instagram-mobile-music-bridge.yml` — testes offline; não executam comandos ADB, não entram na conta, não publicam.
- O comando sem `--execute` apenas lista a publicação pendente e bloqueia tentativas sem música escolhida.
- Falha em qualquer tela, conta, faixa ambígua ou ausência de confirmação **mantém o post em `awaiting_native_music`**; jamais inventar sucesso ou republicar. Não usa reconhecimento OCR nem toca em coordenadas fixas sem encontrar o controle pelo texto/acessibilidade.
- O GitHub Actions **não tem acesso ao Android pessoal**. Runners cloud são efêmeros e experimentos anteriores com emulador não conseguiram instalar/autenticar Instagram. Assim o código **NÃO é uma automação em produção/24h**, mas é um controlador de execução preparado para um dispositivo Android autorizado.

## Execução no Windows com aparelho Android autenticado

Pré-requisitos, uma única vez, executados pelo dono:

1. Android Platform Tools (`adb`) no PATH, Python 3.12, aplicativo Instagram oficial logado na conta certa.
2. Habilitar **Opções de desenvolvedor > Depuração USB** e autorizar a conexão ADB no próprio aparelho. Nunca compartilhar senha, cookies ou código de 2FA. O telefone precisa estar desbloqueado durante a execução.
3. Executar de dentro do clone GitHub com `git` autenticado para gravar o recibo verificado. Nenhum API key de música e nenhuma assinatura paga.
4. Aprovar a música **por título e artista exatos** no manifesto do post; sem isso não há seleção automática segura.

Comandos de diagnóstico, por padrão somente leitura:
```powershell
adb devices
python scripts/instagram_mobile_music.py
```

Comandos de execução, **somente depois de aprovar música/autorizar ADB**, usando valores de exemplo ilustrativos; substituir por faixa e artista reais, disponíveis no Instagram:
```powershell
python scripts/instagram_mobile_music.py --id halloween-2026-10-31-historia-8-laminas --track "FAIXA_EXATA" --artist "ARTISTA_EXATO" --execute
```

Os controles do Instagram podem variar por versão/idioma; **a automação não foi validada no dispositivo real**. Se o controle de menu, busca ou salvar não estiver acessível em `uiautomator dump`, falha fechada; não presumir êxito. Para compatibilidade mais ampla, conectar Appium/UIAutomator2 a um Android persistente pode ser necessário; não há prova de funcionamento de ponta a ponta.

## Estado de publicação

- Confirmado: fotos, sequência e legenda publicadas no permalink original.
- Confirmado: botão **Adicionar música** aparece no app Android.
- **Pendente:** seleção de música, salvamento e verificação no mesmo post.
- Pendente: conexão ADB autorizada com um dispositivo real para teste do controlador.

Não ativar programação automática de outro post sem aprovação editorial. Não reativar GeeLark. Sem API privada/instagrapi e sem custo novo.

## Adicionado: execução sequencial opcional a cada 10 minutos (Windows)

- `scripts/instagram_music_watch.py`: busca estado mais recente da main, considera apenas **um** carrossel com música/autor explícito e `awaiting_native_music`; reserva local uma única tentativa por `media_id` e aciona `instagram_mobile_music.py --execute` no Android autorizado. Se houver falha ou interface alterada, **não tenta de novo automaticamente** nem marca publicado.
- `scripts/install_instagram_music_watch.ps1`: instalador/desinstalador do Windows Task Scheduler **somente sob `-Install` explícito**. Frequência: 10 minutos enquanto o Windows estiver ligado. Não foi executado neste ambiente, portanto **não existe tarefa instalada ou serviço rodando no PC**.
- Toggle de ativação local: `INSTAGRAM_ANDROID_MUSIC_ENABLED=true`. Sem toggle e sem música `music_track` + `music_artist` no carrossel aprovado, o watcher só emite `dry_run`.
- Comandos locais, após preparar ADB e configurar música exata na fila:
```powershell
adb devices
python scripts/instagram_mobile_music.py
python scripts/instagram_music_watch.py --skip-pull
powershell -ExecutionPolicy Bypass -File scripts/install_instagram_music_watch.ps1 -Install
```
- Remoção: `powershell -ExecutionPolicy Bypass -File scripts/install_instagram_music_watch.ps1 -Uninstall`.
- CI offline: [9 testes passaram](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41335729599) em 01/11/2026. **Não é teste de clique no Instagram real**.

### Estado real de operação

O Instagram TUE **já publicou o Halloween**, e a captura enviada pelo proprietário mostra o botão **Adicionar música** em `Editar informações` no app Android para esse mesmo carrossel. Este é um avanço factual sobre o teste anterior. Ainda faltam:

1. Definir **título e artista exatos** de uma música disponível e licenciada na biblioteca para a conta, a fim de permitir escolha automática; a configuração atual de Halloween não contém `music_track` ou `music_artist`.
2. Autorizar ADB uma vez num Android com app Instagram logado; não há dispositivo conectado ao executor GitHub.
3. Testar no Android **real** a árvore de acessibilidade, busca/seleção da faixa, botão Salvar e readback do mesmo post. Se alguma tela não for exposta ao ADB, a automação falha de modo conservador e exige adaptação Appium, sem ações cegas.
4. Instalar opcionalmente o watcher no **Windows local**. Não existe uma automação em nuvem 24/7 que edite a música diretamente na conta nesta configuração; a Graph API não oferece essa operação.

**Concluído até aqui:** código e testes; **não concluído:** música salva no Instagram nem execução móvel desacompanhada. A conta continua sem API privada de instagrapi e sem GeeLark.
