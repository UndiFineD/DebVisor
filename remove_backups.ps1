#!/usr/bin/env pwsh
<#
.SYNOPSIS
Removes all *.md.backup files from the workspace.

.DESCRIPTION
This script recursively searches for and removes all markdown backup files (*.md.backup)
in the current directory and all subdirectories.

.PARAMETER Path
The root path to search for backup files. Defaults to current directory.

.PARAMETER DryRun
If specified, shows what would be deleted without actually deleting.

.EXAMPLE
.\remove_backups.ps1
# Removes all *.md.backup files in current directory and subdirectories

.EXAMPLE
.\remove_backups.ps1 -DryRun
# Shows what would be deleted without actually deleting

.EXAMPLE
.\remove_backups.ps1 -Path "C:\MyProject"
# Removes all *.md.backup files in C:\MyProject and subdirectories
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$Path = ".",
    
    [Parameter(Mandatory=$false)]
    [switch]$DryRun = $false
)

# Resolve to absolute path
$AbsPath = (Resolve-Path $Path).Path

Write-Host "🔍 Searching for backup files in: $AbsPath" -ForegroundColor Cyan

# Find all backup files
$BackupFiles = @(Get-ChildItem -Path $AbsPath -Recurse -Filter "*.md.backup" -File -ErrorAction SilentlyContinue)

if ($BackupFiles.Count -eq 0) {
    Write-Host "✅ No backup files found." -ForegroundColor Green
    exit 0
}

Write-Host "📊 Found $($BackupFiles.Count) backup file(s):" -ForegroundColor Yellow
Write-Host ""

# Display files to be removed
foreach ($file in $BackupFiles) {
    $size = [math]::Round($file.Length / 1KB, 2)
    Write-Host "  • $($file.FullName) ($size KB)" -ForegroundColor Gray
}

Write-Host ""

if ($DryRun) {
    Write-Host "🔄 DRY RUN MODE - No files will be deleted" -ForegroundColor Yellow
    exit 0
}

# Confirm deletion
Write-Host "⚠️  Ready to delete $($BackupFiles.Count) backup file(s)." -ForegroundColor Yellow
$confirmation = Read-Host "Continue? (yes/no)"

if ($confirmation -ne "yes" -and $confirmation -ne "y") {
    Write-Host "❌ Cancelled - No files deleted." -ForegroundColor Red
    exit 1
}

# Remove files
$successCount = 0
$failCount = 0

foreach ($file in $BackupFiles) {
    try {
        Remove-Item -Path $file.FullName -Force -ErrorAction Stop
        Write-Host "🗑️  Deleted: $($file.Name)" -ForegroundColor Green
        $successCount++
    }
    catch {
        Write-Host "❌ Failed to delete: $($file.Name)" -ForegroundColor Red
        Write-Host "   Error: $_" -ForegroundColor Red
        $failCount++
    }
}

Write-Host ""
Write-Host "✅ Operation Complete:" -ForegroundColor Green
Write-Host "   Deleted: $successCount file(s)" -ForegroundColor Green
if ($failCount -gt 0) {
    Write-Host "   Failed: $failCount file(s)" -ForegroundColor Red
}

if ($failCount -gt 0) {
    exit 1
} else {
    exit 0
}
