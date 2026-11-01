# Instagram TUE — carrossel musical 100% em nuvem, orquestrado pelo GitHub

## Contrato editorial
- Conta: `@temumaexplicacao`; nunca publicar em outro perfil.
- Carrossel de **oito imagens originais 1080×1350**, na ordem do manifesto `content/schedule.json`; hashes SHA-256 obrigatórios.
- Música **nativa do catálogo Instagram** via referência pública a Reel/Post com áudio aprovado. Nunca transformar em Reel, nunca publicar sem música.
- Agendamento sem PC/GUTHY, **uma tarefa por vez**. O estado precisa ser durável para bloquear duplicatas.
- Não marcar como publicado apenas porque o provedor devolveu um ID de tarefa. Validar link, tipo carrossel, identidade e música separadamente.

## Alternativa pesquisada
GeeLark oferece modelo de Automação no cloud phone: **Post Carousel photo on Instagram** / API `POST /open/v1/rpa/task/instagramPubReelsImages`, com `image` (até 10 fotos), `description`, `scheduleAt`, `sameStyleUrl` (referência de áudio), `publishPost=true` (publicar como carrossel em vez de Reel) e `needShareLink=true`.
Documentação oficial:
- https://www.geelark.com/automation-marketplace/post-carousel-photo-on-instagram/
- https://github.com/GeeLark/geelark-openapi/blob/main/docs/en/Cloud%20Phone%20API/Automation/Instagram/Instagram_publish_Reels_image.md
- https://www.geelark.com/features/api/
- https://www.geelark.com/pricing/

**Importante:** o fornecedor descreve suporte ao formato e parâmetros; nossa conta **ainda não comprovou** o fluxo ponta a ponta nem a disponibilidade de uma faixa específica. A automação por app nativo pode sofrer alterações e exigir verificações de segurança. O serviço pode cobrar por tempo de celular/API e é externo ao GitHub.

## Implementado no GitHub
1. `scripts/instagram_geelark_cloud.py`: modos `check`, `submit`, `auto` e `reconcile`, todos no GitHub-hosted Ubuntu. `submit` faz download e SHA das imagens, envia ao armazenamento temporário GeeLark e cria a tarefa musical usando o endpoint documentado. `auto` agenda no máximo um carrossel aprovado por rodada; `reconcile` lê o estado remoto sem repetir publicações ambíguas.
2. `.github/workflows/instagram-geelark-cloud.yml`: check read-only em pushes; `workflow_dispatch` para check/submit/reconcile; verificação serial a cada dez minutos **apenas depois** da habilitação explícita.
3. `content/geelark-task-state.json`: ledger independente, registro de `claimed` antes de chamadas de mutação, seguido de `scheduled` após ID oficial do provedor; falhas -> `needs_review`, sem retentativa cega.
4. `content/geelark-music-plan.json`: arquivo atualmente vazio; associa conteúdo aprovado a data original e URL de áudio aprovada. Nenhum post velho é automaticamente remarcado.
5. `scripts/test_instagram_geelark_cloud.py`: testes offline de conta, formato, URL de música, janela de agendamento, travas, idempotência e modelo de chamada do provedor.
6. `scripts/configurar_geelark_cloud.sh`: envia token do provedor pelo stdin ao GitHub Actions Secret sem expor credenciais, com as três travas de publicação inicialmente desativadas.

## O que falta — um login legítimo
**Primeiro login necessário: GeeLark.** Criar/entrar em uma conta do serviço, verificar limites de custo, provisionar um cloud phone com Android e instalar o Instagram pela loja interna do provedor. O painel GeeLark pode requerer um cliente próprio para controlar a tela; confirmar disponibilidade no Work/browser antes de solicitar instalação local. **Não assinar plano ou gerar cobrança sem autorização explícita.**

**Segundo login necessário: Instagram no Android virtual.** Somente o proprietário digita as credenciais na interface do app oficial do Instagram, sem enviá-las ao chat, GitHub ou API privada. Confirmar `@temumaexplicacao` visível no perfil. **Não repetir a autenticação por instagrapi**, que recebeu o bloqueio temporário `PleaseWaitFewMinutes`.

Depois de autenticar ambos, salvar o token do GeeLark em **GitHub Actions Repository Secrets**: `GEELARK_TOKEN`. Identificar o cloud phone em `GEELARK_PHONE_ID` (Repository variable). Os nomes são metadados, os valores não devem entrar em commits, logs ou chat. Pode usar o script `bash scripts/configurar_geelark_cloud.sh` em Codespaces, com GitHub CLI autorizado e `GITHUB_TOKEN`/ `GH_TOKEN` removidos pelo script.

As variáveis `GEELARK_PUBLISH_ENABLED`, `GEELARK_ACCOUNT_CONFIRMED` e `GEELARK_COST_APPROVED` devem ficar `false` até a prova de conta correta, o teste real de música e o consentimento para eventuais custos. A integração permanece **inativa** sem elas.

## Primeiro teste operacional após os logins
- Selecionar no Instagram uma postagem/Reel pública que ofereça exatamente a faixa autorizada, guardar apenas a URL pública e conferir disponibilidade na conta.
- Testar no GeeLark uma preparação/draft e o modelo de carrossel (8 fotos, 4:5, `publishPost=true`, `sameStyleUrl`); inspecionar tela antes de qualquer postagem.
- Registrar o conteúdo em `content/geelark-music-plan.json` com `approved=true`, mantendo o `due_at` original e um horário **futuro**. O Halloween 31/10 continua vencido, sem remarcação automática.
- Após a publicação do teste autorizado, confirmar no Instagram **perfil, 8 fotos, legenda e música** e guardar o permalink.
- Só depois habilitar a rotina de dez minutos; ela não agendará nada sem foto/música aprovadas.

## Evidência versus promessa
Testes offline e verificação dos assets provam somente a implementação. Até haver login GeeLark, celular conectado e teste real do Instagram, **não afirmar que carrossel musical foi publicado ou agendado**.
