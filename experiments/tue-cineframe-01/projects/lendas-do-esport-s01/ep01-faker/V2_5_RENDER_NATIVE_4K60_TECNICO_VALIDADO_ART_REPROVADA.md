# EP01 FAKER V2.5 — Exportação nativa 4K60 com composição por camadas (08/11/2026)

**STATUS: PASSOU TECNICAMENTE EM 1 SEGUNDO; REPROVADO ARTISTICAMENTE. NÃO É PILOTO OU VÍDEO COMPLETO. NÃO PUBLICAR.**

## Problema resolvido nesta etapa

A versão V2.4.1 renderizava o SVG inteiro em cada quadro e travou no quadro 41/60. A nova versão **separa o cenário nativo 4K em fundo e primeiro plano** (arquitetura/chão e oclusão de mesa), rasterizados apenas uma vez, e rasteriza por quadro o recorte vetorial do ator **em escala de pixel nativo do cenário**, depois faz a composição com FFmpeg. Não se amplia vídeo de baixa resolução para chamar de 4K.

## Teste efetivamente executado no container (CPU)

| Métrica | Medido |
|---|---|
| Resolução do MP4 técnico | 2160 × 3840 |
| FPS verificado por ffprobe | 60/1 |
| Quadros reais lidos | 60 de 60 |
| Duração | 1,000 segundo |
| Codec | H.264 |
| Quadros distintos de ator | 60 |
| Tempo de fundo+primeiro plano | 0,939 s |
| Tempo de render do ator | 10,350 s |
| Codificação/composição | 5,586 s |
| Tempo total aproximado | 17,212 s |
| GPU | Não utilizada |
| QC de arte, corpo e cenário | **REPROVADO/PENDENTE** |
| Narração Rasalgethi | **AUSENTE** |
| Filme completo 105–125 s | **NÃO RENDERIZADO** |

**SHA-256 da amostra MP4 técnica local**, sem upload/entrega: `353fa99d5d0929eadebecf851154748f0bb42107627a1308fb859ea0c15fd2be`. Vídeo foi mantido apenas como validação local, nunca apresentado ao usuário porque sua arte não atinge a ficha original.

## Fonte e relatório arquivados (não é um vídeo)

ZIP de código, assets SVG locais, README, dependências e relatório da execução: https://drive.google.com/file/d/17Sw2fOj6k9ulpxtaOXlq3UH4oXrQf-tM/view

Pasta interna: https://drive.google.com/drive/folders/1ZcO0TNjW8Cf18BKRXHfqY8qJc_6SoAgE

Arquivo verificado por leitura de metadados: **19.168 bytes**; SHA-256 do ZIP local: `3c197ad1cce8102d24e6d526d2409f7199d043b4470e964bd30781d543afb352`. O ZIP contém código fonte do render, gerador de composição da cena SH02, os dois SVG de entrada, dependências e JSON de QC. **Não inclui MP4 de teste**.

## Limites e continuação obrigatória

- Um segundo renderizado em 17,2 s não prova escalabilidade linear a 112 s. A qualidade do desenho do Faker e a cinemática dos movimentos ainda falham; não há nenhuma tomada final aprovada.
- O desenho de Faker na cena SH02 continua distante da folha 2D original; rosto, óculos, franja, pose sentada, dedos e contato com periféricos precisam ser melhorados. A arte de cenário ainda é maquete.
- Vistas perfil e 3/4 precisam ser desenhadas em qualidade final, não deformadas do rosto frontal.
- Narração Rasalgethi original ainda não está disponível; não usar voz substituta, nem API paga.
- Script é somente prova técnica de 1 segundo; não disparar pipeline de publicação.
- Seguir `NO_PREVIEW_UNTIL_QUALITY_PASS`. Somente após desenho e acting aprovados, 14 tomadas, som e QC final é permitido entregar MP4 4K60 verificado pelo Google Drive com link na conversa.

**Decisão editorial:** pipeline técnico validado; entrega bloqueada.
