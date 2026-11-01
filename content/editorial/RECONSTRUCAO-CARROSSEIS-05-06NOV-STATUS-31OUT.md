# Instagram TUE — reconstrução de carrosséis de 05–06/11/2026

**Estado em 31/10/2026: pacote de REVISÃO, NÃO aprovado, NÃO agendado, NÃO publicado.** O arquivo não substitui revisão artística humana nem altera o registro de publicações.

## Nova entrega conferida no Drive

- [Prévia 05/11, Foguetes — 8 páginas](https://drive.google.com/file/d/1cugCgPybN8mht5hkkZLO3tDdogUZmVY-/view?usp=drivesdk)
- [Prévia 06/11, Lua — 8 páginas](https://drive.google.com/file/d/1Znc_OF1d2jIoh0Go81rGSMfezzn030U3/view?usp=drivesdk)
- [Pacote ZIP de revisão — 16 arquivos JPG](https://drive.google.com/file/d/1i0_41L26XmGyoXtnhMYZ38kCpZPOMABr/view?usp=drivesdk)
- [Pasta de revisão de 05 e 06/11](https://drive.google.com/drive/folders/1isgaT3MnQK-ObM8ooPfc35bfaL0rTVLz)

O pacote contém oito JPGs por carrossel, cada um em 1080×1350, além de prévias e MANIFESTO-REVISAO.json com hashes SHA-256. Integridade do ZIP (CRC) verificada. Imagens de lançamento/estrada/lua são ILUSTRAÇÕES, não registros fotográficos oficiais da NASA.

## Qualidade: o que ainda está bloqueado

- 05/11 18h (Foguetes), páginas 1–8: arte de IA na paleta aceita, mas o Lúmino foi reproduzido visualmente, e **ainda não está demonstrado que é a inserção pixel a pixel da PNG original**.
- 06/11 18h (Lua), páginas 1–2: arte de IA na paleta aceita, com o mesmo impedimento de identidade pixel a pixel.
- 06/11 18h (Lua), páginas 3–8: composição editorial controlada com inserção da PNG canônica **sem redesenhar o personagem**. O padrão técnico de identidade é respeitado nessas páginas; a equivalência artística das cenas com as capas **permanece sujeita à revisão manual**.
- Não promover nenhum arquivo para `content/approved`, pois o pacote misto ainda não satisfaz o validador completo de `scripts/instagram_visual_standard.py`.
- Reels dos mesmos dias ainda precisam de narração Rasalgethi e MP4 sincronizado; capas não comprovam vídeo final.

## Padrão obrigatório já implantado

O projeto possui assets oficiais sob `content/brand/`, configurações `padrao-visual.json`, compositor `scripts/render_instagram_carrossel.py`, verificador `scripts/instagram_visual_standard.py` e bloqueios em `.github/workflows/instagram-scheduler.yml`.

A produção só poderá ser tratada como aprovada depois de 8 JPGs finais por carrossel, manifesto técnico íntegro usando a PNG original, revisão individual de legibilidade/fatos e nova autorização do proprietário. **Não mudar `content/schedule.json` nem `content/publication-state.json` nesta reconstrução.**

## Conteúdo factual

- Foguetes: ignição, empuxo como reação ao jato, força resultante, densidade atmosférica, estágio e velocidade orbital. Fonte [NASA Glenn — Rocket Thrust](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/rocket-thrust/).
- Lua e paralaxe: objetos próximos apresentam maior variação angular aparente durante deslocamento; a Lua muito distante varia muito pouco para um trajeto rodoviário. Ilusão da Lua no horizonte é fenômeno perceptivo distinto. Referência geral [NASA Science — Moon](https://science.nasa.gov/moon/).

A capa do conteúdo de Lua não afirma que o satélite acompanha realmente o veículo.
