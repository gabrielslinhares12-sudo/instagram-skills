# FAKER — V4.6: orientação vertical obrigatória (10/11/2026)

**A V4.5 e a abertura anterior foram reprovadas: usavam imagens horizontais.** O usuário proibiu **fotografias originalmente horizontais** para o Reels. Esta regra vale para abertura, campeonatos, vida pessoal, fotos de equipes e material de arquivo.

## Prévia realmente refeita
- [Abertura reconstruída em 2160×3840/60fps, 8s, apenas retrato originalmente vertical de Faker](https://gcdn.picsart.com/media-engine/d958a791-7c2a-4c9a-b9e8-9e1ad2679d03.mp4)
- Fonte original: https://news.nateimg.co.kr/orgImg/fk/2026/04/07/52087_45949_1724.png — **1280×1563**, 2026, orientação retrato. `cover` mantém proporção uniforme e recorta apenas bordas, sem esticar, distorcer ou gerar bordas falsas. O arquivo 4K exportado **não** significa que a fotografia seja originalmente 4K.
- Alternativa vertical 2025 T1 (original 1080×1350): https://img-cdn.theqoo.net/jUkiPd.jpg
- Foto documental vertical 2023 T1/Worlds (original 3000×4000), crédito Creative Silver CC BY 4.0: https://upload.wikimedia.org/wikipedia/commons/b/b4/T1_hold_2023_Summoners_Cup.jpg

## Regra de QC bloqueante
1. **Aceitar apenas fotos com metadados originais `width < height`; se ausentes, reprovar a fonte.** Não basta a fotografia aparecer vertical após crop de original horizontal.
2. **Proibido `fit=fill`, escalas X/Y distintas, blur-fill, faixas criadas pela foto repetida, colagens esticadas, ou imagens deformadas para 9:16.** `cover` é permitido somente para fontes **originalmente verticais** e sem afetar rostos/troféus.
3. **Vídeos reais de partidas são outra classe de fonte:** podem usar enquadramento editorial vertical, mantendo o jogo fiel e sem distorção. A proibição expressa se refere a **fotografias horizontais**.
4. **Preferência por fontes originais >= 2160×3840**. Fonte menor só com aviso/QC; não chamar de nativa 4K.
5. Fotos não substituem replays reais, conquistas e comemoracões. Não criar fotos com zoom fingindo vídeo.
6. Introdução única Lendas do E-Sport, depois Lee Sang-hyeok/Faker, legenda inferior só junto da voz Rasalgethi no filme definitivo.
7. V4.2 permanece reprovada. O vídeo de 8s é **prévia de abertura**, não o episódio completo. Não publicar/agendar antes de aprovação visual e áudio.

## Material verificável
O pacote de validação [ZIP](pacote local V4.6 (link no chat)) contém `vertical_photo_gate.py` e manifesto. Atualizar link apenas se upload confirmar; o arquivo local de origem é `FAKER_V46_CORRECAO_FOTOS_VERTICAIS_GATES.zip`.
