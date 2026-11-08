# EP01 FAKER — registro verificável de produção 2D / 4K60

**Data:** 08/11/2026
**Padrão:** TUE-CINEFRAME-01, branch experimental isolada.
**Estado atual:** MOVIMENTO 2D RENDERIZADO — 20 SEGUNDOS. **NÃO É O FILME COMPLETO; não há voz Rasalgethi.**
**Publicação:** bloqueada até aprovação editorial.

## Arquivo gerado
- Nome: `EP01_FAKER_TESTE_MOVIMENTO_2D_4K60_20s_SEM_VOZ.mp4`.
- Drive MP4 verificado: https://drive.google.com/file/d/1O_NdJVLblBu8bDeG1U2aAjbb6tM4Jsoa/view
- Pasta exclusiva EP01 no Drive: https://drive.google.com/drive/folders/1nBTh0Jbx4_qhxm2ttFIH3IsKVLN_h49G
- Características conferidas por ffprobe: H.264, **2160×3840**, **60/1 FPS**, **1200 quadros**, **20,000 s**, AAC mono 48000Hz.
- Tamanho de upload verificado via Drive: **57.055.443 bytes**.
- SHA-256 do MP4 local: `b9e860a75891404bd71715a993257eace387538b8dd269d140376fc41540dc41`.
- Qualidade dos vetores: rasterizados diretamente por Cairo em 2160×3840 a cada quadro; não são stills de baixa resolução escalados.
- Animação: rig procedimental de cabeça, membros, mãos, postura, piscar de olhos, troféu preso à mão, atores de apoio e confete; mudanças reais entre quadros consecutivos. **Fidelidade ao boneco de referência ainda depende de QC.**
- Trilha: instrumental original sintetizado, sem biblioteca comercial, sem voz; não substitui Rasalgethi.

## Sequência temporal do teste
- 00–04 s: Faker treinando no equipamento, braços/mãos movimentando-se no teclado e cabeça em ação.
- 04–08 s: conquista de 2013; personagem entra no palco e levanta troféu preso à mão.
- 08–12 s: derrota de 2017; postura desaba, cenário escurece gradualmente.
- 12–16 s: treino e estudo, movimentos da mão sobre o papel e dos braços.
- 16–20 s: retorno em 2025; vários personagens articulados, postura de celebração e partículas.
- Legendas: provisórias, apenas para indicar as passagens históricas; **não são transcrição de voz**.

## Fontes de produção no Drive
- Folha 2D do Faker: https://drive.google.com/file/d/163C38f5RBR1mtf7r8z9FBYuQfrJubQnF/view
- Código de rig vetorial executável `render_faker_rig.py`: https://drive.google.com/file/d/1_s66YNTDj-Xhtt-vGQ6s-1dP1TT5vxVp/view
- Gerador de trilha `create_soundtrack.py`: https://drive.google.com/file/d/1mLhErerD1S-66750P5evIM2BjYqGQd8Z/view
- Trilha `score_original_20s.wav`: https://drive.google.com/file/d/1CjoEUY5NpxV6zpB7Yhy-xnn5Y17qzSL2/view

## Comando de render (Linux runner + FFmpeg/Cairo)
Após instalar `python3-cairo`, `ffmpeg`, `numpy`:
```bash
python create_soundtrack.py
python render_faker_rig.py --duration 20 --stdout |
  ffmpeg -y -f rawvideo -pixel_format bgra -video_size 2160x3840 -framerate 60 -i pipe:0 \
    -i score_original_20s.wav -c:v libx264 -preset ultrafast -crf 19 \
    -pix_fmt yuv420p -c:a aac -b:a 160k -shortest EP01_FAKER_TESTE_MOVIMENTO_2D_4K60_20s_SEM_VOZ.mp4
```

## Bloqueios antes de chamar de final
1. **Design QC:** o boneco é uma implementação vetorial simplificada do personagem-base. Precisa de refinamento visual para aproximar-se da ficha ilustrada em cabelos, rosto, volume, figurino e timing de atuação. Não promover este artefato como aprovado.
2. **Narrativa:** roteiro integral no `roteiro_direcao.md` (aprox. 78s). O teste de 20s não cobre todos os fatos.
3. **Voz:** gerar narração Rasalgethi via Google AI Studio autentificado, preservar MP3/WAV, ajustar timecodes das cenas. Nada de substituir por outra voz sem autorização ou pagar API.
4. **Animação:** adaptar o rig às 10 tomadas planejadas, garantir coerência visual, geografia, pés fixos e mãos interagindo.
5. **QC:** validar sincronismo e assistir sem som e com som, 4K60 original, sem apenas fotos e zoom, sem marcas-d'água.
6. **Entrega:** após concluído, enviar versão completa para a mesma pasta Drive, confirmar metadados, compartilhar link aqui. **Nenhuma publicação ou agendamento automático.**

## Nota
O arquivo é um **teste de movimento efetivamente gerado e enviado ao Drive**, não o episódio narrado final. A transmissão para o Drive foi validada por leitura de metadados de arquivo após upload.
