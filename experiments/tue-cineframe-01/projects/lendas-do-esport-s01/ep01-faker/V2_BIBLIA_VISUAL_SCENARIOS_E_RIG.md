# EP01 FAKER — DIREÇÃO DE ARTE E AMBIENTES V2 (REGRA BLOQUEANTE)

**REVISÃO EDITORIAL:** o piloto V1 de 20s foi REPROVADO por baixa fidelidade facial, corpo esquemático, espaços rasos e acting limitado. O padrão de arte aprovado para o personagem é a **ficha original 2D**, NÃO o rig procedural V1.

**Ficha visual canônica:** Google Drive https://drive.google.com/file/d/163C38f5RBR1mtf7r8z9FBYuQfrJubQnF/view
**Vídeo enviado pelo usuário como referência FUNCIONAL (não para copiar):** `1002358369.mp4`, 96,68s, 720×1280, 30fps, somente análise local. Não colocar esse MP4 nem seus fotogramas em GitHub público, não redistribuí-lo e não reutilizar suas marcas, publicidade, imagens de gameplay ou arte de terceiros.
**Laboratório separado:** https://drive.google.com/drive/folders/1nBTh0Jbx4_qhxm2ttFIH3IsKVLN_h49G
**Rejeitados segregados:** https://drive.google.com/drive/folders/1rjFZslg1k_leiU2tlI4nnxX7fHIyLWeL
**Novos assets V2 (ainda não gerados):** https://drive.google.com/drive/folders/1ZcO0TNjW8Cf18BKRXHfqY8qJc_6SoAgE

## Leitura do vídeo de referência do usuário

- Linguagem vertical editorial, espaço de arena escura azul-marinho com trilhas luminosas em perspectiva, arquibancada em profundidade e foco no atleta.
- Câmera que se desloca dentro de um cenário com chão, luz e volumes espaciais coerentes.
- Gráficos de estatísticas, placares e mapas são parte da cenografia e acompanham o assunto; não são overlays alheios à cena.
- Estrutura alterna atleta atuando, ações de jogo mostradas como diagramas, estatísticas comparativas e comemoração.
- Isso NÃO autoriza reproduzir imagens e mecânicas protegidas dos jogos. A aplicação precisa ser original, mais refinada na atuação e mais cinematográfica.

## Character lock — Faker (imutável)

O concept sheet aprova: rosto jovem adulto coreano **estilizado e identificável** (não geometria genérica), rosto esguio com queixo estreito, cabelo castanho-escuro quase preto em franja volumosa irregular, óculos pretos de armação fina com lentes retangulares arredondadas, olhos escuros expressivos, sobrancelhas definidas; silhueta esguia proporcional a ~7,5 cabeças; camiseta de e-sport preta com painéis vermelho escuro e cinza/branco, calça preta, tênis claros. NÃO alterar feições nem trocar cores entre tomadas. Não inferir que as roupas são reproduções de uniformes históricos verdadeiros; figurino é interpretação original do concept.

### Rig obrigatório em camadas (todos os componentes precisam de assets de arte COM qualidade 4K)

`HEAD_BACK`, `EAR_L`, `EAR_R`, `FACE_SHAPE`, `EYE_L`, `EYE_R`, `UPPER_LID_L`, `UPPER_LID_R`, `EYEBROWS`, `NOSE`, `MOUTH_NEUTRAL`, `MOUTH_MICROSMILE`, `HAIR_BACK`, `HAIR_FRINGE`, `GLASSES_FRAME`, `GLASSES_LENS_L`, `GLASSES_LENS_R`, `NECK`, `TORSO_FRONT`, `TORSO_BACK`, `SHOULDER_L`, `UPPER_ARM_L`, `FOREARM_L`, `HAND_L_KEYBOARD`, `SHOULDER_R`, `UPPER_ARM_R`, `FOREARM_R`, `HAND_R_MOUSE`, `HAND_L_OPEN`, `HAND_R_TROPHY`, `PELVIS`, `THIGH_L`, `SHIN_L`, `FOOT_L`, `THIGH_R`, `SHIN_R`, `FOOT_R`, `JERSEY_FABRIC`.

Rigs para **frente, 3/4, perfil**; não deformar rosto frontal para simular perfil extremo. Cada vista usa arte condizente com a ficha aprovada. O cabelo se move com amplitude controlada sem “morphing”; os óculos seguem o crânio, não flutuam; olhos e pálpebras se movem sem transformar o rosto. Pivôs e oclusões consistentes, não apenas segmentos tipo linha/oval.

### Protocolo de fidelidade

1. Converter a ficha aprovada em **arte nova separada por camadas**, preservando desenho exato e microdetalhes; os recortes pequenos da ficha NÃO são assets finais 4K. Exigir redraw autoral em resolução suficiente para close. Não redibujar o Faker como outra pessoa.
2. Renderizar close em três ângulos, expressões calma, atenção, frustração, retomada de foco e sorriso discreto; comparar diretamente com a ficha (face, óculos, franja, nariz, proporções).
3. Teste de atuação corporal: mão apoiada de fato no teclado, pulso girando mouse, ombro/peito respirando, pescoço/cabeça acompanhando foco; mão segura troféu e a borda oclui dedos corretamente; pés plantados nas poses de palco.
4. Se face ou gesto perder fidelidade, **reprovar o take e não entregar**. “Mudar a câmera” não corrige arte ruim.

## Cenários originais premium, não fundos vazios

### SET A — Sala de treino / 2013
Planta 3/4 com três planos independentes: primeiro plano de teclado/mouse/cabo de headset/mesa; plano médio com Faker sentado, monitor e cadeira; fundo com porta, paredes e prateleiras discretas; iluminação prática por monitor e luminária. Atuação: Faker ajusta cadeira, coloca headset, apoia mãos, tecla e gira para ouvir técnico. Ninguém desliza.

### SET B — Arena histórica 2013/2015/2016
Palco com piso de placas 2.5D, passarela, linha LED vermelha no chão, monitores e assentos fisicamente ancorados, arquibancadas em 3 camadas de escala com plateia de silhuetas distintas. A câmera entra por passagem lateral e muda o eixo APÓS estabelecer geografia. Troféu original genérico, sem replicar Summoner's Cup.

### SET C — Cabine da derrota de 2017
Mesmo palco da final, agora iluminação mais fria e distância entre câmera/atores menor. A tensão nasce de Faker soltar os dedos do teclado, retirar uma das mãos do mouse, baixar a cabeça e fazer uma pausa, enquanto colegas se levantam em segundo plano. Sem lágrima exagerada, sem rostos deformados ou overlay “TRISTE”.

### SET D — Segundo revés 2022
Corredor dos bastidores com portas, credenciais genéricas, reflexos controlados em piso e luz de serviço; time se aproxima e se consola por gestos completos. Não simular vídeo de transmissão real.

### SET E — Sala de análise e preparação
Parede de diagramas inventados com mapas abstratos (não UI de LoL), fichas posicionadas pelo treinador e Faker marcando rota no papel. Composições plano/contraplano com continuidade de mão e objetos. Mostrar prática coletiva e mudança de estratégia.

### SET F — Arena 2023/2024/2025
Três passagens temporais claramente distinguidas por arquitetura, escala, iluminação e cor de plateia, sem reciclar mesmo palco vazio: 2023 atmosfera quente vermelha; 2024 âmbar e azul-marinho; 2025 ouro/escarlate. Bloqueio do elenco próprio por tomada. O palco 2025 contém painel físico de marcador 1–2 > 2–2 > 3–2 com peças que deslizam sobre trilho no cenário, **não uma tela extra aleatória**.

### SET G — Galeria do legado / Hall of Legends
Arquitetura simbólica editorial com seis nichos iluminados de maneira realista, cada um contendo um ano verificável: 2013, 2015, 2016, 2023, 2024, 2025. A inscrição “Hall of Legends — 2024” é dado tipográfico factual discreto, não reprodução de logotipo oficial. Câmera acompanha Faker atravessando o espaço em animação real articulada, sem movimento de imagem fixa.

## Cinematografia

Lentes equivalentes 35mm para geografia, 50mm para interpretação, 85mm para emoção e detalhes. No retrato 9:16, pés, mão e objeto precisam permanecer no quadro quando a ação depende do contato. Regra de 180 graus, entradas/saídas contínuas, primeiro plano deve ocluir o personagem quando atravessa o espaço. Sombras de piso ancoradas no movimento das luzes práticas. Não usar zoom dramático indiscriminado: mudança de plano justificada por ação.

## Direção de elenco secundário

Companheiros de equipe ilustrados sem atribuir identidades reais não verificadas; 4 silhuetas distintas por fase (2013, 2017, 2022, 2023, 2024, 2025), técnico/assistente e pequena plateia com ao menos 6 variantes sem clones. Os figurinos do elenco mudam por período com design original; nenhum logo, rosto identificável de pessoa não indicada ou uniforme real recriado indevidamente.

## Regras de áudio

A narração Rasalgethi deve existir como WAV/MP3 original verificável, gerado com o texto V2 e duração não acelerada. Cena e legenda são remarcadas pelo áudio real. Música e SFX não mascaram fala. Se não houver Rasalgethi, não existe entrega final.

## Entrega bloqueada

MP4 2160×3840 nativo, 60 FPS, H.264/AAC, 9:16; 14 tomadas coerentes com duração final ajustada pela voz, cenários premium, material de animação realmente articulado, sem cópia do vídeo de referência, selo QC humano aprovado, Drive confirmado, link enviado aqui **somente após aprovação real**. Qualquer falha -> REPROVADO, não mostrar piloto. Sem publicação/agendamento.
