# API oficial da Meta: @temumaexplicacao

Conta: `@temumaexplicacao`, tipo Criador. App ID informado:
`1132499782513526`.

## Situação atual: token expirado

A integração já comprovou a leitura da conta pela API, mas a credencial atual
expirou. A [verificação mais recente no Actions](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41104067516),
executada em **2026-10-30 às 18:07 UTC** no commit
`d927f00a7afdb2808d152c60a3b6f8e03536a899`, passou nos **30 testes offline** e
falhou na consulta com HTTP `401`, código `190`, **subcódigo `463` (Expired)**.
A etapa identificada foi `discovery_user_token`, na descoberta inicial com o
token de usuário. A conexão não está disponível com essa credencial expirada.

Os metadados atuais informaram 293 caracteres e formato compatível com um
token Facebook, sem aspas ou espaços. O formato não comprova validade;
o subcódigo de expiração
retornado pela Meta determina a ação necessária. É preciso obter um token
novo, estendê-lo para longa duração e substituir o Secret existente antes de
validar novamente. A extensão e a renovação automática ainda não estão
configuradas. Nenhuma publicação foi realizada.

## Comprovação anterior de leitura

A conexão de leitura do executor com **@temumaexplicacao** foi validada pela
API oficial com Facebook Login, versão `v26.0`, antes da expiração. A
[execução 41074008740 no GitHub Actions](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41074008740),
no commit `c13daee69eb789bee22f6f80952df7f14013129c`, terminou com sucesso.
Os logs foram conferidos de forma independente: os **30 testes offline**
passaram e, em **2026-10-30 às 14:42:38 UTC**, o comando `--check` retornou:

```json
{
  "ok": true,
  "mode": "check",
  "login": "facebook",
  "page_id": "1385407341325017",
  "instagram_user_id": "17841433004716815",
  "username": "temumaexplicacao"
}
```

Esse teste fez somente consultas GET. Nenhuma publicação foi realizada;
a publicação ainda não foi testada nem aprovada. Cada publicação exige
aprovação explícita da imagem final, legenda e destino.

A Página **Tem uma Explicação**, disponível em
https://www.facebook.com/61595789771857/, está vinculada à conta profissional
Instagram esperada. O ID da Página retornado pela API é `1385407341325017`;
o identificador da URL pública não deve substituí-lo. A conta Instagram
vinculada tem ID `17841433004716815` e username `temumaexplicacao`.

Durante a configuração do app **Tem uma Explicação**, ID `1132499782513526`,
as consultas de permissões no Graph API Explorer confirmaram as concessões
`instagram_basic`, `instagram_content_publish`, `pages_show_list`,
`pages_read_engagement`, `business_management` e `public_profile` nos tokens
então usados. O recurso **Business Asset User Profile Access** foi adicionado.
O `--check` bem-sucedido no Actions não consulta `me/permissions`: ele validou
a autenticação, a descoberta e a identidade Página-Instagram, sem confirmar
as concessões do token final para publicação nem exercê-las. Nenhuma concessão
de mensagens foi solicitada neste trabalho; o acesso habilitado na Caixa de
Entrada da Página não comprova uma integração com a API de mensagens.

O proprietário substituiu manualmente a credencial no Secret criptografado
`FACEBOOK_USER_ACCESS_TOKEN`, copiando o campo **Token de acesso** completo.
O teste bem-sucedido confirma que a credencial do executor era utilizável
naquele momento. O Secret temporário `INSTAGRAM_SETUP_CHECK` foi removido e
sua ausência foi conferida. Token, App Secret, senha e códigos de autenticação
não foram incluídos no código nem neste documento.

Os erros anteriores HTTP `401` / código `190` foram resolvidos após essa
substituição. O diagnóstico seguro permitiu localizar a falha na credencial
de usuário. A confirmação **Confirm access** do GitHub foi concluída pelo
proprietário no próprio navegador; salvar o perfil de sessão não substituiu
essa confirmação para a automação.

A validade exata não havia sido conferida na configuração inicial; a
verificação das 18:07 UTC confirmou que a credencial já estava expirada. A
opção **Extend Access Token** exigiu nova autenticação na Meta e ainda não
foi concluída. O token expirado não pode ser usado para obter um token de
longa duração: é necessário gerar um token novo primeiro.

A [documentação oficial da Meta](https://developers.facebook.com/documentation/facebook-login/guides/access-tokens/get-long-lived)
informa que um token de usuário de longa duração geralmente vale cerca de
**60 dias**. Esse prazo não é garantia: o token pode ser invalidado antes.
Conferir a data efetiva de expiração no Debugger e acompanhar revogação;
a extensão não configura renovação automática neste projeto.

## Caminho selecionado: Facebook Login

Foi preparado também `scripts/facebook_poster.py`, separado do protótipo
Instagram Login. Ele usa somente `graph.facebook.com`, descobre as Páginas
autorizadas e seleciona a única Página cujo Instagram corresponde ao username
esperado. O token da Página fica somente em memória; não é impresso nem salvo.
O cliente reconfirma o vínculo e a identidade antes de qualquer publicação.

O vínculo Página-Instagram, as concessões do token e a descoberta dos ativos
no Graph API Explorer foram concluídos. O Secret `FACEBOOK_USER_ACCESS_TOKEN`
também está salvo no GitHub Actions. As seguintes Variables estão salvas no
repositório:

| Nome | Valor |
|---|---|
| `INSTAGRAM_API_VERSION` | `v26.0` |
| `INSTAGRAM_USERNAME` | `temumaexplicacao` |
| `FACEBOOK_PAGE_ID` | `1385407341325017` |
| `FACEBOOK_INSTAGRAM_USER_ID` | `17841433004716815` |

Os dois filtros numéricos restringem a seleção aos ativos já confirmados pela
API. O cliente também confere o username esperado antes de prosseguir.

O Secret e as Variables estão cadastrados; a leitura foi comprovada às
14:42 UTC e deixou de funcionar com a expiração detectada às 18:07 UTC.
O workflow **Verificar conexão Instagram via Facebook** está na branch padrão,
é iniciado manualmente e executa os 30 testes offline seguidos da consulta de
identidade. Um resultado `ok: true`, `mode: check` confirma a conexão naquele
momento; não autoriza publicações nem comprova que um envio de mídia terá
sucesso.

### Concluir o token de longa duração

O proprietário precisa concluir a extensão na interface oficial da Meta e
salvar o valor estendido no GitHub, no mesmo navegador próprio:

1. Abrir o [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
   e selecionar **Tem uma Explicação**, App ID `1132499782513526`, versão
   `v26.0`. Gerar um novo token de **usuário Facebook** e confirmar as permissões
   necessárias; o token expirado não serve para a extensão.
2. No painel à direita, localizar **Token de acesso**. Usar o ícone **Copy
   Token** ao lado do campo para copiar o valor completo. O seletor deve
   indicar **Token do usuário**.
3. Abrir o [Access Token Debugger oficial](https://developers.facebook.com/tools/debug/accesstoken/),
   colar o novo token no campo da ferramenta e clicar em **Debug**. Conferir
   o app e o tipo de token exibidos.
4. Clicar em **Extend Access Token** e concluir a autenticação solicitada
   diretamente na Meta. Copiar o **token estendido** retornado pela ferramenta
   e conferir sua data de expiração. Não reutilizar o valor curto original.
5. Abrir a
   [edição do Secret existente no repositório](https://github.com/gabrielslinhares12-sudo/instagram-skills/settings/secrets/actions/FACEBOOK_USER_ACCESS_TOKEN).
   Colar o token estendido completo em `FACEBOOK_USER_ACCESS_TOKEN`, sem
   acrescentar aspas ou o prefixo `Bearer`.
6. Clicar em **Update secret**, concluir **Confirm access** nessa mesma sessão
   e aguardar o retorno à lista de Secrets. Conferir o horário de atualização.
7. Informar ao assistente apenas que o token estendido foi salvo e a data de
   expiração exibida. O assistente executará uma nova verificação somente de
   leitura e conferirá os logs de forma independente. Não enviar token, App
   Secret, código de autenticação ou senha pelo chat.

Depois de uma alteração relevante, executar **Verificar conexão Instagram via
Facebook** e conferir os logs de forma independente, sem publicar. Em caso de
falha, o `--check` informa a etapa e metadados de formato, sem caracteres da
credencial nem mensagens brutas da API. Tokens são opacos: tamanho, prefixo,
aspas e espaços ajudam na investigação, mas não comprovam validade ou tipo.
Se houver uma falha futura de cópia, conferir se foi copiado o campo **Token de
acesso**, em vez dos IDs do aplicativo, Página ou conta Instagram.
Não repetir o cadastro nem criar novos marcadores sem um diagnóstico que
justifique a ação.

Os Secrets de Actions não são transferidos ao ambiente do Codex. Para execução
local, configurar as variáveis no ambiente de lançamento. O comando de teste
faz somente leituras e retorna IDs e username, sem expor credenciais:

```bash
python3 scripts/facebook_poster.py --check
```

Depois de restabelecer a credencial válida, usar o cliente nas skills pelo
ambiente de lançamento, nunca por `.env`:

```bash
export INSTAGRAM_SKILLS_CUSTOM_POSTER='python3 scripts/facebook_poster.py'
```

O exemplo de `publish()` mais abaixo é compatível com esse cliente, sempre
com imagem e legenda aprovadas. O comando publica imediatamente; não o usar
para testar credenciais. O cliente do Facebook também
suporta apenas imagem única, sem agendamento, Reels, carrosséis ou Stories.

## 1. Escolher a autenticação disponível

Abra https://developers.facebook.com/apps/1132499782513526/dashboard/.

Para o Unified login, selecione um portfólio empresarial que você esteja
autorizado a administrar, ou aguarde a Meta permitir a criação do portfólio do
projeto. Depois, confira no painel as etapas e permissões realmente oferecidas
por esse fluxo antes de configurar o conector.

Como alternativa, o painel oferece Facebook Login. Esse caminho exige uma
Página do Facebook vinculada à conta profissional Instagram e acesso legítimo
para administrar essa Página. O vínculo entre perfis na Central de Contas, por
si só, não comprova o vínculo Página-Instagram exigido pela API.

Com a Página vinculada:

1. Abra **Configuração da API com login do Facebook**.
2. Na seção **Gerenciar conteúdo no Instagram**, as permissões principais já
   foram preparadas para testes. A lista exibida inclui
   `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`,
   `business_management` e `pages_show_list`.
3. Complete a autorização pelo Facebook com o usuário que possui o acesso
   necessário à Página e selecione os ativos corretos.
4. Use a API oficial em `graph.facebook.com` para identificar a Página e a conta
   profissional Instagram vinculada, e valide o username antes de publicar.
5. Use o cliente `scripts/facebook_poster.py` para esse fluxo. O token do
   Facebook não deve ser colocado no adaptador Instagram Login existente.

O vínculo da Página, as concessões do token e a descoberta da conta pela API
foram confirmados no Explorer. A conexão de leitura do adaptador foi validada
no Actions às 14:42 UTC; a consulta das 18:07 UTC confirmou a expiração do
token. É necessário substituí-lo e validar novamente antes de usar a
integração. A Meta ainda pode aplicar requisitos a operações futuras.

As seções numeradas 2 a 4 abaixo descrevem apenas o protótipo
Instagram Login. Só devem ser usadas se esse fluxo for confirmado como
disponível e compatível com o app.

O App ID pode ser compartilhado para configurar a integração. Token, App Secret
e códigos de autorização não devem ser publicados no repositório nem no chat.
Para testar a própria conta, o administrador deve possuir a função adequada no
app e acesso aos ativos autorizados. As permissões preparadas no painel ainda
precisam ser concedidas a cada token; os tokens usados anteriormente foram
conferidos em `me/permissions`. Acesso a outras contas pode exigir análise do
app, verificação e permissões adicionais; não é uma exigência universal para
testes dos próprios administradores. Criar o app não publica nada no Instagram.

Referência oficial: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/

Facebook Login: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/

## 2. Guardar as credenciais

No GitHub, abra Settings > Secrets and variables > Actions. Cadastre:

| Tipo | Nome | Conteúdo |
|---|---|---|
| Secret | `INSTAGRAM_ACCESS_TOKEN` | Token do usuário para Instagram Login, compatível com o protótipo |
| Secret | `INSTAGRAM_USER_ID` | ID numérico do usuário Instagram |
| Variable | `INSTAGRAM_API_VERSION` | Versão suportada informada pela Meta |
| Variable | `INSTAGRAM_USERNAME` | `temumaexplicacao` |

O workflow **Verificar conexão Meta** só pode ser iniciado manualmente. Ele
executa testes offline e uma consulta de identidade, sem criar mídia ou publicar.
Selecione a branch que contém esta integração ao executá-lo. O workflow precisa
estar na branch padrão para aparecer normalmente na interface do GitHub.

Os Secrets de Actions não são automaticamente disponibilizados ao ambiente do
Codex. Para executar aqui, configure as mesmas variáveis no ambiente de
execução. O adaptador lê o ambiente de lançamento; não carrega `.env`.

## 3. Verificar sem publicar

Com as quatro variáveis configuradas no ambiente:

```bash
python3 scripts/meta_poster.py --check
```

O resultado precisa informar `ok: true`, `mode: check` e o username esperado.
O token não é exibido. ID ou username divergentes impedem a publicação. Este
teste confirma identidade e acesso básico; a permissão de publicação precisa
ter sido concedida no app e só será exercida quando houver conteúdo aprovado.

## 4. Integrar ao ponto de extensão das skills

Configure o comando no ambiente de lançamento, nunca em um arquivo `.env`:

```bash
export INSTAGRAM_SKILLS_CUSTOM_POSTER='python3 scripts/meta_poster.py'
```

Execute a partir da raiz do projeto ou use o caminho absoluto do script.
Não configure `PUBLORA_API_KEY` e `INSTAGRAM_PLATFORM_ID` juntos: a biblioteca
original dá prioridade a esse backend quando as duas variáveis estão presentes.

Depois de o usuário aprovar a imagem final, a legenda e o destino, a chamada é:

```python
from lib import publish

result = publish(
    "post",
    "Legenda revisada e aprovada.",
    "https://www.instagram.com/temumaexplicacao/",
    media_urls=["https://media.example.com/imagem-aprovada.jpg"],
    approved=True,
)
```

Essa chamada publica imediatamente. Não executá-la para testar credenciais.
O exemplo só deve ser usado depois de substituir a URL por uma imagem real
aprovada. A Meta precisa conseguir baixar a imagem HTTPS sem login, com formato
e dimensões compatíveis com sua API. Links de visualização do Drive não são
URLs diretas de imagem. A conta de Criador não muda essas exigências.

O retorno externo da biblioteca usa `mode: diy`; verifique `returncode` e o JSON
em `stdout` ou `stderr`. Sucesso inclui `media_id` e `creation_id`. Em falha após
uma tentativa de escrita, não repetir automaticamente: consulte o container e
o perfil primeiro. Este adaptador não oferece retomada ou deduplicação de jobs.
Erros não imprimem o token, a URL da mídia nem mensagens brutas da Meta.

## Google Drive

O Drive conectado à conversa serve para organizar roteiros, imagens, vídeos e
relatórios. Essa autorização não é transferida ao código nem ao GitHub Actions.
Uma rotina autônoma que grave no Drive precisará de autorização própria pela
API do Google Drive. O armazenamento não fornece servidor de execução.

Mantenha arquivos de trabalho privados. Se um ativo aprovado precisar de uma
URL pública para a Meta, disponibilize somente esse ativo pelo período
necessário; não torne a pasta inteira pública.

## Limites desta primeira etapa

- Sem OAuth hospedado: a autorização inicial é feita no painel da Meta.
- Sem renovação automática de token: acompanhe validade e revogação no painel.
- Sem publicação agendada: a API não substitui uma fila e um executor.
- Sem upload de arquivos locais, hospedagem de mídia ou sincronização do Drive.
- Sem coleta de métricas, comentários ou mensagens nesta primeira etapa.
- Nenhuma publicação é autorizada apenas por configurar a conexão.

Testes locais, sem credenciais nem rede:

```bash
python3 -m unittest discover -s scripts -p 'test_*poster.py' -v
```
