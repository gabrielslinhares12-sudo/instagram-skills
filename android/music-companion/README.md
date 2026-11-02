# TUE Música — protótipo Android sem PC

Este aplicativo auxiliar **não é o Instagram**. Foi criado para um teste controlado, iniciado por toque do proprietário no próprio Android, com a única finalidade de editar a música de **um carrossel existente**:
- @temumaexplicacao
- https://www.instagram.com/p/DfNVlLDmC8P/
- Thriller — Michael Jackson

## Restrições de segurança

- Não possui permissão INTERNET, armazenamento, câmera, microfone ou contatos.
- Não pede senha do Instagram nem lê ou transmite cookies.
- Serviço de acessibilidade limitado a eventos de `com.instagram.android` e com finalidades explicitamente declaradas.
- Nenhum post é criado, excluído ou reenviado.
- Só inicia uma edição após o usuário tocar **Iniciar edição de música**.
- Confere conta e tema antes de abrir o editor. A seleção da música exige o par exato de título e artista; falhas ou ambiguidades interrompem a execução.
- O Android pode exigir que o proprietário **habilite o serviço de acessibilidade** nas Configurações. Essa autorização é ampla no sistema operacional; pode ser revogada a qualquer momento.
- O protótipo é **experimental**: não foi testado no editor do Instagram real. Uma execução GitHub Actions bem-sucedida confirma apenas compilação APK, não sucesso na interface.
- Esta versão apenas exibe o resultado local no Android. O ledger GitHub segue `awaiting_native_music` até confirmação verificada, e a música não deve ser declarada salva sem teste.
- O aparelho precisa ficar desbloqueado para a interação. A disponibilidade de Thriller na biblioteca depende da licença e tipo de conta.

## Compilação na nuvem, sem computador pessoal

O workflow `.github/workflows/instagram-android-music-apk.yml` compila um APK de teste diretamente no GitHub Actions. O resultado é disponibilizado na execução sob **Artifacts → tue-music-companion-debug-apk**. Não instale arquivos de fontes não verificadas e confira o proprietário do repositório.

No Android, para testes:
1. Faça o download do artifact do workflow do seu próprio repositório e extraia o APK ZIP.
2. Confirme a instalação e revise o aviso de segurança do Android.
3. Abra **TUE Música → Autorizar acessibilidade (uma vez)** e habilite voluntariamente o serviço.
4. Use **Iniciar edição de música** para um teste controlado. Ele tentará localizar os botões do Instagram automaticamente, sem repostar.

A instalação de APKs fora da Play Store pode ser limitada por recursos de segurança do Android; não contorne controles de segurança sem compreender as permissões solicitadas. Para produção, são necessários testes de compatibilidade, assinatura persistente e uma estratégia de inicialização sob as limitações do Android; **isso não é uma automação 24/7 pronta**.
