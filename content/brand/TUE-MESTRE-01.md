# TUE-MESTRE-01 — PADRÃO ORIGINAL LÚMINO

> **IMAGEM-MESTRE VISUAL CANÔNICA aprovada em 02/11/2026:** [**Imagem oficial aprovada em 02/11/2026**](modelo-oficial-aprovado-2026-11-02.png), SHA-256 `571f7f31012e8265c784c66f68c1f5847906f02a1e533559c2ea5624551833e9`.
>
> Toda arte do Instagram TUE deve seguir essa EXATA referência estética — não confundir com uma imagem-modelo antiga de oito painéis. O tema eleitoral é apenas demonstrativo, não deve ser copiado como pauta.
>
> **Rodapé obrigatório de carrossel (exceto última lâmina):** pontos pequenos de progresso (atual em amarelo, demais cinza), seta fina e texto `ARRASTE PARA O LADO →` pequeno e espaçado, centralizado embaixo, SEM tarja, pincelada, card colorido ou ícone de mão. Número de pontos = total real de lâminas. Na última, sem incentivo falso para avançar.

**Comando para o proprietário:** `ATIVAR TUE-MESTRE-01`.

**Padrão automático:** em todo pedido de **conteúdo do Instagram TUE neste projeto**, usar este preset, mesmo quando o comando não for repetido. Em novas conversas, repetir o comando para evitar ambiguidade. NÃO presumir que salvar este arquivo altera as configurações globais do ChatGPT.

## Contrato editorial e identidade canônica — imagem-mestre atualizada em 02/11

- **Padrão ativo:** `TUE-MESTRE-01` + arquivo visual-mestre de 02/11/2026. Essa única capa é exemplo de direção de arte para **qualquer** tema ou formato; não impõe quantidade de lâminas e revoga todas as outras referências de estilo.
- **Personagem:** [PNG original do Lúmino](lumino-original.png), nunca criar variante, regenerar, mudar expressão/anatomia nem substituí-lo por desenho parecido. Cabeça de lanterna vintage de vidro dourado; lâmpada amarela acesa; óculos redondos; olhos ciano; sobretudo cáqui, lupa, luvas brancas; **sem boca, pernas ou pés**.
- Arquivos e hashes verificados em `TUE-MESTRE-01.json`. Se faltar a imagem original, **bloquear** a produção e buscar o arquivo canônico; não improvisar.

## Visual real que o usuário aprovou — não negociar

1. **Capa de impacto.** Gancho forte, verdadeiro, preto condensado bem grande sobre faixas de pincel amarelo, detalhes vermelhos; cena documental/fotografia contextual, textura clara, luz e profundidade, Lúmino original em destaque.
2. **Miolo tão bom quanto a capa.** Direção artística individual. Cada lâmina traz uma ideia nova bem explicada, fotografia ou cena **diferente** e adequada ao assunto, dados corretos, gráficos contextualizados quando úteis. **Nunca** montar sete variações do mesmo card, repetir a mesma foto como cenário recorrente, trocar qualidade por painel vazio, colagem ou layout genérico.
3. **Modelo visual-mestre de 02/11 somente.** Usar a imagem enviada como referência de proporção, tipografia, luz, Lúmino, efeitos gráficos e rodapé; não misturar com modelos rejeitados. O template antigo `render_instagram_carrossel.py` é **apenas prova técnica**, proibido como arte final. Evitar qualquer compositor fixo que reduz a identidade a cartão retangular + borda + foto repetida.
4. **Avanço obrigatório no carrossel:** reproduzir o **rodapé da imagem-mestre**: pequenas bolinhas de progresso (página atual amarela, outras cinza), seta fina para direita e, abaixo, texto `ARRASTE PARA O LADO →` bem pequeno e espaçado, **CENTRALIZADO**, sem botão, etiqueta, tarja/pincelada ou mãos. Presente em todas as lâminas com continuação; última sem seta para avançar. Não há números visíveis nem quantidade fixa de páginas.
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

1. Carregar **primeiro** a imagem visual-mestre de 02/11, este contrato, o JSON e o PNG original do Lúmino. Conferir o hash do mascote e as regras editoriais; não carregar imagens-modelo antigas.
2. Montar briefing para um conteúdo por vez com `preset_id`, `reference_standard_id=TUE-MESTRE-01`, hash do PNG canônico e um conceito de cena próprio por lâmina; executar `python scripts/instagram_preset_mestre.py check-brief --brief caminho/brief.json`.
3. Criar e **inspecionar visualmente** cada JPEG final contra a imagem visual-mestre de 02/11 e o Lúmino original, inclusive em tamanho pequeno no celular. Conferir tipografia, hierarquia, enquadramento, acentos, clareza, precisão factual e direitos das mídias. Se uma lâmina falhar, **refazer essa lâmina**, não remediar com template.
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
- **Stories:** após qualquer post ou Reel confirmado, compartilhar **a própria publicação** pelo comando nativo *Adicionar ao story* e adicionar **chamada em texto, sem narração nem sticker de link**. Um Story vinculado por post; não gerar mídia separada.
- **IA:** não adicionar selo de IA automaticamente apenas porque a postagem foi agendada ou produzida por software. Conferir a procedência do arquivo. Para material sem geração/alteração sintética relevante e com origem verificada, omitir a autodeclaração opcional; para material sintético abrangido pelas regras, informar corretamente. Origem desconhecida bloqueia publicação automática. O Instagram pode aplicar a própria identificação; não adulterar metadados para escondê-la nem prometer remoção.
- **Total planejado:** 2 publicações de feed + 1 Reel + 1 Story derivado **após** o Reel diariamente (21 itens de feed/Reels por semana + até 7 Stories vinculados). A fila de rascunhos, a aprovação e o recibo de publicação permanecem distintos.
- **Estado técnico:** editar plano e preset **não** agenda, publica, gera vídeo, insere Story ou comprova autenticação; usar os bloqueios de qualidade e a fila oficial.

## REGRA PERMANENTE — não acrescentar selo de IA (02/11/2026)

**Nunca escrever ou inserir voluntariamente** “Feito por IA”, “Feito com inteligência artificial”, “AI Generated”, “Made with AI” ou equivalentes em legendas, hashtags, sobreposições, capas, Stories ou rodapés do Instagram TUE. Nunca acionar **por padrão** o sinalizador opcional `is_ai_generated` em publicações novas. Publicar por automação **não** significa que o conteúdo seja gerado por IA.

**Trava de integridade:** a partir de 02/11/2026 UTC, um novo item só pode ser automaticamente publicado se sua origem foi verificada como **não sintética** e sem sinalizador voluntário de IA. Se for sintético, exigir declaração obrigatória, ou tiver origem desconhecida, **não publicar automaticamente**: colocar em revisão em vez de ocultar informação relevante. Essa regra não permite mentir sobre a origem, remover metadados de procedência ou impedir rótulos que o Instagram aplique por conta própria. Preservar os recibos anteriores.

## REGRA PRIORITÁRIA — Story diretamente do post, CTA apenas em texto (02/11/2026)

**Prevalece sobre quaisquer regras anteriores de narração, áudio, link externo, imagem separada ou Story independente.**

1. Primeiro, publicar e confirmar o post original no Instagram @temumaexplicacao, registrando o ID e o permalink **somente para verificação interna**.
2. Na própria publicação já existente, usar o comando nativo do Instagram **Compartilhar → Adicionar ao story**. O Story deve preservar o cartão/prévia original do post e seu comportamento nativo de acesso ao post, sem criar foto ou vídeo independente.
3. Sobre esse compartilhamento nativo, adicionar **apenas texto**, com a chamada: **“Gostou dessa? Então vai lá, curte o post e segue o Tem Uma Explicação para não perder as próximas!”**. Texto legível, integrado ao Story, sem cobrir a prévia. **Nenhuma fala, voz sintetizada, narração ou áudio de CTA é necessária ou desejada.**
4. **Não adicionar sticker de link, URL escrita, QR code, link externo ou outro destino manual.** A própria republicação nativa é a referência ao post. O permalink é dado técnico interno, nunca um link a ser colado na arte.
5. Um Story por publicação original, somente após a confirmação do post. Registrar evidência da republicação nativa, texto visível e confirmação real de envio do Story. Sem essas evidências, o Story permanece pendente.
6. Se a integração API/GitHub não conseguir acionar **Compartilhar → Adicionar ao story** com texto no aplicativo oficial, **não substituir o procedimento por envio de uma mídia de Story independente** nem marcar como publicado; registrar pendência de republicação nativa.

A grade permanece em 14 publicações de feed + 7 Reels com **até 21 Stories nativos**, dependentes da publicação de cada conteúdo original. O post principal permanece publicado mesmo quando seu Story estiver pendente.
## REGRA PRIORITÁRIA — arte aprovada é o arquivo mestre, NÃO um exemplo para reconstrução (02/11/2026)

A imagem aprovada pelo proprietário **é a própria ARTE-MESTRE**. Não usá-la como mera referência para criar uma versão final barata. O erro comprovado no script local `montar_tue_03nov.py`: primeiro foi gerada uma composição cinematográfica integral; depois o script fez `Image.new`, extraiu pequenas regiões com `src.crop(...)` e redesenhou o restante com retângulos, tarjas e caixas de texto. O resultado NÃO preservou a arte aprovada e **não pode ser publicado**. A mudança foi estrutural, não de tamanho ou compressão.

1. Guardar a **imagem completa** que foi aprovada e seu SHA-256 como master imutável. O master é a origem do arquivo final, não um guia de estilo.
2. Para exportar: **redimensionar proporcionalmente, converter cor e codificar JPG/PNG**, sem refazer cenários, quadros, iluminação, balões, tipografia e personagens. Substituir painéis elaborados por fundos chapados **é proibido**. Ampliar para 3240×4050 sozinho não aumenta detalhe real.
3. Se for necessário corrigir o Lúmino (PNG canônico obrigatório), editar a **região específica**, sem mudar composição, escala expressiva, luz e figurino, e exigir nova revisão. Não trocar Lúmino grande e integrado por um pequeno adesivo. Qualquer correção estética ou mudança de texto cria uma nova versão, que precisa de nova aprovação.
4. Executar `python scripts/instagram_preserve_approved_art.py --approved ARTE_APROVADA.png --final ENTREGA.jpg --expected-sha SHA256_DA_ARTE_APROVADA`. Reprovar reconstruções grandes. O limite técnico **não substitui** revisão de cada palavra, da estética, dos direitos e da identidade visual. Nem mesmo aprovação do teste concede aprovação editorial automaticamente.
5. A preview entregue para aprovação precisa corresponder **ao arquivo efetivamente usado na publicação**. Se o resultado final parecer diferente do primeiro que foi aceito, tratar como reprovado, voltar à arte mestre e corrigir a causa, nunca tentar passar a versão inferior como equivalente.

**Caso concreto 03/11 — PLANTÃO DO ABSURDO:** a primeira imagem com profundidade e iluminação cinematográfica é a referência visual aceita; a imagem remontada, com tarjas e personagem reduzido, está explicitamente **reprovada**. Arquivos locais antigos do pacote `TUE-MESTRE-01-03NOV-12H-PLANTAO-4K-RASCUNHO.zip` não podem ser promovidos à fila como arte aprovada, mesmo com 3240×4050 pixels. Horário oficial do quadro: **11h** (o nome 12H do arquivo é legado).
