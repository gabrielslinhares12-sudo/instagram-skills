# Odisseia V11 — QC visual da cena Polifemo

**Render de prova:** GitHub Actions [42354119274](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/42354119274). `success` = 5 PNGs foram produzidos, **não** aprovado artisticamente. O material não deve ser publicado nem replicado para as outras 15 cenas.

**Aspectos tecnicamente melhores:** duas identidades humanas procedurais de época, sem a farda militar moderna da V10; armature GLB + Push mocap em Polifemo; 5 estágios de animação 3D; cenário com rochas irregulares e câmera de aproximação; todos os PNGs renderizados; áudio original Rasalgethi permanece intocado.

**QC artístico: REPROVADO para uso no filme final.** Inspeção do contato de 5 PNGs:
- O ciclope ainda parece um humano de loincloth com prótese ocular branca projetada. A anatomia de UM olho central integrado à face não ficou convincente.
- A rocha à frente da caverna tem geometria ovoide artificial. Precisa parecer um monólito pesado, mineral e irregular, com textura PBR verdadeira e sombras de contato.
- Os maciços da caverna continuam com volume de esferas visíveis em vez de rocha natural contínua.
- Não se compreende a diferença de escala de Polifemo e de homens de 1,8 m. Um homem está oculto no fundo durante o empurrão.
- O corte interno de 360 quadros mostra praticamente só o monólito, sem os marinheiros encurralados. Consequência dramática ausente.
- Continuidade de mãos/rocha e ação corporal precisa ser avaliada na prévia de vídeo real, que está rodando separadamente como ação 42354238407; não declarar aprovado antes desse teste.
- O render é 720x1280 QC, longe de 2160x3840/60fps master, mas aumentar resolução não corrige a história.

**Critérios para retomar as 16 cenas:** escultura orgânica do rosto de Polifemo; rig face + braços com contato verificável; cliff rock PBR contínuo (sem esferas/cubos percebidos); plano interno com marinheiros reconhecíveis + saída efetivamente obstruída; plano que estabeleça que gigante é ~3 vezes mais alto que homens; revisar uma sequência completa sem áudio antes de expandir.

**Audio:** Google AI Studio Rasalgethi original de 220,56s, SHA-256 `9be8b79920b318c76f23874d38d12f4f77b46f8a9871833612ac1efa82b5d667`. Os 16 cortes estão organizados por pausa real no arquivo `audio_pause_anchors_v11.json`.

**Bloqueio:** no publishing, no title FINAL, no 4K60-upscale substitute; do not recycle the geometry or sell this as completed cinema quality.
