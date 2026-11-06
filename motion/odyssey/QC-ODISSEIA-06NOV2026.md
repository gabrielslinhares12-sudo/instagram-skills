# Odisseia — auditoria cinematográfica 06/11/2026

**Status:** em revisão; bloquear postagem até render e escuta dos três episódios.
**Fonte:** Odisseia_O_regresso_a_Itaca_4K60.mp4, 560,1s, 2160x3840, 60 FPS, H.264/AAC.
SHA-256: `33f28ba2a23a9dc8782e8d2dee6ffa47b65c9373aa2384c67545127fe08ed32f`.

## Diagnóstico confirmado no MP4 fonte

Foram comparados 146 quadros-chave, com análise da área visual central (sem títulos/legendas); 430 pares a mais de 35s de distância tiveram diferença média inferior a 6,5/255. **Isso são pares de quadros parecidos, não 430 cenas necessariamente duplicadas.**

- 3:38 e 4:49: horizonte e mar muito parecidos. Recriar travelling próprio do naufrágio e da travessia feácia.
- 5:08 e 6:18: ambiente palaciano visualmente próximo. Recriar encenação física da identificação da cicatriz.
- 3:24 e 8:23: costa com aparência reaproveitada; trocar ângulo, terreno, luz, objetos específicos.
- 0:12 e 7:12: colunatas de palácio recorrentes; distinguir competição do arco com doze eixos alinhados.

## Problemas de produção

1. Caminhar e correr: alternância de calcanhar/apoio, pés imóveis durante o contato com o solo, joelhos IK, movimentos de braços e tronco sincronizados; reduzir postura excessivamente agachada.
2. Legibilidade: protagonistas em plano americano e médio sempre que houver interação relevante; planos gerais apenas para estabelecer geografia.
3. Coro: marinheiros com roupas, cabelos, proporções e fases de passada diferentes. Odisseu deve conservar identidade visual única.
4. Objetos: remaço afeta água, rocha bloqueia caverna, corda acompanha mão e tecido, arco e flecha atravessam 12 machados, cama de oliveira é estruturalmente imóvel.
5. Repetições: cada segmento precisa de background, câmera, blocking e efeitos próprios. Reaparecer em Ítaca não é motivo para reciclar o mesmo plano.
6. Som: original não deve ser substituído por voz diferente. Qualquer retiming exige revisão auditiva das falas e cortes.

## Correções em código testáveis

- `motion/src/actors/gait.ts`: rig determinístico com fase de apoio, arco de swing, ângulos de pé e cinemática inversa.
- `motion/src/actors/OdysseusActor.tsx`: pernas articuladas, pés e sombras, perfis `walk`, `run`, `creep`, `limp`.
- `motion/tests/gait.test.ts`, `motion/tests/odyssey-shotlist.test.ts`: regressão de movimento/continuidade.
- `motion/src/OdysseyGaitQC.tsx`: prévia **14s**, 4 cenários, só para revisar atuação, sem narração.
- `motion/odyssey/PLANO-50-TOMADAS-3-EPISODIOS.json`: **50 cenas em planejamento**, distribuidas por 3 episódios; `needs_narration_alignment` em todas as tomadas.

## Gate de aprovação editorial

A versão final exige:

- render de cada nova tomada (não é aceitável reutilizar o plano fixo original);
- pelo menos 1 rodada de revisão visual para velocidade de caminhada, dimensões de personagem e integração de adereços;
- narração original integral no áudio com cortes alinhados ao conteúdo;
- exportação 2160x3840/60fps com FFprobe, qualidade sem blocos evidentes;
- conferir duplicação e cenas em todos os episódios com detector automático e revisão humana;
- **somente após** esses passos autorizar publicação no Instagram.

Não tratar prévia técnica de 14s como filme acabado. Original e cortes antigos mantidos preservados para referência e recuperação.
