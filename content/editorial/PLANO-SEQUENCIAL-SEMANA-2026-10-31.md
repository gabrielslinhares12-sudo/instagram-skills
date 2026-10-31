# Produção sequencial do Instagram — 31/10 a 06/11/2026

## Correção obrigatória em 30/10/2026
A primeira publicação (Halloween) tinha a **imagem antiga** no manifesto e foi BLOQUEADA. Antes de retomar leia `content/editorial/HALLOWEEN-CORRECAO-MIDIA-2026-10-31.md` e substitua por exato JPEG novo 1080 × 1350 (SHA256: `9b909155390281e5c9648c1eb3cb330f05bc0b459016f07b0a1428eaf3d2bdc8`). Até isso ser verificado, `approved=false`; não publicar a antiga.

## Autorização
Em 30/10/2026 o proprietário autorizou expressamente a produção e o agendamento automático de **um post completo de cada vez**, sem pedir novas aprovações, para o perfil **@temumaexplicacao**, com **notificação sempre que finalizar um** e início do próximo logo em seguida. Esta autorização é limitada ao lote abaixo, e não inclui outros perfis/canais.

## Ordem / prazo editorial / janela de publicação
Todos os horários são **12h de Brasília/Fortaleza (UTC−3), ou 15:00Z**, e alvos sujeitos ao atraso dos cron jobs do GitHub Actions.

| Ordem | ID no manifesto | Conteúdo | Publicação-alvo | Tipo | Status inicial |
|---|---|---|---|---|---|
| 1 | lumino-halloween-2026 | Halloween — meme Lúmino | 31/10/2026 | imagem | arte antiga identificada; aprovado=false até substituição pela versão melhorada correta |
| 2 | lumino-votos-2026 | 46% dos votos registrados vs 51,1% dos válidos | 01/11/2026 | carrossel com oito JPGs | reconstruir antes de liberar |
| 3 | lumino-dolar-2026 | Por que o dólar sobe e desce — fatores e efeitos | 02/11/2026 | carrossel com oito JPGs | reconstruir antes de liberar |
| 4 | lumino-oncas-2026 | Onça-parda vs onça-pintada — espécies, filhotes, melanismo | 03/11/2026 | carrossel com sete JPGs | reconstruir antes de liberar |
| 5 | lumino-enem-2026 | Modo ENEM — meme curioso | 04/11/2026 | imagem | revisar no estilo de referência antes de liberar |
| 6 | lumino-foguete-2026 | Por que foguetes funcionam no vácuo? | 05/11/2026 | Reel MP4 com narração original | revisão completa de duração, mídia e áudio antes de liberar |
| 7 | lumino-lua-2026 | Por que a Lua parece acompanhar o carro? | 06/11/2026 | Reel MP4 com narração original | revisão completa de duração, mídia e áudio antes de liberar |

## Direção estética obrigatória
Seguir `content/editorial/IDENTIDADE-VISUAL-LUMINO.md`, que registra o estilo aprovado do proprietário: **capa de referência “COMO ASSIM 51% DOS VOTOS E NÃO GANHOU?”**, com fundo claro documental texturizado, letras negras enormes e condensadas, pinceladas amarelas, contrapontos em vermelho, Lúmino-lanterna grande e claramente reconhecível, lupa e olhos ciano, textura e profundidade. A redação original do gancho eleitoral é factualmente inadequada para o exemplo presidencial; reescrever mantendo impacto visual. Não usar o antigo visual simplificado de páginas brancas com barras finas. No carrossel, não numerar lâminas nas artes; incluir apenas indicador sutil “Deslize para o lado →”, sem excesso de elementos. O usuário deseja explicações aprofundadas, ancoradas em fontes verificáveis e números corretos.

## Execução — um item por vez, sem aprovação extra
1. **Antes de mexer em qualquer publicação:** ler `content/schedule.json`, `content/publication-state.json`, esta pauta e os arquivos existentes. Se item já `published`, não reenviar. Se `claimed` ou `needs_review`, investigar no Instagram e no container antes de qualquer nova tentativa; nunca repetir publicação incerta.
2. **Preparar somente o próximo item não finalizado.** Confirmar fatos, criar roteiro e legenda, criar mídias em formato aceito pela Meta (JPG 4:5 para posts/carrosséis; MP4 completo para Reel), com o mascote correto, sem marca-d'água, sem API paga.
3. **Verificar mídias finais**, dimensão, integridade, legibilidade, proporção de gráficos, consistência do Lúmino, URLs públicas imutáveis (commit SHA) e legendas. Nunca marcar `approved=true` com mídias antigas que não atendam ao novo roteiro e estilo.
4. **Registrar o item final no manifesto** mantendo ID, conta e data corretos; pôr `approved=true` somente após verificação de mídia e legenda, autorização global já concedida pelo proprietário. Manter os outros itens bloqueados.
5. **Notificar o proprietário ao finalizar cada item** com título, data, links reais das artes, status de agendamento (`manifesto aprovado / aguardando hora` ≠ `publicado`), e eventuais falhas. Não enviar mensagens sem novidade. Quando tiver recibo `published` no ledger, notificar confirmação real com `media_id`.
6. **Iniciar o próximo imediatamente após terminar o anterior** ou na próxima execução da automação. Não criar duas pautas simultâneas. Depois de finalizar o sétimo e conferir o recibo final, desativar monitoramento específico deste lote.

## Controle de qualidade obrigatório
- **Votos:** usar exemplo hipotético Presidência: B=46, A=44, brancos/nulos=10, registrados=100, válidos=90, 46/100=46%, 46/90≈51,1%; 46 é mais que metade de 90, portanto venceria no 1º turno. Não dizer “51% dos válidos e não ganhou”. Brancos/nulos não se transferem a candidatos nem anulam automaticamente eleição.
- **Dólar:** explicar fluxos externos, juros relativos, prêmio de risco, expectativas, preço flutuante, intervenção do BC e repasse incompleto de câmbio aos preços, sem causalidade determinista. Exemplo numérico sempre explicitamente hipotético.
- **Onças:** usar nomes científicos `Puma concolor` e `Panthera onca`; filhotes de parda com manchas e melanismo da pintada; não tratar melanismo como espécie separada.
- **ENEM:** evitar calendário de prova não confirmado; se usar datas, verificar fonte oficial do ano.
- **Reels:** não reutilizar vídeos incompletos apenas porque o MP4 existe; checar sincronismo com texto/voz e adequação ao Reel.
- Verificar que o cron está ativo, que os testes da fila passam, que as concessões do token (preflight) estão válidas e que não há `needs_review` antes de publicar.
- Se ficar impossível concluir o próximo item até a janela prevista, deixar `approved=false`, relatar com precisão e **nunca publicar uma versão sabidamente antiga, errada ou superficial**.

## Observação técnica
O fluxo de `scripts/instagram_queue.py` faz publicação **na janela devida**, não criação de conteúdo; a automação de criação/monitoramento deve preparar cada mídia antes da data. Uma entrada `approved=true` significa conteúdo pronto na fila, NÃO prova que o Instagram já publicou.
