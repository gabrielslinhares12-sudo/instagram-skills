# Instagram TUE — retomada editorial sequencial — 02/11/2026

## Decisão do proprietário
Retomar criação de conteúdo segundo a identidade aprovada; pausar análise de Android persistente, DuoPlus, Clousd, GeeLark e tentativa de música já publicada. NÃO iniciar nem agendar jobs cloud phone adicionais; workflows de diagnóstico ficam disponíveis apenas para histórico, sem uso no fluxo editorial.

## Primeiro item da fila retomado
- Votos válidos — exemplo presidencial hipotético 44/46/10 e percentual de 51,1% sobre 90 válidos.
- O arquivo `content/editorial/votos-validos-reconstrucao-v3.json` é a fonte de conteúdo e pesquisa do primeiro item.
- O renderizador `scripts/instagram_render_votos_v3.py` monta sete artes JPEG 1080×1350 separadas, cada uma com fotografia de urna TSE (Wikimedia Commons) e PNG exato original do Lúmino, sem alterar o mascote.
- O carrossel é variado e tem conteúdo aprofundado. A imagem de referência 2×4 não é usada como capa nem como carrossel.
- A capa utiliza o gancho factual `COMO ASSIM? 46% DOS VOTOS E GANHOU?`, qualificado como hipótese presidencial.
- O rodapé usa deslizamento e pontos discretos sem numeração escrita.
- Três fotos TSE de origem e licença identificadas no manifesto; não representam a eleição hipotética.
- QA automático confirma assets canônicos, anatomia e composição via correspondência PNG, bandas amarelas, área vermelha, fundo claro, 1080×1350, hash e prévia.
- Revisão visual humana ainda obrigatória; `approved=false`. Nenhuma publicação ou agendamento neste workflow.

## Ordem após concluir este item
1. Meme de voto nulo/branco 01/11 — revalidar a tirinha final no padrão próprio.
2. Dólar 02/11 — reconstruir as páginas internas, não misturar capas de versões diferentes.
3. Fatores do câmbio 02/11 — harmonizar e remover duplicações.
4. Onças 03/11 (duas peças) — rever versões finais mais recentes.
5. ENEM 04/11 (meme e carrossel) — checar fontes Inep.
6. Reels e artes da Lua 05–06/11 — dependência da voz Rasalgethi e MP4 real.

## Fontes do primeiro conteúdo
https://www.tse.jus.br/comunicacao/noticias/2022/Outubro/entenda-como-e-eleito-o-presidente-da-republica
https://www.tse.jus.br/comunicacao/noticias/2026/Setembro/faltam-17-dias-votos-nulos-e-brancos-nao-anulam-a-eleicao
https://www.tse.jus.br/comunicacao/noticias/2026/Junho/sabe-o-que-e-o-sistema-eleitoral-majoritario-o-glossario-explica-1

## Controles imutáveis
- Não publicar/agendar por GitHub, nem alterar `content/schedule.json` ou `content/publication-state.json` até revisão e autorização editorial.
- Não duplicar Halloween publicado e não inventar recibos, horários ou música.
- Produzir um carrossel por vez, com validação factual, gráfica e antifraude antes de avançar.
