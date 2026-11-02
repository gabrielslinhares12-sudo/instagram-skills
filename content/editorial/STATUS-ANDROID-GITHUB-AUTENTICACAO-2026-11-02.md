# Instagram TUE — Android oficial no GitHub (02/11/2026)

## Objetivo
Retomar o emulador Android já existente, sem computador pessoal, publicar ou editar posts somente após validar app Instagram oficial, música nativa e conta correta.

## Avanço efetivamente realizado
- Commit: https://github.com/gabrielslinhares12-sudo/instagram-skills/commit/3df75789eb522cfb4b7d8b9493569f5a935468ba
- Workflow GitHub Actions: https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41388475229
- 5 testes offline passaram; job Android 11 terminou com conclusão técnica `success`.
- Play Store oficial presente e funcional no Android virtual (`play_store_installed=true`).
- Tentativa de abrir a página oficial de `com.instagram.android` detectou `google_sign_in_required`.
- `instagram_before=false`, `instagram_after=false`, `install_clicked=false`.
- `credentials_used=false`, `new_posts=0`, `published_posts_edited=0`, `music_applied=false`.
- Resultado integral salvo como artifact de texto não sensível `instagram-android-official-app-readiness`.

## Limitação operacional e segurança
O Android do GitHub Actions é efêmero. A Google Play solicita autenticação Google para instalar o Instagram oficial; mesmo um login Google/Instagram concedido em um job desaparecerá quando a VM for descartada. Não colocar senhas, cookies, códigos MFA, backups de sessão ou tokens em commits, logs, Issues, caches/artifacts de CI. Não instalar APK de fornecedores não oficiais para evitar a Play Store.

## Intervenção imprescindível para próximo passo
É necessária uma decisão do proprietário sobre **autorizar avaliar um Android em nuvem persistente** (podendo envolver custo e sempre com aprovação antes de cobrança). Nesse ambiente, o proprietário poderá fazer a autenticação Google Play e Instagram pela interface privada e legítima. O GitHub poderá depois disparar uma automação contra esse Android persistente. Nenhuma contratação ou login foi iniciada.

## Preservação
O carrossel Halloween já publicado continua inalterado: https://www.instagram.com/p/DfNVlLDmC8P/. Música Thriller — Michael Jackson continua pendente. Não republicar Halloween, não assumir sucesso pelo CI e não iniciar agendamento de carrosséis com música antes de validar no app oficial.

## Notas
Resultados anteriores: Android e oito fotos válidos em https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41262601439 ; Google Play sem login em https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41262799886. O seletor de oito fotos do aplicativo de teste anterior não comprovou seleção; não equivale ao seletor do Instagram oficial.
