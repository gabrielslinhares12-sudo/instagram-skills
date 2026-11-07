# Odisseia — direção visual e bíblia de personagens (padrão vinculante)

**Escopo:** todos os novos roteiros, shot contracts, designs, rigs, storyboards, renders e revisões da Odisseia.  
**Situação:** especificação de produção; **não** significa vídeo aprovado ou autorização para publicar.  
**Autoridade técnica complementar:** [PRODUCTION_RULES.md](PRODUCTION_RULES.md). Se houver conflito, manter o requisito de cenas **3D reais** como entrega final; a ilustração 2D é linguagem estética/referência ou teste, e não licença para voltar a sobreposições, pan/zoom de fotografias ou recortes flutuantes.

## 1. Princípio central

**Movimento isolado não compensa design incompleto.** Antes da animação, cada plano precisa de:
1. protagonista reconhecível por **rosto, silhueta, paleta, roupas, adereços, idade aparente, postura e papel narrativo**, não apenas por legenda;
2. objetos completos e proporcionais, com construção, junções, materiais, pontos de apoio e contato;
3. cenário habitável e funcional com escala, passagem, orientação espacial, primeiro/médio/fundo e detalhes que expliquem a ação;
4. início, mudança e consequência visíveis na imagem; nenhuma caminhada de enchimento, retorno sem razão, personagem clonado ou cena reciclada;
5. continuidade do mesmo personagem e da mesma peça ao mudar câmera, luz, tomada ou episódio.

**Estética-alvo:** épico mitológico grego de **realismo estilizado cinematográfico**, com formas legíveis, anatomia convincente, materialidade artesanal, detalhes em bronze, tecido, couro, pedra, madeira, sal e desgaste; atmosfera histórica, aventura e emoção contida. Uma versão 2D ilustrada pode servir como *concept art* e animatic, mas o produto integral segue os requisitos espaciais do motor 3D independente.

## 2. Personagens: ID estável e reconhecimento

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

## 3. Figurino, elmo e objetos: regras de construção

- Cada peça é um objeto desenhado/modelado **com estrutura verificável**: bordas, espessura, fixações, costuras, fechos, amarras, juntas e materiais; superfícies não atravessam corpo.
- Elmo de Odisseu: verificar perfil/3⁄4/frente, abertura do rosto, inserção da crista, protetores laterais, textura de bronze e sombra de contato. Não simplificar a ponto de perder leitura. **Conferir enquadramento fechado antes de aprovar**.
- Espadas entram/saem de bainha; remos entram na água; cordas se prendem a objetos; personagens pisam em chão/degrau/passarela fisicamente existentes; capa reage à gravidade, corpo e vento sem atravessar braço ou escudo.
- Escala invariável: tamanho da porta/pedra, casco, embarcação, convés, passarela, humanos, animais, móveis. Sem aumento/diminuição para facilitar um corte.
- Adereços persistem ou mudam por ação motivada: não desaparecem, teleportam ou mudam de mão fora de quadro sem justificativa.
- Incluir desgaste **funcional** (amassados, sal, manchas, dobras); não textura aleatória decorativa.

## 4. Cenários completos, com função dramática

- Todo cenário tem **planta de piso, elevações, coordenadas, ponto de entrada/saída, iluminação motivada e zonas transitáveis**. O elenco e objetos coexistem em geometria 3D, compartilham escala, projeção, colisão, sombras/oclusão.
- A costa de Ítaca: baía rochosa crível, oliveiras e vegetação mediterrânea, relevo distante, transição água-praia/pedra, horizonte/luz de manhã, cargas/presentes e embarcação com geometria naval coerente. **Não inventar cais/passarela em uma adaptação fiel da chegada narrada no poema.**
- Navio: proa/poppa reconhecíveis, casco com bordas, bancos, remos, mastreação, cordames, carga. Manobras devem decorrer de vento/remadores/leme e contatos.
- Caverna de Polifemo: uma única abertura contínua, profundidade interna, posição de ovelhas/alimentos, rocha proporcional. A fuga respeita a posição anterior da pedra.
- Palácio: arquitetura navegável; portas, mesas, salão, arco, tear e leito de oliveira posicionados consistentemente.
- Ambientes têm detalhes **que contam o contexto**; evitar fundos vazios, adereços aleatórios ou decoração exagerada que confunde o foco.

## 5. Roteiro técnico obrigatório **antes de renderizar**

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

## 6. Caso de referência: chegada a Ítaca (corrigido conforme Homero)

**Fonte:** *Odisseia*, canto XIII. Os feácios transportam Odisseu **adormecido** e o depositam na costa, com seus presentes, antes de partirem. O herói desperta em Ítaca mais tarde. O rascunho de testes anteriores no qual ele caminha por passarela de um cais é **uma adaptação criativa**, não a chegada literal narrada pelo poema. Não misturar os dois como se fossem o mesmo evento sem declaração explícita.

- **Plano A / aproximação:** embarcação feácia em mar calmo, remadores distintos em posições reais, Odisseu adormecido sob tecido de viagem, costa rochosa amanhecendo; a câmera orienta o sentido da viagem.
- **Plano B / deposição:** tripulantes recolhem Odisseu com apoio plausível de ombros, braços e pernas; levam-no pela borda/terra em blocking contínuo; sacos/presentes mantêm continuidade.
- **Plano C / partida:** feácios voltam ao mesmo navio, executam ação completa de afastamento; Odisseu permanece na margem adormecido com seus presentes, sem reaparecer no convés.
- **Plano D / despertar:** Odisseu desperta, levanta-se com peso e estranha a paisagem; rosto inequívoco **sem elmo**. O entorno e os presentes conservam posições.
- **Plano E / descoberta:** a decisão/identificação de Ítaca surge da trama e da voz do master, sem afirmar que ele reconhece imediatamente o lugar; plano fecha na reação, não em gesto heroico genérico.

Esse exemplo **não substitui timecodes**, que dependem da narração original sincronizada. Se a voz original descreve outra ação, ajustar o plano à fala; se a narração contraria o poema, documentar explicitamente como adaptação antes de aprovar.

## 7. Prompt-mestre para gerar/dirigir novas cenas

> Produza [SHOT_ID] da Odisseia em 3D cinematográfico estilizado com identidade visual fixa segundo esta bíblia: CHAR_IDs constantes, proporções e figurinos adequados à fase, rosto/silhueta reconhecíveis de plano para plano, objetos e cenários com construção completa e escala verificável, elmo de bronze apenas quando narrativamente presente e fisicamente bem modelado. Mostre preparação, ação específica e consequência dentro de um único mundo 3D com profundidade real, contato de mãos e pés, física consistente, câmera motivada, luz/materialidade cinematográficas e atuação emocional discreta. Use o timecode e a fala exata do master, sem inventar acontecimentos nem repetir cenas. Descreva cada batida de blocking, elementos presentes e ausentes, câmera, set, som e continuidade antes da geração. Rejeite clones, rosto flutuante, cascos amorfos, movimento em skate, sobreposição 2D, objetos sem dono, passagem impossível, escala instável, corte que teleporta, cenário vazio, desvio do roteiro, nova voz não autorizada e qualquer plano que não passe no QC visual real.

## 8. Critérios de aceitação *fail closed*

**Reprovar o plano** se qualquer item abaixo estiver inadequado:
- capacete/rosto/silhueta irreconhecíveis ou inconsistentes; mesma face/roupa entre papéis diferentes;
- falta de acessórios ou peças estruturais (crista, protetores, fechos, calçado, bainha, corda, casco, piso etc.) quando necessários;
- cenário visualmente vazio, sem geografia funcional, props sem contato ou escala incorreta;
- pés deslizando, joelho quebrado, mãos sem pegada, peças atravessando corpo/paredes, movimento repetido sem objetivo;
- ação/ordem incoerentes com frase do áudio, ausência de preparação ou consequência, aparição inexplicada de personagem;
- ausência de inspeção de cenas e transições, teste não nativo declarado como 4K nativo, áudio/legendas dessíncronos.

**Pipeline:** roteiro e ficha → bible/asset lock → key poses / blocking → playblast → revisão de arte e identidade → correção de física/continuidade → render de QC → revisão integral com e sem áudio → render 4K60 final → aprovação explícita → somente então considerar publicação. Não modificar agendamentos ou publicar a partir desta atualização documental.
