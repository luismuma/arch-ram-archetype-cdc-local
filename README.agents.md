# AI Agents — Setup

## Required skill: `database-relacional`

This repository requires the `database-relacional` skill to generate or modify
code correctly. The skill contains the conventions, patterns, and best practices
for the MAPFRE Relational Database archetype (Liquibase, PostgreSQL, Oracle, MySQL, DB2).

---

## Step 1 — Check if `clai` is installed

Run in your terminal:

```bash
clai --version
```

- If you see a version number → **`clai` is installed**. Go to [Step 2](#step-2--install-the-skill).
- If you see `command not found` → **you need to install `clai`**. Follow [Step 1a](#step-1a--install-clai).

---

## Step 1a — Install `clai`

> If you already work with MAPFRE reference architectures that use Azure Artifacts
> for npm dependencies, you likely have the registry configured already.
> In that case skip directly to step **3**.

### 1. Add the MAPFRE npm registry

**macOS / Linux:**

```bash
echo '@mapfre-tech:registry=https://pkgs.dev.azure.com/devopsmapfre/devopsmapfre/_packaging/releases/npm/registry/' >> ~/.npmrc
echo 'always-auth=true' >> ~/.npmrc
```

**Windows (cmd):**

```cmd
echo @mapfre-tech:registry=https://pkgs.dev.azure.com/devopsmapfre/devopsmapfre/_packaging/releases/npm/registry/ >> %USERPROFILE%\.npmrc
echo always-auth=true >> %USERPROFILE%\.npmrc
```

### 2. Authenticate with Azure Artifacts

**Windows:**

```cmd
npx vsts-npm-auth -config %USERPROFILE%\.npmrc
```

A browser window will open to sign in.

**macOS / Linux:**

Generate a [Personal Access Token (PAT)](https://dev.azure.com/devopsmapfre/_usersSettings/tokens)
with scope **Packaging → Read & Write**, encode it in base64, and add it to `~/.npmrc`:

```bash
node -e "require('readline').createInterface({input:process.stdin,output:process.stdout,historySize:0}).question('PAT> ',p=>{console.log(Buffer.from(p.trim()).toString('base64'));process.exit()})"
```

Then add (replace `TOKEN_BASE64` with the value above):

```bash
cat >> ~/.npmrc << 'EOF'
//pkgs.dev.azure.com/devopsmapfre/devopsmapfre/_packaging/releases/npm/registry/:username=devopsmapfre
//pkgs.dev.azure.com/devopsmapfre/devopsmapfre/_packaging/releases/npm/registry/:_password=TOKEN_BASE64
//pkgs.dev.azure.com/devopsmapfre/devopsmapfre/_packaging/releases/npm/registry/:email=npm requires email to be set but doesn't use the value
//pkgs.dev.azure.com/devopsmapfre/devopsmapfre/_packaging/releases/npm/:username=devopsmapfre
//pkgs.dev.azure.com/devopsmapfre/devopsmapfre/_packaging/releases/npm/:_password=TOKEN_BASE64
//pkgs.dev.azure.com/devopsmapfre/devopsmapfre/_packaging/releases/npm/:email=npm requires email to be set but doesn't use the value
EOF
```

### 3. Authenticate GitHub CLI

```bash
gh auth login
```

### 4. Install `clai`

```bash
npm install -g @mapfre-tech/clai
```

### Verification

```bash
clai --version
```

---

## Step 2 — Install the skill

Once `clai` is installed, run the command for your tool:

```bash
# GitHub Copilot
clai skill install database-relacional

# Claude Code
clai skill install database-relacional --target claude-code

# OpenCode
clai skill install database-relacional --target opencode
```

Once installed, load the skill before responding to any code task in this repository.
