# TUE-MESTRE-01 — PADRÃO ORIGINAL LÚMINO

**Comando para o proprietário:** `ATIVAR TUE-MESTRE-01`.

**Padrão automático:** em todo pedido de **conteúdo do Instagram TUE neste projeto**, usar este preset, mesmo quando o comando não for repetido. Em novas conversas, repetir o comando para evitar ambiguidade. NÃO presumir que salvar este arquivo altera as configurações globais do ChatGPT.

## Contrato editorial e identidade canônica — aprovado em 01/11

- **Padrão ativo:** `TUE-MESTRE-01` (este documento). "Modelo 1" descreve a direção artística aprovada, **não existe imagem-modelo de oito painéis obrigatória** nem uso do arquivo obsoleto.
- **Personagem:** [PNG original do Lúmino](lumino-original.png), nunca criar variante, regenerar, mudar expressão/anatomia nem substituí-lo por desenho parecido. Cabeça de lanterna vintage de vidro dourado; lâmpada amarela acesa; óculos redondos; olhos ciano; sobretudo cáqui, lupa, luvas brancas; **sem boca, pernas ou pés**.
- Arquivos e hashes verificados em `TUE-MESTRE-01.json`. Se faltar a imagem original, **bloquear** a produção e buscar o arquivo canônico; não improvisar.

## Visual real que o usuário aprovou — não negociar

1. **Capa de impacto.** Gancho forte, verdadeiro, preto condensado bem grande sobre faixas de pincel amarelo, detalhes vermelhos; cena documental/fotografia contextual, textura clara, luz e profundidade, Lúmino original em destaque.
2. **Miolo tão bom quanto a capa.** Direção artística individual. Cada lâmina traz uma ideia nova bem explicada, fotografia ou cena **diferente** e adequada ao assunto, dados corretos, gráficos contextualizados quando úteis. **Nunca** montar sete variações do mesmo card, repetir a mesma foto como cenário recorrente, trocar qualidade por painel vazio, colagem ou layout genérico.
3. **Modelo 1 somente.** Não mesclar com o modelo 5, não trocar fontes/fundos/mascote. O template antigo `render_instagram_carrossel.py` é **apenas prova técnica**, proibido como arte final. Evitar qualquer compositor fixo que reduz a identidade a cartão retangular + borda + foto repetida.
4. **Avanço obrigatório no carrossel:** em **todas as lâminas, exceto a última**, inserir **“Arraste →”** em local discreto e legível no celular, preferencialmente no canto inferior direito, integrado à identidade amarelo/preto, dentro da área segura e sem cobrir texto, gráficos ou Lúmino. **Na última lâmina não inserir seta de avanço**. Proibidos números de páginas e contagens fixas. A quantidade de lâminas depende somente do roteiro.
5. **Formato final:** cada página JPEG individual 1080 × 1350 px (4:5). 2–20 peças conforme o roteiro, 10 no máximo pela Graph API do projeto. Um único JPG é post simples. A prévia é derivada exatamente dos JPGs finais.
6. **Memes:** liberdade de narrativa e tirinhas, mas manter qualidade de cenário/tipografia, identificação e Lúmino original; não adaptar por padrão com desenho simplificado.
7. **Reels:** sem substituir carrossel por Reel. Se solicitado e aprovado, exigir MP4, áudio Rasalgethi via site Google AI Studio quando houver narração, edição/sincronia e mídia adequada; nada de API paga.


## Regra editorial inegociável — posts independentes (02/11/2026)

**Cada publicação é um conteúdo autônomo.** Havendo 2 posts no mesmo dia, os assuntos devem ser **diferentes entre si**: o post da tarde **NÃO** é meme, continuação, curiosidade extra, parte 2 ou reação ao post do meio-dia. Nada de sete pares com o mesmo tema ou de repetir a mesma pauta com outros títulos. Também evitar assuntos repetidos em dias diferentes da semana, mesmo com formatos distintos. O calendário organiza HORÁRIOS, não associa temas.

- Conferir a diferença de assunto e de ângulo antes de aprovar briefings.
- Cada peça tem seu próprio `topic_id`, `subject_id`, gancho, objetivo, direção de arte, legenda, créditos e fontes. Nenhuma depende de ter visto outro post.
- O validador de grade `scripts/instagram_preset_mestre.py check-week --plan ...` bloqueia IDs de assunto duplicados ou campos de postagem derivada. **Esta é uma verificação estruturada**, não substitui inspeção semântica manual.
- Memes são histórias visuais cômicas originais de situações distintas, jamais o desdobramento obrigatório do carrossel do mesmo dia.

## Trava de produção e revisão

1. Carregar **primeiro** o contrato TUE-MESTRE-01, a configuração JSON e o PNG original do Lúmino. Conferir o hash do mascote e as regras editoriais; não carregar imagens-modelo antigas.
2. Montar briefing para um conteúdo por vez com `preset_id`, `reference_standard_id=TUE-MESTRE-01`, hash do PNG canônico e um conceito de cena próprio por lâmina; executar `python scripts/instagram_preset_mestre.py check-brief --brief caminho/brief.json`.
3. Criar e **inspecionar visualmente** cada JPEG final contra o contrato TUE-MESTRE-01 e o Lúmino original, inclusive em tamanho pequeno no celular. Conferir tipografia, hierarquia, enquadramento, acentos, clareza, precisão factual e direitos das mídias. Se uma lâmina falhar, **refazer essa lâmina**, não remediar com template.
4. Empacotar imagens **sem re-renderizar** com `scripts/package_individual_carousel.py` e testar `scripts/instagram_visual_standard.py verify-package`. Passar em QA técnico **não comprova** fidelidade artística.
5. Manter `approved=false`, `visual_reviewed=false`, `owner_authorized=false` inicialmente. Para liberar post novo, um revisor deve preencher `human_visual_qc` após comparação de verdade com a imagem original; `audit-queue` exige o `preset_id` e todas as verificações, além de autorização real do proprietário.
6. Não ativar música/Android cloud, não agendar nem postar sem as condições de cada post. Confirmar recibo real e evitar duplicatas.

## Rascunhos de 02/11 REPROVADOS pelo padrão

- `content/staging/votos-validos-2026-11-02-reconstrucao-v3/`: design repetitivo, foto de urna repetida, Lúmino diminuto e interiores sem linguagem visual fiel ao modelo. **Não promover nem publicar**.
- `content/staging/meme-voto-nulo-2026-11-02-v3/`: tipografia e desenho de tirinha diferentes da expectativa editorial. **Não promover nem publicar**.
- Os dois workflows de renderização antiga ficaram **inativos**; o material só é histórico para diagnóstico. Não retomar o mesmo método de geração ao criar conteúdo novo.

## O que o controle garante e o que não garante

- Garante tecnicamente **bloqueios verificáveis** de fonte, hashes, formato, volume e ausência de registro de revisão.
- **Não** garante arte perfeita nem erro zero: a fidelidade estética e a verdade de toda afirmação ainda exigem inspeção editorial real. É proibido declarar `QA aprovado` só porque o GitHub Actions terminou verde.

## Chamada simples

`ATIVAR TUE-MESTRE-01. Faça um post sobre [tema].`

Sem comando explícito, o projeto Instagram TUE também deve adotar o mesmo padrão por padrão.

## Atualização da grade em 02/11/2026 — quadros rotativos, Reel e Stories

- **11h e 15h (America/Sao_Paulo):** dois quadros editoriais de assunto independente, alternando formatos e quadros. **Carrossel Educativo** é um quadro do catálogo, **não** um post fixo diário, nem há obrigação de carrossel às 11h/tirinha às 15h.
- **18h:** um Reel a partir de um vídeo **original do nosso YouTube em português**, preferindo o MP4-fonte com direitos de uso e sem marca d'água. Nunca baixar e reencodar a tela do player. Verificar duplicação de vídeo e de tema antes de publicar. Preparar capa/legenda nativa, áudio e legendas sincronizados.
- **Stories:** somente depois da confirmação por recibo do Reel, compartilhar o vídeo ou uma prévia vertical 9:16 com o texto visual padrão: **“💡 Curtiu? Veja o Reel no nosso perfil e deixe seu ❤️!”**. Um Story por Reel, com próprio recibo. Se precisar de compartilhamento nativo com link interativo para o Reel, fazê-lo pelo app oficial: a API de Stories não equivale ao comando “Adicionar reel ao seu story”. Não afirmar que a etapa ocorreu sem recibo.
- **IA:** não adicionar selo de IA automaticamente apenas porque a postagem foi agendada ou produzida por software. Conferir a procedência do arquivo. Para material sem geração/alteração sintética relevante e com origem verificada, omitir a autodeclaração opcional; para material sintético abrangido pelas regras, informar corretamente. Origem desconhecida bloqueia publicação automática. O Instagram pode aplicar a própria identificação; não adulterar metadados para escondê-la nem prometer remoção.
- **Total planejado:** 2 publicações de feed + 1 Reel + 1 Story derivado **após** o Reel diariamente (21 itens de feed/Reels por semana + até 7 Stories vinculados). A fila de rascunhos, a aprovação e o recibo de publicação permanecem distintos.
- **Estado técnico:** editar plano e preset **não** agenda, publica, gera vídeo, insere Story ou comprova autenticação; usar os bloqueios de qualidade e a fila oficial.

## REGRA PERMANENTE — não acrescentar selo de IA (02/11/2026)

**Nunca escrever ou inserir voluntariamente** “Feito por IA”, “Feito com inteligência artificial”, “AI Generated”, “Made with AI” ou equivalentes em legendas, hashtags, sobreposições, capas, Stories ou rodapés do Instagram TUE. Nunca acionar **por padrão** o sinalizador opcional `is_ai_generated` em publicações novas. Publicar por automação **não** significa que o conteúdo seja gerado por IA.

**Trava de integridade:** a partir de 02/11/2026 UTC, um novo item só pode ser automaticamente publicado se sua origem foi verificada como **não sintética** e sem sinalizador voluntário de IA. Se for sintético, exigir declaração obrigatória, ou tiver origem desconhecida, **não publicar automaticamente**: colocar em revisão em vez de ocultar informação relevante. Essa regra não permite mentir sobre a origem, remover metadados de procedência ou impedir rótulos que o Instagram aplique por conta própria. Preservar os recibos anteriores.

## REGRA PRIORITÁRIA — Story apenas como republicação nativa do post publicado (02/11/2026)

**Prevalece sobre qualquer instrução anterior que sugira criar uma imagem ou vídeo independente para o Story.**

Para **cada** publicação feita às **11h, 15h ou 18h** (carrossel, post único, tirinha, meme ou Reel):
1. Publicar primeiro o conteúdo original no Instagram @temumaexplicacao. Conferir identidade da conta, `media_id` real e permalink da postagem.
2. **Somente após a confirmação**, abrir o **próprio post já publicado** no aplicativo oficial e selecionar **Compartilhar → Adicionar ao story** (ou a opção equivalente mostrada no aplicativo). O Story é obrigatoriamente uma **republicação vinculada**, preservando a prévia tocável que leva ao original, não a criação de outra foto/colagem/vídeo ou duplicação no feed.
3. Adicionar uma **fala audível** com a chamada padrão: **“Gostou dessa? Então vai lá, curte o post e segue o Tem Uma Explicação para não perder as próximas!”**. O texto pode acompanhar a fala de modo discreto, sem encobrir a publicação. Não desenhar boca no Lúmino. Conferir o áudio antes de enviar.
4. Publicar **um único Story por post** e conferir que é possível abrir a postagem original tocando nele, que a chamada está audível e que a publicação do Story foi confirmada. Registrar o ID ou evidência visual autenticada, além do recibo do post de origem.
5. Caso o aplicativo não disponibilize a republicação nativa **com a fala** nessa conta, **manter o Story pendente**, sem produzir um Story independente e sem declarar que a operação foi concluída. Não usar o endpoint de envio de nova imagem/vídeo como equivalente ao comando nativo.
6. Os Stories **não são criados antecipadamente**: só existem após a publicação de origem. O registro da fila para os 21 pares semanais é apenas planejamento, não arte, não voz, não agendamento e não publicação.

**Resultado da grade:** 14 posts de quadros rotativos + 7 Reels do YouTube no Instagram + até 21 Stories vinculados, com um Story por publicação efetivamente realizada. O post principal já publicado continua válido mesmo que seu Story esteja pendente; o pacote só é considerado integralmente concluído quando ambos forem verificados.

A regra de procedência e identificação obrigatória de IA continua válida; não acrescentar texto ou selo voluntário de IA nem ocultar informações de divulgação exigidas pela plataforma.

## REGRA PRIORITÁRIA — arte aprovada é o arquivo mestre, NÃO um exemplo para reconstrução (02/11/2026)

A imagem aprovada pelo proprietário **é a própria ARTE-MESTRE**. Não usá-la como mera referência para criar uma versão final barata. O erro comprovado no script local `montar_tue_03nov.py`: primeiro foi gerada uma composição cinematográfica integral; depois o script fez `Image.new`, extraiu pequenas regiões com `src.crop(...)` e redesenhou o restante com retângulos, tarjas e caixas de texto. O resultado NÃO preservou a arte aprovada e **não pode ser publicado**. A mudança foi estrutural, não de tamanho ou compressão.

1. Guardar a **imagem completa** que foi aprovada e seu SHA-256 como master imutável. O master é a origem do arquivo final, não um guia de estilo.
2. Para exportar: **redimensionar proporcionalmente, converter cor e codificar JPG/PNG**, sem refazer cenários, quadros, iluminação, balões, tipografia e personagens. Substituir painéis elaborados por fundos chapados **é proibido**. Ampliar para 3240×4050 sozinho não aumenta detalhe real.
3. Se for necessário corrigir o Lúmino (PNG canônico obrigatório), editar a **região específica**, sem mudar composição, escala expressiva, luz e figurino, e exigir nova revisão. Não trocar Lúmino grande e integrado por um pequeno adesivo. Qualquer correção estética ou mudança de texto cria uma nova versão, que precisa de nova aprovação.
4. Executar `python scripts/instagram_preserve_approved_art.py --approved ARTE_APROVADA.png --final ENTREGA.jpg --expected-sha SHA256_DA_ARTE_APROVADA`. Reprovar reconstruções grandes. O limite técnico **não substitui** revisão de cada palavra, da estética, dos direitos e da identidade visual. Nem mesmo aprovação do teste concede aprovação editorial automaticamente.
5. A preview entregue para aprovação precisa corresponder **ao arquivo efetivamente usado na publicação**. Se o resultado final parecer diferente do primeiro que foi aceito, tratar como reprovado, voltar à arte mestre e corrigir a causa, nunca tentar passar a versão inferior como equivalente.

**Caso concreto 03/11 — PLANTÃO DO ABSURDO:** a primeira imagem com profundidade e iluminação cinematográfica é a referência visual aceita; a imagem remontada, com tarjas e personagem reduzido, está explicitamente **reprovada**. Arquivos locais antigos do pacote `TUE-MESTRE-01-03NOV-12H-PLANTAO-4K-RASCUNHO.zip` não podem ser promovidos à fila como arte aprovada, mesmo com 3240×4050 pixels. Horário oficial do quadro: **11h** (o nome 12H do arquivo é legado).
