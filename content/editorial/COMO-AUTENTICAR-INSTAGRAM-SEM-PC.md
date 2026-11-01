# Autenticação única do Instagram TUE no GitHub Actions — sem PC

## Antes de começar

Esta instrução configura a sessão para **instagrapi** (API móvel **não oficial**, com risco de desafios, bloqueios ou restrições da conta). Não equivale à autenticação da API oficial da Meta e **não** publica conteúdo. Use apenas se entender e aceitar esse risco.

**Nunca** envie a senha, código 2FA, cookies, JSON de sessão ou valor Base64 por chat, e-mail, Issues, Pull Requests, arquivos do repositório ou logs do GitHub.

### Pelo celular, com GitHub Codespaces

1. Faça login no GitHub pelo navegador do celular, na conta administradora do repositório.
2. Abra https://github.com/gabrielslinhares12-sudo/instagram-skills e acesse **Code > Codespaces > Create codespace on main**. Se necessário, use a versão para computador no navegador. A disponibilidade de Codespaces e seus limites depende da conta.
3. No terminal integrado, rode **uma única linha**:

   ```bash
   bash scripts/configurar_sessao_instagram.sh
   ```

4. O procedimento instala `instagrapi==3.2.2` num ambiente Python temporário (fora da pasta versionada), verifica que o GitHub CLI tem permissão para configurar secrets, pede consentimento **ACEITO** e solicita a senha e, se aplicável, o código 2FA no terminal com **entrada oculta**. O script confirma que a conta autenticada é exatamente `@temumaexplicacao`.
5. Se a conta passar na validação, o script codifica as configurações da sessão em Base64 e envia o valor **diretamente ao Actions Secret `INSTAGRAM_PRIVATE_SESSION_B64`** usando `gh secret set` com entrada padrão. Nenhuma senha ou sessão deve ser escrita no repositório ou exibida na tela. O GitHub CLI criptografa localmente o valor antes de enviar. **Base64 por si só não é criptografia.**
6. O terminal deve exibir **SUCESSO: sessão armazenada no GitHub Actions Secret**. Se mostrar falha de autenticação do GitHub CLI, faça `gh auth status`, autentique o GitHub CLI como proprietário do repositório pelo fluxo oficial `gh auth login` e repita o comando. Se o Instagram solicitar desafio, confirme o login no aplicativo oficial; não repita tentativas de senha rapidamente.
7. Confira em https://github.com/gabrielslinhares12-sudo/instagram-skills/settings/secrets/actions que o nome `INSTAGRAM_PRIVATE_SESSION_B64` existe como **Repository secret**, sem precisar abrir o valor (o GitHub não o revela após salvar).
8. Faça um teste sem publicar pela aba Actions: workflow **Instagram TUE - validar biblioteca de carrossel com musica na nuvem**, **Run workflow**. Ele verifica apenas que o Secret existe e se o código tem dependências e arquivos válidos. **Não** efetua login, pesquisa de música ou publicação.

### Cuidados

- Se Codespaces solicitar custos ou não estiver disponível, interrompa e escolha outro ambiente privado; não pague sem avaliar.
- Este secret concede uma sessão com acesso à sua conta. Se houver suspeita de exposição, revogue a sessão pelo Instagram e remova/substitua o secret no GitHub.
- Depois da sessão, **a publicação continua desativada** por segurança. Habilitação e aceite dos riscos da API não oficial são passos separados.
- A sessão pode ser rejeitada por diferenças de IP/dispositivo da nuvem; não existe garantia de funcionamento. Caso isso ocorra, não faça tentativas ilimitadas.
- O post Halloween de 31/10 perdeu sua janela editorial; não mude o agendamento nem o formato automaticamente.
- O fluxo **oficial** para carrossel sem música já é independente, usa o Graph API e não depende deste secret.
