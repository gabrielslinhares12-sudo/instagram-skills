> **ATIVAÇÃO PERMANENTE NESTE PROJETO: `TUE-MESTRE-01` — [ver padrão mestre](brand/TUE-MESTRE-01.md).** Usar por padrão em TODO pedido de conteúdo Instagram TUE; modelo 1 original somente; rascunhos V3 de 02/11 rejeitados; não agendar nem publicar. Regras antigas contraditórias abaixo são históricas.

> **REGRA VISUAL PERMANENTE — LÚMINO ORIGINAL (31/10/2026):** o proprietário enviou o [PNG canônico do Lúmino](https://drive.google.com/file/d/1F2n5GLNtdfhxu6pgEvucexrBW_8c8Fdv/view). Usar esse arquivo exato como camada, sem redesenhar nem alterar anatomia; conferir SHA-256 `f905d801f013c2e253b8a17ae3bc1279b57022d1b805baa632f291a3b73e0c1b`. Olhos LED ciano, lanterna de vidro com lâmpada visível, sobretudo cáqui, luvas brancas, **sem boca nem pernas**. O [model sheet](https://drive.google.com/file/d/1ihraal4wKH3FHQWme3vx5llYNiRSma5T/view) orienta poses; nunca usar recriações do mascote no lugar do PNG. [Entregas 05–06/11](https://github.com/gabrielslinhares12-sudo/instagram-skills/blob/main/content/editorial/ENTREGA-05-06NOV-LUMINO-ORIGINAL-REVISAO.md) são rascunhos; os Reels ainda não têm MP4 e voz Rasalgethi.

# Instagram TUE — estado operacional e política de publicação

**Atualizado em 31/10/2026.** Este documento substitui descrições antigas de lotes aprovados que não refletem mais a identidade visual atual.

## Regra canônica: quantidade variável por post (01/11/2026)

A referência aprovada com **8 painéis** serve exclusivamente para replicar a **linguagem visual**, não para fixar 8 imagens por carrossel. Cada tema recebe o número necessário de peças individuais e distintas; não preencher, subdividir ou repetir conteúdo para chegar a oito. Aceitar 2–20 pelo aplicativo Instagram, até 10 pela API oficial; 1 imagem é post simples. Ver `content/brand/padrao-visual.json` e os testes de `scripts/test_individual_carousel.py`.

**GeeLark descartado por decisão do proprietário em 01/11/2026:** não usar o fornecedor, não solicitar tokens/contas e não acionar seus workflows. Código executável e cron do fornecedor removidos; documentação de experimentos anteriores, quando presente, é somente histórica. Priorizar API oficial da Meta. Carrossel com música nativa permanece aguardando inclusão no aplicativo oficial, com autenticação legítima e confirmação de publicação; não substituir por Reel nem eliminar música sem decisão editorial específica.

## Publicações com aprovação vigente

- 31/10 às 12h (America/Sao_Paulo): tirinha de Halloween, já publicada. O recibo real está em `content/publication-state.json`; nunca reenviar.
- 31/10 às 18h: carrossel aprovado "A história do Halloween", com oito mídias individuais; `content/schedule.json` já contém a fila. O workflow `.github/workflows/halloween-31out-2026.yml` tem cron às 21:00 UTC e retry às 21:10 UTC. Isto **não** constitui prova de publicação: confirmar `media_id` no ledger depois da execução.

## Semana de 01 a 06/11

- Grade editorial: duas peças por dia, 12h e 18h (America/Sao_Paulo); são 12 conteúdos.
- As 10 peças gráficas do Google Drive são rascunhos em revisão, incluindo V2 de Votos, meme V2, Dólar V2/V3, Onças e demais temas. Os dois Reels aguardam áudio da voz **Rasalgethi** pelo site do **Google AI Studio** e arquivo MP4 sincronizado.
- Os dois itens de 01/11 presentes em `content/schedule.json` estão `approved=false`; **não autorizados para publicar**. Os demais itens do pacote de 01–06/11 não devem ser acrescentados como aprovados até revisão final e autorização expressa.
- Modelo **obrigatório** de cada carrossel: `content/editorial/IDENTIDADE-VISUAL-LUMINO.md` e [referência visual 2×4 do proprietário](https://drive.google.com/file/d/1FPAIpEijBQ3tHkr-Hg9V_-yCw-dqSHhl/view). Cada arte final deve ser JPEG individual 1080×1350. Nunca usar a colagem como arquivo de postagem, nem reutilizar imagens V1 rejeitadas.
- Modelo do Lúmino: lanterna de vidro vintage dourado, filamento quente, olhos ciano nos óculos redondos, sobretudo e lupa; sem substituir por animal ou humano. Tarjas amarelas pintadas, títulos pretos condensados, vermelho pontual, fotos e cenas documentais, composição variada, legível no celular.
- Na votação, o modelo visual original possui dados fictícios **incorretos para a tese do post**. O exemplo válido é hipotético e presidencial: A=44, B=46, brancos+nulos=10, 100 depositados, 90 válidos, B=46/90=51,1%; nunca alegar que 51% dos votos válidos perdeu.
- Inspeções e pendências específicas: `content/editorial/AUDITORIA-E-ENTREGA-SEMANA-01-A-06-NOV-2026.md` e `content/editorial/CONFERENCIA-FACTUAL-SEMANA-01-A-06-NOV-2026.md`.

## Segurança e execução

1. `content/schedule.json` é a **fonte de verdade** dos itens efetivamente na fila, URLs, aprovação e horário; plano editorial ou arquivo do Drive não agenda automaticamente.
2. `content/publication-state.json` é o **registro de execução**. Para afirmar publicação, exigir `published`, `media_id` e `published_at` confirmados. Não apagar estado de item com resultado incerto para forçar retry.
3. O workflow `instagram-scheduler.yml` apenas faz `workflow_dispatch` manual, por decisão do proprietário. Não restabelecer cron recorrente ou acionar a publicação de 01–06/11 sem a autorização específica prometida **após** a apresentação do lote final.
4. O workflow excepcional `halloween-31out-2026.yml` permanece intacto para as duas janelas autorizadas em 31/10. Não alterar cron, imagens ou hashes para tentar publicar em duplicidade.
5. Publicação usa `media_urls` HTTPS públicas, versionadas por commit imutável, nunca links Google Drive nem ZIPs. Conferir hashes, resolução, legenda, identidade Instagram, permissões Meta e duplicações antes de liberar.
6. A credencial Meta permanece exclusivamente em GitHub Secrets, nunca em conteúdo do repositório. `scripts/instagram_preflight.py` é obrigatório e não prova que o upload foi concluído.
7. Política de aprovação: **não inferir** `approved=true` de transferência, hash, presença de JPG, revisão textual ou gatilho. A publicação da nova semana depende de material final revisado e nova autorização do proprietário.

Pasta de revisão no [Google Drive](https://drive.google.com/drive/folders/1YnMlMXWX3CEmxwnvHa7GSzjGkHFN--EE). O trabalho é do **Instagram Cloud**, separado do GUTHY de YouTube/TikTok.
