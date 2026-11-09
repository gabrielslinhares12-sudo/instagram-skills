# Faker V4.0 — reconstrução 4K nativa (09/11/2026)

**ESTADO: V3.9.2 REPROVADA. NÃO PUBLICAR.** Esta entrada não afirma que existe master V4.0. O pacote técnico tem o quality gate e manifest em [Google Drive](https://drive.google.com/file/d/1D1NkSlpG4wwDGYi0Q8jbpQrXeScJxCiv/view).

## Diagnóstico
- V3.9.2 verificada localmente: 112 segundos, 1080×1920 a 30 FPS, 3360 quadros H.264; fontes anteriores 720p. Não é 4K nativo, nem tem narração Rasalgethi.
- Preflight com `quality_gate_4k.py` produziu **REPROVADO** por dimensão, fps, frames e falta de fontes de alta resolução comprovadas.
- Má qualidade de origens não é corrigível com upscaling artificial.

## Critérios para o próximo master
1. Master vertical **2160×3840, 60 FPS, 112 segundos = 6720 quadros**. Vetores rasterizados na resolução final; nenhuma animação ou imagem de 720p/1080p ampliada de forma enganosa.
2. Fotografias e vídeos **reais de torneios**, com origem, data, autor, licença/autorização verificados e respeito aos eventos. Fotografias não podem ser usadas como vídeo com zoom simulado.
3. Os três blocos de mapa conservam Summoner's Rift fiel, com campeões, rotas e objetivos animados em 4K60; indicar que simulações táticas não são replays históricos.
4. Abertura única com **imagem real de Faker + logo Lendas do Esport + identificação**. Não inserir títulos centrais persistentes. Legendas apenas inferiores, **sincronizadas ao WAV Rasalgethi** quando efetivamente gerado.
5. Incluir vida além dos campeonatos: fama cultural na Coreia do Sul, encontros com BTS/ENHYPEN, trabalho UNICEF e reconhecimento esportivo; conferir direitos de imagens de terceiros (artistas e emissoras).
6. Segurar publicação até revisão editorial, cinematográfica e técnica aprovada.

## Fontes documentais identificadas (não baixadas para o runtime nesta rodada)
- Creative Silver / 2023 / 3000×4000 / CC BY 4.0: https://commons.wikimedia.org/wiki/File:T1_hold_2023_Summoners_Cup.jpg
- Creative Silver / 2023 / 4000×3000 / CC BY 4.0: https://commons.wikimedia.org/wiki/File:T1_win_2023_Worlds.jpg
- Foto de T1 em MSI 2025 / 3926×1621 / CC BY-SA 4.0: https://commons.wikimedia.org/wiki/File:T1_preparing_for_their_first_game_against_BLG_at_MSI_2025.jpg
- Acervo fotográfico oficial LoL Esports, itens podem ter **All rights reserved**: https://www.flickr.com/photos/lolesports/albums/72177720330194082/
- Regras Riot: https://www.riotgames.com/pt-br/juridico . A política oferece autorização condicional para projetos de fãs; NÃO concede licença irrestrita de todo VOD/foto/música de terceiros.

## Pipeline de QC
Baixe o ZIP do Drive e execute:

```bash
python quality_gate_4k.py --video VIDEO_4K60.mp4 --manifest FAKER_4K_SOURCE_MANIFEST.json --report QC.json
```

Só editar `status` de cada tomada para `received_and_verified` depois de obter, validar e registrar a mídia. Um arquivo MP4 em 4K por si só não prova resolução **nativa** das imagens. Sem produção completa/locução nesta etapa. Sem agendamento.
