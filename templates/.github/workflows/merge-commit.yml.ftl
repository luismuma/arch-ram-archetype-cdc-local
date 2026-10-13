# Copyright (c) MAPFRE DevOps Platform
#
# Merge Commit Workflow. Triggers when:
#   - A pull request to develop is closed and merged
#   - A pull request to main is closed and merged
#
# acr-folder: The folder where the artifact will be stored in the Azure Container Registry. More information about naming conventions can be found here https://marketplace.mapfre.com/docs/default/mapfredocument/devopsplatformdoc/github-azure-container-registry/#using-azure-container-registry-on-github
# Required secrets:
#   - AZURE_ARTIFACTS_USER    (Organization)
#   - AZURE_ARTIFACTS_PW      (Organization)
#   - GH_TOKEN_ENCRYPTION_PASSPHRASE (Organization) more info in: https://docs.zeus.mapfre.com/8ba7b8109dad11d180b400c04fd430cf/1f7094066cf557db9391713055249220

name: Merge Commit

run-name: "Generate ${r"${{ fromJson(github.base_ref == 'main' || github.base_ref == 'master') && 'Release' || 'Snapshot' }}"} Artifact #${r"${{ github.run_number }}"}"

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
    uses: luismuma/arch-ram-reusable-workflows/.github/workflows/cdc.tests.merge-commit.yml@main
    secrets:
      AZURE_ARTIFACTS_USER: ${r"${{ secrets.AZURE_ARTIFACTS_USER }}"}
      AZURE_ARTIFACTS_PW: ${r"${{ secrets.AZURE_ARTIFACTS_PW }}"}
      GH_TOKEN_ENCRYPTION_PASSPHRASE: ${r"${{ secrets.GH_TOKEN_ENCRYPTION_PASSPHRASE }}"}