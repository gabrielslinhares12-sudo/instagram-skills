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
