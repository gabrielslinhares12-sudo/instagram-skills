# API oficial da Meta: @temumaexplicacao

Conta: `@temumaexplicacao`, tipo Criador. App ID informado:
`1132499782513526`.

## Situação confirmada no painel da Meta

As capturas do aplicativo mostram dois caminhos: **API setup with Unified
login**, recomendado pela Meta, e **Configuração da API com login do Facebook**,
marcado como legado. Não foi encontrada uma opção separada de Instagram Login.

O Unified login exige selecionar um portfólio empresarial. Na tentativa
anterior, a criação do portfólio foi recusada porque a conta do Facebook era
recente; o aviso orientava tentar novamente em uma hora. O caminho selecionado
é Facebook Login, usando a Página e a conta profissional que o usuário
administra. A autorização e a descoberta dos ativos foram validadas no Graph
API Explorer, usando a versão `v26.0`.

A sessão do Facebook está autenticada no perfil de navegador TinyFish usado
para a configuração. A Página **Tem uma Explicação** está disponível em
https://www.facebook.com/61595789771857/. O painel também informou o
identificador de ativo `1385407341325017`. A consulta `me/accounts` confirmou
esse último valor como ID da Página na API, com o nome **Tem uma Explicação**,
e a conta Instagram vinculada `17841433004716815`, username
`temumaexplicacao`. O identificador presente na URL pública da Página não deve
ser usado como substituto do ID retornado pela API.

O vínculo da Página com **@temumaexplicacao** foi concluído e confirmado por
uma mensagem de sucesso e pelo estado final **Conectado / Habilitado** no
painel. O fluxo de conexão também habilitou o acesso às mensagens pela Caixa
de Entrada da Página. Essa opção da interface não comprova configuração de
permissões, tokens ou webhooks da API de mensagens.

O usuário autorizou o assistente a executar a configuração. No aplicativo Meta
**Tem uma Explicação**, ID `1132499782513526`, as permissões principais de
conteúdo foram confirmadas como prontas para testes no painel. O recurso
**Business Asset User Profile Access** também foi adicionado. Permissões de
mensagens já apareciam na lista do app, mas não foram solicitadas concessões
de mensagens neste trabalho. Um token de usuário Facebook foi gerado e a
consulta `me/permissions` confirmou as concessões `instagram_basic`,
`instagram_content_publish`, `pages_show_list`, `pages_read_engagement`,
`business_management` e `public_profile`. O token foi salvo no Secret
criptografado `FACEBOOK_USER_ACCESS_TOKEN` do repositório, sem ser incluído no
código ou neste documento. A validade do token não foi exibida no Explorer.

O adaptador inicial `scripts/meta_poster.py` foi preparado para Instagram Login
em `graph.instagram.com`. Ainda não foi validado com o fluxo exibido neste app.
Ele não aceita automaticamente tokens do Facebook Login nem do Unified login.
As alterações de configuração são preparadas em uma branch para revisão antes
de integrar a branch padrão. O [PR de configuração #1](https://github.com/gabrielslinhares12-sudo/instagram-skills/pull/1)
permanece em rascunho. Ainda faltam concluir as Variables do GitHub e executar
o teste real do adaptador no Actions; a validação no Explorer não substitui
essa execução.

O protótipo verifica identidade e publica somente uma imagem por vez, após
aprovação explícita. Reels, carrosséis, Stories e agendamento ainda não estão
implementados nele.

## Caminho selecionado: Facebook Login

Foi preparado também `scripts/facebook_poster.py`, separado do protótipo
Instagram Login. Ele usa somente `graph.facebook.com`, descobre as Páginas
autorizadas e seleciona a única Página cujo Instagram corresponde ao username
esperado. O token da Página fica somente em memória; não é impresso nem salvo.
O cliente reconfirma o vínculo e a identidade antes de qualquer publicação.

O vínculo Página-Instagram, as concessões do token e a descoberta dos ativos
no Graph API Explorer foram concluídos. O Secret `FACEBOOK_USER_ACCESS_TOKEN`
também está salvo no GitHub Actions. Para concluir a configuração do executor:

1. Salvar as Variables `INSTAGRAM_API_VERSION=v26.0` e
   `INSTAGRAM_USERNAME=temumaexplicacao` no repositório. Essa etapa ainda está
   pendente de confirmação.
2. Integrar o workflow à branch padrão após concluir as verificações do PR e
   executar **Verificar conexão Instagram via Facebook**. O teste real do
   adaptador ainda está pendente.

`FACEBOOK_PAGE_ID=1385407341325017` e
`FACEBOOK_INSTAGRAM_USER_ID=17841433004716815` são filtros numéricos opcionais
para restringir a seleção aos ativos já confirmados pela API. O cliente também
confere o username esperado antes de prosseguir.

Os Secrets de Actions não são transferidos ao ambiente do Codex. Para execução
local, configurar as variáveis no ambiente de lançamento. O comando de teste
faz somente leituras e retorna IDs e username, sem expor credenciais:

```bash
python3 scripts/facebook_poster.py --check
```

O novo workflow **Verificar conexão Instagram via Facebook** executa testes
offline e essa consulta, sem publicar. Ele precisa ser integrado à branch padrão
para aparecer normalmente na interface de Actions. Um PR de configuração por
si só não ativa publicações nem configura credenciais.

Depois de validar a conexão, selecionar o cliente nas skills pelo ambiente de
lançamento, nunca por `.env`:

```bash
export INSTAGRAM_SKILLS_CUSTOM_POSTER='python3 scripts/facebook_poster.py'
```

O exemplo de `publish()` mais abaixo é compatível com esse cliente após a
validação, sempre com imagem e legenda aprovadas. O comando publica
imediatamente; não o usar para testar credenciais. O cliente do Facebook também
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

A Meta ainda pode exigir outras etapas ou aplicar restrições à conta recente.
O vínculo da Página, as concessões do token e a descoberta da conta pela API
estão confirmados. A execução do adaptador pelo Actions ainda precisa ser
validada.

As seções numeradas 2 a 4 abaixo descrevem apenas o protótipo
Instagram Login. Só devem ser usadas se esse fluxo for confirmado como
disponível e compatível com o app.

O App ID pode ser compartilhado para configurar a integração. Token, App Secret
e códigos de autorização não devem ser publicados no repositório nem no chat.
Para testar a própria conta, o administrador deve possuir a função adequada no
app e acesso aos ativos autorizados. As permissões preparadas no painel ainda
precisam ser concedidas a cada token; as concessões deste token foram
confirmadas em `me/permissions`. Acesso a outras contas pode exigir análise do
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
