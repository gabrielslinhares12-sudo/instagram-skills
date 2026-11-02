# Teste real: editar áudio do carrossel Halloween no Meta Business Suite

Data: 2026-11-02. Escopo: **inspeção de interface; nenhuma alteração salva**.

## Publicação

- Instagram: `@temumaexplicacao`.
- Carrossel existente de oito imagens publicado 01/11/2026.
- Permalink: https://www.instagram.com/p/DfNVlLDmC8P/
- Meta media ID no ledger: `18107496023215107`.
- Música solicitada: **Thriller — Michael Jackson**; a música continua **não confirmada como aplicada**.

## Execução verificada

- Ferramenta: navegador autenticado do Meta Business Suite, com sessão Facebook salva.
- Navegação: https://business.facebook.com/latest/content → Conteúdo → Posts e reels → carrossel de Halloween → menu de três pontos → Gerenciar post → Editar publicação.
- Execução e evidência: https://agent.tinyfish.ai/runs/25ae40d7-c64b-45be-b88e-e9b0ddd69638
- Foi localizado o post alvo e aberto seu editor de publicação existente.
- Opções observadas: **Editar fotos**, **Remover foto**, **Adicionar foto/vídeo**, campo de legenda, hashtags, emoji, sugestões de texto da Meta AI, localização e ações Cancelar/Publicar.
- **Não foram encontrados** controles denominados `Adicionar música`, `Música`, `Adicionar áudio` ou equivalentes no editor do carrossel já publicado.

## Conclusão rigorosa

**No editor exibido nessa conta e nessa publicação, o Meta Business Suite não disponibilizou a adição de música após publicação.** Não extrapolar isso para todas as contas/regiões ou versões futuras sem novo teste. A possibilidade foi confirmada pelo proprietário **no app Instagram para Android**, uma superfície diferente.

Não foi aberta sessão Android, não houve seleção de `Thriller`, nenhuma edição foi salva e **não foi publicada nova cópia do carrossel**. O ledger permanece `awaiting_native_music`. A API Graph já utilizada para publicar o álbum **não disponibiliza endpoint documentado** para adicionar música nativa a um álbum existente.

## Próximos limites

Nenhum gatilho GitHub Actions pode transformar uma opção ausente do Business Suite em API. Para cumprir a condição **somente GitHub, sem PC e sem cliques no celular**, seria necessário um método válido de edição em sessão móvel autenticada sob infraestrutura de nuvem (e não apenas uma API de publicação). Não declarar a automação concluída sem êxito e recibo do áudio no **mesmo permalink**.
