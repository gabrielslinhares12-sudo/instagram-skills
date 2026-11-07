# Templates de direção — TUE-CINEFRAME-01

Estes templates são agnósticos ao gerador. Adaptar campos ao formato permitido por cada ferramenta. Não enviar material privado sem autorização.

## A. Referência imutável do personagem
Crie uma folha de referência original com [CHARACTER_ID] e a descrição canônica [DESCRIÇÃO_FIXA].
Exiba uma vista frontal, perfil e três-quartos, mais 4 expressões, mantendo geometria facial, cabelo, roupa, proporções, acessórios e paleta rigorosamente consistentes. Fundo neutro, contorno legível, luz uniforme, nenhum texto ou marca d'água. Não inventar detalhes ausentes da bíblia. Registrar a imagem escolhida como referência master e manter as alternativas fora do conjunto ativo.

## B. Ambiente mestre
Crie imagem de referência do set [SET_ID] com planta e dimensões [LAYOUT], objetos fixos [PROPS], direção da luz [LIGHTING], pontos de entrada/saída [EXITS] e paleta [PALETTE]. Preveja ângulos de câmera [ANGLES] sem trocar arquitetura ou escala entre views.

## C. Cena image-to-video
Use estritamente a referência de personagem [CHARACTER_REF] e cenário [SET_REF].
Ação única: [PREPARATION] -> [ACTION] -> [CONSEQUENCE].
Duração [DURATION] segundos. Estado inicial [START_STATE]; estado final [END_STATE].
Câmera [SHOT_TYPE], lente [LENS], altura [HEIGHT], eixo [AXIS], movimento [CAMERA_MOVE], foco [FOCUS].
Contato físico: [CONTACTS]; iluminação [LIGHTING]; identidade [CHARACTER_LOCK].
Narração/fala exata [EXACT_DIALOGUE] e sincronismo [AUDIO_TIMECODE] somente quando aplicável.
Não alterar rosto/roupa, gerar membros extras, deslizar os pés, atravessar objetos, trocar cenário, reutilizar movimento ou inventar texto. Gerar duas alternativas se o take for crítico e manter apenas uma versão validada.

## D. Alternativa gratuita de animação 2D
Importe os sprites com IDs fixos. Para cada tomada, animar poses-chave de cabeça, tronco, ombros, cotovelos, mãos, quadril, joelhos, pés, olhos e tecido em tempo real; plantar pés em apoio; preservar agarramento em objetos; fundo em camadas coerentes. Renderizar quadros usando Python/Pillow/Remotion e codificar no FFmpeg. O resultado deve representar a ação real, não movimento de câmera em imagens estáticas.

## E. Ordem editorial para cada prompt
Personagem -> objetivo -> ambiente -> preparação/ação/consequência -> câmera -> movimento -> tempo -> estados inicial/final -> voz -> proibições. Evitar excesso de estímulos e pedir uma ação central por tomada.

## Política de semelhança
Prefira personagens originais ou de domínio público tratados de modo original. Não usar imagem ou voz de pessoa real nem material de terceiros sem direitos/consentimento.
