# PADRÃO CANÔNICO VISUAL — ODI SSEIA / CAVALO DE TROIA (IMUTÁVEL)

**Decisão editorial vigente — 07/11/2026:** o usuário esclareceu que a “primeira animação” a preservar é **Odisseu e o Cavalo de Troia**, o vídeo de 60 segundos já produzido, **NÃO** a primeira renderização da nova Odisséia V19/V20 e **NÃO** um novo estilo 2D genérico. A revisão deve melhorar o **modelo existente**, não criar outro.

## Fonte visual oficial (read-only)
- MP4 original: `content/media/instagram/2026-11-05/odisseu-troia/Cavalo_Troia_4K60_Meta_10h.mp4`, 60 s, 9:16, 2160×3840, 60 fps; é referência **de desenho/personagem**, não fonte obrigatória para reaproveitar texto, narração, logos ou marca d'água.
- Registro de aprovação: `content/approved/tue-2026-11-05-10-cavalo-de-troia/approval.json`.
- Referências extraídas da própria animação (NÃO geradas por IA): `odyssey_2d/reference/TROIA_2D_APROVADA_03s.jpg`, `14s.jpg`, `28s.jpg`, `43s.jpg`, `54s.jpg`.
- Fontes de trabalho alternativas: somente variantes comprovadamente idênticas ao modelo original do Cavalo de Troia, verificadas visualmente lado a lado. Não usar desenhos genéricos V19/V20 como base para o elenco.

## Identidade obrigatória do primeiro filme
- **Odisseu:** preservar a silhueta pequena e estilizada em desenho vetorial com **contorno escuro de espessura evidente**, capacete de bronze com **crista/pluma vermelha**, armadura de placas em tons de bronze e couro, **capa vermelha**, rosto e proporções reconhecíveis do primeiro vídeo. Reutilizar mesmo rosto e vestuário, modificando apenas os estados narrativos (viajante/mendigo/ferimentos) sem trocar a geometria facial.
- **Cavalo de Troia:** reaproveitar o **mesmo modelo de madeira castanha**, perfil de cavalo claramente legível, pescoço/cabeça/orelhas/crina/cauda, **quatro patas**, porta lateral, prancha/base e **rodas visíveis**. Não substituí-lo pelo cavalo poligonal simplificado da V19/V20.
- **Lúmino:** quando couber no projeto, somente a imagem/arte aprovada, jamais um robô semelhante redesenhado; não deixar que seu papel de apresentador cubra ação/narração.
- **Cenários e iluminação:** fundos desenhados em camadas, céu com gradientes crepusculares azul-petróleo, areia/ocre, sol circular amarelo-creme, torres e muralhas micênicas estilizadas, cidades e colinas em silhueta, ruas noturnas e luzes discretas; preto/castanho como contorno.
- **Tipografia:** legenda inferior limpa e legível, no máximo 2 linhas, sem multiplicação de sobreposições. Elementos históricos discretos na parte alta apenas quando realmente agregarem.
- **Não reproduzir marcas d'água** eventualmente presentes no vídeo de referência. O objetivo é a identidade do desenho, não transcrever marcas de edição.

## Único trabalho autorizado sobre o modelo
**Refinar o que existe:** reutilizar/recuperar sprites e componentes do primeiro vídeo, e criar rig 2D para segmentos de **cabeça, pescoço, tronco, ombro/braço/antebraço/mão, quadril/coxa/joelho/pé, capa**, cavalo, cordas, rodas e portas. Os segmentos devem **continuar parecendo exatamente os originais**.

### Animação e física a corrigir
1. Ação explícita por tomada: preparação → execução → contato → consequência, sem pessoas surgindo/desaparecendo, atravessando obstáculos ou andando de costas sem intenção.
2. Pisada com apoio plantar: fixar o pé de suporte ao solo, alternar carga corporal, dobra de joelho/quadril e oscilação discreta de tronco/capa.
3. Mãos devem agarrar as cordas, o arco, as lanças ou a pedra no mesmo ponto enquanto objetos se movem.
4. Portões abrem com dobradiças/escala coerentes; o **cavalo inteiro atravessa a abertura**, com rodas girando; guerreiros **saem do cavalo por uma porta visível** e abrem os portões a partir do lado correto.
5. Polifemo e o rochedo demonstram força/peso e escala; gigante com um único olho legível; não empurrar um objeto minúsculo.
6. Cenas S01–S16 seguem o roteiro integral com atores visualmente persistentes (não reciclar um corpo genérico para Penélope, Circe, Telêmaco, Argos, etc.).
7. Evitar movimentos repetidos, corrida em loop, simples oscilação de braços sem propósito, os mesmos 5 quadros reusados e câmera movendo sobre fundo imóvel.
8. QC automático: frames em início/meio/fim; QC humano: comparação lado a lado com o **modelo original de Troia** para cada personagem e para as primeiras tomadas; não aprovar se a silhueta, rosto ou paleta mudarem.

## Rejeição dos protótipos posteriores
**V19/V20/V21/V22** de `odyssey_2d/render_16_scene_film.py` e outras versões com personagens simples de retângulos/túnicas e cabeças diferentes são apenas protótipos mecânicos. **Reprovadas como modelo visual**. Não usar essas figuras genéricas como cast final; não confundir “16 cenas com som” com o filme dentro do padrão.

## Áudio, roteiro e publicação
Preservar o roteiro integral de 16 cenas; voz Rasalgethi original de 220,56 s, sem gerar outra e sem acelerar; 9:16, meta 4K/60fps; música e SFX subordinados ao diálogo. Não publicar/agendar sem aprovação visual e narrativa. **O trabalho agora é adaptar a animação da Odisséia para o desenho do primeiro Cavalo de Troia, melhorando o rig e o acting, não recriando personagens.**

**Critério de aceite prioritário:** antes de renderizar 3min40, demonstrar uma sequência curta com **o exato Odisseu do filme Cavalo de Troia**, caminhando com peso e interagindo fisicamente com um objeto, e confirmar a fidelidade visual. Não derivar um rosto novo.
