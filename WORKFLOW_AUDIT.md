# Workflow Linux Dependency Audit

Workflows requiring Linux-specific commands that need adaptation for Windows self-hosted runner.

## Summary

**Critical**: Workflows using `nftables`, `iptables`, `systemd` cannot run on Windows and require a Linux self-hosted runner.

**Adaptable**: Workflows using `apt-get install` for common tools (shellcheck, markdownlint) can be adapted to use portable binaries.

---

## Workflows Requiring Linux Self-Hosted Runner

### 1. `blocklist-integration-tests.yml`

**Linux Dependencies**:

- `nftables` - Linux firewall framework (no Windows equivalent)
- `iptables` - Legacy Linux firewall (no Windows equivalent)
- `shellcheck` - Can be made portable

**Recommendation**: **Add a Linux self-hosted runner** OR disable these specific test jobs on Windows.

**Quick Fix** (add label filter):

```yaml

runs-on: [self-hosted, linux]  # Only run on Linux runners

```text

**Lines needing attention**:

- Line 113: `sudo apt-get install -y shellcheck` → Use portable binary
- Line 304: `sudo apt-get install -y nftables` → **Requires Linux**
- Line 327-328: `sudo nft` commands → **Requires Linux**
- Line 339: `sudo apt-get install -y iptables` → **Requires Linux**

### 2. `validate-syntax.yml`

**Linux Dependencies**:

- `systemd` - Linux init system (no Windows equivalent)

**Recommendation**: **Requires Linux runner** for systemd unit validation.

**Lines**:

- Line 27-28: `sudo apt-get update && sudo apt-get install -y systemd`

**Alternative**: Skip systemd validation on Windows or use a Linux-specific job.

---

## Workflows That Can Be Adapted

### 3. `lint.yml`

**Current Linux Commands**:

- Line 81: `sudo apt-get install -y shellcheck`
- Line 95: `sudo npm install -g markdownlint-cli`

**Adaptation Strategy**:

#### ShellCheck (Portable)

Replace:

```yaml

- name: Install ShellCheck

  run: sudo apt-get install -y shellcheck

```text

With:

```yaml

- name: Install ShellCheck

  run: |
    if [ "$RUNNER_OS" = "Linux" ]; then
      sudo apt-get update && sudo apt-get install -y shellcheck
    elif [ "$RUNNER_OS" = "Windows" ]; then
      # Download portable binary
      mkdir -p tools
      curl -sSL <https://github.com/koalaman/shellcheck/releases/download/v0.9.0/shellcheck-v0.9.0.windows.x86_64.zip> -o shellcheck.zip
      unzip -q shellcheck.zip -d tools
      mv tools/shellcheck-v0.9.0/shellcheck.exe tools/
      echo "$(pwd)/tools" >> $GITHUB_PATH
    else
      echo "Unsupported OS: $RUNNER_OS"
      exit 1
    fi

```text

#### Markdownlint

Already uses npm (cross-platform), but needs `sudo` removed:

```yaml

- name: Install markdownlint

  run: npm install -g markdownlint-cli  # Remove sudo

```text

---

## Recommended Actions

### Option 1: Add Linux Self-Hosted Runner (Recommended)

**Pros**:

- Native support for all Linux tools
- No workflow modifications needed
- Better for firewall/network testing

**Steps**:

1. Set up Ubuntu VM or WSL2 instance
1. Install GitHub Actions runner
1. Configure with label: `self-hosted,linux`
1. Update workflows:

   ```yaml

   runs-on: [self-hosted, linux]  # For Linux-only jobs
   runs-on: [self-hosted, windows]  # For Windows jobs
   runs-on: self-hosted  # For either (will pick first available)

```text

### Option 2: Adapt Workflows for Windows (Partial)

**Pros**:

- Single runner setup
- Simpler infrastructure

**Cons**:

- Cannot test firewall features (nftables/iptables)
- Cannot validate systemd units
- Some integration tests will be skipped

**Implementation**:

1. Use `scripts/setup-runner-tools.sh` pattern
1. Create `scripts/install-shellcheck.sh`:

   ```bash

   #!/usr/bin/env bash
   set -e

   if command -v shellcheck &>/dev/null; then
     echo "shellcheck already installed"
     exit 0
   fi

   TOOLS_DIR="${TOOLS_DIR:-$(pwd)/tools}"
   mkdir -p "$TOOLS_DIR"

   case "$RUNNER_OS" in
     Windows)
       curl -sSL <https://github.com/koalaman/shellcheck/releases/download/v0.9.0/shellcheck-v0.9.0.windows.x86_64.zip> -o /tmp/sc.zip
       unzip -q /tmp/sc.zip -d "$TOOLS_DIR"
       mv "$TOOLS_DIR/shellcheck-v0.9.0/shellcheck.exe" "$TOOLS_DIR/"
       rm -rf "$TOOLS_DIR/shellcheck-v0.9.0"
       ;;
     Linux)
       sudo apt-get update && sudo apt-get install -y shellcheck
       ;;
     macOS)
       brew install shellcheck
       ;;
   esac

   echo "$TOOLS_DIR" >> "$GITHUB_PATH"

```text

1. Update workflows to call installation script
1. Add `if: runner.os == 'Linux'` to firewall/systemd steps

### Option 3: Hybrid Approach

- Windows runner: General CI (lint, tests, builds)
- Linux runner: Firewall tests, systemd validation, security scanning
- Use job-level `runs-on` to target specific runners

---

## Workflow-by-Workflow Action Plan

| Workflow | Adaptation | Priority |
|----------|-----------|----------|
| `blocklist-integration-tests.yml` | Add Linux runner OR disable firewall tests | High |
| `validate-syntax.yml` | Add Linux runner OR skip systemd validation | Medium |
| `lint.yml` | Install shellcheck portably; remove `sudo` from npm | Low |
| `release-reverify.yml` | ✅ Already adapted (API + portable tools) | Done |
| `runner-smoke-test.yml` | ✅ Already cross-platform | Done |

---

## Next Steps

1. **Immediate**: Update `lint.yml` to use portable shellcheck and remove `sudo` from npm
1. **Short-term**: Decide on Linux runner strategy (dedicated VM, WSL2, or cloud instance)
1. **Medium-term**: Implement runner labels (`self-hosted,linux` vs `self-hosted,windows`)
1. **Long-term**: Create reusable composite actions for tool installation

---

## Sample: Conditional Job Execution

```yaml

jobs:
  test-windows:
    runs-on: [self-hosted, windows]
    steps:

      - name: Windows-specific test

        run: echo "Running on Windows"

  test-linux:
    runs-on: [self-hosted, linux]
    steps:

      - name: Linux-specific test

        run: |
          sudo apt-get update
          echo "Running on Linux"

  test-cross-platform:
    runs-on: self-hosted  # Any available
    steps:

      - name: OS detection

        run: echo "OS is $RUNNER_OS"

      - name: Linux-only step

        if: runner.os == 'Linux'
        run: sudo systemctl --version

      - name: Windows-only step

        if: runner.os == 'Windows'
        run: Get-Service | Select-Object -First 5
        shell: pwsh

```text

---

## References

- ShellCheck portable releases: <https://github.com/koalaman/shellcheck/releases>
- Runner labels documentation: <https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/using-labels-with-self-hosted-runners>
- Conditional execution: <https://docs.github.com/en/actions/learn-github-actions/expressions>
