# Correção crítica de mídia — Halloween 31/10/2026

Status: **ARTE CORRETA PREPARADA, ENVIO PARA PUBLICAÇÃO BLOQUEADO ATÉ A SUBSTITUIÇÃO**.

## Erro confirmado
A fila `content/schedule.json` apontava para a arte antiga:
`https://raw.githubusercontent.com/gabrielslinhares12-sudo/instagram-skills/362fde4997128c20fb86ad0fd450a9179af92b45/content/media/2026-10-31-lumino/halloween.jpg`.

O proprietário identificou o erro em 30/10/2026. Essa imagem antiga **não pode ser publicada**.

## Arte final correta
- Título: **“Eu dizendo que sou racional... até ouvir um barulho na cozinha de madrugada.”**
- Visual: Lúmino em sofá com gato, cobertor de Halloween; segundo quadro Lúmino com gato assustado com ruído na cozinha.
- Origem exata: arquivo gerado e preservado nesta conversa `racionalidade_até_o_primeiro_crac.png`, 1122 × 1402 px.
- Arquivo FINAL convertido para publicação Instagram: `halloween-lumino-versao-final-2026-10-31.jpg`, **1080 × 1350 px**, JPEG RGB, 526981 bytes.
- **SHA256 do JPG convertido:** `9b909155390281e5c9648c1eb3cb330f05bc0b459016f07b0a1428eaf3d2bdc8`.
- Referência de arquivo ChatGPT (não é URL pública para Meta): `file_00000000ff6c820e9a531a37963f88bf`.
- A mídia também foi salva como asset privado em Canva ID `MAHZiiUDLHw`; **não usar o thumbnail expirável como origem da publicação**.

## Próxima ação obrigatória
1. Transferir o **JPG exato**, sem redesenho, para `content/media/2026-10-31-lumino/halloween-final-2026-10-31.jpg` (ou outra origem pública HTTPS estável e verificável).
2. Verificar visual, dimensões 1080 × 1350 px, JPEG e hash SHA256 do binário. Imagem antiga nunca deve ser usada.
3. Alterar apenas o item `lumino-halloween-2026` no manifesto, substituindo `media_urls[0]` por URL pública nova fixada em commit SHA do GitHub, opcional `media_sha256` com SHA acima.
4. Antes de reativar, consultar `content/publication-state.json` e Instagram para verificar ausência de publicação/claim. Se já constar `claimed`, `published` ou `needs_review`, não repetir sem investigação.
5. Com mídia correta verificada, ativar `approved=true` e preservar `due_at = 2026-10-31T15:00:00Z` se ainda futura, sem alterar os demais itens.
6. Notificar o proprietário de que a imagem foi efetivamente substituída; após a execução, notificar o media_id de publicação confirmado.

## Registro da proteção
Em 30/10/2026 foi aplicado `approved=false` ao item do Halloween com commit `daf1333bf7301a31267d7fe7e0d6c963fd3398b3`. Isso evita que o cron atual publique por engano a versão antiga.
