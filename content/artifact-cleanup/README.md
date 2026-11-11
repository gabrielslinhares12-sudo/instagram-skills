# Limpeza de artefatos — TUE / Instagram

Objetivo: manter mídias definitivas no Google Drive e remover **somente** artefatos temporários equivalentes do GitHub Actions após verificação independente de SHA-256.

## Rotina instalada

Workflow: `.github/workflows/verified-drive-artifact-cleanup.yml`

- Executa automaticamente ao alterar um recibo em `content/artifact-cleanup/drive_verified.json` e diariamente às 04:23 UTC.
- Execução manual padrão `verify_only=true`: confere, **não exclui**.
- Execução automática verifica OAuth Drive, metadados (IDs, nomes, tamanho, pasta), baixa os bytes originais de ambos os lugares, compara SHA-256 e só então exclui **aquele** artefato GitHub.
- Se a autenticação falhar, arquivo não existir ou houver qualquer divergência, **não exclui**.
- A lista inicial inclui oito artefatos V5.4 do Faker, que já tiveram seus ZIPs pareados localmente. A rotina revalida na nuvem antes de excluir.
- Não exclui releases, commits, logs, execução de Actions, arquivos do Drive, vídeos locais, estado de publicação, arquivos sem recibo ou mídias ainda não transferidas.

## Como integrar em novos fluxos de produção

1. Gerar mídia e subir o arquivo definitivo ao Google Drive; conferir upload, existência, tamanho e download integral.
2. Para um artefato temporário do Actions que contenha o mesmo ZIP byte a byte, guardar um recibo em `content/artifact-cleanup/drive_verified.json` com `artifact_id`, `run_id`, `artifact_name`, `size_bytes`, `drive_file_id`, `drive_name`, `drive_parent_id`, `sha256`.
3. O commit do recibo dispara o workflow automaticamente. Este rebaixa e verifica os arquivos no Drive e GitHub **antes da exclusão**.
4. Preferir `retention-days: 1` para **novos** artefatos puramente temporários após confirmar que o fluxo produz o recibo e que a mídia final é recuperável no Drive. Não reduzir retenção de workflows ainda não migrados.
5. Guardar o hash SHA-256 e identificadores no manifesto; não guardar tokens nem URLs assinadas.

**Não é uma regra global de exclusão de todos os artefatos.** Novas produções passam pela política automática quando os workflows emissores registrarem um comprovante correspondente. Até lá, são preservadas.