# Instagram TUE — operação 100% na nuvem com GitHub Actions

**Implantação:** infraestrutura de agendamento GitHub-hosted, sem runner GUTHY, PC Windows ou telefone Android conectado. O repositório ainda precisa de autorização Meta válida para efetivar as publicações. Não confundir execução do workflow com um post publicado.

## Regras editoriais e limites da Meta

- A produção mantém cada arte final do carrossel como um JPEG independente, 1080×1350, Lúmino original inalterado e número de páginas variável conforme o conteúdo.
- Carrosséis no **app Instagram** permitem 2–20 fotos; via **Instagram Graph API**, 2–10 fotos.
- A **API oficial não associa música nativa a carrosséis de fotos**. O suporte novo de Instagram Audio API destina-se a **Reels**, não a carrosséis.
- **Nunca** converter um carrossel em vídeo sem aprovação do formato. **Nunca** publicar sem música um post que foi aprovado como carrossel musical e nunca anunciar elegibilidade de Reels como publicação garantida.
- Publicar e adicionar música nativa **sem PC** requer uma integração oficial futura que aceite esse formato ou um cliente móvel autenticado fora do escopo desta operação; Android emulador em GitHub Actions não substitui um método oficial confiável de autenticação.

## GitHub hospedado — execução periódica

Workflow único: [`.github/workflows/instagram-scheduler.yml`](../../.github/workflows/instagram-scheduler.yml).

- `runs-on: ubuntu-latest`: computador da **infraestrutura do GitHub**, não o GUTHY.
- `schedule: */10 * * * *`: tenta conferir a fila a cada 10 minutos UTC (GitHub pode atrasar agendamentos).
- `workflow_dispatch`: permite conferir a fila (`dry_run=true`) ou executar somente itens elegíveis.
- `concurrency: instagram-temumaexplicacao-publication` impede duas execuções simultâneas. A antiga agenda `halloween-31out-2026.yml` não tem mais cron nem ação de publicar.
- `content/schedule.json` guarda os horários exatos em UTC; nenhuma faixa musical é inventada.
- `scripts/instagram_queue.py` registra uma reivindicação durável em `content/publication-state.json` **antes** da escrita na API. Se o retorno da Meta for incerto, coloca o item em `needs_review` e **não tenta reenviar automaticamente**, para evitar duplicações.
- Itens fora de `MAX_LATENESS=2h` são marcados `missed_window`, não enviados tardiamente por cron.
- `scripts/instagram_visual_standard.py audit-queue` continua exigindo pacote editorial correto, preservação dos pixels, revisão e autorização para qualquer novo item publicado via API.
- A execução inclui pré-verificação da identidade e permissões da Meta. Status dos itens aparece no resumo do workflow no GitHub.

## Roteamento sem surpresas

| Tipo / distribuição na fila | Resultado no cron |
|---|---|
| `post` (foto única) revisado, aprovado, horário devido | Pode publicar via Graph API após preflight |
| `carousel` + `native_music_carousel` (padrão) | **`requires_native_music`**; não enviar sem música |
| `carousel` + `api_carousel_without_native_music` | Só pode publicar com `owner_authorized_without_music=true` **e** controles editoriais |
| `reel` com MP4 previamente preparado e aprovado | O publicador técnico suporta MP4, mas novos Reels **não passam** sem validação editorial específica; não reclassificar carrossel automaticamente |
| Itens não aprovados, publicados, reivindicados ou atrasados | Não publicar |

Para liberar excepcionalmente um carrossel **sem** música via API, há dois registros de autorização, independentes: os campos de publicação da fila (`distribution_mode=api_carousel_without_native_music` e `owner_authorized_without_music=true`) e o manifesto editorial validado com esse mesmo modo e autorização. A escolha não pode ser feita automaticamente pela automação.

## Alternativa experimental 100% GitHub: carrossel deslizável com música (API móvel não oficial)

A biblioteca de código aberto **instagrapi** (versões recentes) documenta `album_upload_with_music(paths, caption, track)`, que simula o fluxo da API móvel privada e **pode** publicar uma lista de fotos com música nativa, sem converter em Reel. **Isso não é o Graph API oficial da Meta**: disponibilidade da música, login, mudanças internas e comportamento da conta não são garantidos. Pode gerar desafios de login, bloqueios temporários ou restrições. Não utilizar para contornar verificações de segurança; parar em qualquer desafio.

Implementado como **alternativa isolada, desligada por padrão**:

- [`.github/workflows/instagram-private-music.yml`](../../.github/workflows/instagram-private-music.yml): cron GitHub-hosted a cada dez minutos, cinco minutos após o fluxo oficial; **só roda automaticamente com a variável de habilitação**. Compartilha o mesmo grupo de concorrência para não executar duas publicações ao mesmo tempo.
- [`scripts/instagram_private_music.py`](../../scripts/instagram_private_music.py): baixa JPGs da revisão imutável do GitHub e confirma os hashes SHA-256, dimensões, conta `@temumaexplicacao`, ausência de duplicatas, título e artista aprovados da biblioteca do Instagram. Só chama `album_upload_with_music` após um registro durável prévio no ledger.
- Em caso de dúvida no retorno ou na presença da música, marca `needs_review` e **não repete a postagem**.
- Sem segredo de sessão ou sem uma aprovação explícita na fila, o cron não envia nada. Não use usuário/senha em YAML, logs, arquivos ou na conversa do ChatGPT.

**Ativação exige configuração única, sem PC:** criar uma sessão autorizada do `instagrapi` em ambiente seguro e salvar o JSON de sessão codificado como base64 em **GitHub Actions Secret `INSTAGRAM_PRIVATE_SESSION_B64`**. A sessão do navegador do TinyFish **não é** um arquivo `instagrapi` e não pode ser reutilizada diretamente. Para criar/gerenciar esse segredo pode-se usar uma Codespace pelo navegador do celular ou as configurações de Secrets do GitHub, seguindo a autenticação da própria conta. Evitar guardar ou imprimir cookies em logs.

Em **Settings → Secrets and variables → Actions** no GitHub, após avaliar e aceitar os riscos:

1. Secret `INSTAGRAM_PRIVATE_SESSION_B64`: JSON de sessão móvel autenticada, protegido como Secret (não basta login do Facebook).
2. Variável `INSTAGRAM_PRIVATE_RISK_ACCEPTED=true`: ciência de que o método é não oficial e pode sofrer restrições.
3. Variável `INSTAGRAM_PRIVATE_PUBLISH_ENABLED=true`: habilita as tentativas automáticas no runner GitHub; padrão é `false`.
4. Cada novo item `kind=carousel` que usar esse método precisa de `approved=true`, `private_api_authorized=true`, `music_track` e `music_artist` exatos, hashes de todos os JPGs e manifesto editorial aprovado. Não selecionar música aleatória ou com letras impróprias.
5. Primeiro executar o workflow pelo botão `workflow_dispatch` com `dry_run=true` e conferir os logs. O teste offline passou, **mas uma postagem real com música ainda precisa de validação na conta**.

**Importante:** os carrosséis já atrasados não são reenviados automaticamente. O Halloween de 31/10 às 18h continua pendente até reprogramação editorial explícita. Não divulgar esta rota como concluída só porque o código foi implantado; só um `media_id` e a conferência da música no Instagram comprovam o resultado.

## Dependência indispensável: credenciais Meta

O usuário precisa uma única vez autorizar a conta profissional `@temumaexplicacao` e a Página Facebook correspondente, com as permissões necessárias. O repositório usa:

- Secret `FACEBOOK_USER_ACCESS_TOKEN` (token de acesso Facebook válido; **não** colocar no código, issues ou logs).
- Variáveis `FACEBOOK_PAGE_ID`, `FACEBOOK_INSTAGRAM_USER_ID`, `INSTAGRAM_API_VERSION`, `INSTAGRAM_USERNAME`.
- Variável opcional `INSTAGRAM_SCHEDULER_ENABLED=false` para desligar publicações; padrão atual é habilitado, mas itens sem aprovação não saem da fila.

**Falha verificada em 31/10/2026:** o preflight da Meta retornou HTTP 400 / erro de permissão `code 200` antes de qualquer upload do carrossel de Halloween das 18h. O GitHub não pode conceder permissões sem uma reautorização legítima. Consulte [incidente documentado](../editorial/INCIDENTE-2026-10-31-18H-HALLOWEEN.md). Restaurar a autorização não reenvia automaticamente o post atrasado.

## Formatos musicais possíveis

1. **Carrossel deslizável com música nativa:** exige publicação no Instagram/app, atualmente **não 100% automática via Graph API**.
2. **Reel MP4 com música** (original/licenciada ou catálogo autorizado de Reels): pode ser preparado/publicado por GitHub Actions após nova aprovação editorial do formato e validação de áudio/vídeo; é um **vídeo**, não um carrossel de fotos deslizável.
3. **Carrossel sem música via API:** automatizável integralmente, mas apenas se autorizado expressamente, pois perde a estratégia musical.

Este documento descreve o que está operacional na nuvem e identifica separadamente o que **não** está resolvido. Um workflow verde só comprova testes ou execução do agendador, não a existência de post no Instagram. A prova é `media_id` real persistido.
