# A Odisseia — O Regresso a Ítaca — V35B (produção 2D, não aprovada)

O objetivo editorial é refazer **A Odisseia** usando o filme original de 60 s **Odisseu e o Cavalo de Troia** como **referência estética obrigatória**, com o Odisseu e o cavalo extraídos daquele filme, novos personagens no mesmo universo e diferentes ações em todos os blocos da narração. Arquivos das versões V19–V34 **não devem ser usados como filmes finais**.

## O que de fato foi reconstruído neste pacote

- 16 ambientes 2D ilustrados, compostos em `environments_v35.py`: muralhas e ruas de Troia, costa cícone e floresta de lótus, caverna com portal e monólito, palácio de Circe, mundo dos mortos, rochedos das sereias, geografia permanente de Cila/Caríbdis, ilha dos bois, ilha de Calipso, salão feácio, palácio de Ítaca, cabana de Eumeu, quarto do tear, cama enraizada e pomar de Laertes.
- 68 ações de roteiro, uma por tomada, no contrato `retimed_68_shots.json`; tempos relativos reajustados por **segmentação manual de cláusulas**. Não é alinhamento ASR palavra por palavra. Os limites de cena foram mantidos conforme pausas previamente verificadas no áudio.
- Reescrita dos oito momentos com erros críticos (`special_acting_v35.py`): Polifemo empurra a rocha, recebe vinho, cambaleia e sofre o ataque da estaca; seis cabeças de Cila com seis vítimas; Penélope junto ao tear, tecendo/desfazendo; Argos com cabeça, patas e focinho reconhecíveis.
- Animação do desenho original de Odisseu e do cavalo proveniente do vídeo da conta do usuário, não ilustrações genéricas em seu lugar.
- Planos de câmera com diferentes proximidades, aplicados à cena animada, nunca fotos com `zoompan`.
- Faixa de voz original (Google AI Studio Rasalgethi) de 220,56 s, SHA256 `9be8b79920b318c76f23874d38d12f4f77b46f8a9871833612ac1efa82b5d667`.

## Regras editoriais e limites honestos

Esta entrega é uma **montagem de revisão**, não a versão final aprovada. Os movimentos dos personagens secundários e a complexidade dos ambientes ainda podem ser insuficientes perante a referência oficial. Algumas ações utilizam o motor 2D herdado como infraestrutura, apesar da cenografia e das oito ações citadas terem sido refeitas. A sincronização dos acontecimentos com a fala foi aproximada por distribuição manual de texto, não confirmada por alinhamento palavra a palavra. O raster de desenho é nativo 540×960 e a cópia de visualização renderizada em 720×1280/30fps; **não afirmar 4K/60fps nativo**.

**Não publicar, agendar ou trocar vídeos em redes sociais sem QC visual e autorização do usuário.**

## Como renderizar

Requer Python 3.10+, Pillow e FFmpeg. O ambiente local deve ter `audio.wav` e `assets` (recortes originais do vídeo de Troia). As cenas podem ser recalculadas via:

```bash
python render_v35.py --voice audio.wav --output ODISSEIA_V35B_QC.mp4 --width 720 --height 1280 --fps 30 --crf 18
```

O arquivo `.qc.json` registra os dados de render e a reprovação editorial; o contato visual está em `V35_QC_FINAL_STILLS_1.jpg` e `V35_QC_FINAL_STILLS_2.jpg` no pacote ou no diretório de revisão.