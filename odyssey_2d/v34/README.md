# A Odisséia — Reestruturação 2D V33

## Referência editorial
Modelo visual **Odisseu e Cavalo de Troia**, vídeo de 60 segundos criado/aprovado pelo proprietário em 05/11/2026. Este pacote recupera a cabeça original de Odisseu e o cavalo do filme original, não inventa substitutos para eles. Os personagens adicionais são desenhados pelo motor de animação 2D e requerem revisão artística rigorosa para harmonizar completamente com o primeiro vídeo.

## Conteúdo
- `shot_contract.json`: contrato de **68 tomadas específicas**, distribuídas pelas 16 cenas e pelos 220,56s originais.
- `render_v33.py`: motor de quadros, ações individuais e áudio original, sem Blender/Runway/Guthy ou APIs pagas.
- `scenery_v28.py`: ambientes completos com layers de palácio, ruas de Troia, mares, cavernas e objetos históricos.
- `render_16_cenas.py`, `canon_rig.py`, `base_tue.py`: bibliotecas de composição, elenco e fala.
- `assets/`: extrações visuais de Odisseu e cavalo, com transparência.
- `audio.wav`: narração Rasalgethi original, SHA256 `9be8b79920b318c76f23874d38d12f4f77b46f8a9871833612ac1efa82b5d667`.

## Reprodução
```bash
python3 -m pip install Pillow
sudo apt install ffmpeg
python3 render_v33.py --voice audio.wav --fps 30 --width 720 --height 1280 --output ODISSEIA_68_TOMADAS_RASALGETHI_QC.mp4
```

## LIMITES DESTA VERSÃO
A edição é **completa tecnicamente**, mas continua **não aprovada editorialmente**. São cenários vetoriais/procedurais, não a animação com cenários ilustrados ao nível que o usuário solicitou. Legendas estão alinhadas por frases estimadas dentro das 16 cenas; ainda não há alinhamento palavra a palavra. Os 68 beats têm ações distintas previstas, mas as figuras secundárias e a atuação da cena de Polifemo ainda exigem animação de alta fidelidade. 720p/30 é revisão, não mestre 4K nativo/60. Não publicar automaticamente.

## V34 — melhorias efetivamente aplicadas
O protagonista deixa de ser um corpo redesenhado: `puppet_original_v30.py` aplica máscaras articuladas ao desenho recuperado do Cavalo de Troia. A pedra do gigante recebeu faces, fraturas e sombra de contato; a mixagem externa final usa narração original e a trilha instrumental existente, em volume baixo. O vídeo renderizado foi validado por ffprobe e decodificação integral. **Essas melhorias não equivalem a aprovação visual profissional**.