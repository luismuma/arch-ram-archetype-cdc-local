# Pull Request Workflow.
# Triggers:
#   - feature/* -> develop
#   - hotfix/*  -> main

name: PR workflow

run-name: ${r'"Build and Test #${{ github.run_number }}: ${{ github.event.pull_request.title }}"'}

permissions:
  contents: read
  pages: write
  id-token: write

on:
  pull_request:
    types:
      - opened
      - synchronize
    branches:
      - develop
      - main
      - master

jobs:
  pull-request:
    name: Build and Test

    if: >-
      startsWith(github.head_ref, 'feature/') ||
      startsWith(github.head_ref, 'hotfix/')

    uses: luismuma/arch-ram-reusable-workflows-local/.github/workflows/cdc.pull-request.yml@main

    secrets:
      # Permite utilizar el token genérico o el nombre anterior.
      EXTERNAL_GITHUB_TOKEN: ${r"${{ secrets.EXTERNAL_GITHUB_TOKEN || secrets.GH_GIT_TOKEN }}"}

      # Contraseña para cifrado de tokens centralizados.
      GH_TOKEN_ENCRYPTION_PASSPHRASE: ${r"${{ secrets.GH_TOKEN_ENCRYPTION_PASSPHRASE }}"}

      # Credenciales de Azure Artifacts.
      AZURE_ARTIFACTS_USER: ${r"${{ secrets.AZURE_ARTIFACTS_USER }}"}
      AZURE_ARTIFACTS_PW: ${r"${{ secrets.AZURE_ARTIFACTS_PW }}"}

      # Compatibilidad con workflows que siguen utilizando GH_GIT_TOKEN.
      GH_GIT_TOKEN: ${r"${{ secrets.GH_GIT_TOKEN }}"} 
