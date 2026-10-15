<#--
  Merge Commit Workflow (FreeMarker Template)
  Triggers when:
   - A pull request to develop is closed and merged (Snapshot tag/package)
   - A pull request to main/master is closed and merged (Release tag/package)

  Required secrets:
   - AZURE_ARTIFACTS_USER
   - AZURE_ARTIFACTS_PW
   - GH_TOKEN_ENCRYPTION_PASSPHRASE
   - RAM_GITHUB_GIT_TOKEN (o EXTERNAL_GITHUB_TOKEN para compatibilidad)
-->

name: Merge Commit

run-name: "Generate ${r"${{ (github.base_ref == 'main' || github.base_ref == 'master') && 'Release' || 'Snapshot' }}"} Artifact #${r"${{ github.run_number }}"}"

permissions:
  contents: read
  pages: write
  id-token: write

on:
  pull_request:
    types:
      - closed
    branches:
      - main
      - master
      - develop

jobs:
  merge:
    name: CDC Merge and Package Workflow

    # Solo se ejecuta cuando el PR se ha integrado.
    if: ${r"${{ github.event.pull_request.merged == true }}"}

    uses: luismuma/arch-ram-reusable-workflows-local/.github/workflows/cdc.merge-commit.yml@main

    secrets:
      AZURE_ARTIFACTS_USER: ${r"${{ secrets.AZURE_ARTIFACTS_USER }}"}
      AZURE_ARTIFACTS_PW: ${r"${{ secrets.AZURE_ARTIFACTS_PW }}"}
      GH_TOKEN_ENCRYPTION_PASSPHRASE: ${r"${{ secrets.GH_TOKEN_ENCRYPTION_PASSPHRASE }}"}

      # Mapeo de tokens de GitHub compatibles.
      # RAM_GITHUB_GIT_TOKEN: ${r"${{ secrets.RAM_GITHUB_GIT_TOKEN || secrets.EXTERNAL_GITHUB_TOKEN || secrets.GH_GIT_TOKEN }}"}
      RAM_GITHUB_GIT_TOKEN: ${r"${{ secrets.GH_GIT_TOKEN }}"}

