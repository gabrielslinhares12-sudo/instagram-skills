# ODISSEIA — V5/V7.1 REPROVADAS — NÃO PUBLICAR
**Data:** 06/11/2026
**Decisão editorial:** REFAZER A ANIMAÇÃO, NÃO RETOCAR CENAS.
**Responsável pela decisão:** revisão após devolutiva explícita do proprietário.
**Materiais V5/V7.1:** apenas referência técnica; jamais aprovar/publicar pelo fato de terem 4K, 60 fps e áudio.

## Constatações objetivas após inspeção de 31 pontos entre 0 e 550 s
1. **Personagens e objetos sobrepostos sem relação espacial.** A camada genérica `Odysseus` aparece diante de cenários e objetos que pertencem a acontecimentos separados; algumas ações também adicionam outro ator em `ExtraActs` e outros `RoleActor` sem delimitação de cena.
2. **Cenografia que não conta o evento.** Ex.: diante de Troia, figura central de pé e barcos sobrepostos; no mar o mesmo guerreiro em primeiro plano; em episódios de Penélope o protagonista surge sem estabelecer seu lugar na cena.
3. **Falta de atuação contínua.** Ações descritas em nomes não correspondem necessariamente à mecânica corporal (pegar, empurrar, entrar, cair, abraçar); os movimentos parecem slides de bonecos.
4. **Trocas excessivas / perda de causalidade.** 131 eventos em 560,1 segundos (média ~4,28 s por evento); cabeçalhos e modelos não substituem ação completa e não se pode tratar cada evento como uma nova cena obrigatória.
5. **Escala e perspectiva inconsistentes.** Em particular o gigante, a pedra, o cavalo e as portas não compartilham volume, plano e trajetória convincente.
6. **Critérios de aceite anteriores inadequados.** Compilação, duração, formato, 4K e FPS dizem apenas se o vídeo é tecnicamente decodificável.

## Bloqueio editorial imediatamente aplicável
- `ODISSEIA_V5`, `ODISSEIA_V7` e `ODISSEIA_V71`: **REPROVADO**, independentemente do nome FINAL nos arquivos antigos.
- **Não publicar/agendar** qualquer arquivo dessas gerações no Instagram ou outra plataforma.
- Manter a narração original como fonte, mas primeiro mapear as frases completas, palavra/intervalo e contexto por sequência; nenhum cenário é decidido apenas por marcador temporal aproximado.
- Proibido montar remendos de 5 segundos na versão reprovada e declarar concluído.
- Proibido anexar Lúmino ou Odisseu como figurante recorrente fora do lugar na história.

## Arquitetura nova exigida — shots em vez de camadas avulsas
Cada tomada possuirá **um set exclusivo** com entidades admitidas explicitamente e arranjo 3D/2.5D coerente:
- `background`: cenário com perspectiva e iluminação da tomada.
- `actors`: personagens indispensáveis somente, com identidade consistente e profundidade definida.
- `interactive_props`: objetos com escala e ponto de contato; braços/mãos seguem a física do objeto.
- `occluders`: portas/colunas/rochas que ocultam corretamente pessoas e objetos quando passam atrás.
- `camera`: enquadramento orientado à ação (não panorâmica de fotos).
- `audio_span`: tempo real da frase, ações que começam antes da frase terminar e consequência visível.
- `continuity`: posições, direção de movimento, acessórios e quem está presente na tomada anterior.
- `semantic_qc`: teste visual e auditivo, não apenas ffprobe.

**Regra de exclusividade:** cada tomada decide quais personagens aparecem; não existe o ator hero global desenhado sobre todas as cenas.
**Regra de causalidade:** apresentar preparação → ação → consequência. Mostrar a saída pelo portão quando a fala cita fuga; não apenas cavalo, guerra e pessoas estáticas.
**Regra antirrepetição:** não reciclar bonecos andando/indo-e-voltando como preenchimento; só repetir locais quando a narrativa efetivamente volta a eles.

## Estrutura da história — referência, ainda a conferir contra cada frase do áudio
| Minutagem do master | Núcleo dramático | Ação que PRECISA ficar compreensível |
|---|---|---|
| 00:00–00:17 | Fim de Troia | Cidade em ruínas → embarque → frota deixa a costa; corte claro para Ítaca onde Penélope espera |
| 00:17–00:28 | Cícones | Confronto reconhecível → reforços inimigos → tripulação bate em retirada |
| 00:28–00:38 | Lótus | Ilha → fruto oferecido → marinheiro esquece a missão → Odisseu o retira |
| 00:38–00:55 | Polifemo | Heróis entram na caverna → gigante aparece → pedra ENORME é empurrada e VEDA a abertura |
| 00:55–01:16 | Ninguém | Vinho dado ao ciclope → adormece → estaca → carneiros passam pela saída |
| 01:16–01:28 | Poseidon | Odisseu revela seu nome → gigante pede vingança → mar muda violentamente |
| 01:28–01:53 | Éolo | Saco de ventos recebido → terra natal à vista → marinheiros abrem saco → tempestade os afasta |
| 01:53–02:07 | Lestrigões | Porto cercado → gigantes atacam e afundam navios → um navio escapa |
| 02:07–02:28 | Circe | Convite → poção → companheiros viram porcos → Odisseu enfrenta magia e liberta tripulação |
| 02:28–02:55 | Hades | Travessia escura → profecia → reencontro impossível com a mãe → espírito intangível |
| 02:55–03:08 | Sereias | Tripulação põe cera → herói é amarrado ao mastro → navio passa sem ceder |
| 03:08–03:25 | Cila e Caríbdis | Dois perigos de lados opostos → remadores atravessam o estreito enquanto a criatura ataca |
| 03:25–03:44 | Gado do Sol | Fome → tripulação viola proibição → raio destroça o navio → único sobrevivente |
| 03:44–03:59 | Calipso | Ilha → promessa de abrigo imobiliza o herói → desejo de regressar |
| 03:59–04:18 | Penélope | Pretendentes ocupam salão → tear trabalha de dia e é desfeito de noite |
| 04:18–04:36 | Telêmaco | Filho parte à procura do pai → recebe auxílio → evita emboscada |
| 04:36–04:55 | Jangada | Hermes exige a partida → construção realmente manual → jangada chega ao mar e naufraga |
| 04:55–05:16 | Feácios | Náusicaa acolhe náufrago → recepção → rei providencia navio para Ítaca |
| 05:16–05:38 | Costa de Ítaca | Odisseu acorda na praia → reconhece terra → Atena fornece disfarce |
| 05:38–05:58 | Pai e filho | Aproximação na cabana → identidade revelada → abraço → plano de recuperar a casa |
| 05:58–06:14 | Argos | Cão reconhece o dono; olhar e reação devem ser o foco, não soldado em destaque |
| 06:14–06:36 | Cicatriz | Pretendentes humilham mendigo → ama lava pé → vê cicatriz → promete silêncio |
| 06:36–06:56 | Arco | Homens tentam encordoar → ninguém consegue → Odisseu empunha |
| 06:56–07:15 | Doze machados | Machado alinhado em profundidade → flecha atravessa orifícios → pretendentes percebem quem ele é |
| 07:15–07:35 | Penélope | Apresentação da suspeita dela → reconhecimento ainda precisa de prova |
| 07:35–08:00 | Cama e oliveira | A cama fixa à árvore torna-se prova; objetos devem compartilhar um único espaço compreensível |
| 08:00–08:05 | Memória de Troia | Lembrança do cavalo entra como flashback visivelmente distinto; retorno nítido à cena presente |
| 08:05–08:15 | Reencontro | Odisseu e Penélope de fato se aproximam e se abraçam — não personagens de pé na frente de uma cama |
| 08:15–08:35 | Remo | Jornada em terra firme carregando remo; encontro com estranho e ato de fincar remo |
| 08:35–08:48 | Laertes | Reconhece o pai no pomar; diferenças físicas claras e reação emocional |
| 08:48–09:20 | Paz | Conflito final → Atena intervém efetivamente → armas baixam → Ítaca em paz |

*Observação: marcações por assunto são provisórias, baseadas no roteiro anterior. Sincronismo definitivo demanda verificação por frases do áudio fonte. Cortes de episódio 1 = 88,6 s; 2 = 228,8 s; 3 = 242,7 s.*

## Nova régua de aceite (FAIL-CLOSED)
1. Protótipo de **uma única sequência de 10–15s**, com ação física real e narrativa clara, sem pan de imagens. Não replicar para os demais episódios enquanto falhar.
2. Assistir sem narração: espectador consegue dizer quem fez o quê e por quê.
3. Assistir com voz: nenhum objeto personagem contradiz a fala; legenda perfeitamente alinhada.
4. Verificar por inspeção a cada corte: silhueta, escala, contato da mão, continuidade, perspectivas, oclusão; nenhum objeto por cima do outro sem intenção.
5. Conferir percurso corporal completo e sem patinação, mãos no contato, pernas apoiadas e resposta ao peso.
6. Só depois concluir o episódio 1 em 4K/60 FPS e submetê-lo à revisão visual integral; repetir ciclo para os outros dois.
7. **Jamais usar a palavra FINAL ou iniciar publicação com qualquer reprovação editorial em aberto.**
