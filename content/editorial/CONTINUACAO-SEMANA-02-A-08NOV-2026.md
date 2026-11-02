# Instagram TUE — recuperação da produção semanal (02–08/11/2026)

**Atualizado:** 02/11/2026 · **Preset obrigatório:** TUE-MESTRE-01 · **Fuso:** America/Sao_Paulo.

## Resultado verificável desta etapa

- 02/11: dois posts do feed confirmados no ledger oficial da Meta e o Reel dos cães publicado com ID `18141640543620936`, permalink https://www.instagram.com/reel/DfQTVD6iOTA/.
- De 03 a 08/11: **36 PNGs** recuperados diretamente da Biblioteca pessoal e copiados ao Google Drive, distribuídos pelos 12 posts de feed (cada assunto independente).
- As imagens estão no **Drive em revisão editorial**, não são mídias finais nem URL da Meta. A pasta mantém uma folha de contato com as 12 capas, mais uma variação histórica da tirinha de 03/11.
- Foram associados **quatro MP4s originais verificados (03–06/11)** ao planejamento diário de Reels às 18h, sem usar GUTHY novamente. Para 07–08/11 ainda faltam MP4s independentes.
- **Não houve publicação ou agendamento de novos posts nesta etapa.** `content/schedule.json` e o ledger não foram modificados.

## Pastas e índices

- [**Pasta no Drive — artes 03–08/11**](https://drive.google.com/drive/folders/1Ad_thDQq9O66jrTk9m6pp_ljtGli-hZ3)
- [**Prévia das 12 capas no Drive**](https://drive.google.com/file/d/1ct2c9KisVAlH5_blzGwQcvR3sXhvdB0c/view)
- `content/editorial/ARTES-RECUPERADAS-03-A-08NOV-2026.json` — manifesto preciso de cada um dos 36 arquivos, ID/URL do Drive, quantidade por post e QC ainda pendente.
- `content/editorial/REELS-E-STORIES-2026-11-02-a-08.json` — quatro originais de Reel selecionados, com SHA-256, dimensões, duração, legendas e cinco hashtags.
- `content/editorial/semana-independente-2026-11-02-a-08/briefs/` — roteiros de cada imagem, fontes, descrições e legendas individuais já criados.

## Grade por horário

| Dia | 11h — Feed | 15h — Feed | 18h — Reel |
|---|---|---|---|
| 3/11 | URGENTE: REUNIÃO CRIA MAIS REUNIÕES (1 PNG, revisão) | O DESERTO ACORDOU COBERTO DE FLORES? (5 PNGs, revisão) | De onde vem todo o sal do mar? (MP4 no Drive; URL Meta pendente) |
| 4/11 | NO PLANETA VERMELHO O SOL SE PÕE AZUL? (5 PNGs, revisão) | O MUSEU DOS CABOS SEM DONO (1 PNG, revisão) | Por que os cães se sacodem quando estão molhados? (MP4 no Drive; URL Meta pendente) |
| 5/11 | LAVA AZUL? O VULCÃO TE ENGANOU. (5 PNGs, revisão) | TRIBUNAL DOS POTES SOLTEIROS (1 PNG, revisão) | O furacão que atingiu a categoria 5 (MP4 no Drive; URL Meta pendente) |
| 6/11 | CASO 047: A MEIA EVAPOROU (1 PNG, revisão) | QUEM PINTOU ESSE LAGO DE ROSA? (5 PNGs, revisão) | Por que prédios altos balançam? (MP4 no Drive; URL Meta pendente) |
| 7/11 | O OVNI ESTÁ PARADO NO CÉU? (5 PNGs, revisão) | A CADEIRA PEDIU DEMISSÃO (1 PNG, revisão) | Fonte MP4 pendente |
| 8/11 | O CÉU PEGOU FOGO? (5 PNGs, revisão) | SAC DO DESPERTADOR OFENDIDO (1 PNG, revisão) | Fonte MP4 pendente |

**Regra:** 11h e 15h são conteúdos independentes; 18h é Reel do canal original. Não são três partes de um mesmo assunto.

## QC visual: bloqueios observados (não esconder)

- As capas recuperadas têm qualidade gráfica promissora, mas **personagem redesenhado**, não comprovadamente o PNG imutável `content/brand/lumino-original.png`.
- As capas de carrossel foram produzidas com **seta grande isolada**, enquanto o mestre aprovado exige bolinhas pequenas de progresso e texto discreto `ARRASTE PARA O LADO →`, sem seta gigante. Cada carrossel deve ter a indicação até a penúltima lâmina; não na última.
- A arte de reunião 03/11 é um rascunho com construção de cena; o usuário havia rejeitado uma remontagem posterior simplificada. Nenhuma delas se converte automaticamente em versão final.
- As imagens observadas nesta etapa têm **1122 × 1402 px**, enquanto os JPGs de publicação precisam de **1080 × 1350 px**. Resize preservando a proporção é etapa posterior à revisão visual; não equivale a criação de detalhe em 4K.
- Algumas capas têm a identificação `ILUSTRAÇÃO EDITORIAL`, coerente com materiais ilustrados. Não substituir por fotos inventadas nem simular imagens documentais do satélite/Copernicus ou da NASA.
- Verificar todas as 36 páginas quanto a tipografia, fatos, identidade, direito de uso e conteúdo sintético. A checagem das capas não substitui análise dos miolos.

**Decisão de segurança:** manter `approved=false`, `visual_reviewed=false` e ausência de agendamento até efetuar as correções visuais e revisar individualmente os JPEGs finais. Roteiro e cópia de rascunho não são aprovação nem publicação.

## Reels e Stories

- Reels 03–06/11: os MP4s estão em pasta privada do Drive. Antes de publicar pela Meta, cada arquivo requer URL pública de mídia, checagem de duplicação, liberação de procedência e recibo independente.
- Reels 07–08/11: sem seleção de fonte verificada. Não reciclar vídeo ou inventar link.
- Stories: **21 vínculos planejados** para os 7 dias × 3 postagens. Como exige o padrão aprovado, são **compartilhamentos NATIVOS do post original**, somente após o feed/Reel existir, com chamada **em TEXTO**, sem narração e sem link externo. O Reel dos cães já tem o link do post-pai registrado, mas o Story ainda não foi compartilhado nem confirmado.
- Música em carrosséis requer mecanismo legítimo de publicação com recurso nativo; a Graph API não prova anexação de música nativa. Não registrar reprodução de áudio inexistente.

## Retomada sequencial

1. Revisar **03/11 11h — Reunião** diretamente contra o PNG original e a referência visual de 02/11, evitando reconstituir cena aprovada; caso falhe, corrigir apenas esse conteúdo.
2. Fazer QC final do carrossel **03/11 15h — Atacama**: cinco lâminas, tipografia, indicador de arrastar, personagens e créditos/Copernicus.
3. Validar e hospedar o MP4 de **03/11 18h — Sal do mar**, com hash, checagem de duplicatas e publicação apenas após a mídia estar tecnicamente apta.
4. Seguir **04/11 → 08/11**, um item completo por vez, e após cada publicação confirmada executar/verificar o Story nativo vinculado.

**Não confundir esta recuperação editorial com postagem agendada ou entregue no Instagram.**

## Complemento — revisão de legendas e QC automatizado

- As **12 legendas independentes de 03–08/11** foram escritas em `content/editorial/LEGENDAS-REVISTAS-03-A-08NOV-2026.json`. Cada uma contém chamada própria, contexto editorial e **cinco hashtags específicas**. Continuam `approved=false` até liberar a arte.
- A validação editorial estrutural passou no [GitHub Actions 41536460193](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41536460193). Ela confirma integridade do preset, planos, regras de Stories nativos e rejeição do renderizador genérico; **não valida esteticamente nem aprova automaticamente as 36 imagens**.
- Foram corrigidos testes históricos que supunham incorretamente que o Reel de 02/11 ainda não estava publicado ou que a antiga imagem-modelo estava vigente. A exceção para o Reel já publicado exige comprovante real da Meta no ledger, sem liberar Reels futuros.
- Uma comparação visual humana ainda é obrigatória e a arte da reunião/mascotes não pode ser promovida só por ter passado em testes de código.
