# Instagram TUE — produção editorial 01–06/11/2026

Status verificado em 31/10/2026. **Produção em revisão; não equivale a aprovação ou publicação.**

## Regra editorial obrigatória
- Carrossel: 1080×1350, uma lâmina por JPG, composição variável de acordo com o MODELO OFICIAL aprovado pelo usuário: https://drive.google.com/file/d/1FPAIpEijBQ3tHkr-Hg9V_-yCw-dqSHhl/view
- Lúmino original: lanterna vintage dourada, filamento, olhos ciano e lupa; **sem boca humana nem rosto substituído**. Varie a pose, composição e fundo entre lâminas.
- Tipografia preto-condensada em pinceladas amarelas, destaques vermelhos, fundos documentais/fotos temáticas e elementos explicativos grandes.
- Memes podem ter linguagem visual própria; factual e legível.
- Para Reels, TTS via Google AI Studio com voz Rasalgethi, sem API paga; NÃO publicar se a narração não foi conferida.
- Dois horários por dia: 12:00 e 18:00 America/Sao_Paulo. Não aprovar automaticamente arte antiga.

## Status de cada conteúdo

| Data e hora | Tema | Situação e bloqueios |
|---|---|---|
| 01/11 12h | Como ganhou com 46% dos votos depositados? | 8 JPGs V2 **verificados em SHA-256** e individualizados no GitHub; texto factual conferido com o TSE; **revisão visual do padrão ainda pendente**. No schedule, approved=false. |
| 01/11 18h | Meme sobre mito do voto nulo | Tirinha nova em 4 quadros, linguagem factual neutra, JPEG 1080×1350 gerado pelo Actions; **revisão visual final ainda pendente**. No schedule, approved=false. |
| 02/11 12h | Por que o dólar sobe/desce? | V1 com 8 JPGs/legenda no Drive; V2 parcial em pasta separada, **não aprovar V1 só porque existe**. |
| 02/11 18h | Fatores que movem o câmbio | V1 com 8 JPGs/legenda no Drive; V2 parcial/com duplicações. Reconciliar e revisar antes de publicar. |
| 03/11 12h | Onça-parda x pintada | V1 oito JPGs; V2 parcial com capa onde o Lúmino ficou antropomorfizado/alterado. **Corrigir mascote e composição**. |
| 03/11 18h | Onde vivem e caçam as onças | V1 sete JPGs; está muito uniforme, necessita fotos documentais e ângulos diversos; não aprovar. |
| 04/11 12h | Meme ENEM | V1 JPG e legenda no Drive; checar arte, texto e referência ao Inep. |
| 04/11 18h | Estratégias e logística ENEM | V1 oito JPGs; conferir editais/horários e melhorar composição. Datas oficiais 8 e 15/11/2026. |
| 05/11 12h | Foguete funciona no vácuo (Reel) | Somente roteiro, fontes e plano; **áudio Rasalgethi e MP4 final faltantes**. |
| 05/11 18h | Lançamento espacial | V1 oito JPGs; aguarda redesign/checagem visual. |
| 06/11 12h | Por que Lua parece seguir carro (Reel) | Somente roteiro e fontes; **áudio Rasalgethi e MP4 final faltantes**. |
| 06/11 18h | Lua, distância e paralaxe | V1 oito JPGs; revisar ciência e composições, não aprovar automaticamente. |

## Fontes verificadas
- TSE — sistema majoritário e votos válidos: https://www.tse.jus.br/comunicacao/noticias/2026/Junho/sabe-o-que-e-o-sistema-eleitoral-majoritario-o-glossario-explica-1
- TSE — brancos/nulos não anulam eleição: https://www.tse.jus.br/comunicacao/noticias/2026/Setembro/faltam-17-dias-votos-nulos-e-brancos-nao-anulam-a-eleicao
- Inep — ENEM 2026, 8 e 15 de novembro: https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/enem/enem-2026-participantes-ja-podem-conferir-os-locais-de-prova/

## Onde estão os arquivos
- Google Drive, 65 artes V1 + novas versões em revisão: https://drive.google.com/drive/folders/1YnMlMXWX3CEmxwnvHa7GSzjGkHFN--EE
- Votos V2 — oito JPEGs SHA-256 verificados pelo Actions: content/staging/votos-validos-2026-11-01/
- Meme V2 — JPEG 4:5: content/staging/2026-11-01/meme-voto-branco-nulo-v2-final.jpg
- Fila técnica: content/schedule.json — **as duas entradas de 01/11 estão approved=false, não serão publicadas sem aprovação.**
- Halloween 31/10: tirinha publicada às 12h06 (recibo de Meta registrado no ledger), carrossel de 18h aprovado e na fila. Não duplicar.

## Prioridades de execução
1. Conferir visualmente Votos V2 e Meme V2 contra o padrão obrigatório.
2. Melhorar Dólar e Onças (V2 incompletas), com Lúmino idêntico e imagens dinâmicas.
3. Revisar ENEM à luz do Inep, finalizar Reels com áudio Rasalgethi.
4. Somente após QA por post, marcar approved=true. Confirmar publicação apenas com media_id no ledger.
