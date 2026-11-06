# A Odisseia — auditoria cinematográfica e correção de animação

Data da auditoria: 06/11/2026. Alvo editorial: 07/11/2026. **Não aprovar publicação sem novos arquivos renderizados.**

## Fonte verificada
- `Odisseia_O_regresso_a_Itaca_4K60.mp4`, duração 560,100 s; 2160×3840; 60 fps; H.264 e áudio AAC estereofônico 48 kHz.
- Bitrate do vídeo **aproximadamente 1,98 Mb/s**, baixa margem para 4K; mereceria exportação a taxa visual maior **apenas após remontagem dos vetores originais**.
- Filme integral e trilogia antiga em `/mnt/data`; a versão antiga é **arquivo de referência, não versão revisada**.
- As composições do longa não foram encontradas na árvore GitHub `main` dos repositórios conectados; o projeto `motion` de `feat/tue-motion-base` contém o curta Troia e o rig do Odisseu, não o projeto editável de 9min20s. Os próximos itens devem ser reconstruídos em cenas editáveis, não mascarados sobre o render antigo.

## Defeitos e intervenções por tempo (do longa original)
| Minutagem | Cena | Falha identificada | Correção exigida |
|---|---|---|---|
| 00:00–00:26 | Troia e partida | Plano de personagens distantes, retorno do mesmo cenário | Close de despedida com Penélope/Telêmaco; frota de 12 barcos com velas/cordas/água animada; intercalar vista alta e convés |
| 00:27–00:38 | Lótus | Caminhada em fila pouco articulada; pessoas diminutas | Ação efetiva de colher/comer lótus, mudança de reação facial, Odisseu agarrando companheiro; pé de apoio fixo |
| 00:38–01:16 | Polifemo | Ciclope frequentemente quase imóvel; protagonistas minúsculos e gestos simplificados | Rig de olho, ombros, mão, maça e expressão; abertura da caverna, roca/ovelhas, estaca em movimento e reação; enquadramentos inéditos |
| 01:17–01:29 | Poseidon | Barco e penhasco quase sem ação | Água espirrando, braços de remo visíveis, câmera inferior e tempestade reagindo ao brado |
| 01:29–02:02 | Éolo e lestrigões | Barco repetido; poucos gestos de abrir bolsa e ataque | Saco com tecido reativo; remadores, mastros, redemoinhos; gigantes arremessando rochas; ação multiângulo |
| 02:02–02:27 | Circe | Palácio muito similar a outros interiores; mãos/poção pouco expressivas | Sala da feiticeira única, caldeirão, frascos, porcos se movendo; atores não repetidos entre planos |
| 02:28–02:50 | Hades | Figurino/gesto em plano genérico, atmosfera pouco dramática | Rio escuro, névoa espacial, luzes narrativas, sombra de Tirésias entrando fisicamente em cena |
| 02:51–03:20 | Sereias / Cila-Caríbdis | Reaparece mesmo barco e penhasco | Nós amarrando Odisseu, remos alternados, sereias distintas, seis cabeças como silhueta sem ataque gráfico e redemoinho com rotação física |
| 03:21–03:40 | Gado do Sol | Animais e barco estáticos; naufrágio simplificado | Rebanho em deslocamento, raio de Zeus interagindo com vela/mastro, fragmentos e mar agitado |
| 03:40–04:14 | Calipso e Ítaca | Dois personagens parados; o mesmo jardim e praia | Expressão, emoção e cenas adicionais de Penélope desfazendo a tecelagem em close |
| 04:15–05:17 | Telêmaco / jangada / feácios | O mesmo palácio/convés volta a aparecer | Telêmaco com fisionomia própria; montagem de navegação com mar, neblina, remo, navegadores e aproximação da costa |
| 05:18–05:57 | Retorno e filho | Aproximação sem passos críveis e reencontro distante | Disfarce de mendigo, reação de reconhecimento, aproximação com pegada no chão e abraço em close |
| 05:58–06:13 | Argos | O cão é usado majoritariamente estático | Animação quadrúpede: cabeça, orelhas, cauda e respiração; close no olhar do dono |
| 06:14–06:35 | Euricleia | Lavagem dos pés em cenário recorrente | Cena de bacia e mãos próprias, reconhecimento da cicatriz, reação da ama |
| 06:36–07:12 | Arco dos pretendentes | Os personagens são pequenos; movimento do arco fica implícito | Arco verossímil com tensão, flecha perfurando os 12 machados no mesmo eixo, cortes entre flecha e expressão |
| 07:13–07:34 | Penélope desce | Mesmo interior palaciano repetido; reações mínimas | Plano escada, travellings discretos no cenário animado, reações específicas de Penélope |
| 07:35–08:14 | Oliveira e reencontro | Personagens estáticos no momento mais emocional; retorno do cavalo de Troia reaparece como reciclagem | Quarto com leito vivo talhado em oliveira, objeto da prova com movimento, abraço com mãos e postura coerentes; REMOVER o cavalo de Troia desta parte como ilustração reciclada |
| 08:15–09:20 | Epílogo / paz | Campo/palácio repetido, figuras pequenas e conclusão lenta | Assembleia com composição exclusiva, reconciliação, retorno a casa, encerramento Lúmino correto e sem áudio reciclado |

## Regras de aceitação visual e técnica
1. Cada acontecimento visível precisa de animação própria; **sem usar cenas reaproveitadas com legendas diferentes**. IDs de planos únicos e checagem perceptual dos cenários.
2. Caminhada orgânica: quadril, joelho, tornozelo e braço oposto animados em IK; pé de apoio permanece fixo no mundo enquanto o torso avança; 60fps.
3. Diferenciar silhuetas, roupas, proporções, cabelo e gestos de Odisseu, Penélope, Telêmaco, Polifemo, Circe e figurantes. Não reutilizar clones do herói para todos os marinheiros.
4. Personagem protagonista ocupar de **35% a 65% da altura da composição** nos planos de atuação; estabelecer planos gerais somente quando necessário, alternando com close.
5. 3 episódios como narrativa: 00–01:29, 01:29–05:12, 05:12–09:20; os pontos exatos de corte devem respeitar a frase de narração.
6. Priorizar novos desenhos vetoriais, texturas e detalhes **na cena**, não sobrepor fotografias nem chamar movimento de câmera sobre foto de animação.
7. Entrega: 2160×3840, 60 fps reais, áudio original sincronizado, H.264 CRF 16–18; sem marca-d'água; verificar silêncio, clipping, sincronismo e início/fim de frases.
8. Aprovação editorial somente depois de comparar o MP4 renderizado ao antigo, testar transições, conferir fisicamente cada ação e assistir os três arquivos inteiros. Sem agendamento cego.

## Ações executadas
- Inspeção programática de 146 quadros-chave ao longo dos 560s.
- Criação de quatro folhas de contato, cobrindo toda a jornada.
- Diagnóstico do problema de reutilização de enquadramentos.
- Início de correção do rig de caminhada no ramo `feat/tue-motion-base`, com testes de IK e estabilidade do pé de apoio. O **filme inteiro não foi reanimado por essa mudança de rig isolada**.

**Status geral:** revisão concluída; fonte completa editável do longa não encontrada no GitHub; publicação de 07/11 permanece condicionada a render final e QC.
