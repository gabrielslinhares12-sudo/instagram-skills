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

## Rodada adicional — testes de seleção múltipla e Meta (2026-11-01)

### Conexão oficial da Meta (PASSOU; somente leitura)
Execução https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41263684039

- `FACEBOOK_USER_ACCESS_TOKEN`, `FACEBOOK_PAGE_ID` e `FACEBOOK_INSTAGRAM_USER_ID`: presentes como secret/vars; valores nunca impressos.
- `scripts/instagram_preflight.py` retornou `META_PREFLIGHT=passed`, `MISSING_PERMISSIONS=` (nenhuma), identidade e permissões conferidas.
- Nenhum POST de publicação. Este resultado **não implica** que a API suporte música em carrossel: não suporta na documentação conhecida.

### Files / DocumentsUI no Android (8/8 fotos presentes; seleção ainda NÃO APROVADA)

1. https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41263275531: fotos SHA-256 8/8, MediaStore 8/8, picker reconheceu 8 arquivos; tentativa de oito toques **sem confirmação** de seleção. Capturas e logs anexos à execução.
2. https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41263638581: falha transitória no início (`/sdcard/Pictures` não montado). O workflow foi ajustado para aguardar montagem.
3. https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41263804787: Files em visualização **lista**, oito fotos visíveis e indexadas; pressionar longo sobre primeiro arquivo não entrou em modo de seleção. Teste falhou corretamente.
4. https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41264124074: compilado e instalado com sucesso aplicativo Android **original, offline e temporário** (sem rede/Instagram), usando `ACTION_OPEN_DOCUMENT` + `EXTRA_ALLOW_MULTIPLE`. O aplicativo abriu picker e oito arquivos, mas o toque não gerou seleção confirmada; teste falhou.
5. https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41264388301: experimentados toque por coordenadas exatas do nome e da miniatura, em aplicativo chamador real. Não houve `PICKER_RESULT_COUNT=8` nem confirmação de seleção. Teste falhou. Continuar depurando essa interação **antes** de integrar qualquer app real.

### Bloqueios antes de poder publicar COM música

- Nenhum teste conseguiu instalar o app oficial Instagram: Android emulador efêmero precisa autenticar a Google Play Store; nenhuma credencial foi transferida.
- O serviço GitHub Actions fornece VM nova por job. **Não colocar cookies/sessões Google ou Instagram em actions/cache/artifacts**. Documentação de segurança do GitHub desaconselha explicitamente dados sensíveis em cache.
- Um Android persistente e com autenticação legítima, acionado pelo GitHub como orquestrador, é uma opção **não implementada**; infraestrutura externa pode ter custo e exigirá testes de compatibilidade, UI e política da plataforma.
- A API oficial da Meta está autenticada e pode publicar carrosséis **sem música**, mas não resolve o requisito editorial de música nativa.
- O Halloween de oito imagens segue **NÃO PUBLICADO**. Não converter automaticamente em Reel, não enviar sem música quando ela for obrigatória e não marcar como publicado sem permalink real.


## Rodada complementar — diagnóstico real do Android input (2026-11-01)

Workflow: https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41265191917

**Resultado de CI:** `success` significa somente que o roteiro de diagnóstico executou as oito situações sem lançar erro. **NÃO** significa que o seletor ou o Instagram estejam prontos.

Testes isolados por cenário, sempre no aplicativo de diagnóstico `com.temumaexplicacao.pickerprobe`, sem conexão com Instagram:

| Método de entrada | Comando ADB | Resultado de seleção de fotos |
|---|---|---|
| Toque simples no arquivo | `input tap` | Não confirmado |
| Toque do tipo touchscreen | `input touchscreen tap` | Não confirmado |
| Pressão longa na miniatura | `input swipe` | Não confirmado |
| Toque no ícone de prévia | `input tap` | Não confirmado |
| Atalho Ctrl+A | `input keycombination 113 29` | Não confirmado |
| Tab | `input keyevent KEYCODE_TAB` | Não confirmado |
| Shift+Enter | `input keycombination 59 66` | Não confirmado |
| D-pad Enter | `input keyevent KEYCODE_DPAD_CENTER` | Navegou na interface; sem seleção |

Capturas e dumps XML do gerenciador de arquivos disponíveis no artifact `instagram-android-input-diagnostic-41265191917`. XML confirma nós de arquivo com `selected=false`. Os cenários não geraram retorno `PICKER_RESULT_COUNT=8` no aplicativo. As oito artes continuam intactas e reconhecidas no Android. A execução reforça a necessidade de validar automação **dentro do aplicativo Instagram real**, pois o SAF DocumentsUI de diagnóstico não é equivalente ao seletor da galeria do Instagram.

### Decisão operacional
- **Pronto:** Linux cloud do GitHub, Android virtual, MediaStore e transferência íntegra dos oito JPEGs; identidade/permissões Meta em modo leitura.
- **Não pronto:** Instagram oficial instalado no emulador, login seguro persistente, escolha de música nativa, oito fotos selecionadas no aplicativo real e comprovante de publicação.
- **Não iniciar autopublicação com música** até haver teste ponta a ponta com conta correta, escolha de música legítima e permalink. A publicação via Graph API sem música é um fluxo distinto, que requer autorização editorial explícita.
- **Não repetir experimentalmente login com APKs de terceiros nem guardar sessões nos artifacts do GitHub**. Para automação de app nativo sem PC, investigar Android persistente privado, possivelmente contratado, com provisionamento seguro; runners hospedados pelo GitHub são efêmeros.


## Última análise visual de toques no Android e escolha de arquitetura

Run https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41266024332 — executou todos os cenários de toque no centro e borda do bloco de imagem, toque na prévia e pressão longa em celular virtual Android 11. O workflow terminou `success` **apenas como diagnóstico**: nenhum callback `PICKER_RESULT_COUNT` foi recebido pelo app de teste, a seleção múltipla não foi comprovada. O arquivo `instagram-android-input-diagnostic-41266024332` contém capturas e XML antes/depois. Não confundir com publicação do Instagram.

A rota mais promissora para postagem de carrossel **com música** exclusivamente por GitHub é um cliente móvel não oficial (instagrapi). Testado com 9 testes offline e 8 JPGs originais validados: https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41266303138. **Não está autorizado nem autenticado** e portanto permanece desligado. Detalhes e riscos em [Operação carrossel com música na nuvem](OPERACAO-CARROSSEL-COM-MUSICA-NUVEM.md).
