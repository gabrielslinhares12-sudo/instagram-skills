# Odisseia — novo padrão integral em produção (06/11/2026)

## Fonte e estrutura
- Duração original recuperada: **560,100 s** de narração Rasalgethi em AAC 48 kHz.
- Arquivo original de narração e master de referência existem na Biblioteca do projeto; não renarrar.
- Novo código editável no branch `feat/tue-motion-base`:
  - `motion/src/odysseyTimeline.ts`: **110 atuações distintas**, sem sobreposição ou lacunas entre 0 e 560,1 s.
  - `motion/src/OdysseyFullAnimation.tsx`: atores 2D, cenários, navegação, Cyclops+rocha de entrada, tecelagem de Penélope, mastros e sereias, Cila/Caríbdis, reencontros; cenas independentes por evento.
  - `motion/src/Root.tsx`: composição contínua **OdysseySagaFull** (33.606 frames) e composições dos três episódios.
  - `motion/scripts/mux-odyssey-original-audio.sh`: remonta os arquivos visuais novos sobre a narração AAC original.
- Cortes preservados: E1 0–88,6 s (5.316 frames); E2 88,6–317,4 s (13.728 frames); E3 317,4–560,1 s (14.562 frames).
- Exportação alvo: **2160×3840 e 60 fps**, por Remotion `--scale=2`, sem pagamento de API e sem depender do PC.

## Execuções verificáveis
- QC Polifemo V1 técnico: [run 42277442700](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/42277442700) — concluído com êxito técnico.
- QC Polifemo V2 rocha maior / gigante dentro do quadro: [run 42278410074](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/42278410074) — concluído com êxito técnico.
- Renderização paralela dos três episódios, sem publicação: [run 42278628925](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/42278628925), iniciada; consultar Jobs para estado real.
- **Atenção à versão:** o render de três episódios está fixado no commit `1f62f05fd6d979faa6869cbab398ae5140f6321f`. O branch evoluiu depois, com tecelagem de Penélope, chegada à costa e master integral. As saídas desse render exigem revisão de continuidade e, caso necessário, novo render com o commit mais recente.

## QC editorial obrigatório
1. Avaliar cada corte dos três episódios na tela, não apenas o teste que verifica codec/tamanho/duração.
2. Confirmar o fechamento da porta pelo Polifemo: pedra cobre inteiramente entrada da caverna, mãos e corpo participam fisicamente do movimento; não ocorre teleporte do objeto.
3. Confirmar o jogo de pernas com apoio do pé no chão, sem skate, e interações entre objetos/atores em todos os 110 trechos.
4. Confirmar todos os figurinos, variedade das tomadas e coerência de capítulo com a narração.
5. Remontar o AAC Rasalgethi original e conferir sincronismo das legendas inferiores antes da publicação.
6. Somente após QC editorial completo liberar a publicação do episódio 1 e agendamento do episódio 2.

**Nenhuma etapa deste processo contém publicação ou agendamento no Instagram.**


## Revisão narrativa confirmada por quadros do master (06/11, 20:25 UTC)
- O primeiro storyboard de 110 ações tinha **desalinhamento grave** com a narração original entre 224s e 317s (Calipso, tear de Penélope, Telêmaco e retorno pelos feácios). Não pode ser publicado.
- Foi substituído no branch `feat/tue-motion-base` por **131 ações únicas organizadas em 30 capítulos** nos tempos efetivamente observados no MP4 original, com regressões em `motion/tests/odyssey-timeline.test.ts`.
- O novo corte cria cenas distintas dos cícones, Penélope tecendo e desmanchando o tear, a viagem de Telêmaco, a jangada de Odisseu, os feácios, o barqueiro/o remo em terra firme, o pomar de Laertes e a paz com intervenção de Atena.
- A física do ciclope foi refeita com ambos os braços tentando manter contato com a grande pedra; passou pela compilação e pelo QC 4K60 de curta duração, mas a atuação ainda precisa de revisão visual integral.
- O sistema de 110 cortes ficava escuro ~0,48s entre ações; removido esse escurecimento artificial no código posterior.
- Legendas originais **recuperadas da faixa inferior do próprio master via máscara de luminância**, sem OCR e sem API paga. Teste com áudio original, legenda e 2160×3840/60 FPS validado, salvo também no Drive:
  https://drive.google.com/file/d/1SJEU8YnrYP2XhPs5JMLEI8nDZdXQTZye/view?usp=drivesdk
- Script de montagem reproduzível: `motion/scripts/restore-odyssey-captions.sh`, na branch. Fonte MP4 original fornecida pelo usuário é necessária para mesclar a narração e as legendas; ela **não está no repositório GitHub**.
- [Render de três episódios atualizado V5](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/42288210740), em fila no momento desta anotação. Confirme Jobs e artifacts para seu estado atual.
- Nenhum vídeo desta nova geração foi enviado ao Instagram; publicação depende de inspeção visual/editorial e da remontagem final da voz e legendas originais.
