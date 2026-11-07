# A ODISSEIA — O REGRESSO A ÍTACA
## Roteiro definitivo de direção para PRODUÇÃO (não confundir com filme pronto)

**Padrão normativo:** [TUE-ANIMACAO-MESTRE-01](../odyssey_v8/PADRAO_MESTRE_TUE_ANIMACAO.md)  
**Canal:** Tem Uma Explicação  
**Duração-alvo:** 03:05 (185,000 segundos) · **16 sequências** · **74 tomadas dirigidas** · **11.100 quadros a 60 FPS**  
**Alvo de entrega:** vertical 9:16 · 2160 × 3840 · 60 FPS · realismo estilizado 3D · PT-BR  
**Voz:** Rasalgethi — Google AI Studio (interface web, sem API paga)  
**Estado de produção:** ROTEIRO DE DIREÇÃO EDITORIAL; não indica áudio gerado, cena renderizada, aprovação ou autorização de publicação.  
**FONTE DAS FALAS:** texto fornecido pelo usuário, preservado literalmente e também presente em `odyssey_185/manifest_v9.json`.

> **Regra de composição:** a S01 é um flashforward de suspense para o arco. S02 retorna a Troia; S02–S16 percorrem a história temporalmente. O retorno ao salão em S15 é um reencontro visual com o prólogo, não reutilização preguiçosa de tomada. A narrativa histórica é uma adaptação condensada do poema atribuído a Homero, não reconstituição documental de arqueologia.

## A. Contrato visual global

**Personagens:** mesmo CHAR_ID, base facial, medidas, paleta, UV/texturas e rig em todos os planos. Variações `guerreiro`, `viajante`, `mendigo`, `revelado` não alteram a identidade facial. **Não inserir um ator fora do elenco listado em cada tomada.** Equipes/grupos usam instâncias únicas e diferentes; acrescentar figurantes adicionais somente com ficha completa de rosto, corpo e vestimenta.

**Odisseu:** homem maduro (~45 na chegada, idade artística aproximada), nariz característico, barba escura com grisalhos, cabelos ondulados, olhos castanhos, ombros largos, marcas de guerra e cicatriz na porção superior da coxa. Guerreiro: couro/bronze, túnica ocre, manto vermelho escurecido, elmo completo opcional somente em cenas adequadas. Viajante: túnica desgastada e manto cinza-terroso, sem elmo. Mendigo: túnica puída, capuz e curvatura deliberada, mantendo o mesmo rosto sob transformação de Atena. Revelado: porte reerguido e traje civil de Ítaca.

**Penélope:** madura, cabelos castanho-escuros trançados, postura firme, linho marfim e azul-violeta; mãos hábeis no tear, estratégia e desconfiança. **Telêmaco:** ~20 anos, mais esguio que o pai, barba curta, capa azul-acinzentada; evolução gradual da postura. **Antínoo:** mais forte, maxilar amplo, manto açafrão, gestos possessivos. **Eurímaco:** mais esguio, cabelo penteado, manto púrpura-acinzentado, expressão manipuladora.

**Polifemo:** um olho central, ~5,5 m na escala da adaptação, volumetria pesada, mão de força e patas/pés massivos; a pedra é maior do que o vão. **Circe:** cabelo negro longo, túnica verde-cobre, olhar enigmático, gestual preciso. **Calipso:** cabelos longos, túnica creme, traços serenos e olhar melancólico. **Atena:** olhos cinzentos, bronze detalhado com motivos próprios, postura nobre, lança funcional; magia visualiza transformação, não corte que troca ator. **Hermes:** jovem adulto, aparência e capa distintas, um único prop vegetal moly. **Nausícaa:** jovem adulta de túnica azul-clara, voz e comportamento de hospitalidade; **Alcínoo:** rei feácio de barba prata curta, manto azul-marinho, gestos de comando. **Laertes:** mais idoso e curvado que o filho, barba branca, roupa de pomar ocre-clara. **Eumeu:** pastor de ombros gastos, barba grisalha e túnica marrom, mãos de trabalho. **Euricleia:** idosa de manto creme, dedos finos e expressão de reconhecimento. **Argos:** cão idoso único, pelo marrom-branco, membros frágeis e olhar cansado.

**Tripulantes feácios:** três rostos, estaturas e figurinos constantes e diferentes dos gregos; A alto/magro de azul lavado, B robusto em ocre, C idoso em cinza-azulado. **Companheiros gregos:** A barba castanha/linho natural, B mais baixo/barba ruiva/manto terracota, C alto/cabelo escuro/túnica azul-cinza; outros D/E/F recebem modelos distintos antes da cena de Cila. Monstros, fantasmas, pretendentes e demais personagens nomeados têm biblioteca independente. Nunca copiar o rig visual completo do protagonista para povoar cena.

**Arte/materiais:** mundo micênico estilizado da Idade do Bronze; madeira irregular, couro tensionado, bronze com espessura/costura/fixação, linho/lã, rocha volumétrica, água tridimensional e fogo com iluminação incidente. Evitar elmos ou arquitetura romana; a crista de crina no elmo de Odisseu é licença artística explícita, não uma alegação histórica. Cores: Troia cobre/fogo, mar profundo azul-petróleo, Circe verde-cobre, Hades cinza-azul, Ítaca quente/dourado. Toda cena tem planta, superfície transitável, acesso, escala, primeiro/médio/fundo, luz motivada e props funcionais.

**Animação:** root motion com ciclo de marcha acoplado a distância, IK de pés e mãos, transferência de peso, contato contínuo de prop, colisão, simulação física moderada de manto e cabelos, expressão facial intencional. Mostrar antecipação → movimento → reação/resultado; sem inversão arbitrária de direção, patinação ou bonecos deslizando. Objetos e atores são renderizados no mesmo espaço 3D e com oclusão real.

**Câmera:** lentes 24/35/50/85 mm; 24 para geografia/escala; 35 para ação; 50 para emoção/interações; 85 para olhos e peças-chave. Eixo, altura, direção da luz e geografia devem respeitar continuidade. Nada de órbita decorativa para disfarçar falta de animação. Transições são motivadas pelo último estado do plano anterior.

**Som/montagem:** construir primeiro a narração Rasalgethi integral, depois refinar timecodes sem acelerar artificialmente a voz. Trilha instrumental original sem vocal cantado; efeitos de ambiente nas fontes que se veem; silencios de impacto dramático. Legendas inferiores PT-BR, sem serifas, até duas linhas e margem segura do Instagram; sem sobreposição de frases, marcas d’água ou textos técnicos. As 16 janelas são provisórias e só viram horários fixos quando o áudio real for medido.

**Limites narrativos/fidelidade:** S12 deve mostrar feácios depositando Odisseu *adormecido* em Ítaca; ele não reconhece a ilha imediatamente (canto XIII). A cicatriz é na parte alta da coxa de ferimento antigo por javali, encontrada por Euricleia (canto XIX). A cama é construída ao redor do tronco de uma oliveira viva e não pode ser deslocada (canto XXIII); o encontro com Laertes e a paz instituída por Atena são do canto XXIV. O cavalo de Troia é tradição mitológica conhecida, usado aqui como prólogo de contexto.

**Controle de qualidade:** toda tomada começa `approved=false` até playblast, revisão de geometria, integridade visual de elmo, mãos, olhos, joelhos e pés, contato de objetos, QC sem áudio, correspondência da fala e revisão do MP4 final. Não utilizar o status “finalizado” nem publicar apenas porque há um arquivo 4K.

## B. Roteiro com direção por tomada

### S01 — ABERTURA - O ARCO (00:00–00:07, 7 s)

**Narração integral (sem alterações):** “Um velho mendigo ergueu um arco diante de dezenas de guerreiros. Ninguém imaginava quem ele realmente era.”

**Elenco / figurinos:** CHAR_ODYSSEUS:mendigo; CHAR_ANTINOOS; CHAR_EURYMACHOS; CHAR_PRETENDENTE_A; CHAR_PRETENDENTE_B. **Set:** `SET_PALACIO_SALAO`. **Props rastreáveis:** `PROP_ARCO_REAL`, `PROP_MACHADOS_12`, `PROP_TACA_BRONZE`, `PROP_TOCHA_SALAO`.

**Direção de arte e luz:** flashforward no salão micênico: pilares de madeira, reboco pigmentado, bancos e comida; luz âmbar de tochas com sombras volumétricas. Odisseu veste linho rasgado e manto cinza, rosto envelhecido por disfarce, sem capacete.

**Câmera e encenação:** 85 mm arco/mãos → 50 mm olhos → 35 mm relações de poder

**Tomadas e marcação de movimento:**

- **S01-T01 · 00:00–00:02 · 85 mm:** Macro lateral: polegar do mendigo percorre entalhe do arco e tensiona brevemente a corda; mão e madeira têm contato real. **Foley:** madeira e fricção.
- **S01-T02 · 00:02–00:04 · 35 mm:** Contra-plano: Antínoo, robusto de manto açafrão, ri; Eurímaco, esguio de manto púrpura, ergue taça, figurantes variam em rosto e gestos. **Foley:** taça e murmúrios.
- **S01-T03 · 00:04–00:07 · 50 mm:** Dolly lento revela olhos castanhos de Odisseu sob capuz; postura passa de curvada a firme, sem armar o arco ainda. Corte elíptico para Troia. **Foley:** música suspende.

**Continuidade de saída → entrada:** Gancho temporal identificado por corte visual e motivação: volta para o passado em S02; mesmo arco, marcas e aposento reaparecem em S15.

**Reprovar se:** Não revelar antecipadamente a identidade nem apresentar pretendentes como soldados clonados.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S02 — A QUEDA DE TROIA (00:07–00:17, 10 s)

**Narração integral (sem alterações):** “Era Odisseu, o estrategista que ajudara a destruir Troia com um gigantesco cavalo de madeira. Após dez anos de guerra, ele finalmente partiu para casa.”

**Elenco / figurinos:** CHAR_ODYSSEUS:guerreiro; CHAR_TRIPULANTE_A; CHAR_TRIPULANTE_B; CHAR_TRIPULANTE_C; CHAR_TROIANO_A; CHAR_TROIANO_B. **Set:** `SET_TROIA_MURALHAS_NAVIO`. **Props rastreáveis:** `PROP_CAVALO_TROIA`, `PROP_PORTAO_TROIA`, `PROP_CORDA_FUGA`, `PROP_NAVIO_01`, `PROP_MASTRO_01`.

**Direção de arte e luz:** Idade do Bronze mediterrânea: muralhas monumentais em alvenaria, madeira e bronze; calor cobre/fogo, fachos e amanhecer na praia. Cavalo oco com cabeça, pescoço, quatro patas, armação interna e portinhola.

**Câmera e encenação:** 24 mm geografia → 35 mm mecanismo e portão → 24 mm partida

**Tomadas e marcação de movimento:**

- **S02-T01 · 00:07–00:9.5.50 · 24 mm travelling:** O enorme cavalo de madeira, apoiado em base de rolagem, atravessa um portão mais alto que a estrutura; troianos puxam cordas com tensão e pegada verificáveis. **Foley:** madeira e rodas.
- **S02-T02 · 00:9.5.50–00:11.5.50 · 35 mm:** Interior do cavalo: mãos distintas de guerreiros seguram travessas; Odisseu sinaliza silêncio, ombro e braço articulam com espaço real. **Foley:** respiração contida.
- **S02-T03 · 00:11.5.50–00:14 · 35 mm:** Noite: portinhola abre, guerreiros descem; um solta o fecho, outro empurra os batentes do portão em movimento completo; sombras do incêndio avançam. **Foley:** gonzos e fogo.
- **S02-T04 · 00:14–00:17 · 24 mm amplo:** Odisseu e três tripulantes embarcam; cordas se soltam, remos entram na água e a embarcação parte, deixando a cidade em chamas distante. **Foley:** remadas e mar.

**Continuidade de saída → entrada:** O elmo de crista, quando usado, é estruturalmente completo; antes de navegar, mudança de traje/arma exige ação ou corte temporal identificável. Barco fixa escala e orientação usados no mar.

**Reprovar se:** Nada de cavalo sem forma, portão pequeno demais, tropa clone ou personagens surgindo do nada.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S03 — CÍCONES E LOTÓFAGOS (00:17–00:25, 8 s)

**Narração integral (sem alterações):** “Mas a viagem começou com tragédias. Na terra dos cícones, perdeu homens em combate. Entre os lotófagos, precisou resgatar companheiros que haviam esquecido o próprio lar.”

**Elenco / figurinos:** CHAR_ODYSSEUS:viajante; CHAR_TRIPULANTE_A; CHAR_TRIPULANTE_B; CHAR_TRIPULANTE_C; CHAR_CICONE_A; CHAR_CICONE_B; CHAR_LOTOFAGO_A. **Set:** `SET_CICONES_E_ILHA_LOTUS`. **Props rastreáveis:** `PROP_NAVIO_01`, `PROP_ESCUDO_CICONE`, `PROP_FRUTO_LOTUS`, `PROP_REMO_A`.

**Direção de arte e luz:** Cícones: praia pedregosa em poeira avermelhada, fumaça distante; lótus: dunas claras, folhas espessas, vegetação dourada e águas calmas; duas locações com corte inequívoco.

**Câmera e encenação:** 35 mm retirada corporal → 50 mm rosto perdido → 35 mm resgate

**Tomadas e marcação de movimento:**

- **S03-T01 · 00:17–00:20 · 35 mm lateral:** Os cícones contra-atacam; grupo recua enquanto cobre o último homem; um companheiro cai fora de quadro, os sobreviventes alcançam o mesmo navio e o afastam da margem. **Foley:** passos, escudos, remos.
- **S03-T02 · 00:20–00:22 · 50 mm próximo:** Em outra ilha, lotófago oferece fruto ao tripulante A; ele come, deixa o remo escorregar e olha distraído a paisagem. **Foley:** som ambiente abafado.
- **S03-T03 · 00:22–00:25 · 35 mm travelling:** Odisseu agarra o antebraço do mesmo homem, ele resiste sem agressividade; ambos percorrem o trajeto até a prancha do barco, com passos que apoiam no chão. **Foley:** roupa, passos e madeira.

**Continuidade de saída → entrada:** O mesmo tripulante A come o fruto e abandona o remo; ele é reconhecível antes, durante e após ser puxado ao barco.

**Reprovar se:** Não fazer o companheiro simplesmente se teletransportar nem perder o remo no plano seguinte.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S04 — POLIFEMO (00:25–00:43, 18 s)

**Narração integral (sem alterações):** “Em uma caverna, foram aprisionados por Polifemo, um gigante de um olho só. Odisseu o embriagou, disse chamar-se Ninguém e cegou o monstro. Seus homens escaparam escondidos sob ovelhas. Mas, ao revelar seu verdadeiro nome, Odisseu provocou a vingança de Poseidon.”

**Elenco / figurinos:** CHAR_ODYSSEUS:viajante; CHAR_POLYPHEMUS; CHAR_TRIPULANTE_A; CHAR_TRIPULANTE_B; CHAR_TRIPULANTE_C; CHAR_OVELHA_A; CHAR_OVELHA_B; CHAR_OVELHA_C. **Set:** `SET_CAVERNA_POLIFEMO_E_PRAIA`. **Props rastreáveis:** `PROP_ARCO_CAVERNA`, `PROP_PEDRA_SELAMENTO`, `PROP_TACA_VINHO`, `PROP_ESTACA`, `PROP_CARNEIRO`, `PROP_NAVIO_01`.

**Direção de arte e luz:** Caverna úmida de basaltos e rochas volumétricas, entrada única legível, tochas e recipientes funcionais; olho central do ciclope, 5,5 m na escala artística; ovelhas diferenciadas.

**Câmera e encenação:** 24 mm escala inicial → 35 mm contatos → 50 mm tensão → 24 mm exterior

**Tomadas e marcação de movimento:**

- **S04-T01 · 00:25–00:28 · 24 mm baixo:** Odisseu e homens cruzam soleira real e chegam aos alimentos; Polifemo aparece com rebanho e ocupa a escala da entrada. **Foley:** ecos e ovelhas.
- **S04-T02 · 00:28–00:31 · 35 mm lateral:** Polifemo firma os pés, flexiona quadril, apoia duas mãos na pedra maior que o vão e a move até vedar a entrada inteira; poeira e escuridão reagem. **Foley:** rocha arrastando.
- **S04-T03 · 00:31–00:34 · 50 mm:** Odisseu enche taça e oferece vinho, o gigante pega com dedos em contato, bebe e adormece; Odisseu murmura a identidade 'Ninguém' na versão visual sem inserir fala adicional. **Foley:** copo e sono.
- **S04-T04 · 00:34–00:37 · 50 mm → close reação:** Marinheiros erguem estaca aquecida juntos; aproximação do olho seguida de corte para sombras/rosto gritando, sem mostrar ferimento gráfico. **Foley:** fogo e grito.
- **S04-T05 · 00:37–00:40 · 35 mm baixo:** O ciclope cego remove a mesma pedra e apalpa dorsos; homens presos sob carneiros saem pela abertura existente, um após outro. **Foley:** passos do rebanho.
- **S04-T06 · 00:40–00:43 · 24 mm reverso:** No navio em fuga, Odisseu proclama seu nome; Polifemo estende braços em súplica a Poseidon, o mar passa de claro a escuro. **Foley:** vento e trovão remoto.

**Continuidade de saída → entrada:** PEDRA_SELAMENTO maior que a luz do vão e bloqueia totalmente a passagem; só a ação posterior de removê-la permite fuga sob os carneiros. Mesma entrada e posição durante toda a sequência.

**Reprovar se:** Sem mini-pedra ou pedra atravessando o arco; sem gore explícito; não usar gestos de empurrar sem contato físico.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S05 — ÉOLO E LESTRIGÕES (00:43–00:53, 10 s)

**Narração integral (sem alterações):** “Éolo lhe entregou um saco contendo os ventos perigosos. Seus homens o abriram por engano, afastando a frota de Ítaca. Depois, gigantes lestrigões destruíram quase todos os navios.”

**Elenco / figurinos:** CHAR_ODYSSEUS:viajante; CHAR_AIOLOS; CHAR_TRIPULANTE_A; CHAR_TRIPULANTE_B; CHAR_LESTRIGAO_A; CHAR_LESTRIGAO_B. **Set:** `SET_NAVIO_VENTOS_PORTO_LESTRIGOES`. **Props rastreáveis:** `PROP_SACO_VENTOS`, `PROP_NAVIO_01`, `PROP_NAVIO_FROTA`, `PROP_ROCHAS_GIGANTES`.

**Direção de arte e luz:** Sala de Éolo com painéis de madeira e têxteis, depois proa à vista de Ítaca; porto estreito com penhascos monumentais e múltiplos navios realmente distribuídos no espaço.

**Câmera e encenação:** 50 mm entrega → 24 mm vista aérea do porto → 35 mm fuga

**Tomadas e marcação de movimento:**

- **S05-T01 · 00:43–00:45 · 50 mm:** Éolo entrega saco de couro fechado, Odisseu recebe o peso com as duas mãos e o prende junto à vela. **Foley:** couro e nó.
- **S05-T02 · 00:45–00:47 · 35 mm:** Ítaca surge ao longe; com o herói adormecido, tripulante B afrouxa o nó, confunde o conteúdo e abre o saco. **Foley:** amarra soltando.
- **S05-T03 · 00:47–00:49 · 24 mm:** A vela infla violentamente, mastros e corpos inclinam; embarcação muda de rumo e Ítaca desaparece ao horizonte. **Foley:** vendaval.
- **S05-T04 · 00:49–00:51 · 24 mm aéreo:** Vista superior do porto: gigantes lestrigões em posições distintas lançam pedregulhos que destroem navios aprisionados; pedras colidem com casco/água. **Foley:** madeira quebrando.
- **S05-T05 · 00:51–00:53 · 35 mm proa:** O único navio próximo à passagem usa remos e leme para escapar, deixando a frota destruída atrás. **Foley:** remadas apressadas.

**Continuidade de saída → entrada:** A amarração do saco passa da mão de Éolo à de Odisseu; ao abrir, corda e boca se movem fisicamente. Navio de Odisseu fica na saída do porto.

**Reprovar se:** Vento não é poeira genérica; mostrar por vela, cordas, água, roupas e direção do navio; gigantes não diminuem de tamanho.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S06 — CIRCE (00:53–01:04, 11 s)

**Narração integral (sem alterações):** “Na ilha de Circe, seus companheiros foram transformados em porcos. Protegido por Hermes, Odisseu resistiu à magia e conseguiu libertá-los. Mas, antes de continuar, recebeu uma ordem terrível.”

**Elenco / figurinos:** CHAR_ODYSSEUS:viajante; CHAR_CIRCE; CHAR_HERMES; CHAR_TRIPULANTE_A; CHAR_TRIPULANTE_B. **Set:** `SET_CIRCE_PALACIO_BOSQUE`. **Props rastreáveis:** `PROP_COPA_CIRCE`, `PROP_ERWA_MOLY`, `PROP_PORTA_PALACIO`, `PROP_MANTO_CIRCE`.

**Direção de arte e luz:** Palácio doméstico micênico com vigas de madeira, jardins verdes e cobre envelhecido; magias como deformações volumétricas coerentes e mudança luminosa, sem corte substituindo personagem.

**Câmera e encenação:** 35 mm distribuição → 50 mm transformação e desafio

**Tomadas e marcação de movimento:**

- **S06-T01 · 00:53–00:55 · 35 mm:** Circe oferece taça ao tripulante A; ele bebe e sente fraqueza, mantendo a mesma posição de pés. **Foley:** taça tilintando.
- **S06-T02 · 00:55–00:57.5.50 · 50 mm fixo:** Transformação contínua de anatomia/tecido: corpo reduz e assume forma de porco; a taça cai, demais homens reagem. **Foley:** cerâmica no piso.
- **S06-T03 · 00:57.5.50–00:59.5.50 · 50 mm:** Em bosque adjacente, Hermes entrega planta moly a Odisseu; o herói segura pelo caule e avança. **Foley:** folhas e vento.
- **S06-T04 · 00:59.5.50–01:1.5.50 · 50 mm duas pessoas:** Circe lança encantamento; luz envolve Odisseu sem alterar seu rig, expressão de Circe passa de domínio a espanto. **Foley:** sopro mágico contido.
- **S06-T05 · 01:1.5.50–01:04 · 35 mm de grupo:** Odisseu exige libertação; marujos retornam à forma humana e se reconhecem; Circe indica a rota sombria em continuidade gestual. **Foley:** suspense da próxima viagem.

**Continuidade de saída → entrada:** O tripulante A mantém identidade, posição e escala durante transformação; peças de roupa transformam-se ou caem com gravidade. Hera/Hermes entra fisicamente em trecho separado.

**Reprovar se:** Não gerar porco sobreposto à foto do homem; metamorfose visível em volume, sem atravessar chão.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S07 — MUNDO DOS MORTOS (01:04–01:14, 10 s)

**Narração integral (sem alterações):** “Ele precisou descer aos limites do mundo dos mortos. Ali, Tirésias revelou os perigos restantes. Odisseu também encontrou a própria mãe, mas não conseguiu abraçá-la.”

**Elenco / figurinos:** CHAR_ODYSSEUS:viajante; CHAR_TIRESIAS; CHAR_ANTICLEIA. **Set:** `SET_COSTA_HADES`. **Props rastreáveis:** `PROP_NAVIO_01`, `PROP_LAMPADEIRA_RITUAL`.

**Direção de arte e luz:** Costa brumosa do mundo dos mortos, água sem brilho, névoa volumétrica, rochas com textura fria e luminosidade azul acinzentada; espíritos translucentes com volume e oclusão justificadas.

**Câmera e encenação:** 24 mm chegada → 50 mm revelação → 85 mm desamparo

**Tomadas e marcação de movimento:**

- **S07-T01 · 01:04–01:06 · 24 mm:** Proa penetra neblina; Odisseu desce em costa sombria por apoio de pedra real, observa figuras distantes. **Foley:** onda imóvel e vento.
- **S07-T02 · 01:06–01:09 · 50 mm dois planos:** Tirésias emerge sob luz fria e ergue um braço para advertir; Odisseu desacelera e inclina o rosto para ouvi-lo. **Foley:** voz espectral ambiente, sem fala adicional.
- **S07-T03 · 01:09–01:12 · 50 mm frontal:** Anticleia surge à distância reconhecível como mãe; Odisseu caminha dois passos e estende braços, lágrimas discretas. **Foley:** tema de cordas.
- **S07-T04 · 01:12–01:14 · 85 mm mãos/rosto:** As mãos atravessam o volume translúcido da mãe; ele para, dedos sem apoio, baixa os ombros; névoa dissolve para espuma da próxima cena. **Foley:** silêncio.

**Continuidade de saída → entrada:** Anticleia não ganha corpo sólido; mãos de Odisseu atravessam a silhueta etérea por mudança de estado mágico explicitada, não falha de colisão.

**Reprovar se:** Sem figurantes espectrais idênticos preenchendo quadro; sem paisagem aleatória reciclada.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S08 — SEREIAS (01:14–01:25, 11 s)

**Narração integral (sem alterações):** “Depois vieram as sereias. Seu canto atraía navegantes para a morte. Odisseu pediu para ser amarrado ao mastro, enquanto seus homens remavam com os ouvidos protegidos.”

**Elenco / figurinos:** CHAR_ODYSSEUS:viajante; CHAR_TRIPULANTE_A; CHAR_TRIPULANTE_B; CHAR_TRIPULANTE_C; CHAR_SEREIA_A; CHAR_SEREIA_B. **Set:** `SET_ESTREITO_SEREIAS`. **Props rastreáveis:** `PROP_NAVIO_01`, `PROP_MASTRO_01`, `PROP_CORDAS_MASTRO`, `PROP_CERA_AUDITIVA`, `PROP_REMOS`.

**Direção de arte e luz:** Rochedos claros, mar ondulado e aves marinhas; sereias com morfologia própria inspirada no imaginário grego antigo, podendo ter traços de ave, não clones de nadadoras com cauda.

**Câmera e encenação:** 35 mm mastreação → 85 mm olhos → 24 mm navegação

**Tomadas e marcação de movimento:**

- **S08-T01 · 01:14–01:17 · 35 mm médio:** Dois homens colocam cera nos ouvidos e passam cordas em volta do peito de Odisseu, dão nós no mastro enquanto ele se mantém imóvel. **Foley:** cera e atrito de corda.
- **S08-T02 · 01:17–01:20 · 50 mm → 85 mm:** Duas sereias distintas cantam sobre rochedos em planos físicos diferentes; o mar ganha reverberação sonora; olhos de Odisseu mudam ao ouvi-las. **Foley:** vocalizações originais sem letra.
- **S08-T03 · 01:20–01:22 · 50 mm lateral:** O herói tenta inclinar o corpo, cordas tensionam e impedem deslocamento, mãos e costelas reagem à resistência. **Foley:** corda tensionada.
- **S08-T04 · 01:22–01:25 · 24 mm aberto:** Remadores não olham para o chamado e mantêm remadas fora de fase; o navio passa e as sereias recuam em distância. **Foley:** remadas e canto sumindo.

**Continuidade de saída → entrada:** Cordas contornam o corpo e se prendem ao mastro real; mãos dos tripulantes levam cera aos próprios ouvidos antes da travessia.

**Reprovar se:** Corda não atravessa manto/corpo; sem voz da sereia como narração concorrente nem canto com palavras protegidas.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S09 — CILA E CARÍBDIS (01:25–01:36, 11 s)

**Narração integral (sem alterações):** “Em um estreito mortal, precisou escolher entre Caríbdis, um redemoinho gigantesco, e Cila, um monstro de seis cabeças. O navio escapou, mas seis marinheiros morreram.”

**Elenco / figurinos:** CHAR_ODYSSEUS:viajante; CHAR_TRIPULANTE_A; CHAR_TRIPULANTE_B; CHAR_TRIPULANTE_C; CHAR_TRIPULANTE_D; CHAR_TRIPULANTE_E; CHAR_TRIPULANTE_F; CHAR_SCYLLA. **Set:** `SET_ESTREITO_SCYLLA_CHARYBDIS`. **Props rastreáveis:** `PROP_NAVIO_01`, `PROP_REMOS`, `PROP_REDEMOINHO_CHARYBDIS`.

**Direção de arte e luz:** Canal rochoso 3D com Cila presa à falésia de um lado e Caríbdis no outro; seis cabeças/pescoços de Cila com anatomia própria; água gerada por força circular coerente.

**Câmera e encenação:** 24 mm aéreo geografia → 35 mm bordo → 50 mm perda

**Tomadas e marcação de movimento:**

- **S09-T01 · 01:25–01:27 · 24 mm drone virtual:** Plano aéreo orienta direita/esquerda e deixa claro o perigo: voragem de água de um lado, Cila presa ao outro. **Foley:** ressaca grave.
- **S09-T02 · 01:27–01:29 · 35 mm proa:** Odisseu ordena manobra junto à falésia; remos corrigem trajetória do navio para evitar o vórtice. **Foley:** gritos de comando não inteligíveis.
- **S09-T03 · 01:29–01:33 · 35 mm câmera embarcada:** Seis pescoços emergem em tempos alternados; cada cabeça agarra um dos seis marinheiros identificados, retirando-os de vista sem gore. Odisseu tenta alcançar um. **Foley:** impactos, rugidos.
- **S09-T04 · 01:33–01:36 · 50 mm fixo:** Navio sai do estreito; espaços vazios no convés e remo abandonado evidenciam perda; Odisseu baixa a mão sem tocar ninguém. **Foley:** música recua.

**Continuidade de saída → entrada:** Definir lados fixos do estreito por mapa de cena; seis homens saem do convés, deixando seis posições vazias; os que sobrevivem mantêm identidades.

**Reprovar se:** Não inverter lados do canal entre cortes ou inserir sereias no lugar do monstro.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S10 — O ÚLTIMO NAVIO (01:36–01:48, 12 s)

**Narração integral (sem alterações):** “Famintos, seus homens desobedeceram à ordem de não tocar nos rebanhos sagrados do Sol. Zeus destruiu o último navio com um raio. Todos morreram, menos Odisseu.”

**Elenco / figurinos:** CHAR_ODYSSEUS:viajante; CHAR_TRIPULANTE_A; CHAR_TRIPULANTE_B; CHAR_TRIPULANTE_C. **Set:** `SET_TRINACIA_TEMPESTADE`. **Props rastreáveis:** `PROP_REBANHO_SOL`, `PROP_FOGO_SACRIFICIO`, `PROP_NAVIO_01`, `PROP_MASTRO_01`, `PROP_DESTROCO`.

**Direção de arte e luz:** Sol forte em pradaria costeira, bois corpóreos e sombras reais; depois nuvens de tempestade, clarão que ilumina material e água volumétrica. Metáfora visual de solidão no mar.

**Câmera e encenação:** 35 mm transgressão → 24 mm naufrágio → 50 mm sobrevivência

**Tomadas e marcação de movimento:**

- **S10-T01 · 01:36–01:39 · 35 mm lateral:** Tripulantes cansados observam o rebanho sagrado e um deles inicia o sacrifício, enquanto Odisseu está afastado. **Foley:** gado e vento.
- **S10-T02 · 01:39–01:41 · 50 mm rosto:** Odisseu retorna, encontra restos do ritual e recua em horror; reação do rosto distinta de raiva genérica. **Foley:** música de prenúncio.
- **S10-T03 · 01:41–01:44 · 24 mm amplo:** No mar, céu fecha; um raio atinge o mastro e ilumina casco, velas e água; mastreação se quebra na ligação física. **Foley:** trovão.
- **S10-T04 · 01:44–01:46 · 35 mm subaquático:** Navio parte; homens se perdem nas ondas; Odisseu cai e gira sob a água, olhos abertos, busca madeira visível. **Foley:** água abafada.
- **S10-T05 · 01:46–01:48 · 50 mm abrindo a 24 mm:** Odisseu sobe ao fragmento do próprio barco, exausto; plano amplo enfatiza ausência de companheiros. **Foley:** som do oceano isolado.

**Continuidade de saída → entrada:** Destruição vem depois do sacrifício; o protagonista não aparece em dois pontos simultâneos do mesmo navio. Destroço vem do casco apresentado.

**Reprovar se:** Não mostrar Odisseu comandando o sacrifício; sem mortes gráficas ou objetos desaparecendo por corte.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S11 — CALIPSO (01:48–01:59, 11 s)

**Narração integral (sem alterações):** “Ele chegou à ilha de Calipso, que o manteve ali por sete anos e lhe ofereceu a imortalidade. Mas Odisseu só desejava voltar para Penélope e Telêmaco.”

**Elenco / figurinos:** CHAR_ODYSSEUS:viajante; CHAR_CALYPSO; CHAR_HERMES. **Set:** `SET_OGIGIA_CALYPSO`. **Props rastreáveis:** `PROP_ROCHA_OGIGIA`, `PROP_JANGADA`, `PROP_CORDA_JANGADA`, `PROP_MACHADO_MADEIRA`.

**Direção de arte e luz:** Ilha tropical mediterrânea idealizada, vegetação exuberante, cascatas e tecidos claros; luz agradável que se transforma em melancolia nas expressões do herói, sem cenário opressor artificial.

**Câmera e encenação:** 35 mm chegada → 50 mm tensão emocional → 24 mm partida

**Tomadas e marcação de movimento:**

- **S11-T01 · 01:48–01:50 · 35 mm baixo:** Calipso encontra Odisseu exausto na costa, toca seu ombro e o ajuda a respirar; o mesmo corpo é reconhecível. **Foley:** mar e folhas.
- **S11-T02 · 01:50–01:52 · 50 mm lento:** Passagem do tempo em mesmo ponto da ilha: estações e barba/tecidos evoluem com continuidade; Odisseu olha para além da baía. **Foley:** tema repetido com variação.
- **S11-T03 · 01:52–01:54 · 50 mm dois rostos:** Calipso oferece a mão em convite à vida imortal; Odisseu hesita e se volta ao horizonte como resposta. **Foley:** silêncio emocional.
- **S11-T04 · 01:54–01:56 · 35 mm:** Hermes chega com decisão divina; Calipso baixa a mão, Odisseu reage com esperança contida. **Foley:** vento.
- **S11-T05 · 01:56–01:59 · 24 mm travelling:** Odisseu fixa tábuas e cordas de uma jangada funcional; empurra para a água, sobe e afasta-se da ilha. **Foley:** machado, corda, ondas.

**Continuidade de saída → entrada:** Passagem de sete anos sinalizada por desgaste/novas vestes e dissolução sazonal breve, mantendo mesmo rosto. Jangada construída por trabalho real com peças persistentes.

**Reprovar se:** Não insinuar que a ninfa acorrentou fisicamente Odisseu; o cativeiro tem natureza mítica e emocional.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S12 — FEÁCIOS E ÍTACA (01:59–02:10, 11 s)

**Narração integral (sem alterações):** “Depois de outra tempestade, foi acolhido pelos feácios. Ao conhecerem sua história, eles o levaram de navio até Ítaca. Vinte anos depois, ele estava em casa.”

**Elenco / figurinos:** CHAR_ODYSSEUS:viajante; CHAR_NAUSICAA; CHAR_ALCINOUS; CHAR_PHAEACIAN_A; CHAR_PHAEACIAN_B; CHAR_PHAEACIAN_C. **Set:** `SET_ESQUERIA_E_COSTA_ITACA`. **Props rastreáveis:** `PROP_NAVIO_FEACIO`, `PROP_PRESENTES_FEACIOS`, `PROP_VELO_VIAGEM`.

**Direção de arte e luz:** Esquéria com praia, vegetação, navegação e salão com tapetes em cores próprias; Ítaca rochosa ao amanhecer, presentes em ânforas/tecidos/baús; não inserir cais artificial.

**Câmera e encenação:** 35 mm acolhimento → 50 mm banquete → 24 mm viagem/chegada → 50 mm despertar

**Tomadas e marcação de movimento:**

- **S12-T01 · 01:59–02:01 · 35 mm praia:** Nausícaa encontra Odisseu cansado na praia, mantém distância respeitosa e sinaliza proteção. **Foley:** folhas e mar.
- **S12-T02 · 02:01–02:03 · 50 mm salão:** Palácio feácio: Alcínoo ouve o herói narrar, marinheiros distintos preparam presentes e embarcação. **Foley:** ambiente de banquete.
- **S12-T03 · 02:03–02:06 · 24 mm travessia:** Navio avança sob estrelas; Odisseu adormece no convés; feácios remam coordenados sem gestos clones. **Foley:** remos e vento.
- **S12-T04 · 02:06–02:08 · 35 mm lateral:** Tripulação levanta o herói adormecido com apoio dos ombros/pernas, deixa-o na areia com os presentes e volta à mesma embarcação. **Foley:** passos sobre areia.
- **S12-T05 · 02:08–02:10 · 50 mm olhos/mãos:** Odisseu desperta, toca o solo, vê a paisagem turva e se orienta sem reconhecimento imediato; preparar encontro com Atena. **Foley:** acorde de retorno.

**Continuidade de saída → entrada:** Feácios depositam **Odisseu ainda adormecido** com presentes e retornam ao barco. Ele acorda sem reconhecer de imediato a ilha devido à névoa; não o mostrar desembarcando acordado por passarela.

**Reprovar se:** Sem guerreiro de capacete em Ítaca; não fazer feácios e homens de Troia iguais.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S13 — PALÁCIO TOMADO (02:10–02:25, 15 s)

**Narração integral (sem alterações):** “Mas seu palácio estava ocupado por pretendentes que queriam se casar com Penélope e tomar o reino. Ela resistia. Seu filho Telêmaco, agora adulto, também procurava notícias do pai.”

**Elenco / figurinos:** CHAR_PENELOPE; CHAR_TELEMACHUS; CHAR_ANTINOOS; CHAR_EURYMACHOS; CHAR_ODYSSEUS:viajante; CHAR_ATHENA; CHAR_EUMAEUS; CHAR_PRETENDENTE_A; CHAR_PRETENDENTE_B. **Set:** `SET_PALACIO_TEAR_CAMINHO_EUMEUS`. **Props rastreáveis:** `PROP_TEAR_PENELOPE`, `PROP_MANTA_TEAR`, `PROP_TACA_BRONZE`, `PROP_PORTA_SALAO`.

**Direção de arte e luz:** Palácio micênico com mapa navegável, mesas e travessas; Penélope veste linho marfim com faixa azul violeta, Telêmaco capa azul-acinzentada. A noite do tear tem fonte de luz própria.

**Câmera e encenação:** 24 mm estabelecimento → 50 mm tecelagem/decisão → 35 mm disfarce/caminho

**Tomadas e marcação de movimento:**

- **S13-T01 · 02:10–02:13 · 24 mm:** Plano amplo de pretendentes ocupando mesas e consumindo comida; Antínoo arroga o comando enquanto Eurímaco o influencia com gesto discreto. **Foley:** taças e riso.
- **S13-T02 · 02:13–02:15.5.50 · 50 mm:** Penélope entra firme e recusa um gesto invasivo; olhos atentos, postura sólida, sem choro automático. **Foley:** ambiente baixa.
- **S13-T03 · 02:15.5.50–02:18 · 85 mm mãos:** Tear de dia: lançadeira passa por fios, mãos de Penélope acrescentam parte do tecido com geometria intacta. **Foley:** madeira e fios.
- **S13-T04 · 02:18–02:20 · 50 mm mãos/rosto:** À noite, a mesma Penélope desmancha os fios no mesmo local; lunar frio contrasta com luz anterior. **Foley:** cordas suaves.
- **S13-T05 · 02:20–02:22 · 35 mm:** Telêmaco retorna após procurar notícias; encara o salão, evitando confronto prematuro, e se volta para o exterior. **Foley:** passos.
- **S13-T06 · 02:22–02:25 · 35 mm lateral:** Em costa externa, Atena transforma Odisseu em mendigo; mudança facial/roupa gradual sem trocar identidade; ele caminha objetivamente até a cabana de Eumeu. **Foley:** vento e tecidos.

**Continuidade de saída → entrada:** Tecido cresce de dia e é desfeito à noite pela mesma trama no mesmo tear; Atena fornece disfarce antes da chegada à cabana de Eumeu.

**Reprovar se:** Penélope não é figurante chorosa; sem repetição de grupo de pretendentes com mesma face.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S14 — RECONHECIMENTOS (02:25–02:37, 12 s)

**Narração integral (sem alterações):** “Disfarçado de mendigo, Odisseu reencontrou Telêmaco e preparou a vingança. Seu velho cão Argos o reconheceu. Mais tarde, a ama Euricleia descobriu sua identidade pela cicatriz.”

**Elenco / figurinos:** CHAR_ODYSSEUS:mendigo; CHAR_TELEMACHUS; CHAR_EUMAEUS; CHAR_ATHENA; CHAR_ARGOS; CHAR_EURYKLEIA. **Set:** `SET_CABANA_EUMEUS_ACESSO_PALACIO`. **Props rastreáveis:** `PROP_BACIA_BRONZE`, `PROP_AGUA_BACIA`, `PROP_CICATRIZ_COXA`, `PROP_PORTAO_PALACIO`.

**Direção de arte e luz:** Cabana do pastor em madeira, palha e barro; caminho até o palácio e entrada com cão envelhecido; bacia de bronze com luz de lareira. Ternura baseada em posturas e contato.

**Câmera e encenação:** 50 mm reencontro → 85 mm Argos → 50 mm cicatriz

**Tomadas e marcação de movimento:**

- **S14-T01 · 02:25–02:28 · 50 mm dois rostos:** Atena restaura aparência de Odisseu na cabana; Telêmaco percebe semelhança, aproxima-se e abraça o pai; Eumeu permanece no mesmo ambiente. **Foley:** respiração e tema de reencontro.
- **S14-T02 · 02:28–02:31 · 85 mm olhar do cão:** Corte de deslocamento ao portão do palácio: Argos, idoso e de pelagem manchada, ergue a cabeça e reconhece o mendigo; este controla lágrima e segue. **Foley:** respiração do animal.
- **S14-T03 · 02:31–02:34 · 50 mm mãos/rosto:** Euricleia inclina-se e lava as pernas do visitante na bacia; descobre cicatriz alta na coxa, interrompe a ação, expressa surpresa. **Foley:** água e metal.
- **S14-T04 · 02:34–02:37 · 85 mm dedos e olhos:** Odisseu segura delicadamente a mão de Euricleia e pede silêncio com olhar; ela recompõe a expressão sem abandonar o objeto. **Foley:** silêncio.

**Continuidade de saída → entrada:** Atena desfaz temporariamente o disfarce de Odisseu para reconhecimento do filho; ao ir ao palácio ele está novamente disfarçado. Cicatriz no alto da coxa, ligada a ferida antiga de javali.

**Reprovar se:** Não incluir o cão em sala interna nem fazer Euricleia reconhecer por rosto antes da cicatriz.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S15 — O ARCO E A LUTA (02:37–02:50, 13 s)

**Narração integral (sem alterações):** “Penélope anunciou uma prova: quem armasse o arco de Odisseu e atravessasse doze machados com uma flecha poderia desposá-la. Todos falharam. O mendigo conseguiu. Era o rei. Com Telêmaco, derrotou os pretendentes.”

**Elenco / figurinos:** CHAR_ODYSSEUS:mendigo; CHAR_TELEMACHUS; CHAR_ANTINOOS; CHAR_EURYMACHOS; CHAR_PRETENDENTE_A; CHAR_PRETENDENTE_B. **Set:** `SET_PALACIO_SALAO`. **Props rastreáveis:** `PROP_ARCO_REAL`, `PROP_FLECHA_REAL`, `PROP_MACHADOS_12`, `PROP_ESCUDO_PRETENDENTE`, `PROP_TACA_BRONZE`.

**Direção de arte e luz:** Mesmo salão do prólogo, mesmas marcas do arco, das mesas e do piso. Pretendentes vestem túnicas e mantos nobres diferentes; 12 machados reais alinhados na profundidade.

**Câmera e encenação:** 85 mm mãos → 35 mm alinhamento → 35 mm combate espacial

**Tomadas e marcação de movimento:**

- **S15-T01 · 02:37–02:40 · 50 mm mãos e reações:** Duas tentativas distintas fracassam; Antínoo força o arco e Eurímaco desvia o olhar, ambos visivelmente contrariados no mesmo salão. **Foley:** madeira tensa.
- **S15-T02 · 02:40–02:42 · 85 mm close:** Odisseu recebe o mesmo arco da S01, posiciona pés e arma a corda com facilidade mecânica e tensão corporal real. **Foley:** corda.
- **S15-T03 · 02:42–02:44 · 35 mm em eixo:** Lançamento: flecha avança na linha formada pelos doze olhais de machados, com trajetória contínua, sai pelo último. **Foley:** disparo.
- **S15-T04 · 02:44–02:46 · 50 mm reverso:** Antínoo reconhece perigo; Odisseu retira o capuz e revela firmeza do rosto; Telêmaco vem para seu lado. **Foley:** silêncio e respiro.
- **S15-T05 · 02:46–02:49 · 35 mm ação:** Combate de ações legíveis: Odisseu atinge um adversário, bloqueia outro; Telêmaco cobre passagem, os pretendentes recuam para corredor real. **Foley:** impactos controlados.
- **S15-T06 · 02:49–02:50 · 50 mm estável:** Fim do confronto: salão vazio de agressões, arco baixo, Odisseu exausto; preservar limites de espaço para próximo corte. **Foley:** respiração.

**Continuidade de saída → entrada:** Retomar instante da S01 sem reproduzir a tomada anterior como preenchimento: mesmo arco, Odisseu agora executa a ação até a consequência. Telêmaco entra pelo eixo conhecido do salão.

**Reprovar se:** A flecha não deve atravessar metal sólido; deve cruzar os orifícios geometricamente alinhados. Combate sem gore e sem teletransporte.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

### S16 — PENÉLOPE, LAERTES E PAZ (02:50–03:05, 15 s)

**Narração integral (sem alterações):** “Penélope ainda duvidou, até ele revelar o segredo da cama construída sobre uma oliveira viva. Ela o reconheceu. Odisseu reencontrou o pai, Laertes, e Atena encerrou a vingança. Depois de vinte anos, finalmente estava em casa. Tem uma explicação.”

**Elenco / figurinos:** CHAR_ODYSSEUS:revelado; CHAR_PENELOPE; CHAR_TELEMACHUS; CHAR_LAERTES; CHAR_ATHENA; CHAR_PARENTE_PRETENDENTE_A. **Set:** `SET_QUARTO_OLIVEIRA_POMAR_PAZ`. **Props rastreáveis:** `PROP_LEITO_OLIVEIRA`, `PROP_TRONCO_OLIVEIRA`, `PROP_LANCA_ATENA`, `PROP_ARMAS_PAZ`.

**Direção de arte e luz:** Quarto de pedra/madeira ligado ao tronco vivo da oliveira; manto de Penélope marfim-violeta, Odisseu sem elmo e com rosto revelado; pomar de Laertes e paisagem de Ítaca com luz de amanhecer dourado.

**Câmera e encenação:** 50 mm prova íntima → 85 mm mãos e abraço → 35 mm pai → 24 mm panorama final

**Tomadas e marcação de movimento:**

- **S16-T01 · 02:50–02:53 · 50 mm → 85 mm:** Penélope ordena mover a cama para testar o homem; Odisseu reage ao impossível, toca o poste e descreve seu encaixe no tronco vivo, mostrado em detalhe estrutural. **Foley:** madeira e silêncio.
- **S16-T02 · 02:53–02:56 · 50 mm estável:** Penélope compreende, aproxima-se em dois passos, mãos tocam as costas dele e abraço envolve ambos com tecido reagindo ao contato. **Foley:** tema de cordas.
- **S16-T03 · 02:56–02:58.5.50 · 50 mm duas pessoas:** No pomar, Laertes idoso reconhece o filho; Odisseu aproxima-se e o abraça com diferença clara de porte e idade. **Foley:** vento nas árvores.
- **S16-T04 · 02:58.5.50–03:01 · 35 mm amplo:** Parentes de pretendentes avançam com armas; Atena aparece e interrompe a ofensiva, os braços abaixam as lanças com consequência legível. **Foley:** metal cessando.
- **S16-T05 · 03:01–03:05 · 24 mm afastamento:** Ao amanhecer, Odisseu, Penélope e Telêmaco olham Ítaca do terraço; vento move mantos, câmera recua até ilha e mar. Fade com a narração 'Tem uma explicação.' **Foley:** tema final, fade.

**Continuidade de saída → entrada:** O leito não pode ser movido: seu poste integra o tronco ainda enraizado. No confronto final Atena intervém de modo claro e armas baixam. Assinatura pertence ao áudio, não a um letreiro inesperado.

**Reprovar se:** Não trocar o quarto por cenário genérico; não comprimir abraço em corte instantâneo; paz deve ser uma ação visível e não apenas fade.

**Estado:** NÃO APROVADA — depende de playblast e QC visual/físico/narrativo.

## C. Entrega e contrato de QC

1. **Pré-produção:** travar model sheets completos (frente, perfil, 3/4 e costas), rigs, figurinos, IDs, props, escala e geografia do set antes do primeiro render.
2. **Blocking:** aprovar poses-chave, trajetória e espaço ocupado com render simplificado; o personagem pisa/segura/apoia em superfícies e objetos reais. Escolher o que se vê em 9:16 sem cortar rosto/ação.
3. **Animação/polimento:** rig, IK de apoio, contatos sincronizados, resposta de tecidos, expressão natural, transições entre tomadas e verificação de materiais/iluminação. Verificar as 16 sequências e os 74 planos.
4. **Master de áudio:** a voz Rasalgethi é gerada via interface Google AI Studio sem API paga; o áudio final, **quando existir**, determina os cortes. Se durar mais de 185 s, ampliar a duração ou reescrever editorialmente com aprovação; não acelerar de modo antinatural.
5. **Render:** primeiro playblasts e QCs em baixa resolução; somente planos aprovados vão a 2160×3840/60 FPS. Separar entrega "4K nativo" de qualquer upscale. H.264/H.265 + AAC 48 kHz estéreo, taxa de bits adequada.
6. **Revisão integral:** assistir sem som (narrativa visual) e com som (sincronismo), checar atravessamentos, telas pretas, cópias de personagens, trocas de roupa, objetos sem dono, contraste/legendas, ritmo, final e créditos.
7. **Publicação:** bloqueada por padrão; revisão de qualidade/controle editorial e aprovação humana do arquivo final antes de agendar.

### Regras adicionais de aceitação
- Nada de motion de imagens, slideshow, animação por movimentos de câmera apenas, sobreposições sem espaço real ou clipes reaproveitados como ação diferente.
- Em S02 o cavalo passa por portão e abre porta por dentro; em S04 a pedra veda a caverna; em S08 cordas realmente prendem; em S09 seis perdas são observáveis; em S15 o arco é o mesmo e a flecha cruza realmente os doze machados; em S16 o leito não se move e os três atos finais têm consequência visível.
- Roteiro é um contrato visual: toda nova tomada deve declarar quem está, o que faz, seu ponto de partida, seu destino e o estado que deixa ao plano seguinte.
- **Nota de produção:** 446 palavras distribuídas em 185 segundos (média 2,41 palavras/s, aproximadamente 145 palavras/min), mas S03 exige ~195 palavras/min; é preciso testar a locução e, se necessário, redistribuir alguns segundos entre cenas. Nenhum cálculo de tempo substitui a medição do áudio.

## D. Referências literárias para conformidade histórica/narrativa
- Homero, *Odisseia*, canto XIII: https://beta.perseus.tufts.edu/urn:cts:greekLit:tlg0012.tlg002.hobbes1667molesworth-eng2/book:13/
- Homero, *Odisseia*, canto XIX: https://beta.perseus.tufts.edu/urn:cts:greekLit:tlg0012.tlg002.hobbes1667molesworth-eng2/book:19/
- Odisseia, cantos XXIII–XXIV: https://www.sparknotes.com/lit/odyssey/overview12/
- Padrão-mestre do próprio projeto: `odyssey_v8/PADRAO_MESTRE_TUE_ANIMACAO.md`.

**FIM DO ROTEIRO DE DIREÇÃO · VERSÃO PARA PRODUÇÃO (NÃO RENDERIZADA).**
