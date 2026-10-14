
# Pull Request Workflow.
# Triggers:
#   - feature/* -> develop
#   - hotfix/*  -> main

name: PR workflow

run-name: "Build and Test #${{ github.run_number }}: ${{ github.event.pull_request.title }}"

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
      # NUEVO: permite utilizar un token genérico.
      # COMPATIBILIDAD: si no está definido, utiliza GH_GIT_TOKEN.
      EXTERNAL_GITHUB_TOKEN: ${{ secrets.EXTERNAL_GITHUB_TOKEN || secrets.GH_GIT_TOKEN }}

      # Contraseña para cifrado de tokens centralizados.
      GH_TOKEN_ENCRYPTION_PASSPHRASE: ${{ secrets.GH_TOKEN_ENCRYPTION_PASSPHRASE }}

      # Credenciales de Azure Artifacts.
      AZURE_ARTIFACTS_USER: ${{ secrets.AZURE_ARTIFACTS_USER }}
      AZURE_ARTIFACTS_PW: ${{ secrets.AZURE_ARTIFACTS_PW }}

      # COMPATIBILIDAD: conservar si el reusable declara y utiliza este secreto.
      GH_GIT_TOKEN: ${{ secrets.GH_GIT_TOKEN }}
