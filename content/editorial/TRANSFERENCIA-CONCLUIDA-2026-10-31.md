# Transferência concluída — pacote semanal do Instagram TUE

**Estado verificado em 31/10/2026:** O pacote semanal foi transmitido ao repositório GitHub, reconstituído e extraído com sucesso pelo workflow de **execução única**. A importação validou os hashes SHA-256 das 27 mídias e atualizou `content/schedule.json` para URLs fixadas em um commit imutável.

## Comprovações
- Repositório: `gabrielslinhares12-sudo/instagram-skills`.
- Commit de transferência original (18 partes ZIP): `bad63f040ec092466b747fcdb1ca360e08cd0ac7`.
- Commit contendo os **27 arquivos finais**: `7f178c9d633798c0e0612ed0d52a2b1ce4c814b5`.
- Workflow de importação: `https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41166898759` — **success**; log: `ZIP reconstructed: 13,777,509 bytes, 27 intact media items`, `Validated and extracted 27 media files`, `IMPORTED: 27 assets, 7 posts, all approvals disabled`.
- Pasta final: `content/media/semana-2026-10-31-final/`.
- As sete entradas do calendário têm URLs imutáveis e hashes correspondentes; nenhum item está com `approved=true`.
- `content/publication-state.json` não tem recibos de publicação, então **NENHUMA publicação no Instagram foi confirmada**.
- O workflow de publicações e o importador **não têm gatilho recorrente**. O gatilho de upload do importador foi desativado após a importação; continua disponível somente acionamento manual.
- A cópia temporária usada como ponte foi excluída de seu armazenamento intermediário depois da confirmação.

## Contagem de arquivos por pauta
| Tema | Tipo | Arquivos finais |
|---|---|---:|
| Halloween | Post JPG | 1 |
| Votos | Carrossel JPG | 8 |
| Dólar | Carrossel JPG | 8 |
| Onças | Carrossel JPG | 7 |
| ENEM | Post JPG | 1 |
| Foguete | Reel MP4 | 1 |
| Lua | Reel MP4 | 1 |
| **Total** | | **27** |

**Próxima fase separada (não solicitada neste pedido de transferência):** revisar a versão final de cada post, verificar a integração Meta, decidir datas ainda válidas e liberar/agendar as publicações individualmente. Não assumir que `due_at` representa agendamento ativo quando `approved=false`. Não reativar verificação periódica sem nova orientação.
