# A ODISSEIA — versão atual 2D TUE | direção de produção

**Decisão explícita posterior do usuário (07/11/2026):** "Não crie a parte da animação 3d, faça em 2D dentro do nosso formato atual". É a instrução vigente para o filme. Toda diretriz herdada que exige tridimensionalidade está substituída para esta produção; conservar narrativa, figurinos, escala e qualidade visual do roteiro.

**Motor:** animação cel-shaded 2D com personagens articulados (braços, pernas, cabeça, tronco, mãos), fundos desenhados no mesmo estilo, sprites/rigs persistentes, perspectiva 2.5D coerente, múltiplas expressões. Produzir com Python/Pillow/NumPy/FFmpeg ou Remotion **sem Blender 3D**, sem Runway/GUTHY e sem APIs pagas. Referência audiovisual de identidade: `content/media/instagram/2026-11-05/odisseu-troia/Cavalo_Troia_4K60_Meta_10h.mp4` e o trabalho original de animação 2D articulada.

**Narrativa:** Odisseia completa, 16 cenas na ordem especificada, sem nenhuma cena substituída por fundo parado, zoom de foto, clipe genérico ou boneco deslizante; estrutura preparação → ação → consequência. Manter rosto, cores e figurinos de cada personagem consistentes. O cavalo deve parecer e se mover como cavalo, atravessar o portão; Polifemo/rocha proporcionais; retorno de Telêmaco, Argos, prova do arco e oliveira precisam ocorrer como ações animadas reconhecíveis.

**Áudio original:** WAV Rasalgethi da gravação do usuário, 220,56s, SHA256 `9be8b79920b318c76f23874d38d12f4f77b46f8a9871833612ac1efa82b5d667` armazenado exclusivamente em repositório privado `tem-uma-explicacao`. Sem sintetizar substituto, sem comprimir tempo de fala. Duração final ~3m40s. Legendas inferiores em até duas linhas; fonte limpa.

**Mestre solicitado:** vertical 9:16, 2160×3840, 60 fps; se o processamento inicial for resolução menor, rotular como prévia, nunca como 4K60 nativo. Exportar H.264/AAC, sem marcas d'água.

**Gates:** inspeção de quadros e vídeo por sequência; QC de continuidade, atuação, áudio, legendas; nunca publicar/agendar sem aprovação editorial. Não mascarar testes antigos 3D reprovados como cenas finais.

**Repositório:** arquivos antigos de 3D mantidos apenas para auditoria, workflows V18 3D arquivados (manual-only) e fora do caminho principal. Diretório novo para produção 2D: `odyssey_2d/`.

**Estado:** contrato 2D aprovado como direção por instrução do usuário; filme final ainda não renderizado neste momento. Caminho vigente substitui o documento 3D `PRODUCAO_V18_CONTRATO_FILME_3D_20261107.md`, que permanece somente registro histórico.
