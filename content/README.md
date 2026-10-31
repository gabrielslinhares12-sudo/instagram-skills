# Instagram TUE — estado operacional e política de publicação

**Atualizado em 31/10/2026.** Este documento substitui descrições antigas de lotes aprovados que não refletem mais a identidade visual atual.

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
