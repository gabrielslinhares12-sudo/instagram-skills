# Testes Android na nuvem — Instagram TUE — 2026-11-01

## Escopo
Dois smoke tests **reais**, executados inteiramente em GitHub-hosted `ubuntu-latest`, sem PC/runner GUTHY, sem envio de posts e sem credenciais de Instagram/Google.

## Teste 1 — Android e imagens (sucesso)
Run: https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41262601439

- Android 11 emulador inicializado com aceleração KVM: **OK**.
- Oito JPGs originais do Halloween baixados do GitHub, SHA-256 conferido com `content/schedule.json`: **8/8 OK**.
- `adb push` para `/sdcard/Pictures/InstagramTUEProbe`: **8 arquivos OK**.
- Intent `android.intent.action.GET_CONTENT` para selecionar imagens: **iniciado**, com screenshot armazenado como artifact. A conclusão da seleção múltipla pelo usuário **não foi testada**.
- `com.instagram.android`: **não instalado**.
- Música, login e publicação: **não testados**.

## Teste 2 — Google Play Store no Android cloud (sucesso do diagnóstico)
Run: https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41262799886

- Android 11 usando target `google_apis_playstore`: **iniciado**.
- `com.android.vending`: **instalado**.
- Intent oficial `market://details?id=com.instagram.android`: enviado.
- Screenshot mostra Play Store na tela inicial pedindo **SIGN IN**, sem sessão autenticada.
- `com.instagram.android`: **não instalado**.
- Login Google, download APK e publicação: **não realizados**.

## Conclusão verificável
A infraestrutura do GitHub para emular Android e carregar 8 fotos é viável. **Ainda NÃO foi demonstrada** publicação de carrossel com música nativa. Para continuar sem PC é necessário acesso legítimo ao app Instagram e uma estratégia segura de autenticação persistente em ambiente cloud. Os runners GitHub hospedados são efêmeros; não armazenar senhas, cookies, sessões ou tokens em logs/artifacts/cache públicos. Não instalar APK de repositórios não oficiais. Verificar regras da plataforma e confiabilidade antes de iniciar produção. O método oficial de publicação Graph API continua incapaz de atribuir música nativa a um carrossel de fotos.

## Segurança editorial
Não publicar o Halloween antigo sem novo preflight de identidade, aprovação e prevenção de duplicações. Não trocar carrossel por Reel, não omitir áudio exigido, não afirmar sucesso sem permalink verificável.
