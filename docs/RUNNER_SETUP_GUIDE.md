# Self-Hosted Runner Setup Guide

Complete guide for configuring and troubleshooting the Windows self-hosted GitHub Actions runner.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Service Installation](#service-installation)
- [PATH Configuration](#path-configuration)
- [Troubleshooting](#troubleshooting)
- [Verification](#verification)
- [Tool Dependencies](#tool-dependencies)

## Prerequisites

### Required Software

1. **Git for Windows** (required for bash, curl, sha256sum, gpg)

   - Download: <<<https://git-scm.com/download/win>>>
   - During installation, ensure "Git from the command line and also from 3rd-party software" is selected
   - Verify installation:

     ```powershell

     where bash
     # Should show: C:\Program Files\Git\bin\bash.exe

```text

1. **GitHub Actions Runner** (already downloaded to `C:\actions-runner`)

   - Latest release: <<<https://github.com/actions/runner/releases>>>

### Recommended Software

- **PowerShell 7+**: <<<https://github.com/PowerShell/PowerShell/releases>>>
- **Windows Terminal**: <<<https://aka.ms/terminal>>>

## Service Installation

### Step 1: Obtain Registration Token

1. Navigate to: `<<<https://github.com/UndiFineD/DebVisor/settings/actions/runners/new`>>>
1. Copy the registration token (valid for 1 hour)

### Step 2: Remove Existing Configuration (if needed)

Open **PowerShell as Administrator**:

```powershell

cd C:\actions-runner

# Remove old configuration

.\config.cmd remove --token <YOUR_REMOVAL_TOKEN>

```text

### Step 3: Configure as Service

In the same **Administrator PowerShell**:

```powershell

cd C:\actions-runner

# Configure with service options

.\config.cmd `
  --url <https://github.com/UndiFineD/DebVisor> `
  --token <YOUR_NEW_TOKEN> `
  --runasservice `
  --windowslogonaccount "NT AUTHORITY\SYSTEM"

# Verify service was created

Get-Service | Where-Object Name -Like 'actions.runner*'

```text

### Step 4: Start Service

```powershell

# Find service name

$serviceName = (Get-Service | Where-Object Name -Like 'actions.runner*').Name

# Start service

Start-Service $serviceName

# Verify status

Get-Service $serviceName

# Check service is running

if ((Get-Service $serviceName).Status -eq 'Running') {
    Write-Host "✅ Runner service is running" -ForegroundColor Green
} else {
    Write-Host "❌ Runner service failed to start" -ForegroundColor Red
}

```text

### Why SYSTEM Account?

Running as `NT AUTHORITY\SYSTEM`:

- ✅ Has Administrator privileges (needed for Python symlinks)
- ✅ Runs automatically at boot (no login required)
- ✅ Has full disk access
- ✅ Can install software during workflows

## PATH Configuration

### Current Issue

Your terminal showed `jq` command failing, indicating PATH issues. Windows self-hosted runners need Git Bash tools in PATH.

### Check Current PATH

```powershell

# View PATH entries

$env:PATH -split ';' | Select-String -Pattern 'git|bash|bin'

# Check bash location

where.exe bash

# Check which bash is first

(Get-Command bash).Source

```text

### Fix PATH Order

Git Bash should appear **before** WSL bash:

#### Option A: System Environment Variables (Permanent)

1. Press `Win + X` → System
1. Advanced system settings → Environment Variables
1. Under "System variables", select `Path` → Edit
1. Ensure this order (move if needed):

   - `C:\Program Files\Git\cmd`
   - `C:\Program Files\Git\mingw64\bin`
   - `C:\Program Files\Git\usr\bin`
   - *(other entries)*
   - `C:\Windows\System32` (contains WSL)

1. Click OK, then restart the runner service:

   ```powershell

   Restart-Service actions.runner.*

```text

#### Option B: Runner Service PATH (Service-Specific)

Edit the service to include Git paths:

```powershell

# Get service details

$service = Get-Service -Name 'actions.runner.*'
$serviceName = $service.Name

# Stop service

Stop-Service $serviceName

# Add to service environment (requires registry edit)

# Navigate to: HKLM\SYSTEM\CurrentControlSet\Services\<serviceName>\Environment

# Add: PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\bin;%PATH%

# Or recreate service with updated config.cmd

```text

### Verify PATH After Fix

```powershell

# In new PowerShell window

bash -c 'echo $PATH'
bash -c 'which bash'
bash -c 'which curl'
bash -c 'which jq || echo "jq will be installed by setup script"'

```text

## Troubleshooting

### Service Won't Start

**Symptom**: `Start-Service` fails or service shows "Stopped"

**Solutions**:

1. Check event logs:

   ```powershell

   Get-EventLog -LogName Application -Source "actions.runner.*" -Newest 20

```text

1. Run interactively to see errors:

   ```powershell

   cd C:\actions-runner
   .\run.cmd
   # Watch for error messages

```text

1. Verify token hasn't expired (1-hour validity):

   - Generate fresh token from GitHub
   - Re-run `config.cmd`

### Python Setup Fails with "Administrator Privilege Required"

**Symptom**: Workflows using `actions/setup-python` fail with symlink errors

**Root Cause**: Service not running as SYSTEM or Administrator

**Solution**: Ensure service configured with `--windowslogonaccount "NT AUTHORITY\SYSTEM"` (see [Service Installation](#service-installation))

### Bash Commands Fail

**Symptom**: `gh: command not found`, `jq: command not found`, heredoc syntax errors

**Root Cause**: Wrong bash (WSL) or missing Git Bash in PATH

**Solutions**:

1. Fix PATH order (see [PATH Configuration](#path-configuration))
1. Verify workflow uses:

   ```yaml

   defaults:
     run:
       shell: bash

```text

1. Test manually:

   ```powershell

   bash -c 'echo $BASH_VERSION'
   # Should show: 5.x.x (Git Bash), not 4.x (WSL)

```text

### Linux Commands Fail (apt-get, sudo, etc.)

**Symptom**: `sudo: command not found`, `apt-get: not found`

**Root Cause**: Workflows written for Linux runners

**Solutions**:

1. Use portable tool installation (see `scripts/setup-runner-tools.sh`)
1. Replace `apt-get install jq` with:

   ```yaml

   - name: Install tools

     run: |
       chmod +x scripts/setup-runner-tools.sh
       ./scripts/setup-runner-tools.sh

```text

1. For unavoidable Linux requirements, consider:

   - Adding a Linux self-hosted runner
   - Using WSL2 within workflow steps (advanced)
   - Adapting commands for Windows (e.g., `choco install` instead of `apt-get`)

### Jobs Queue but Never Start

**Symptom**: Workflows show "Queued" indefinitely

**Possible Causes**:

1. **Runner offline**: Service not running

   ```powershell

   Get-Service actions.runner.* | Start-Service

```text

1. **Runner labels mismatch**: Workflow uses `runs-on: ubuntu-latest` instead of `runs-on: self-hosted`

1. **Multiple queues**: Check if jobs are waiting for hosted runners (billing issue)

   - View workflow YAML: ensure `runs-on: self-hosted`
   - Check GitHub billing limits

### OIDC Token Errors

**Symptom**: Cosign fails with "OIDC token unavailable"

**Solutions**:

1. Verify workflow permissions:

   ```yaml

   permissions:
     id-token: write  # Not 'read'
     contents: read

```text

1. Test OIDC in runner:

   ```bash

   # In workflow step
   echo "OIDC URL: $ACTIONS_ID_TOKEN_REQUEST_URL"
   echo "OIDC Token: ${ACTIONS_ID_TOKEN_REQUEST_TOKEN:0:20}..."

```text

1. If missing, runner may need reconfiguration or GitHub Actions environment issue

## Verification

### Run Smoke Test Workflow

After setup, test your runner:

```powershell

# Trigger smoke test via GitHub UI or gh CLI

gh workflow run runner-smoke-test.yml --ref main

```text

Or manually push to trigger:

```powershell

git add .github/workflows/runner-smoke-test.yml scripts/setup-runner-tools.sh
git commit -m "feat: add runner smoke test"
git push

```text

Check workflow run at: `<<<https://github.com/UndiFineD/DebVisor/actions/workflows/runner-smoke-test.yml`>>>

### Manual Verification

Test key components directly:

```powershell

# Start bash shell

bash

# Inside bash:

echo "Bash version: $BASH_VERSION"
curl --version
git --version
sha256sum --version
gpg --version || echo "GPG: Install Git for Windows or Gpg4win"

# Test jq install script

cd /c/Users/kdejo/DEV/DebVisor
chmod +x scripts/setup-runner-tools.sh
./scripts/setup-runner-tools.sh

# Verify tools

jq --version
cosign version

```text

## Tool Dependencies

### Installed via `setup-runner-tools.sh`

- **jq**: JSON processor (portable binary download)
- **cosign**: Container signing/verification (portable binary)

### Expected from Git for Windows

- **bash**: Shell interpreter
- **curl**: HTTP client
- **sha256sum**: Checksum utility
- **gpg**: GPG/PGP signing (in `C:\Program Files\Git\usr\bin`)
- **git**: Version control

### Optional (install manually if needed)

- **gh CLI**: GitHub command-line tool
- Download: <<<https://cli.github.com/>>>
- Install via `winget install GitHub.cli`

- **Docker Desktop**: For container workflows
- Download: <<<https://www.docker.com/products/docker-desktop>>>

## Next Steps

1. ✅ Install runner as service (follow [Service Installation](#service-installation))
1. ✅ Fix PATH to prioritize Git Bash (follow [PATH Configuration](#path-configuration))
1. ✅ Run smoke test workflow (see [Verification](#verification))
1. ✅ Review workflow audit results (check for Linux-only commands)
1. ✅ Update workflows to use `scripts/setup-runner-tools.sh`

## Support

- **Runner Documentation**: <<<https://docs.github.com/en/actions/hosting-your-own-runners>>>
- **Actions Troubleshooting**: <<<https://docs.github.com/en/actions/learn-github-actions/troubleshooting-github-actions>>>
- **Runner Logs**: `C:\actions-runner\_diag\` (when running interactively)
- **Service Logs**: Event Viewer → Windows Logs → Application → Source: actions.runner.*

## Quick Reference Commands

```powershell

# Service Management

Get-Service actions.runner.* | Format-List
Start-Service actions.runner.*
Stop-Service actions.runner.*
Restart-Service actions.runner.*

# Check Runner Status

Get-EventLog -LogName Application -Source "actions.runner.*" -Newest 5

# Interactive Mode (for debugging)

cd C:\actions-runner
.\run.cmd

# Reconfigure Runner

.\config.cmd remove --token <TOKEN>
.\config.cmd --url <https://github.com/UndiFineD/DebVisor> --token <TOKEN> --runasservice

# View Runner Info

Get-Content C:\actions-runner\.runner -Raw | ConvertFrom-Json | Format-List

```text
