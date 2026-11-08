# ODISSÉIA V35F — Relatório editorial objetivo e não-aprovação

**Data de medição:** 08/11/2026. **Estado final desta execução: vídeo técnico completo, revisão artística pendente, NÃO PUBLICAR.**

A referência única é o desenho original de 60s "Odisseu e o Cavalo de Troia", e não as versões reprovadas V19–V34. O PNG canônico de Odisseu foi usado também nos planos de disfarce. Os cenários continuam autorais em 2D, porém ainda ilustrados em linguagem de rig simplificado; NÃO declarar que seu nível de detalhe iguala o filme original.

## Entrega técnica verificada
- MP4 privado: `tem-uma-explicacao/private_media/odisseia_v35f/qc/ODISSEIA_V35F_16_CENAS_68_TOMADAS_RASALGETHI_QC.mp4`.
- 16 cenas, 68 beats narrativos, 220,567 segundos, 720×1280, 30 FPS H.264, AAC.
- WAV Rasalgethi SHA256 confirmado: `9be8b79920b318c76f23874d38d12f4f77b46f8a9871833612ac1efa82b5d667`.
- Arte nativa rasterizada a 540×960; NÃO apresentar como 4K/60 nativo.
- Legendas por cláusula (marcação editorial), NÃO alinhamento preciso palavra a palavra.
- MP4 exclusivamente em GitHub privado para QC. Sem Instagram/YouTube.
- Render run: `42489621487`, success. Motion QA run: `42489940097`, success.

## Métrica comparativa de movimento (somente técnica)
Amostra: 3 FPS de 220.56 s, 662 quadros; delta médio RGB entre quadros consecutivos de cada beat, threshold de quase-estático abaixo de 1,7. Comparação com tomadas não adjacentes com média RGB menor que 3,5. Esse limiar é uma **heurística**, NÃO avalia a qualidade narrativa nem a originalidade estética.

| Versão | Tomadas quase estáticas | Imagens não adjacentes quase idênticas |
| --- | ---: | ---: |
| V34 (reprovada anteriormente) | 24/68 | não certificado no mesmo processamento |
| V35D | 15/68 | 0 |
| V35E | 4/68 | 0 |
| **V35F** | **0/68** | **0** |

Arquivo original do QA: `tem-uma-explicacao/private_media/odisseia_v35f/qc/motion/MOVEMENT_QC_V35F.json`.
Pranchas: `CONTACT_V35F_1.jpg`, `CONTACT_V35F_2.jpg` no mesmo diretório.

## Pendências que um teste de movimento NÃO resolve
1. **Fidelidade estética:** fontes de figurantes, monstros, Penélope, Circe, Calipso, Telêmaco e cenários ainda simplificados quando comparados ao filme de 60 s aprovado. A V35F não atende plenamente ao pedido de cenários complexos cinematográficos sem parecer elementos vetoriais repetidos.
2. **Bloqueio cênico e escala realista:** partes da luta e dos objetos (Polifemo/pedra, Cila/navio, arco/corpos) merecem revisão artística em vídeo contínuo; a área colorida se movimentar não prova o gesto narrado correto.
3. **Sincronia com áudio:** divisão temporal em clauses e pausas aproximadas, não revisão fonema ou palavra por palavra. A presença de legendas fiéis ao roteiro não comprova alinhamento do momento exato do evento.
4. **Personagens:** o Odisseu exato foi recuperado, mas o traje de mendigo ainda usa o modelo militar original quando aparece em cena. É preciso modelar uma variante por componentes que preserve rosto/silhueta, mas represente de fato o disfarce.
5. **Qualidade de saída:** 540×960 de pintura nativa e 30 FPS de saída, abaixo do alvo 2160×3840/60 FPS nativo.

**Status editorial:** `VISUAL_REVIEW_REQUIRED` / `OWNER_NOT_APPROVED` / `NO_SOCIAL_PUBLISH`. O pipeline deve manter essa trava até correções substanciais, não apenas elevar a taxa de quadros ou resolução.
