# EP01 Faker V2.7 — Atuação preservando o conceito aprovado (08/11/2026)

**Padrão:** TUE-CINEFRAME-01. **Estado:** RECONSTRUÇÃO ARTÍSTICA INCOMPLETA — teste apenas interno, **nenhum vídeo liberado**.

## Por que esta mudança foi necessária

A V2.6 tinha um boneco genérico que não respeitava a referência ilustrada aprovada. A V2.7 muda a origem do estudo de movimento: parte da **pose sentada real da folha de referência** e não da cabeça vetorial redesenhada que se afastou da identidade do Faker.

### Teste efetivamente realizado

- Extraiu-se **uma pose de 415×320 pixels** do concept original para **guia de movimento interno**, jamais como arte final 4K.
- A animação usa campos locais de deformação com controle independente da cabeça (cabelo, olhos e óculos movem juntos), mão esquerda sobre o mouse, mão direita no teclado e movimento sutil do torso. Fundo de treino separado do ator: **não é zoom nem pan de fotografia**.
- A máscara alfa foi corrigida para remover halos e pontilhados no contorno do personagem.
- Foi renderizado um ensaio interno de **4 segundos / 540×960 / 30 FPS**, com 120 fotogramas lidos por ffprobe e 120 fotogramas únicos, sem arquivo truncado.
- Verificamos as regiões da imagem em separado: cabeça = **15,11** de variação média máxima em nível RGB; mão do mouse = **7,98**; mão do teclado = **11,94**; fundo estático = **0,044**. Portanto, há movimento localizado no ator com fundo estável, não só transição de câmera. São métricas de diferença de pixels, **não** certificação de naturalidade.
- Ainda não é animação de personagem de alta qualidade e **não atende** à política de pilotos originais 2160×3840/60 FPS.

## Pacote técnico conferido no Google Drive

`EP01_FAKER_V27_FIDELIDADE_E_MICROATUACAO_FONTE_INTERNA_NAO_APROVADA.zip`

ID Drive: `1E1On1RxizmcBPLUEu1oChM_dYl_UKZoK`

Link interno: https://drive.google.com/file/d/1E1On1RxizmcBPLUEu1oChM_dYl_UKZoK/view

- Arquivo confirmado por metadados: **1.555.824 bytes**.
- ZIP local com 12 entradas e `testzip()` sem erros.
- SHA-256 local: `02570efa755a5811295bfb506c02210b42e05cd134e20b672d8dbbae42a421bc`.
- Inclui código reproduzível, concept nativo de 415×320, cenário de treino SVG, máscara guia, cinco fotogramas de QA, manifestos de direção e relatório de teste. **O MP4 de QA não está neste ZIP nem foi enviado ao Drive**, pois o usuário autorizou entrega de vídeos somente com fidelidade/cinematografia aprovadas.

## Resultado do QC

| Aspecto | Resultado |
|---|---|
| Originalidade das feições preservadas durante o estudo | **Aprox. preservadas**, já que o movimento usa pixels da ficha aprovada |
| Fundo permanece estável, ator se movimenta em regiões separadas | **OK técnico** |
| Codificação completa dos 120 quadros de 30 FPS | **OK técnico** |
| Corte e máscara do concept | **OK como guia interno** |
| Arte 4K nativa redrawn para frente / 3/4 / perfil | **FALTA** |
| Rigs com articulações de mãos e dedos, contato orgânico, peso de corpo | **FALTA** |
| Cenário de treino premium com continuidade e direção final | **FALTA** |
| 14 tomadas cinematográficas concluídas | **FALTA** |
| Narração Rasalgethi com timecodes e legendas sincronizadas | **FALTA** |
| MP4 completo de 105–125 segundos 2160×3840 60 FPS | **FALTA** |
| Aprovação editorial | **BLOQUEADA** |

## Direção de arte que permanece obrigatória

1. Redesenhar as **três vistas originais** de rosto e corpo em resolução adequada a planos próximos 4K, sem ampliá-las e chamá-las nativas.
2. Preservar cor da franja, óculos de armação fina, nariz, proporção craniana e figurino preto/vermelho (ficha: https://drive.google.com/file/d/163C38f5RBR1mtf7r8z9FBYuQfrJubQnF/view).
3. Completar rig nas camadas de pescoço, pálpebras, cabelo, ombros, antebraços, pulsos, mãos e dedos; garantir contatos físicos e oclusão.
4. Construir sets de arena/treino e movimento corporal bem resolvidos, não somente sprites com pequenas distorções.
5. Gravar Rasalgethi original via Google AI Studio, ajustar tempo de cena pela narração e montar o filme.
6. Só liberar 4K60 nativo, audiovisual QC editorial e envio Drive com link verificado.

**Decisão:** toda a V2.7 é trabalho técnico em progresso, não um piloto aprovado. **Nenhum vídeo foi publicado/agendado.**