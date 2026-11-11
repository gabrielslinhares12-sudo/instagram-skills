# TUE — limpeza segura dos artefatos GitHub Actions

**Regra obrigatória:** nunca apagar um artefato antes de verificar que uma cópia ZIP idêntica está acessível no Google Drive. O script compara nomes, tamanho, SHA-256 completo e integridade ZIP do GitHub e Drive, e **só depois** pode chamar a exclusão de um artefato.

O workflow `.github/workflows/tue-verified-drive-artifact-cleanup.yml` executa diariamente às 06:17 UTC e pode ser acionado manualmente em modo `dry_run`. Sem as três secrets `GDRIVE_OAUTH_CLIENT_ID`, `GDRIVE_OAUTH_CLIENT_SECRET` e `GDRIVE_OAUTH_REFRESH_TOKEN`, não exclui nada. Autentica via `GH_TOKEN` efêmero da execução com permissão `actions: write`.

## Quais arquivos são elegíveis

1. Artefatos explicitamente enumerados em `storage/artifact-drive-verified.json` com nome, tamanho, hash e nome exato da cópia no Drive; ou
2. Novos artefatos com nome começando por `tue-drive-backed-` cuja cópia no Drive se chama exatamente `<nome-do-artefato>.zip`. A exclusão só ocorre com hash e bytes idênticos após novo download das duas fontes.

O script nunca apaga códigos, commits, workflows, arquivos do Drive, histórico de execuções, nem artefatos contendo `ledger`, `publication-state`, `receipt`, `audit`, `logs` ou `report` no nome. Não apaga artefatos com menos de uma hora, cópias inexistentes/ambíguas, ZIPs danificados ou artefatos expirados. Falhas impedem a exclusão do item e ficam registradas no resumo da execução.

## Como integrar novos uploads

- Envie o arquivo ZIP definitivo para o Drive com o **mesmo conteúdo binário** do ZIP criado pelo GitHub Actions. Não basta que o conteúdo descompactado seja equivalente: o SHA-256 precisa ser o mesmo.
- Prefira criar um artefato chamado `tue-drive-backed-<identificador-unico>` e enviar uma cópia com o nome `tue-drive-backed-<identificador-unico>.zip` para o Drive. O agendador localizará a cópia e fará a verificação; se houver inconsistência, nada é apagado.
- Para arquivos com nomes diferentes, acrescente uma entrada explícita com `artifact_id`, `artifact_name`, `drive_name`, `size_bytes` e `sha256` ao manifesto. Nunca marque cópias como verificadas só porque os tamanhos coincidem.
- Não reduza cegamente a retenção padrão de artefatos de produção: uma transferência incompleta precisa manter o original. Após **backup confirmado**, a limpeza automatizada diária dá retenção efetiva de até cerca de um dia; workflows especializados podem definir `retention-days: 1` somente quando houver backup verificado independente.

Execução manual de conferência: `python3 scripts/tue_verified_drive_artifact_cleanup.py`.
Execução autenticada (exclui os que passarem): `python3 scripts/tue_verified_drive_artifact_cleanup.py --execute`.

A limpeza não realiza publicações sociais, não modifica filas e não copia fotos ou vídeos.