# Instagram TUE — duas etapas: publicar carrossel e adicionar música depois

**Atualizado em 01/11/2026 — preparado, NÃO ativado para nenhum item da fila.**

## Evidência e limitações

- O Instagram lançou a opção **Substituir áudio** em 21/07/2026 para publicações de foto e carrosséis já publicados, preservando o post e o engajamento. Referências: https://techcrunch.com/2026/07/21/instagram-now-lets-you-swap-out-the-music-in-your-old-posts/ e https://support.unitedmasters.com/hc/en-us/articles/53945937105939-How-to-Change-or-Add-Audio-to-Published-Instagram-Posts
- O suporte da UnitedMasters também descreve adicionar música a uma publicação anterior **sem áudio**, mas a disponibilidade depende da conta, região, catálogo e do aplicativo.
- **Teste real somente leitura de 01/11/2026:** no perfil autenticado @temumaexplicacao, foi aberta a edição do post `DfKcMUQFw0X` no Instagram web. Menu Edit info SEM Adicionar música / Substituir áudio. Evidência: https://agent.tinyfish.ai/runs/71b0a164-00f0-4293-8820-deb04847604c
- Portanto o próximo teste de música precisa ser no **aplicativo oficial Android/iOS**, não no navegador. **Não foi testado nem confirmado áudio no app ou em carrossel real.**

## Fluxo seguro disponível para posts futuros

1. Preparar fotos individuais dentro do número editorialmente necessário, legenda, música exata `music_track` e artista `music_artist`; realizar QC e aprovação do post específico.
2. Só depois de testar a opção no aplicativo do proprietário, marcar no item do `content/schedule.json`:
   - `kind: carousel`
   - `distribution_mode: api_carousel_then_native_music`
   - `owner_authorized_two_step_music: true`
   - `music_track` e `music_artist` com a faixa aprovada
   - `approved: true` e `due_at` futuro, com aprovação editorial real.
3. Na hora: o workflow oficial Meta publica **fotos SEM música**. Se houver `media_id` de sucesso, o ledger grava `awaiting_native_music`, a faixa escolhida e o horário. Não marca `published` (post completo) até que a música seja efetivamente verificada.
4. No Instagram mobile: abrir o carrossel existente → ⋯ → **Editar** → **Adicionar música** ou **Substituir áudio** → selecionar faixa/trecho → salvar.
5. Confirmar que o **mesmo post** mantém seu ID, fotos, legenda e música audível; somente então registrar confirmação editorial separada. Não inventar confirmação a partir do recibo Meta, que só atesta fotos.

**Importante:** `awaiting_native_music` bloqueia republicação pelo scheduler. Uma falha ao adicionar música não pode ser tratada como ausência do post nem receber retry de upload. A confirmação de música ainda é **manual** porque a Graph API não dispõe de edição da trilha nativa.

## Teste sem criar publicação nova

No aplicativo Instagram, abrir a publicação existente do perfil `@temumaexplicacao`, de shortcode **DfKcMUQFw0X** (`https://www.instagram.com/p/DfKcMUQFw0X/`), tocar em ⋯ → **Editar** e verificar se aparece opção para adicionar música. Esta publicação é uma FOTO, não um carrossel: valida a disponibilidade da ferramenta na conta, **não comprova** a experiência em carrossel. Não apagar nem reenviar esse post.

Até validar o recurso no Android/iOS **nenhuma postagem futura será automaticamente convertida** para o modo de duas etapas. A atual fila não foi alterada, não houve publicação ou cobrança no GitHub.
