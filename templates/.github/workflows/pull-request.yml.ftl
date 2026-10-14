<#-- 
  Pull Request Workflow (FreeMarker Template)
  Triggers when:
     - A pull request from feature to develop is created / synchronized
     - A pull request from hotfix to main is created / synchronized
-->

name: PR workflow
run-name: "Build and Test #${r"${{ github.run_number }}"}: ${r"${{ github.event.pull_request.title }}"}"

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
    if: startsWith(github.head_ref, 'feature/') || startsWith(github.head_ref, 'hotfix/')
    uses: luismuma/arch-ram-reusable-workflows-local/.github/workflows/cdc.pull-request.yml@main
    
    secrets:
      AZURE_ARTIFACTS_USER: ${r"${{ secrets.AZURE_ARTIFACTS_USER }}"}
      AZURE_ARTIFACTS_PW: ${r"${{ secrets.AZURE_ARTIFACTS_PW }}"}
      GH_TOKEN_ENCRYPTION_PASSPHRASE: ${r"${{ secrets.GH_TOKEN_ENCRYPTION_PASSPHRASE }}"}
      
      <#-- [MODIFICADO]: Se pasa el token externo o se conmuta al antiguo de forma compatible mediante FreeMarker o sintaxis nativa de GitHub -->
      EXTERNAL_GITHUB_TOKEN: ${r"${{ secrets.EXTERNAL_GITHUB_TOKEN || secrets.GH_GIT_TOKEN }}"}
