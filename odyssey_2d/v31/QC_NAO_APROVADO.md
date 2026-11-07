# A Odisseia — Auditoria visual e reconstrução 2D V31

**Estado em 7 de novembro de 2026: REPROVADO para publicação e entrega como filme final.**

## Por que a V27 foi reprovada

1. A V27 tratava 16 cenas como 64 trechos em quatro partes, mas reutilizava nomes de cenários: 11 tomadas em `hall`, 10 em `sea`, 7 em `island`, 4 em `underworld`. As repetições visuais não correspondiam às mudanças narrativas.
2. Grande parte das ações correspondia a pequenos movimentos genéricos de braços. Não comprovava início, execução, contato e consequência.
3. O desenho do Odisseu variava do material canônico. A cabeça era próxima, mas o tronco, figurino e proporções foram reilustrados no render anterior.
4. Caverna e pedra não mantinham a escala convincente de Polifemo (5,5m) diante de Odisseu (1,84m), e o contato das mãos era insuficiente.
5. As legendas eram aproximadas por subdivisões de áudio, não alinhadas palavra a palavra.
6. A resolução do arquivo final era ampliada a partir de fonte de resolução inferior; **4K/60fps entregue como arquivo não constitui animação nativa 4K/60fps**.

## O que de fato foi implementado nesta reconstrução

- Recuperação do **sprite exato e transparente de Odisseu da animação de Troia**, em 238×381 px, e extração de cabeça, torso, braços, pernas e capa em articulações 2D reutilizáveis sem reilustrar a aparência.
- Motor `troia_puppet_rig_v30.py` para andar, levantar braços, empurrar e tensionar o arco; teste real de 180 quadros a 30 FPS.
- Substituição do ciclope genérico por um novo modelo 2D com anatomia estilizada, **um único olho central**, cabelos, corpo, braços, pernas, roupa e pés no solo, conforme `troia_cyclops_art_v31.py`.
- Reorganização da cena 04 em **oito momentos diferentes**: entrada, pedra, vinho, sono, estaca, ovelhas, declaração do nome e invocação de Poseidon.
- Correção do erro de **encolher Polifemo** durante a queda: a altura nominal permanece fixa.
- Substituição do boulder circular por contorno irregular apoiado no piso.
- Criação de contrato editorial com **68 tomadas de ação distintas** e narração completa de 220,56 segundos, com nenhuma ação de roteiro duplicada.
- Trecho S04 animado de **19,833 s, 540×960, 24 FPS, H.264 + AAC** com áudio extraído sem alteração do WAV Rasalgethi original; arquivo apenas para revisão.

## Falhas remanescentes — bloqueadores

- Ainda há recortes do ciclope nas extremidades do enquadramento quando a pedra ocupa a boca da caverna.
- A ação do sono e a perda de equilíbrio precisam de poses reais, sem redução de escala, e o contato das duas mãos com a pedra ainda exige ajuste quadro a quadro.
- As ovelhas e personagens secundários ainda não têm o acabamento do Cavalo de Troia original.
- Os cenários criados proceduralmente para as outras 15 cenas ainda não atingem a qualidade do vídeo original; trocar fundo genérico por detalhes não basta.
- **O filme completo com 16 cenas NÃO foi aprovado visualmente nesta versão.** O único vídeo V31 gerado é o teste S04, não um filme de três minutos.
- As legendas da cena04 continuam temporizadas editorialmente, não por transcrição de alinhamento palavra a palavra.

## Critérios de aprovação antes do próximo master

1. **Visual**: personagens, linhas, paleta e materiais comparados ao vídeo canônico `Cavalo_Troia_4K60_Meta_10h.mp4` em cada quadro-chave.
2. **Narrativa**: 68 ações do contrato exibem exatamente os fatos que a narração menciona, sem começar uma ação e abandonar antes da consequência.
3. **Física**: porte relativo Odisseu 1,84m, Polifemo 5,5m; pedra maior que a entrada; mãos/armas/cordas agarradas; pés apoiados no chão.
4. **Cenários**: cada cenário completo tem geografia consistente, e seu desenho pertence ao mesmo mundo da animação original.
5. **Tempo**: confirmar pelo áudio os intervalos de cada frase; não acelerar voz ou reaproveitar a mesma ação em momentos desconexos.
6. **Publicação**: nenhum arquivo pode ser marcado final, enviado ao Instagram ou agendado se houver defeito visual ou narrativo conhecido.

**Conclusão:** houve avanço técnico verificável, mas não há justificativa para declarar o filme finalizado. Os MP4 V27 são versões rejeitadas e NÃO devem ser republicados.