# Faker EP01 — V2.6 | Referências originais, atuação da cena de treino e QC bloqueante

**Data:** 08/11/2026. **Padrão:** TUE-CINEFRAME-01. **Estado:** V2.6 em pré-produção, **NÃO APROVADA PARA VÍDEO**. A versão V1 continua reprovada.

## O que foi efetivamente criado

### 1. Referência do rosto **extraída diretamente da ficha original**, sem reinventar a identidade

- SHA-256 da ficha canônica original: `8b0e7d1b4ae5bfb431ef98fad9c5b7a3105fee37345e36ea4727d2b7f269c4dc`
- 7 arquivos PNG RGBA de **referência de identidade**: frente, 3/4, perfil, concentração, calma, determinação e leve sorriso. A máscara de cada recorte preserva os olhos, a armação dos óculos, o nariz, o cabelo e a silhueta; há manifesto de coordenadas e âncoras para revisão.
- **Dimensões nativas dos recortes são pequenas**, de aproximadamente 113–165 px de largura e 153–239 px de altura. NÃO constituem arte nova 4K, mesmo que alguém amplie esses PNGs.
- Código-fonte reproduzível: `build_reference_turnaround.py` e `validate_reference_usage.py` (disponíveis no ZIP do Drive). A primeira rodada detectou referências de posição fora da máscara; as âncoras foram ajustadas para os pixels efetivamente presentes, registrando deslocamentos. Resultado da verificação de recortes: **PASSOU**, zero referências obrigatórias cortadas.
- O verificador de arte final **deve reprovar**: cinco desenhos nativos obrigatórios (frente, três-quartos, perfil, jogando e comemorando) ainda estão ausentes, além do QC de mãos e de identidade. O teste do gate retornou exit code **1 por reprovação, como esperado**.
- Drive, referência de identidade (arquivo confirmado, 360.293 bytes): https://drive.google.com/file/d/1pAc9QHvef65LWMrvV6vfLveGa925ZZfV/view
- SHA-256 local do ZIP: `d3c8ba2b2e2b4650a468c4f1e9e7b89f3361d08aa325fccbdf74e616127f4570`

### 2. Nova composição interna da cena S02 — treino de 2013

- O cenário original e o boneco candidato foram integrados por camadas e coordenadas, sem fotografias ampliadas fingindo movimento.
- **Correção geométrica:** o assento da cadeira foi elevado para a região do quadril e um monitor auxiliar foi posicionado à direita/frente do atleta; a antiga cadeira tinha o apoio cerca de 140 unidades do palco abaixo da altura do quadril, dando aparência de personagem em pé.
- A cabeça genérica foi temporariamente substituída, **apenas no teste interno**, pela referência 3/4 original aprovada. Isso preserva melhor os traços, mas **a imagem-fonte mede só 125×164 px e não serve como arte final 4K**.
- A cena tem movimentos independentes de cabeça, braços, tronco e mãos (ainda com anatomia insuficiente). O teste interno de 3 segundos gerou 90 quadros diferentes a 540×960, 30 FPS, com ffprobe conferindo duração, resolução e contagem. O arquivo 4K desta rodada é **somente SVG/fotograma estático técnico**.
- O pacote contém **código-fonte, SVGs da sala e do ator, referência 3/4 na resolução original e relatório QC**, sem enviar o MP4 interno; assim ninguém recebe uma prévia que foi reprovada.
- Drive, integração da cena (arquivo confirmado, 52.662 bytes): https://drive.google.com/file/d/1CgKI_xA7m8anrgEh4LXj14uYxuC2z6bG/view
- SHA-256 local do ZIP: `f05802e898c4067d36849c945686ebb36858af59e6cf09f094a596eb61ec358c`

## Resultado editorial desta versão

| Gate | Resultado |
|---|---|
| Preservar fonte aprovada e identificar 7 expressões/vistas | PASSOU |
| Máscaras de referência sem landmarks cortados | PASSOU |
| Documentar arte insuficiente e bloquear 4K de origem falso | PASSOU |
| Separação cenário / corpo / objetos | TÉCNICO, não arte aprovada |
| Corrigir cadeira e posição do monitor | ESTUDO de blocking; QC visual ainda reprovado |
| 90 frames de movimento distintos | PASSOU apenas como QC de microatuação |
| Rosto 2D definitivo de alta resolução nas três vistas | **NÃO EXISTE** |
| Corpo com anatomia convincente, mão sobre teclado/mouse | **REPROVADO** |
| Cenários cinematográficos finais (todas as 14 tomadas) | **PENDENTE** |
| Rasalgethi original e legendas no tempo certo | **PENDENTE** |
| MP4 completo com ação real, 2160×3840, 60 FPS | **NÃO EXISTE** |
| Aprovação editorial e link de MP4 final no Drive | **BLOQUEADO** |

## Próximo trabalho necessário, sem autoaprovação

**A evolução deve ser artística, não mais truques de exportação:** um ilustrador/gerador de arte devidamente autorizado precisa redesenhar o Faker com o traço e as proporções do concept original em camadas reais de resolução nativa; montar as vistas frontal, 3/4 e perfil; desenhar mãos interagindo com mesa e troféu; concluir cenografia e atuar o corpo inteiro. Só depois aplicar as trajetórias V2.1, gravar Rasalgethi e montar as 14 tomadas.

Não basta alterar o status do JSON para aprovado. O gate de aprovação final exige QA visual efetivo e evidência das fontes. Arquivos inferiores permanecem em laboratório e **nunca serão enviados como vídeo de teste ao usuário**.

**Fonte-mestra que não foi alterada:** https://drive.google.com/file/d/163C38f5RBR1mtf7r8z9FBYuQfrJubQnF/view

**Drive do laboratório:** https://drive.google.com/drive/folders/1ZcO0TNjW8Cf18BKRXHfqY8qJc_6SoAgE

**Sem serviços pagos, sem nova voz, sem publicação nem agendamento.**
