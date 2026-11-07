# TUE — PADRÃO-MESTRE ÚNICO DE ANIMAÇÃO CINEMATOGRÁFICA

**ID:** TUE-ANIMACAO-MESTRE-01
**ESCOPO:** Odisseia integral, versões compactas, episódios e novas cenas mitológicas deste projeto.
**STATUS:** DIREÇÃO VIGENTE. Atualização 07/11/2026: o usuário esclareceu que **animação 3D NÃO é exigida**. Retornar ao método anterior de animação 2D articulada, preservando a identidade visual do vídeo de Troia que serviu de referência. Os testes e protótipos não aprovados continuam bloqueados.
**FONTE NORMATIVA ÚNICA:** este arquivo. Não recriar padrões concorrentes; alterações futuras devem editar aqui.

## 0. Princípios obrigatórios e resolução de conflitos

1. **Design completo precede o movimento.** Rosto, porte, idade, silhueta, roupa, armadura, capacete, gestos, paleta e props devem distinguir imediatamente cada personagem, mesmo sem texto ou narração.
2. **Produção final pode ser animação 2D articulada cinematográfica**: retomar a estética e a construção visual já utilizadas no vídeo de Odisseu/Cavalo de Troia, com personagens reconhecíveis, rigs/partes articuladas, ações contínuas, profundidade em camadas coerentes, contato e peso visuais, cenários consistentes e câmeras motivadas. **3D é opcional, não pré-requisito e não pode atrasar o vídeo**. Não substituir a ação por slides, fotos flutuantes, recortes genéricos, personagens deslizando nem colagens incoerentes.
3. **Narrativa visual é preparação → ação → consequência.** Nunca reciclar caminhadas de ida e volta, duplicar personagem, teleportar adereços, colocar protagonista global em todos os planos ou usar cenários sobrepostos sem relação espacial.
4. **Roteiro completo e visualmente dirigível antes do render:** timecodes, fala exata, casting com IDs persistentes, figurinos por fase, câmera, plano, set, arquitetura, clima, escala, objetos, movimentos articulados, contatos, expressões, direção de luz, foley e sincronização de legendas; cada plano contém instruções suficientes para ser reproduzido.
5. **Elmo com construção verdadeira:** calota, contorno, encaixe, crista firmemente presa, protetores, amarras, volume, metal, reflexos e sombras, em frente/perfil/três-quartos. Nunca uma massa genérica ou casco esférico. A versão guerreira pode ter bronze/crina como licença estilizada; na Grécia micênica histórica a aparência exige pesquisa e decisão visual documentada. **Odisseu não usa elmo automaticamente ao regressar à Ítaca.**
6. **Cenários habitáveis:** costa/vegetação/pedra/água/navio/cordame/carga/edificações e ambientes internos com escala, planta, passagens, materiais, iluminação, detalhes com função, distâncias e continuidade.
7. **Sem custo de API e sem dependência de Work/Runway:** preferir o fluxo anterior de **Remotion ou Python/Pillow/NumPy** para animação de personagens articulados, render com FFmpeg e execução em GitHub Actions. Blender é opcional; não substituir esse fluxo por renders 3D pesados sem instrução expressa. Respeitar limites reais de CPU e infraestrutura.
8. **Formato final-alvo:** vertical 9:16, 2160 × 3840, 60 FPS, trilha e voz Rasalgethi PT-BR quando original disponível, legendas inferiores; exportação escalonada deve ser identificada como upscale e não detalhamento 4K nativo.
9. **Prioridade factual:** base narrativa em Homero e na narração master; diferenças devem estar identificadas como adaptação. Na Odisseia XIII os feácios deixam Odisseu **adormecido** na costa com seus bens e partem; ele desperta depois. Os testes anteriores de desembarque consciente com passarela pertencem a uma adaptação visual, não ao cânone.
10. **QC editorial bloqueante:** o render técnico não é aprovação artística. Sem publicação e sem agendamento enquanto narratividade, atuação, consistência, som e legendas não forem revisados integralmente.

## 1. Fonte, versões e estado histórico

- Longa de referência com narração original de 560,100 segundos (Rasalgethi, PT-BR, AAC 48 kHz); não substituir voz sem solicitação, não colocar o master privado/credenciais no repositório.
- EP01 = 0–88,6 s; EP02 = 88,6–317,4 s; EP03 = 317,4–560,1 s. Esses limites são referências da fonte de 560,1 s, não do curta independente de 185 s.
- Existe também a adaptação curta descrita em odyssey_185/manifest_v9.json, com elenco e duração próprios. Aplicar este mesmo padrão de arte, não importar timecodes do longa.
- Storyboards históricos tiveram 110 ações e depois 131 ações distribuídas em 30 capítulos; 131 cortes não são meta obrigatória. Os eventos devem ser segmentados pela ação e sincronismo da fala. Houve problemas narrativos de 224 a 317 s no storyboard antigo; inspecionar cada trecho do master antes de fixar qualquer cena.
- V5/V7.1 foram REPROVADAS editorialmente. Os protótipos V8 não estão automaticamente aprovados. Render 4K60, duração e presença de áudio não substituem revisão.
- Referências estilísticas: mitologia grega e ambientação inspirada na Idade do Bronze e no Mediterrâneo; evitar armaduras romanas, templos clássicos fora de época ou cenários históricos genéricos.
- Roteiros que acompanham vídeo exigem também descrição visual completa; cada figura/objeto precisa ter identidade e estado inicial/final em todas as cenas.

## 2. Contrato espacial e de produção herdado e preservado

## Fonte única da narrativa
- Narração original, duração 560,1 s, idioma português brasileiro, voz Rasalgethi. O master privado original é fonte de áudio e de conferência de texto; NÃO reutilizar seus desenhos, bonecos, camadas ou cenas.
- Divisão prevista: EP01 0–88,6 s, EP02 88,6–317,4 s, EP03 317,4–560,1 s.
- Cada fala deve ser verificada contra cenas do roteiro e legenda original. Um timecode aproximado NÃO aprova nenhum frame.

## Motor de animação aprovado — sem 3D obrigatório
- **Método anterior como primeira opção:** animação 2D com personagens articulados e poses distintas por plano. Usar rigs em partes (tronco, cabeça, braços, mãos, pernas, capa) com trajetórias, interpolação e poses dirigidas pelo roteiro; compor em Remotion ou Python/Pillow/NumPy e codificar com FFmpeg. Não apresentar animação de câmeras sobre imagens paradas como animação dos personagens.
- Oclusão, escala visual, pontos de contato e deslocamento precisam ser coerentes no cenário 2D/2.5D; não exigir motor 3D.
- Personagens articulados com mãos, ombros, joelhos, tornozelos e marcha vinculados ao deslocamento do corpo. Não é permitido deslizar uma figura estática.
- O plano deve mostrar **preparação → ação concreta → consequência**: abrir o portão, atravessar, fechá-lo; embarcar, remar, deixar o cais; chegar à entrada, empurrar a PEDRA MAIOR QUE A PORTA, ver saída completamente bloqueada.
- Objetos têm dono e física: palmas tocam o objeto durante todo empurrão; pés apoiam no solo; ninguém atravessa a parede sem passagem explícita; uma pedra que deveria vedar a abertura deve ser maior do que ela.
- **Sem sobreposição como método de montagem:** proibido colocar protagonista, cenários, barco, objetos ou personagens por cima de uma animação genérica. Todos existem em coordenadas compartilhadas e dependem da câmera com z-buffer.
- Cada tomada tem casting próprio. Odisseu não aparece automaticamente em todos os planos. Cenário não reaproveitado como enchimento.
- Transições respeitam direções de deslocamento e posições do plano anterior; lentes/cortes só mudam com motivação narrativa.

## Modelo de produção, sem APIs pagas, sem PC
- Open-source: retomar arte 2D articulada com Remotion ou Python/Pillow/NumPy/FFmpeg, usando GitHub Actions quando aplicável. Render Blender/VTK 3D é um teste opcional e fica fora do caminho principal.
- O teste da **caverna de Polifemo (38–55 s)** continua útil, mas sua aprovação exige clareza narrativa e qualidade visual no estilo 2D articulado, não geometria 3D. Um teste 720 × 1280/30 FPS NÃO é o produto 4K final.
- Novo storyboard por plano, casting e objetos antes de render. Se um teste falha visualmente, corrigir o sistema e refazer o plano, não empilhar elementos por cima.
- Audio Rasalgethi e legendas do master originais: preservação; o vídeo do Github pode ser silencioso por não expor o master privado no repositório.

## QC *fail closed*
1. Assistir a sequência sem áudio: o observador consegue contar o acontecimento corretamente?
2. Assistir com áudio: cada fato falado aparece na ordem e com causa/consequência?
3. Verificar quadro a quadro entradas/saídas de objetos, contatos, profundidade, continuidade de membros, postura e movimento da câmera.
4. Inspecionar pontos de corte de cada cena e limites de quadro: nenhuma cabeça cortada ou ator oculto acidentalmente.
5. Verificar a ligação do passo ao deslocamento e ausência de teletransporte/animais desaparecendo.
6. Confirmar autoria/licenças das malhas/rigs externos. Sem marca d’água. Divulgação de conteúdo sintético conforme regras da plataforma quando aplicáveis.
7. **Só após QC visual e narrativo real:** render final nativo 2160 × 3840, 60 FPS, sincronismo, revisão completa, e então preparar o arquivo 1080 × 1920 permitido pela Meta API.
8. Sem publicação automática nem agendamento de amostras; V5/V7.1 marcadas REPROVADAS permanecem explicitamente bloqueadas.


## 3. Bíblia visual de personagens, objetos e roteiros

### Arte 1. Princípio central

**Movimento isolado não compensa design incompleto.** Antes da animação, cada plano precisa de:
1. protagonista reconhecível por **rosto, silhueta, paleta, roupas, adereços, idade aparente, postura e papel narrativo**, não apenas por legenda;
2. objetos completos e proporcionais, com construção, junções, materiais, pontos de apoio e contato;
3. cenário habitável e funcional com escala, passagem, orientação espacial, primeiro/médio/fundo e detalhes que expliquem a ação;
4. início, mudança e consequência visíveis na imagem; nenhuma caminhada de enchimento, retorno sem razão, personagem clonado ou cena reciclada;
5. continuidade do mesmo personagem e da mesma peça ao mudar câmera, luz, tomada ou episódio.

**Estética-alvo:** épico mitológico grego de **realismo estilizado cinematográfico**, com formas legíveis, anatomia convincente, materialidade artesanal, detalhes em bronze, tecido, couro, pedra, madeira, sal e desgaste; atmosfera histórica, aventura e emoção contida. Uma versão **2D articulada com movimentos reais dos personagens** pode ser o produto final, seguindo o vídeo de Troia como referência; manter profundidade, gestos, contatos, consistência e continuidade em todas as cenas.

### Arte 2. Personagens: ID estável e reconhecimento

Cada personagem nomeado recebe **CHAR_ID imutável**, model sheet/turnaround (frente, 3/4, perfil, costas), ficha de escala, paleta com valores estáveis, topologia e rig, biblioteca de expressões, figurinos por fase, mapa de adereços, textura de desgaste e pelo menos uma pose de assinatura. **Nunca** gerar novamente um personagem com outra anatomia/rosto a cada plano. Personagens secundários em grupo também precisam variar em altura, corpo, idade, cabelo, barba, roupa, gesto e função, sem trocar a identidade entre tomadas.

### CHAR_ODYSSEUS — Odisseu / Ulisses
- Homem adulto maduro; constituição de guerreiro experiente, ombros firmes, rosto alongado/anguloso, nariz e sobrancelhas característicos, barba escura curta com grisalho discreto, cabelo castanho-escuro ondulado. Identidade facial **permanece igual** em todas as fases.
- Olhar estratégico e observador; expressões predominantemente contidas. Passos ponderados, olhar de reconhecimento, decisões físicas com intenção. Nunca correr/gesticular aleatoriamente em loops.
- Paleta-base: bronze envelhecido, ocre, couro castanho, vermelho queimado e azul-mar profundo em detalhes. Diferenciação por **silhueta e rosto mesmo sem capacete**.
- **Fase guerreiro/Troia:** elmo de bronze de inspiração grega, crista de crina escura **fixada em uma base estrutural**, calota, borda, nasal se aplicável, proteções de bochecha, interior e amarrações coerentes; volume que encaixa anatomicamente na cabeça. O capacete NÃO é esfera, casco amorfo, chapéu mole, máscara solta nem objeto fundido ao cabelo. Conferir lateral, perfil, três-quartos e ação dinâmica. Peitoral/couraça de couro e bronze, manto gasto, sandálias reais, sem adereços sem função.
- **Fase naufrágio/desembarque clandestino/Ítaca:** roupa de viagem simples conforme a cena; **não usar capacete ou armadura automaticamente**. O rosto, a voz, a postura e os gestos continuam identificando o herói.
- **Fase mendigo disfarçado:** figurino e postura de disfarce intencionais, ainda com base facial e corporal coerente; a montagem explicita como e por que muda a aparência.
- Objetos como arco, espada, remo, cordas e manto têm dono, dimensões, pegada, mão e destino no plano seguinte.

### CHAR_PHAEACIAN_CREW_A / _B / _C — tripulantes feácios
- Conjunto de **três designs diferentes**, sem armaduras/copias de Odisseu: A alto e magro, barba castanha e túnica azul dessaturada; B robusto, cabelo curto e túnica areia/ocre; C mais velho, barba grisalha, manto cinza-azulado. Cores, rostos e alturas não intercambiáveis.
- Funções individualizadas: remar, conduzir, segurar amarra ou descarregar presentes. Só executar ações correspondentes à cena; não adicionar marinheiros só para preencher quadro.
- Roupas de fibras naturais, cintos e sandálias com construção consistente; nenhum capacete heroico igual ao de Odisseu.

### CHAR_PENELOPE — Penélope
- Mulher adulta, expressão inteligente e reservada; design próprio de olhos, penteado preso/trançado e manto em tons violeta/azul-profundo/linho. Silhueta vertical e gestos precisos do tear.
- O tear é objeto funcional com fios, lançadeira e tecido com continuidade. Não transformar Penélope em figura infantil nem colocar bebê fora de época.

### CHAR_TELEMACHUS — Telêmaco
- Jovem adulto, reconhecível como filho, mas não cópia facial do pai. Mais esguio, cabelo escuro mais curto, sem barba cheia; azul-marinho/terra-clara, postura em progressão de inseguro para decidido. Escala consistente ao lado de Odisseu.

### CHAR_POLYPHEMUS — Polifemo
- Gigante ciclope de **um olho central**, proporção massiva em escala constante diante da mesma porta, ovelhas e pessoas. Membros completos e articulados, mãos com pegada na pedra, joelhos, ombros e pés com peso.
- A pedra que veda a caverna deve ser **maior do que o vão** e efetivamente bloquear toda a passagem; empurrar exige contato contínuo e reação de corpo/ambiente. Não reaproveitar o rig nem a face dos humanos.

### CHAR_ATHENA — Atena
- Identidade própria: postura lúcida e serena, olhos expressivos, paleta branco-pedra/azul-petróleo/dourado, armamento e iconografia consistentes quando presentes. Transformações/divindade precisam de motivação e transição visível.

### CHAR_EURYKLEIA / CHAR_ARGOS / CHAR_ANTINOOS
- Euricleia: mulher idosa de face e mãos distintas; reconhecimento de cicatriz com blocking e contato real.
- Argos: cão idoso, anatomia e pelagem próprias, gestos pequenos mas reconhecíveis; nunca um sprite genérico.
- Antínoo: pretendente com aparência e figurino explicitamente diferenciados do herói, postura arrogante, escala humana correta e interação física com o salão.

**Personagem novo:** obrigatoriamente acrescentar ficha semelhante antes do primeiro plano; criar asset com CHAR_ID único, nunca recorrer a NPC repetido sem direção de multidão.

### Arte 3. Figurino, elmo e objetos: regras de construção

- Cada peça é um objeto desenhado/modelado **com estrutura verificável**: bordas, espessura, fixações, costuras, fechos, amarras, juntas e materiais; superfícies não atravessam corpo.
- Elmo de Odisseu: verificar perfil/3⁄4/frente, abertura do rosto, inserção da crista, protetores laterais, textura de bronze e sombra de contato. Não simplificar a ponto de perder leitura. **Conferir enquadramento fechado antes de aprovar**.
- Espadas entram/saem de bainha; remos entram na água; cordas se prendem a objetos; personagens pisam em chão/degrau/passarela fisicamente existentes; capa reage à gravidade, corpo e vento sem atravessar braço ou escudo.
- Escala invariável: tamanho da porta/pedra, casco, embarcação, convés, passarela, humanos, animais, móveis. Sem aumento/diminuição para facilitar um corte.
- Adereços persistem ou mudam por ação motivada: não desaparecem, teleportam ou mudam de mão fora de quadro sem justificativa.
- Incluir desgaste **funcional** (amassados, sal, manchas, dobras); não textura aleatória decorativa.

### Arte 4. Cenários completos, com função dramática

- Todo cenário tem **planta de piso, elevações, coordenadas, ponto de entrada/saída, iluminação motivada e zonas transitáveis**. O elenco e objetos coexistem em cenários coerentes, com escala e projeção consistentes, contatos desenhados por rig/pose, sombras e oclusão 2D/2.5D adequadas; **geometria 3D não é obrigatória**.
- A costa de Ítaca: baía rochosa crível, oliveiras e vegetação mediterrânea, relevo distante, transição água-praia/pedra, horizonte/luz de manhã, cargas/presentes e embarcação com geometria naval coerente. **Não inventar cais/passarela em uma adaptação fiel da chegada narrada no poema.**
- Navio: proa/poppa reconhecíveis, casco com bordas, bancos, remos, mastreação, cordames, carga. Manobras devem decorrer de vento/remadores/leme e contatos.
- Caverna de Polifemo: uma única abertura contínua, profundidade interna, posição de ovelhas/alimentos, rocha proporcional. A fuga respeita a posição anterior da pedra.
- Palácio: arquitetura navegável; portas, mesas, salão, arco, tear e leito de oliveira posicionados consistentemente.
- Ambientes têm detalhes **que contam o contexto**; evitar fundos vazios, adereços aleatórios ou decoração exagerada que confunde o foco.

### Arte 5. Roteiro técnico obrigatório **antes de renderizar**

O roteiro não pode conter somente narração ou um prompt amplo. **Cada plano** deve ter uma ficha preenchida:

1. **SHOT_ID, episódio/capítulo, timecode início/fim, duração, frase exata da narração original**, fonte e observação sobre o cânone/adaptação.
2. **Objetivo dramático e estado inicial → ação → consequência**, legíveis sem áudio.
3. **Elenco explícito** por CHAR_ID, fase/figurino, expressão, características físicas persistentes; quem NÃO deve aparecer.
4. **Ambiente/set** com escala, geografia, entradas/saídas, clima, hora do dia, iluminação, props com PROP_ID e função narrativa.
5. **Composição**: lente/FOV, altura e posição da câmera, distância, foco, profundidade, iluminação, movimento e justificativa para o corte.
6. **Blocking por batida temporal**: posição no mundo, trajetória, olhar, gesto, contato das mãos/pés, velocidade, peso, pausas, antecipação, follow-through e reação de personagens secundários.
7. **Continuidade**: posição/vestimenta/objeto/estado de início e fim; regra de passagem para o plano seguinte.
8. **Som**: sincronização exata com voz Rasalgethi já existente, foley/música e legenda inferior, sem renarrar onde houver master aprovado.
9. **Composição/saída**: 9:16, master 2160×3840/60 FPS nativos na etapa final; protótipos devem declarar se são 720p/1080p/30 FPS ou upscale.
10. **QC de aprovação**: checkpoints de close, perfil, vista 3/4, passagem, membros, colisões, props, leitura sem áudio, correspondência com fala, licença e publicação bloqueada por padrão.

### Template de plano (copiar e preencher)
\`\`\`text
SHOT_ID:
CAPÍTULO / EPISÓDIO:
ÁUDIO ORIGINAL (timecodes e fala exata):
FATO DO POEMA / LIBERDADE DE ADAPTAÇÃO:
OBJETIVO DRAMÁTICO:
ELENCO (CHAR_ID / variante de figurino / silhueta / rosto / postura):
OBJETOS (PROP_ID / geometria / dimensões / quem segura / onde termina):
CENÁRIO (SET_ID / escala / piso / pontos de acesso / planos / clima / luz):
CÂMERA (posição / lente / enquadramento / foco / movimento / corte):
BLOCKING (tempo → posição → gesto → contato → reação):
FÍSICA (pé no apoio / mãos / colisão / peso / tecidos):
CONTINUIDADE ENTRADA/SAÍDA:
SOM / LEGENDA:
CRITÉRIOS DE QC E ERROS A EVITAR:
ESTADO: NÃO APROVADO
\`\`\`

### Arte 6. Caso de referência: chegada a Ítaca (corrigido conforme Homero)

**Fonte:** *Odisseia*, canto XIII. Os feácios transportam Odisseu **adormecido** e o depositam na costa, com seus presentes, antes de partirem. O herói desperta em Ítaca mais tarde. O rascunho de testes anteriores no qual ele caminha por passarela de um cais é **uma adaptação criativa**, não a chegada literal narrada pelo poema. Não misturar os dois como se fossem o mesmo evento sem declaração explícita.

- **Plano A / aproximação:** embarcação feácia em mar calmo, remadores distintos em posições reais, Odisseu adormecido sob tecido de viagem, costa rochosa amanhecendo; a câmera orienta o sentido da viagem.
- **Plano B / deposição:** tripulantes recolhem Odisseu com apoio plausível de ombros, braços e pernas; levam-no pela borda/terra em blocking contínuo; sacos/presentes mantêm continuidade.
- **Plano C / partida:** feácios voltam ao mesmo navio, executam ação completa de afastamento; Odisseu permanece na margem adormecido com seus presentes, sem reaparecer no convés.
- **Plano D / despertar:** Odisseu desperta, levanta-se com peso e estranha a paisagem; rosto inequívoco **sem elmo**. O entorno e os presentes conservam posições.
- **Plano E / descoberta:** a decisão/identificação de Ítaca surge da trama e da voz do master, sem afirmar que ele reconhece imediatamente o lugar; plano fecha na reação, não em gesto heroico genérico.

Esse exemplo **não substitui timecodes**, que dependem da narração original sincronizada. Se a voz original descreve outra ação, ajustar o plano à fala; se a narração contraria o poema, documentar explicitamente como adaptação antes de aprovar.

### Arte 7. Prompt-mestre para gerar/dirigir novas cenas

> Produza [SHOT_ID] da Odisseia em animação 2D articulada cinematográfica estilizada com identidade visual fixa segundo esta bíblia: CHAR_IDs constantes, proporções e figurinos adequados à fase, rosto/silhueta reconhecíveis de plano para plano, objetos e cenários com construção completa e escala verificável, elmo de bronze apenas quando narrativamente presente e fisicamente bem modelado. Mostre preparação, ação específica e consequência dentro de uma composição espacial 2D/2.5D coerente com personagens articulados, oclusão e profundidade visual, contato de mãos e pés, física consistente, câmera motivada, luz/materialidade cinematográficas e atuação emocional discreta. Use o timecode e a fala exata do master, sem inventar acontecimentos nem repetir cenas. Descreva cada batida de blocking, elementos presentes e ausentes, câmera, set, som e continuidade antes da geração. Rejeite clones, rosto flutuante, cascos amorfos, movimento em skate, colagens incoerentes, objetos sem dono, passagem impossível, escala instável, corte que teleporta, cenário vazio, desvio do roteiro, nova voz não autorizada e qualquer plano que não passe no QC visual real.

### Arte 8. Critérios de aceitação *fail closed*

**Reprovar o plano** se qualquer item abaixo estiver inadequado:
- capacete/rosto/silhueta irreconhecíveis ou inconsistentes; mesma face/roupa entre papéis diferentes;
- falta de acessórios ou peças estruturais (crista, protetores, fechos, calçado, bainha, corda, casco, piso etc.) quando necessários;
- cenário visualmente vazio, sem geografia funcional, props sem contato ou escala incorreta;
- pés deslizando, joelho quebrado, mãos sem pegada, peças atravessando corpo/paredes, movimento repetido sem objetivo;
- ação/ordem incoerentes com frase do áudio, ausência de preparação ou consequência, aparição inexplicada de personagem;
- ausência de inspeção de cenas e transições, teste não nativo declarado como 4K nativo, áudio/legendas dessíncronos.

**Pipeline:** roteiro e ficha → bible/asset lock → key poses / blocking → playblast → revisão de arte e identidade → correção de física/continuidade → render de QC → revisão integral com e sem áudio → render 4K60 final → aprovação explícita → somente então considerar publicação. Não modificar agendamentos ou publicar a partir desta atualização documental.


## 4. Exigências de cenas emblemáticas

### Cavalo de Troia
Corpo de cavalo identificável, quatro pernas, pescoço, cabeça, volume de madeira, acesso/porta real, proporção compatível com o portão. Mostrar entrada, ação dos guerreiros que saem de dentro, abertura efetiva e consequência. Não usar geometria indistinta ou clones.

### Polifemo
Um olho central, escala constante, membros completos, ovelhas e humanos distintos. A rocha deve ser **maior do que a entrada**, encostar nas mãos do gigante durante o empurrão e **fechar por inteiro** o portal. A fuga posterior depende do mesmo obstáculo ser retirado, sem teleporte.

### Ítaca, Penélope e o reconhecimento
Costa com geografia completa e presentes dos feácios. Odisseu acorda depois de ser deixado adormecido; não equipá-lo como guerreiro sem justificativa. Tear de Penélope é funcional e segue posição e materiais; Argos, Euricleia, Telêmaco e Laertes têm visual e atuação únicos. Na prova do leito, a cama vinculada à oliveira não pode mudar de geometria e lugar; na cena do arco, usar os mesmos objetos, 12 machados distintos e passagem física da flecha.

### Elenco não enumerado na bíblia
Criar CHAR_ID, model sheet, paleta, silhueta, rosto, rig, figurino e comportamento únicos para Circe, Calipso, Nausícaa, Hermes, Éolo, Poseidon, Laertes, Eumeu e demais figuras que surjam no roteiro. Não substituir por homens uniformes com o mesmo rosto.

## 5. Procedimento de aceite e governança

A ordem é: fonte/roteiro → ficha por plano → model sheet → props e set com escala → blocking/poses-chave → teste de 10–15s e revisão sem áudio → sincronismo com Rasalgethi/legendas → inspeção de close, perfil, três-quartos e movimento → correção/refação do plano → vídeo integral em 4K60 → revisão de todos os cortes e das interações → aprovação expressa → somente então preparação para publicação.

**Reprovar** se houver capacete deformado, personagens clonados, roupas incoerentes, mãos sem contato, pés deslizando, objeto sem dono ou escala, passagem impossível, cena sem consequência, repetição como enchimento, falha de continuidade, personagem fora do roteiro, áudio divergente ou cenários vazios.

**Registros, não normas concorrentes:** os relatórios docs/ODISSEIA-QC-06NOV-REANIMACAO-PARCIAL.md, docs/ODISSEIA-RETOMADA-QC-06NOV-2026.md e content/editorial/ODISSEIA-REPROVADA-REFACAO-NARRATIVA-06NOV2026.md devem permanecer para auditoria. Código e testes de odyssey_v8, motion e odyssey_185 não devem ser apagados sob a alegação de ser "padrão anterior". Referências técnicas históricas: Actions 42277442700, 42278410074, 42278628925 e 42288210740, todas sem equivaler a aprovação visual.

**A única fonte de verdade para a direção da Odisseia é odyssey_v8/PADRAO_MESTRE_TUE_ANIMACAO.md.** Contratos e roteiros devem apontar para ele. Outros documentos do Instagram, a identidade Lúmino e os controles de publicação não fazem parte desta substituição.
