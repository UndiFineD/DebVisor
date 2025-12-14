# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#Requires -RunAsAdministrator

<#
.SYNOPSIS
    Adds Git Bash and Python to System PATH for GitHub Actions Runner service
.DESCRIPTION
    The GitHub Actions Runner service runs under SYSTEM account and needs
    Git Bash in the System PATH to execute workflows with shell: bash.
    This script adds the required paths and restarts the runner service.
.NOTES
    Must be run as Administrator
#>

Write-Host "=== GitHub Actions Runner PATH Fix ===" -ForegroundColor Cyan
Write-Host ""

# Get current System PATH
$systemPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
$modified = $false

# Paths to add
$pathsToAdd = @(
    "C:\Program Files\Git\cmd",
    "C:\Program Files\Git\usr\bin",
    "C:\Program Files\Git\bin"
)

# Check Python location from user PATH
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    $pythonDir = Split-Path $pythonCmd.Path
    if (Test-Path $pythonDir) {
        $pathsToAdd += $pythonDir
        $pythonScripts = Join-Path $pythonDir "Scripts"
        if (Test-Path $pythonScripts) {
            $pathsToAdd += $pythonScripts
        }
    }
}

Write-Host "Checking paths to add:" -ForegroundColor Yellow
foreach ($path in $pathsToAdd) {
    if (Test-Path $path) {
        if ($systemPath -notlike "*$path*") {
            Write-Host "  [ADD] $path" -ForegroundColor Green
            $systemPath = "$systemPath;$path"
            $modified = $true
        } else {
            Write-Host "  [OK]  $path (already in PATH)" -ForegroundColor Gray
        }
    } else {
        Write-Host "  [SKIP] $path (not found)" -ForegroundColor Red
    }
}

if ($modified) {
    Write-Host "`nUpdating System PATH..." -ForegroundColor Yellow
    try {
        [Environment]::SetEnvironmentVariable("Path", $systemPath, "Machine")
        Write-Host "System PATH updated successfully" -ForegroundColor Green
    } catch {
        Write-Host "Failed to update System PATH: $_" -ForegroundColor Red
        exit 1
    }

    # Restart runner service
    Write-Host "`nRestarting GitHub Actions Runner service..." -ForegroundColor Yellow
    $service = Get-Service | Where-Object { $_.Name -like "actions.runner.*" }

    if ($service) {
        try {
            Restart-Service $service.Name -ErrorAction Stop
            Start-Sleep -Seconds 3
            $status = Get-Service $service.Name
            Write-Host "Service restarted: $($status.Status)" -ForegroundColor Green
        } catch {
            Write-Host "Failed to restart service: $_" -ForegroundColor Red
            Write-Host "Please restart the service manually:" -ForegroundColor Yellow
            Write-Host "Restart-Service $($service.Name)" -ForegroundColor White
        }
    } else {
        Write-Host "Runner service not found" -ForegroundColor Yellow
        Write-Host "You may need to restart it manually" -ForegroundColor Gray
    }

    Write-Host "`n=== Summary ===" -ForegroundColor Cyan
    Write-Host "System PATH has been updated with Git Bash and Python paths."
    Write-Host "The runner service should now be able to execute bash commands." -ForegroundColor Cyan
    Write-Host "Trigger a workflow to test: gh workflow run runner-smoke-test.yml" -ForegroundColor White
} else {
    Write-Host "`nAll required paths are already in System PATH" -ForegroundColor Green
    Write-Host "No changes needed." -ForegroundColor Gray
}

Write-Host ""
