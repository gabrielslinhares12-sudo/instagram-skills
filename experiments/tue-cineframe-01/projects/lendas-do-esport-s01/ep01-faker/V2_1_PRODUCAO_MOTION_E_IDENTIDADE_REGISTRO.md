# EP01 Faker V2.1 — Controle de movimento e identidade (lote interno, 08/11/2026)

**Status real: PRÉ-PRODUÇÃO / BLOQUEADO PARA EXIBIÇÃO. Não existe vídeo V2.1 aprovado.**

## Novos ativos produzidos

- 14 tomadas planejadas × 480 amostras por tomada = **6.720 amostras de articulação**, em **60 quadros por segundo** (112 segundos de *dados de movimento*, não 112 segundos de vídeo renderizado).
- Controlador `rig_motion_director.py` em Python/NumPy com IK de 2 segmentos para braços e pernas, plantio de pés durante a fase de apoio e mão vinculada aos objetos.
- Continuidade de ação: treino com teclado/mouse, inclinação de cabeça na derrota, sentar/levantar, caminhada, gestos com colegas, objetos em cena, troféu com pega dupla e transição do placar T1–KT de 1–2 para 2–2 e 3–2.
- **Revisão técnica interna:** 14/14 tomadas com trajetória calculada sem erro dos verificadores; nenhum braço fora de alcance após ajuste; nenhuma deriva de pés durante fase de plantio; marcador estratégico preso à mão nas poses de deslocamento.
- Arquivos `.npz` + código + relatório de QA reunidos em um ZIP de produção.
- 16 referências originais da ficha ilustrada convertidas em guias de máscara com coordenadas de articulação, **sem ampliação artificial**.
- Três estados adicionais editáveis da arena 2025, placar físico original em SVG (1–2, 2–2, 3–2), ainda apenas estudos de cena.
- Teste de vetorização automática da cabeça foi **reprovado**: contornos essenciais de óculos/cabelo/olhos perdidos; SSIM indicativa ~0,609 em recorte de referência. Não usar os arquivos rejeitados como personagem final.

## Onde está o pacote de produção

**Drive (somente material técnico, NÃO vídeo):**
https://drive.google.com/file/d/1rixuNGgDLFSVGNLkV7HkVsF-t-QIj7U6/view

Pasta interna exclusiva V2:
https://drive.google.com/drive/folders/1ZcO0TNjW8Cf18BKRXHfqY8qJc_6SoAgE

- Nome armazenado: `EP01_FAKER_V2_1_MOTION_CONTROLS_REFS_INTERNAL_QC_NOT_APPROVED.zip`
- Tamanho validado por leitura de metadados do Drive: **1.812.684 bytes**.
- SHA-256 local do ZIP: `d2fce067cba5063c1552a38d49604c611ddaebe6a3394bf887783b0ab4af5424`
- Teste de integridade ZIP local: nenhum membro corrompido.
- Ficha visual original LOCK: https://drive.google.com/file/d/163C38f5RBR1mtf7r8z9FBYuQfrJubQnF/view

## O que isso **NÃO** significa

- As 6.720 amostras representam posições calculadas de corpo/objetos. **Não são 6.720 fotogramas animados do Faker**.
- Os recortes da ficha não são o redesenho em tamanho 4K necessário para planos próximos; textura de 150–220px continua insuficiente.
- O cenário da arena ainda é um estudo SVG de perspectiva/placar, não a arte 2D premium aprovada.
- Não existe narração Rasalgethi gerada, nem montagem completa, nem aprovação de arte final.
- Não foi gasto crédito pago ou publicada qualquer postagem.

## Bloqueios inalterados

1. Desenhar personagem em camadas a partir da ficha original **com fidelidade de rosto, cabelo, óculos, roupa e proporções**, em qualidade nativa suficiente para render 2160×3840.
2. Produzir cenários de qualidade cinematográfica com profundidade coerente, personagens secundários e organização espacial; rejeitar simplificações.
3. Conectar curvas de motion a camadas reais e renderizar as 14 tomadas; revisar **a animação visível**, não só os dados de curva.
4. Obter áudio original Rasalgethi de Google AI Studio, sincronizar cenas e legendas. **Não substituir voz nem usar API paga.**
5. Montar filme completo, validar MP4 2160×3840/60 FPS e todos os critérios do release gate, com QC humano.
6. Somente então enviar MP4 aprovado ao Drive, confirmar metadados e enviar link aqui. Nenhuma publicação automática.

**Decisão:** `release_policy = NO_PREVIEW_UNTIL_QUALITY_PASS` permanece ativa. O usuário não recebe um vídeo fraco por causa de progresso de rig.
