# Instagram TUE — carrossel de fotos com música, executado pelo GitHub (2026-11-01)

## Objetivo inegociável
Publicar as **imagens individuais** (não um Reel) em carrossel deslizável, com música selecionada no catálogo do Instagram, sem PC/GUTHY e sem duplicatas; preservar Lúmino, identidade visual, ordem e legenda aprovada.

## O que está comprovado — não confundir com publicação
- Meta Graph API: identidade, permissões e variáveis verificadas com **GET**, sem publicação: https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41263684039
- Android virtual no GitHub: imagens originais 8/8 carregadas, mas **não** comprovou seleção múltipla e **não** instalou Instagram.
- Biblioteca Python `instagrapi==3.2.2` (interface móvel **não oficial**) foi instalada em runner GitHub, e o método `Client.album_upload_with_music(paths, caption, track)` foi verificado por assinatura; 8 imagens originais foram baixadas e conferidas por SHA-256; testes unitários passaram. Evidência: https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41266131353
- Estes testes **não** provaram que o Instagram aceitou o envio nem que a música existe na biblioteca da conta.

## Arquitetura segura e sem PC
1. `content/schedule.json`: fila aprovada, caminhos e SHA-256; bloqueia substituição das fotos por vídeo.
2. `.github/workflows/instagram-scheduler.yml`: API **oficial** com cron de 10 minutos, apenas para formatos autorizados; carrossel que exige música permanece bloqueado.
3. `.github/workflows/instagram-private-music.yml`: experimento separado com `instagrapi` em `ubuntu-latest`. **Desligado por padrão**. Requer credenciais de sessão autenticada pré-existente no GitHub Secrets, habilitação explícita e aceite informado do risco.
4. `scripts/instagram_private_music.py`: compara identidade com @temumaexplicacao, verifica JPGs e SHA, busca título+artista aprovados na biblioteca, confere publicações duplicadas, usa claim durável antes de tentativa única e verifica metadados da música após o envio. Resultado incerto -> bloqueio manual de duplicatas.
5. `.github/workflows/instagram-private-music-readiness.yml`: smoke test em nuvem **sem** autenticação, sessão, API Instagram ou publicação.

## Por que ainda NÃO está totalmente operacional
- O GitHub Secret `INSTAGRAM_PRIVATE_SESSION_B64` **não está configurado** no teste de readiness. A sessão web do Facebook/TinyFish **não é** uma sessão móvel instagrapi.
- Não existe aceite explícito dos riscos da API não oficial: `INSTAGRAM_PRIVATE_RISK_ACCEPTED=false` e `INSTAGRAM_PRIVATE_PUBLISH_ENABLED=false`.
- Nenhum carrossel está marcado com `private_api_authorized=true` e faixa+artista confirmados em `content/schedule.json`.
- O carrossel de Halloween venceu sua janela editorial de 2 horas; não alterar sua data automaticamente, nem republicar sem verificação de duplicidade.
- O acesso ao catálogo musical e a identidade da sessão só podem ser testados ao possuir a sessão privada legítima da conta.
- Usar API privada pode levar a bloqueios, desafios de login, restrições da conta ou mudanças sem aviso. **Não é API suportada pela Meta**. Não há garantia de disponibilidade nem de compatibilidade futura.

## Provisionamento seguro (uma única vez, antes de produção)
1. O proprietário escolhe conscientemente se aceita riscos da integração não oficial; não estabelecer aceite em seu nome.
2. Gerar uma sessão de `instagrapi` autenticada legitimamente na conta, em dispositivo/ambiente privado sob seu controle, sem revelar a senha ao chat nem salvá-la no repositório; exportar configurações de sessão em JSON e codificar base64 para o GitHub Actions Secret `INSTAGRAM_PRIVATE_SESSION_B64`. **Base64 não é criptografia**, mas Actions Secrets é armazenamento protegido; nunca exibir o valor em logs.
3. Configurar variáveis do GitHub `INSTAGRAM_PRIVATE_PUBLISH_ENABLED=true` e `INSTAGRAM_PRIVATE_RISK_ACCEPTED=true` apenas após aceite informado e teste prévio de identidade. Não ativar em CI automaticamente.
4. Para cada post aprovado, revisar fonte/ordem de JPGs, título e artista reais e marcar individualmente `private_api_authorized=true` apenas após consentimento específico.
5. Executar o workflow `instagram-private-music.yml` no modo `dry_run`; só depois disso permitir execução real dentro da janela e conferir ID/permalink e a existência da música. Manter monitoramento de duplicatas e bloqueio em falhas ambíguas.

## Se o risco não for aceitável
Manter carrosséis com música como pendentes e utilizar o app Instagram oficial com um dispositivo Android persistente e privado, contratado e autenticado pelo proprietário; o GitHub apenas aciona a automação (e registra resultados). Essa alternativa demanda serviço externo e **ainda não foi implementada**.

## Regra do projeto
**Não concluir como publicado** sem ID/permalink legítimo e áudio confirmado. Não converter a Reel nem descartar música silenciosamente. Não usar aplicativos modificados, APK de fonte desconhecida, credenciais em commits, caches/artifacts públicos ou bypass de autenticação.

## Verificações finais realizadas nesta execução

- **Lib atual e contrato de publicação musical:** instagrapi `3.2.2`, `album_upload_with_music(paths, caption, track)` validado no GitHub Actions. Fotos originais da campanha 8/8 SHA-256 conferidos. **9 testes de unidade passaram**, cobrindo identidade errada, publicação única, duplicata e confirmação de metadados de música. Execução: https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41266303138
- **Conta Instagram real consultada por API oficial (somente GET):** identidade confirmada @temumaexplicacao, **1 item publicado inspecionado**, **nenhum carrossel de Halloween de oito imagens correspondente** encontrado. A ausência foi verificada nesse conjunto recente, não em todo histórico potencial. Execução: https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41266419734
- **NÃO existe sessão móvel do Instagram no GitHub Actions Secret** (`session_secret_configured=false`) e não existe aceite dos riscos da API não oficial (`risk_acceptance_flag=false`). Nenhuma publicação feita ou pretendida nesses testes.
- A rota Android/ADB foi testada repetidamente, mas a seleção múltipla e o login oficial no app não foram confirmados. Não confundir execução de diagnóstico bem-sucedida com uma publicação real.
- **Status editorial:** campanha Halloween do dia 31/10 às 18:00 ainda não publicada como carrossel; manter oito JPGs originais e legenda, não emitir recibo fictício.

