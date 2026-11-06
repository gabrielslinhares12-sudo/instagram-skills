# Odisseia — retomada e bloqueio editorial (06/11/2026)

## Fonte recuperada
- O filme completo `Odisseia_O_regresso_a_Itaca_4K60.mp4` foi recuperado da biblioteca do projeto nesta revisão.
- Metadados medidos com FFprobe: **560,100 s, 2160 × 3840, 60 FPS, H.264, AAC estéreo 48 kHz, cerca de 2,15 Mbps no arquivo inteiro**.
- O áudio original foi preservado; não há autorização para regravar com outra voz nem substituir por voz sintética aproximada.
- Existe uma divisão técnica em três arquivos MP4 com áudio original: 00:00–01:28,6; 01:28,6–05:17,4; 05:17,4–09:20,1. **É a edição de referência, não a versão reanimada final.**

## Atualização de animação
- Código do personagem Odisseu alterado em `feat/tue-motion-base`: gesto de acariciar Argos, figurino civil sem elmo nem colete de guerra, nova pose de abraço.
- Cenas `OdysseyHomeQC.tsx`: Argos na praia, reconhecimento de Euricleia junto à bacia, reencontro com Penélope próximo ao leito da oliveira; posições dos membros refinadas.
- Render de teste de 12 s em 4K/60 FPS e verificação técnica no [Actions v4](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/42272979765).
- A avaliação editorial visual ainda não aceita os 12 s como acabamento cinematográfico: atuar e interagir de maneira convincente, preservar figurinos/estilo do longo e evitar personagem cortado continuam pendentes.

## Quality gates antes da publicação
| Gate | Estado | Evidência ou pendência |
|---|---|---|
| Filme original e áudio com procedência | PASSOU | Fonte MP4 560,1 s recuperada da Biblioteca |
| Exportação 4K 60 FPS | PASSOU TÉCNICO | FFprobe nas saídas de referência e nos QCs |
| Reconstrução de todos os 560 s em cenas editáveis | BLOQUEADO | Rigs editáveis da trilogia integral não foram localizados; QC isolado não reanima o longa |
| Consistência estética dos 20 capítulos | BLOQUEADO | O longa original e os QCs Remotion não usam ainda o mesmo desenho de elenco e cenários |
| Ações físicas complexas / sem cenas recicladas | BLOQUEADO | Auditar e retomar todos os intervalos de `docs/ODISSEIA-QC-06NOV-REANIMACAO-PARCIAL.md` |
| Sincronia de legendas após substituições | BLOQUEADO | Testes novos têm imagem sem a tipografia do filme; precisam de integração real |
| Três episódios finalizados e inspecionados integralmente | BLOQUEADO | As três divisões existentes são de referência e não a entrega aprovada |
| Publicar/agendar Instagram | NÃO EXECUTAR | Sem render final aprovado não publicar para não expor obra inacabada |

## Sequência de correção
1. Recriar cenas editáveis completas por acontecimento narrado, sem repetir fundos ou figuras e mantendo o design de personagem ao longo do filme.
2. Verificar física de caminhar, abraçar, segurar objetos, remar, mover cão e gestos específicos nas cenas de Polifemo, Éolo, Circe, sereias, Cila/Caríbdis, Argos, Euricleia e Penélope.
3. Renderizar e comparar os 560,1 s, sincronizar com a narração original e legendas sem faixas pretas; conferir todos os cortes.
4. Dividir só após aprovação do filme completo, respeitando frases inteiras e continuar com 2160×3840 60 FPS; **não programar publicação antecipadamente**.

**Status: original recuperado e testes reais de animação 4K60 disponíveis; reanimação integral e publicação ainda não concluídas.**
