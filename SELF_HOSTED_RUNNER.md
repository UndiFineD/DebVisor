# Self-Hosted GitHub Actions Runner Setup

## Overview

This repository uses a self-hosted GitHub Actions runner to execute CI/CD workflows on local infrastructure. This provides better control over resources, permissions, and access to local services.

## Benefits

- **Permissions**: Full control over repository and workflow permissions
- **Resources**: Use your own hardware specifications
- **Local Access**: Test against local Ceph clusters, VMs, networks
- **Cost**: No GitHub Actions minutes consumed
- **Customization**: Install any tools, dependencies, or services needed

## Prerequisites

- Windows 10/11 or Windows Server 2019+
- PowerShell 5.1 or later
- Administrator access (for service installation)
- Network access to GitHub (<https://github.com>)

## Installation Steps

### 1. Download and Extract Runner

```powershell

# Create runner directory

mkdir C:\actions-runner
cd C:\actions-runner

# Download latest runner package

Invoke-WebRequest -Uri <https://github.com/actions/runner/releases/download/v2.329.0/actions-runner-win-x64-2.329.0.zip> -OutFile actions-runner-win-x64-2.329.0.zip

# Validate checksum (recommended)

if((Get-FileHash -Path actions-runner-win-x64-2.329.0.zip -Algorithm SHA256).Hash.ToUpper() -ne 'f60be5ddf373c52fd735388c3478536afd12bfd36d1d0777c6b855b758e70f25'.ToUpper()) {
    throw 'Computed checksum did not match'
}

# Extract

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD/actions-runner-win-x64-2.329.0.zip", "$PWD")

```text

### 2. Configure Runner

**Note**: The token in configuration commands expires after 1 hour. Get a fresh token from:
<https://github.com/UndiFineD/DebVisor/settings/actions/runners/new>

```powershell

# Configure runner (replace TOKEN with fresh token from GitHub)

./config.cmd --url <https://github.com/UndiFineD/DebVisor> --token YOUR_TOKEN_HERE

# Follow prompts:

# - Runner name: [default or custom name like "debvisor-windows-1"]

# - Runner group: [press Enter for default]

# - Labels: [press Enter for default, or add custom like "windows,x64,debvisor"]

# - Work folder: [press Enter for default "_work"]

```text

### 3. Run as Service (Recommended)

Running as a Windows service ensures the runner starts automatically:

```powershell

# Install as service (requires Administrator)

./svc.sh install

# Start service

./svc.sh start

# Check status

./svc.sh status

```text

### 4. Manual Run (Development/Testing)

For testing or development, you can run the runner interactively:

```powershell

./run.cmd

```text

Press Ctrl+C to stop.

## Using the Self-Hosted Runner

### Update Workflow Files

Modify workflow files in `.github/workflows/` to use the self-hosted runner:

```yaml

jobs:
  build:
    runs-on: self-hosted  # Changed from: ubuntu-latest

    steps:

      - uses: actions/checkout@v4

      # ... rest of workflow

```text

### Runner Labels

You can target specific runners using labels:

```yaml

jobs:
  build:
    runs-on: [self-hosted, windows, x64]  # Multiple labels

```text

## Required Software on Runner

For DebVisor CI/CD to work, ensure the following are installed on the runner machine:

### Essential Tools

- **Python 3.8+**: For running tests and scripts

  ```powershell

  winget install Python.Python.3.11

```text

- **Git**: For repository operations

  ```powershell

  winget install Git.Git

```text

- **Node.js**: For npm packages (markdownlint, etc.)

  ```powershell

  winget install OpenJS.NodeJS.LTS

```text

### Development Tools

- **GCC/Build Tools**: For compiling Python extensions

  ```powershell

  winget install Microsoft.VisualStudio.2022.BuildTools

```text

- **Docker Desktop**: For container-based workflows (optional)

  ```powershell

  winget install Docker.DockerDesktop

```text

### Python Dependencies

The runner will automatically install Python dependencies from `requirements.txt`, but you can pre-install them:

```powershell

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

```text

### Testing Tools

```powershell

# Linting and formatting

pip install flake8 black pylint mypy

# Security scanning

pip install bandit safety

# Testing

pip install pytest pytest-cov pytest-asyncio

# SBOM generation

pip install cyclonedx-bom

# Markdown linting

npm install -g markdownlint-cli

```text

## Runner Management

### Check Runner Status

On GitHub:

1. Go to <https://github.com/UndiFineD/DebVisor/settings/actions/runners>
1. Look for your runner (green dot = online, gray = offline)

On the runner machine:

```powershell

cd C:\actions-runner
./svc.sh status

```text

### Update Runner

```powershell

# Stop service

./svc.sh stop

# Download new version

Invoke-WebRequest -Uri <https://github.com/actions/runner/releases/download/v2.XXX.X/actions-runner-win-x64-2.XXX.X.zip> -OutFile actions-runner-win-x64-2.XXX.X.zip

# Extract and overwrite

# ...

# Start service (2)

./svc.sh start

```text

### Remove Runner

```powershell

# Stop and uninstall service

./svc.sh stop
./svc.sh uninstall

# Remove runner from GitHub

./config.cmd remove --token YOUR_TOKEN_HERE

```text

## Troubleshooting

### Runner Offline

**Symptoms**: Runner shows as offline in GitHub settings

**Solutions**:

1. Check if service is running:

   ```powershell

   ./svc.sh status

```text

1. Check network connectivity:

   ```powershell

   Test-NetConnection github.com -Port 443

```text

1. Review runner logs:

   ```powershell

   Get-Content C:\actions-runner\_diag\Runner_*.log -Tail 50

```text

### Permission Errors

**Symptoms**: Workflows fail with permission denied errors

**Solutions**:

1. Run service as user with appropriate permissions
1. Grant runner service account access to required resources
1. Check folder permissions on `C:\actions-runner\_work`

### Workflow Fails with "Command not found"

**Symptoms**: Commands like `python`, `git`, `npm` not found

**Solutions**:

1. Ensure tools are installed (see Required Software section)
1. Add tools to system PATH
1. Restart runner service after PATH changes:

   ```powershell

   ./svc.sh stop
   ./svc.sh start

```text

### Token Expired

**Symptoms**: Configuration fails with "invalid token"

**Solutions**:

1. Tokens expire after 1 hour
1. Generate new token: <https://github.com/UndiFineD/DebVisor/settings/actions/runners/new>
1. Copy and use immediately

## Security Considerations

### Runner Isolation

- Self-hosted runners can access your local network
- Only use self-hosted runners for trusted repositories
- Consider network isolation (VLAN, firewall rules)
- Use dedicated user account with minimal permissions

### Secrets Management

- GitHub secrets are available to self-hosted runners
- Ensure runner machine is secured
- Use Windows Credential Manager for additional secrets
- Rotate secrets regularly

### Updates

- Keep runner software updated
- Update OS and security patches regularly
- Monitor GitHub security advisories

## Monitoring

### Runner Logs

Located in `C:\actions-runner\_diag\`:

- `Runner_*.log`: Main runner logs
- `Worker_*.log`: Job execution logs

### Performance Metrics

Monitor:

- CPU usage during workflow runs
- Disk space in `_work` directory
- Network bandwidth
- Memory usage

### Cleanup

Automatically cleans up after each job, but you can manually clean:

```powershell

# Remove old logs

Remove-Item C:\actions-runner\_diag\*.log -Older (Get-Date).AddDays(-30)

# Clean work directory (careful!)

Remove-Item C:\actions-runner\_work\* -Recurse -Force

```text

## Multiple Runners

To run multiple runners on the same machine:

```powershell

# Create separate directories

mkdir C:\actions-runner-1
mkdir C:\actions-runner-2

# Configure each with different names

cd C:\actions-runner-1
./config.cmd --url <https://github.com/UndiFineD/DebVisor> --token TOKEN1 --name runner-1

cd C:\actions-runner-2
./config.cmd --url <https://github.com/UndiFineD/DebVisor> --token TOKEN2 --name runner-2

# Install as separate services

cd C:\actions-runner-1
./svc.sh install
./svc.sh start

cd C:\actions-runner-2
./svc.sh install
./svc.sh start

```text

## Troubleshooting (2)

### Runner Stuck in "Busy" State (Zombie Job)

If the runner appears `online` and `busy` in GitHub settings, but no jobs are running (or `gh run list --status in_progress` returns 0), the runner process might be desynchronized.

**Symptoms:**

- GitHub Actions queue is stuck (jobs are "Queued" but not starting).
- Runner logs (`_diag` folder) show it renewing a job ID that doesn't exist in GitHub.

**Resolution:**
Force restart the runner service to kill the zombie process.

```powershell

# Run as Administrator

Stop-Service "actions.runner.UndiFineD-DebVisor.DESKTOP-F4EG0P1" -Force

# Wait 30 seconds

Start-Service "actions.runner.UndiFineD-DebVisor.DESKTOP-F4EG0P1"

```text

### Check Runner Logs

Logs are located in the `_diag` folder within the runner installation directory (e.g., `C:\actions-runner\_diag`).

```powershell

# View the last 20 lines of the most recent log

Get-ChildItem "C:\actions-runner\_diag\*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | Get-Content -Tail 20

```text

## Next Steps

1. ? Install runner (follow Installation Steps)
1. ? Install required software (see Required Software section)
1. ? Update workflow files to use `runs-on: self-hosted`
1. ? Test with a simple workflow
1. ? Monitor first few runs for issues
1. ? Configure runner as Windows service for auto-start

## References

- [GitHub Self-Hosted Runners Documentation](https://docs.github.com/en/actions/hosting-your-own-runners)
- [Runner Releases](https://github.com/actions/runner/releases)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
