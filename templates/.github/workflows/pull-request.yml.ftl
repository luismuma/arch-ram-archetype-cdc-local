# Pull Request Workflow. Triggers when:
#   - A pull request from feature to develop is created / synchronized
#   - A pull request from hotfix to main is created / synchronized
#
# Required secrets:
#   - SONAR_TOKEN             (Repository) Secret with the SonarQube token
#   - GH_TOKEN_ENCRYPTION_PASSPHRASE (Organization) more info in: https://docs.zeus.mapfre.com/8ba7b8109dad11d180b400c04fd430cf/1f7094066cf557db9391713055249220

name: PR workflow
run-name: ${r'"Build and Test #${{ github.run_number }}: ${{ github.event.pull_request.title }}"'}

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
    uses: luismuma/arch-ram-reusable-workflows/.github/workflows/cdc.pull-request.yml@feature/cdc-archetype
    
    secrets:
      AZURE_ARTIFACTS_USER: ${r"${{ secrets.AZURE_ARTIFACTS_USER }}"}
      AZURE_ARTIFACTS_PW: ${r"${{ secrets.AZURE_ARTIFACTS_PW }}"}
      GH_TOKEN_ENCRYPTION_PASSPHRASE: ${r"${{ secrets.GH_TOKEN_ENCRYPTION_PASSPHRASE }}"}
