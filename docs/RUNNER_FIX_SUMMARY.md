# Self-Hosted Runner Fixes - Implementation Summary

## ✅ Completed Fixes

### 1. Portable Tool Installation Script

**File**: `scripts/setup-runner-tools.sh`

Cross-platform script that installs:

- **jq**: JSON processor (downloads portable binary for Windows/Linux/macOS)
- **cosign**: Container signing tool (downloads portable binary)
- **gpg**: Checks availability and guides installation

**Usage in workflows**:

```yaml

- name: Setup Tools

  run: |
    chmod +x scripts/setup-runner-tools.sh
    ./scripts/setup-runner-tools.sh

```text

### 2. Runner Smoke Test Workflow

**File**: `.github/workflows/runner-smoke-test.yml`

Validates runner environment:

- ✅ Bash version and shell features
- ✅ Core tools (curl, git, sha256sum)
- ✅ Installed tools (jq, cosign, gpg)
- ✅ GitHub API access
- ✅ OIDC token availability

**Trigger**: Manual dispatch or push to main

### 3. Release Reverification Workflow Update

**File**: `.github/workflows/release-reverify.yml`

**Changes**:

- ❌ Removed: `apt-get install jq` and `gh CLI` dependency
- ✅ Added: Portable tool setup using shared script
- ✅ Added: GitHub REST API + curl + jq for release operations
- ✅ Fixed: `id-token: write` permission for OIDC
- ✅ Added: `defaults.run.shell: bash` for consistency

**Now cross-platform compatible** for Windows/Linux self-hosted runners.

### 4. Comprehensive Setup Guide

**File**: `RUNNER_SETUP_GUIDE.md`

Complete documentation covering:

- **Service Installation**: Step-by-step Windows service setup with SYSTEM account
- **PATH Configuration**: Fixing Git Bash precedence over WSL
- **Troubleshooting**: Common issues and solutions
- Service won't start
- Python symlink failures
- Bash command failures
- OIDC token errors
- **Verification**: Testing steps and smoke test instructions
- **Tool Dependencies**: What's needed and where to get it
- **Quick Reference**: PowerShell commands for service management

### 5. Workflow Audit & Remediation Plan

**File**: `WORKFLOW_AUDIT.md`

**Identified Issues**:

- **Critical**: `blocklist-integration-tests.yml` uses nftables/iptables (Linux-only)
- **Critical**: `validate-syntax.yml` uses systemd (Linux-only)
- **Adaptable**: `lint.yml` uses apt-get for shellcheck (can use portable binary)

**Recommendations**:

1. **Option 1** (Recommended): Add Linux self-hosted runner for firewall/systemd tests
1. **Option 2**: Adapt workflows to skip Linux-specific steps on Windows
1. **Option 3**: Hybrid approach with runner labels (`self-hosted,linux` vs `self-hosted,windows`)

### 6. Strategic Shift: GitHub-Hosted Runners (December 2025)

**Context**:
Self-hosted Windows runners proved problematic for Linux-centric workflows (`lint.yml`, `manifest-validation.yml`) due to missing tools (`shellcheck`, `kubeconform`) and OS differences (`tar`, `find`).

**Decision**:
Migrated the following workflows to `ubuntu-latest` (GitHub-hosted runners) to ensure stability and standard tool availability:

- `lint.yml` (ShellCheck, Flake8, Black)
- `manifest-validation.yml` (Kubeconform, Kube-linter, Pluto, Helm Lint)

**Outcome**:

- Eliminated "End-of-central-directory" unzip errors.
- Eliminated path separator and command compatibility issues.
- Simplified workflow maintenance by using standard actions.

---

## 🔧 Manual Steps Still Required

### Priority 1: Install Runner as Service

**Current Issue**: Runner fails to start (exit code 1) because:

- Not running with Administrator privileges
- Configuration attempted without elevation

**Solution** (Run in **Administrator PowerShell**):

```powershell

# Step 1: Get new registration token

# Visit: <https://github.com/UndiFineD/DebVisor/settings/actions/runners/new>

# Step 2: Navigate to runner directory

cd C:\actions-runner

# Step 3: Remove old configuration (if needed)

.\config.cmd remove --token <OLD_TOKEN>

# Step 4: Configure as service

.\config.cmd `
  --url <https://github.com/UndiFineD/DebVisor> `
  --token <NEW_TOKEN> `
  --runasservice `
  --windowslogonaccount "NT AUTHORITY\SYSTEM"

# Step 5: Start service

$serviceName = (Get-Service | Where-Object Name -Like 'actions.runner*').Name
Start-Service $serviceName

# Step 6: Verify

Get-Service $serviceName

```text

**Why This Fixes It**:

- SYSTEM account has Administrator privileges (fixes Python symlink issues)
- Service runs automatically at boot
- No user login required

### Priority 2: Fix PATH Order

**Current Issue**: `jq` command fails in terminal (seen in context: exit code 1)

**Likely Cause**: WSL bash taking precedence over Git Bash

**Verification**:

```powershell

where.exe bash

# Should show Git Bash FIRST:

# C:\Program Files\Git\bin\bash.exe

# C:\Windows\System32\bash.exe (WSL)

```text

**Solution**:

1. Press `Win + X` → System → Advanced system settings
1. Environment Variables → System variables → Path → Edit
1. Move these to **top of list**:

   - `C:\Program Files\Git\cmd`
   - `C:\Program Files\Git\mingw64\bin`
   - `C:\Program Files\Git\usr\bin`

1. Restart runner service:

   ```powershell

   Restart-Service actions.runner.*

```text

### Priority 3: Run Smoke Test

After service install and PATH fix:

```powershell

# Option A: Via GitHub UI

# Navigate to: <https://github.com/UndiFineD/DebVisor/actions/workflows/runner-smoke-test.yml>

# Click "Run workflow"

# Option B: Via gh CLI (if installed)

gh workflow run runner-smoke-test.yml --ref main

# Option C: Push trigger (already enabled)

# Workflow will run automatically on next push to main

```text

---

## 📊 Current Runner Status

**Environment**:

- Location: `C:\actions-runner`
- Configuration: `.runner` file present (workFolder set to `_work`)
- Status: **Not running as service** (manual execution exits with code 1)

**Git Environment**:

- Git for Windows: ✅ Installed (`C:\Program Files\Git`)
- Bash: ✅ Available (may have PATH precedence issue)
- GPG: ✅ Available in Git for Windows (`usr/bin/gpg.exe`)

**Workflow Status**:

- Migration: ✅ All workflows use `runs-on: self-hosted`
- Shell: ✅ All workflows use `defaults.run.shell: bash`
- Permissions: ✅ Fixed `id-token: write` for OIDC
- Dependencies: ⚠️ Some workflows still have Linux-only commands

---

## 🎯 Next Actions (Ordered by Priority)

### Immediate (Blocks all workflow execution)

1. ✅ **Install runner as Windows service** (see Priority 1 above)
1. ✅ **Fix PATH order** to prioritize Git Bash (see Priority 2 above)
1. ✅ **Run smoke test** to validate environment (see Priority 3 above)

### Short-term (Fixes specific workflows)

1. **Decide on Linux runner strategy**:

   - Option A: Add Ubuntu VM as second self-hosted runner
   - Option B: Use WSL2 for Linux-specific jobs (advanced)
   - Option C: Disable Linux-only tests temporarily

1. **Update `lint.yml`** to use portable shellcheck:

   ```yaml

   - name: Install ShellCheck

     run: |
       chmod +x scripts/install-shellcheck.sh
       ./scripts/install-shellcheck.sh

```text

1. **Add runner labels** (if using multiple runners):

   ```yaml

   runs-on: [self-hosted, windows]  # For Windows-specific
   runs-on: [self-hosted, linux]    # For Linux-specific

```text

### Long-term (Optimization)

1. **Create composite actions** for common setup patterns
1. **Monitor runner performance** and resource usage
1. **Set up runner auto-updates** via scheduled task
1. **Document runner maintenance procedures**

---

## 📝 Files Changed

| File | Change Type | Purpose |
|------|-------------|---------|
| `scripts/setup-runner-tools.sh` | Created | Portable tool installation |
| `.github/workflows/runner-smoke-test.yml` | Created | Environment validation |
| `.github/workflows/release-reverify.yml` | Modified | Removed gh CLI, added API calls |
| `RUNNER_SETUP_GUIDE.md` | Created | Service setup documentation |
| `WORKFLOW_AUDIT.md` | Created | Linux dependency analysis |

---

## 🔍 Validation Checklist

After completing manual steps, verify:

- [ ] Runner service status: `Get-Service actions.runner.* | Format-List`
- [ ] Service is running: Status should be "Running"
- [ ] Bash version: `bash -c 'echo $BASH_VERSION'` (should be 5.x, not 4.x)
- [ ] Bash location: `where.exe bash` (Git Bash should be first)
- [ ] jq available: `bash -c 'command -v jq'`
- [ ] Smoke test passes: Check workflow run at Actions tab
- [ ] No startup_failure in workflow runs
- [ ] Python workflows succeed (setup-python creates symlinks)

---

## 📚 Documentation References

- **Setup Guide**: `RUNNER_SETUP_GUIDE.md` - Complete service installation and troubleshooting
- **Workflow Audit**: `WORKFLOW_AUDIT.md` - Linux dependency analysis and remediation
- **Tool Setup Script**: `scripts/setup-runner-tools.sh` - Portable tool installation
- **Smoke Test**: `.github/workflows/runner-smoke-test.yml` - Environment validation

---

## 🆘 Support

If issues persist after following manual steps:

1. **Check Service Logs**:

   ```powershell

   Get-EventLog -LogName Application -Source "actions.runner.*" -Newest 20

```text

1. **Run Interactively** (for debugging):

   ```powershell

   cd C:\actions-runner
   .\run.cmd
   # Watch for error messages in console

```text

1. **Verify Git Bash Tools**:

   ```powershell

   bash -c 'which curl git sha256sum gpg jq'

```text

1. **Check GitHub Actions Documentation**:

   - Runner docs: <<https://docs.github.com/en/actions/hosting-your-own-runners>>
   - Windows service: <<https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/configuring-the-self-hosted-runner-application-as-a-service>>

---

**Status**: All code fixes completed and pushed. Manual service installation required to activate runner.
