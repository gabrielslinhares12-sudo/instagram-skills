# Capacidade real: adicionar música a carrossel EXISTENTE só pelo GitHub

Data de verificação: 2026-11-02.

## Objetivo

O usuário quer que **somente o GitHub Actions** adicione **Thriller — Michael Jackson** ao carrossel de Halloween **já publicado**, sem PC, sem clicar no Android, sem republicação e sem contratar API paga.

Post existente: https://www.instagram.com/p/DfNVlLDmC8P/
Meta media ID: `18107496023215107`. Imagens: 8. Música aprovada: `content/music-assignments.json`.
Estado do recibo: `awaiting_native_music`. O usuário forneceu evidência visual do botão no app móvel, **não de música já salva**.

## Verificação de capacidades documentadas

- A API oficial Meta Graph: fornece `POST /{ig-user-id}/media`, `POST /{ig-user-id}/media_publish` e capacidade de audio **na criação de Reels** por Instagram Audio API. **Não fornece uma operação documentada para adicionar ou substituir a música nativa de um carrossel de fotos existente**.
- O Instagram Android/iOS possui, desde julho de 2026, a opção de editar/substituir/adicionar áudio ao post, conforme confirmação do usuário e fontes públicas.
- O `instagrapi` não oficial tem métodos documentados `album_upload_with_music` e `photo_upload_with_music` para **novas publicações**, enquanto `media_edit` edita legenda, localização e marcações. **Não há método documentado de música em publicação existente**.
- A sessão web autenticada anteriormente **não é** uma sessão móvel e a função de música **não apareceu no editor Instagram Web** quando inspecionado.
- Um GitHub-hosted runner é uma VM efêmera: **não há Android autenticado disponível** para atuar no app. Não existe sessão móvel que possa ser legalmente inferida de um token Meta Graph ou de cookies web.

Referências:
- https://developers.facebook.com/docs/instagram-platform/content-publishing/audio-api
- https://developers.facebook.com/docs/instagram-platform/content-publishing/
- https://subzeroid.github.io/instagrapi/3.0.21/usage-guide/media/
- https://techcrunch.com/2026/07/21/instagram-now-lets-you-swap-out-the-music-in-your-old-posts/
- https://support.unitedmasters.com/hc/en-us/articles/53945937105939-How-to-Change-or-Add-Audio-to-Published-Instagram-Posts

## Política operacional

1. NÃO marcar `music_status=applied` ou alterar `status=published` enquanto música não tiver sido verificada no mesmo permalink.
2. NÃO apagar, reenviar, converter em Reel nem publicar uma segunda cópia do carrossel Halloween.
3. NÃO ativar `instagrapi` apenas para usar upload de novo carrossel com música; além de não resolver o post atual, requer sessão móvel autenticada e traz riscos à conta.
4. NÃO usar um APK experimental/Android local como se fosse automação 100% GitHub; não atende à exigência do usuário.
5. O workflow `instagram-music-cloud-gate.yml` confirma, em modo **somente leitura**, os IDs, hashes lógicos, música aprovada e os limites atuais. Sucesso do job significa **auditoria executada, não música adicionada**.
6. Só implementar edição remota quando houver endpoint realmente funcional ou uma sessão móvel legítima e infraestrutura Android isolada sob controle do GitHub, ambas testadas e aprovadas. Não improvisar ou solicitar credenciais no chat.

## Resultado atual

**100% GitHub para publicar fotos: funcional. 100% GitHub para adicionar Thriller a esse carrossel sem sessão móvel: bloqueado tecnicamente.** O status permanece `awaiting_native_music`.
