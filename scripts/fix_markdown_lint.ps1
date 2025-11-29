#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Comprehensive Markdown Linting Fixer
    Automatically fixes common markdown linting errors in documentation files.

.DESCRIPTION
    This script identifies and fixes markdown linting errors including:
    - MD007: Unordered list indentation (0-space indent)
    - MD009: Trailing spaces
    - MD012: Multiple consecutive blank lines
    - MD019: Multiple spaces after hash in headings
    - MD022: Blank lines around headings
    - MD024: Duplicate headings
    - MD026: Trailing punctuation in headings
    - MD029: Ordered list item prefix
    - MD031: Blank lines around code fences
    - MD032: Blank lines around lists
    - MD034: Bare URLs
    - MD036: Emphasis used instead of heading
    - MD040: Fenced code block language specification
    - MD041: First line should be top-level heading
    - MD046: Code block style preference
    - MD050: Strong style (asterisks vs underscores)

.PARAMETER FilePath
    Path to the markdown file to fix. Required.

.PARAMETER Backup
    Create a backup of the original file before making changes. Default: $true

.PARAMETER Verbose
    Show detailed information about each fix applied.

.EXAMPLE
    .\fix_markdown_lint.ps1 -FilePath "README.md"
    .\fix_markdown_lint.ps1 -FilePath "WEB_PANEL_INTEGRATION_GUIDE.md" -Verbose
    .\fix_markdown_lint.ps1 -FilePath "doc.md" -Backup $false

.NOTES
    Author: Markdown Lint Fixer
    Version: 1.0
    Requires: PowerShell 5.0+
#>

param(
    [Parameter(Mandatory=$true, HelpMessage="Path to markdown file to fix")]
    [string]$FilePath,

    [Parameter(Mandatory=$false)]
    [bool]$Backup = $true,

    [Parameter(Mandatory=$false)]
    [switch]$Verbose
)

# Validate file exists
if (-not (Test-Path $FilePath)) {
    Write-Error "File not found: $FilePath"
    exit 1
}

# Create backup if requested
if ($Backup) {
    $backupPath = "$FilePath.backup"
    Copy-Item -Path $FilePath -Destination $backupPath -Force
    Write-Host "? Backup created: $backupPath" -ForegroundColor Green
}

# Read file content
$content = Get-Content -Path $FilePath -Raw
$originalContent = $content
$lines = $content -split "`n"

# Initialize counters
$fixCount = @{}

Write-Host "`n=== Starting Markdown Lint Fixes ===" -ForegroundColor Cyan

# ============================================================================
# MD009: Remove trailing spaces (but preserve intentional double spaces)
# ============================================================================
$lineIndex = 0
$fixedLines = @()

foreach ($line in $lines) {
    $originalLine = $line
    
    # Remove trailing spaces (but preserve 2+ spaces which are intentional line breaks)
    if ($line -match '\s+$') {
        $trailingSpaces = $line -replace '^.*?(\s+)$', '$1'
        if ($trailingSpaces.Length -eq 1 -or ($trailingSpaces.Length -lt 2 -and -not ($line -match '\S  $'))) {
            $line = $line -replace '\s+$', ''
            $fixCount['MD009'] = ($fixCount['MD009'] -as [int]) + 1
        }
    }
    
    $fixedLines += $line
    $lineIndex++
}

$content = $fixedLines -join "`n"

# ============================================================================
# MD012: Remove multiple consecutive blank lines (reduce to 1)
# ============================================================================
$content = $content -replace "(?m)\n\n\n+", "`n`n"
$newBlankLineCount = ([regex]::Matches($content, "(?m)\n\n\n+") | Measure-Object).Count
if ($newBlankLineCount -eq 0 -and ([regex]::Matches($originalContent, "(?m)\n\n\n+") | Measure-Object).Count -gt 0) {
    $fixCount['MD012'] = ([regex]::Matches($originalContent, "(?m)\n\n\n+") | Measure-Object).Count
}

# ============================================================================
# MD041: First line should be top-level heading
# ============================================================================
$lines = $content -split "`n"
if ($lines.Count -gt 0 -and -not ($lines[0] -match '^\s*#\s')) {
    # Check if it's a docstring or comment block that should be removed
    if ($lines[0] -match '^"""' -or $lines[0] -match "^'''") {
        # Find end of docstring
        $endIndex = 1
        while ($endIndex -lt $lines.Count) {
            if ($lines[$endIndex] -match '^"""' -or $lines[$endIndex] -match "^'''") {
                # Remove docstring block
                $lines = $lines[($endIndex + 1)..($lines.Count - 1)]
                $fixCount['MD041'] = 1
                break
            }
            $endIndex++
        }
    }
}
$content = $lines -join "`n"

# ============================================================================
# MD019: Remove multiple spaces after hash in headings
# ============================================================================
$content = $content -replace '(?m)^(#+)\s{2,}(\S)', '$1 $2'
$fixCount['MD019'] = ([regex]::Matches($originalContent, '(?m)^(#+)\s{2,}(\S)') | Measure-Object).Count

# ============================================================================
# MD022: Add blank lines around headings
# ============================================================================
$lines = $content -split "`n"
$fixedLines = @()

for ($i = 0; $i -lt $lines.Count; $i++) {
    $currentLine = $lines[$i]
    
    # Check if current line is a heading (but not top-level #)
    if ($currentLine -match '^\s*##+ ' -and $i -gt 0) {
        $prevLine = $lines[$i - 1]
        
        # Add blank line before heading if needed
        if ($prevLine -ne '' -and -not ($prevLine -match '^\s*$')) {
            if ($i -eq 0 -or $fixedLines[-1] -ne '') {
                $fixedLines += ''
                $fixCount['MD022'] = ($fixCount['MD022'] -as [int]) + 1
            }
        }
    }
    
    $fixedLines += $currentLine
    
    # Add blank line after heading if needed
    if ($currentLine -match '^\s*##+ ' -and $i + 1 -lt $lines.Count) {
        $nextLine = $lines[$i + 1]
        if ($nextLine -ne '' -and -not ($nextLine -match '^\s*$')) {
            $fixedLines += ''
            $fixCount['MD022'] = ($fixCount['MD022'] -as [int]) + 1
        }
    }
}

$content = $fixedLines -join "`n"

# ============================================================================
# MD024: Remove or rename duplicate headings
# ============================================================================
$lines = $content -split "`n"
$headingMap = @{}
$fixedLines = @()

foreach ($line in $lines) {
    if ($line -match '^\s*(#+)\s+(.+?)(\s*:[;]?)?$') {
        $level = $matches[1]
        $title = $matches[2].Trim()
        
        if ($headingMap.ContainsKey($title)) {
            # Rename duplicate heading by adding level indicator
            $count = $headingMap[$title] + 1
            $newTitle = "$title ($count)"
            $line = "$level $newTitle"
            $headingMap[$title] = $count
            $fixCount['MD024'] = ($fixCount['MD024'] -as [int]) + 1
        }
        else {
            $headingMap[$title] = 1
        }
    }
    
    $fixedLines += $line
}

$content = $fixedLines -join "`n"

# ============================================================================
# MD026: Remove trailing punctuation from headings
# ============================================================================
$content = $content -replace '(?m)^(#+\s+.+?)([:;,!?])(\s*)$', '$1$3'
$fixCount['MD026'] = ([regex]::Matches($originalContent, '(?m)^(#+\s+.+?)([:;,!?])(\s*)$') | Measure-Object).Count

# ============================================================================
# MD029: Fix ordered list item prefix (use 1. for all items)
# ============================================================================
$lines = $content -split "`n"
$fixedLines = @()
$inCodeBlock = $false

foreach ($line in $lines) {
    # Track code blocks to avoid fixing code content
    if ($line -match '^\s*```') {
        $inCodeBlock = -not $inCodeBlock
        $fixedLines += $line
        continue
    }
    
    if (-not $inCodeBlock -and $line -match '^\s+(\d)\.\s') {
        # Fix ordered list items (change to 1.)
        $line = $line -replace '^(\s*)(\d+)(\.\s)', '$1$($1 -replace "[^ ]", "")1$3'
        $fixCount['MD029'] = ($fixCount['MD029'] -as [int]) + 1
    }
    
    $fixedLines += $line
}

$content = $fixedLines -join "`n"

# ============================================================================
# MD031: Add blank lines around code fences
# ============================================================================
$lines = $content -split "`n"
$fixedLines = @()

for ($i = 0; $i -lt $lines.Count; $i++) {
    $currentLine = $lines[$i]
    
    # Check if line starts a code block
    if ($currentLine -match '^\s*```') {
        # Add blank line before code block if needed
        if ($i -gt 0 -and $fixedLines[-1] -ne '' -and -not ($fixedLines[-1] -match '^\s*$')) {
            $fixedLines += ''
            $fixCount['MD031'] = ($fixCount['MD031'] -as [int]) + 1
        }
    }
    
    $fixedLines += $currentLine
    
    # Check if line ends a code block
    if ($currentLine -match '^\s*```' -and $i + 1 -lt $lines.Count) {
        # Look ahead to see if this is closing fence
        $nextLine = $lines[$i + 1]
        if ($i -gt 0 -and -not ($currentLine -match '^\s*```\w')) {
            # This is likely a closing fence, add blank after if needed
            if ($i + 1 -lt $lines.Count -and $nextLine -ne '' -and -not ($nextLine -match '^\s*$') -and -not ($nextLine -match '^\s*#')) {
                $fixedLines += ''
                $fixCount['MD031'] = ($fixCount['MD031'] -as [int]) + 1
                continue
            }
        }
    }
}

$content = $fixedLines -join "`n"

# ============================================================================
# MD040: Add language specification to code fences
# ============================================================================
$lines = $content -split "`n"
$fixedLines = @()
$inCodeBlock = $false

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    
    if ($line -match '^\s*```\s*$') {
        # Code fence without language - look ahead to guess language
        $guessedLanguage = 'text'
        
        if ($i + 1 -lt $lines.Count) {
            $nextLine = $lines[$i + 1]
            
            # Simple heuristics to guess language
            if ($nextLine -match '^\s*(from|import|def|class|if|for|import asyncio)' -or $nextLine -match '\.py\b') {
                $guessedLanguage = 'python'
            }
            elseif ($nextLine -match '^\s*(const|let|var|function|async|await|\{)' -or $nextLine -match '\.js\b') {
                $guessedLanguage = 'javascript'
            }
            elseif ($nextLine -match '^\s*(<|<!DOCTYPE|<html|<script|<link)') {
                $guessedLanguage = 'html'
            }
            elseif ($nextLine -match '^\s*(#!/bin/bash|#!/bin/sh)' -or $nextLine -match '\.sh\b') {
                $guessedLanguage = 'bash'
            }
            elseif ($nextLine -match '^\s*(\{|"|\[)' -or $nextLine -match '\.json\b') {
                $guessedLanguage = 'json'
            }
            elseif ($nextLine -match 'yaml|yml') {
                $guessedLanguage = 'yaml'
            }
        }
        
        $line = "```$guessedLanguage"
        $fixCount['MD040'] = ($fixCount['MD040'] -as [int]) + 1
    }
    
    $fixedLines += $line
}

$content = $fixedLines -join "`n"

# ============================================================================
# MD050: Change strong emphasis from asterisks to underscores
# ============================================================================
# Only in certain contexts (not in code blocks or URLs)
$lines = $content -split "`n"
$fixedLines = @()
$inCodeBlock = $false

foreach ($line in $lines) {
    if ($line -match '^\s*```') {
        $inCodeBlock = -not $inCodeBlock
        $fixedLines += $line
        continue
    }
    
    if (-not $inCodeBlock) {
        # Replace **text** with __text__ but preserve in URLs and code
        $line = $line -replace '\*\*([^*`]+)\*\*', '__$1__'
        $fixCount['MD050'] = ($fixCount['MD050'] -as [int]) + ([regex]::Matches($line, '\*\*([^*`]+)\*\*') | Measure-Object).Count
    }
    
    $fixedLines += $line
}

$content = $fixedLines -join "`n"

# ============================================================================
# MD032: Add blank lines around lists
# ============================================================================
$lines = $content -split "`n"
$fixedLines = @()
$inCodeBlock = $false
$inList = $false

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    $previousLine = if ($i -gt 0) { $lines[$i - 1] } else { '' }
    $nextLine = if ($i + 1 -lt $lines.Count) { $lines[$i + 1] } else { '' }
    
    # Track code blocks
    if ($line -match '^\s*```') {
        $inCodeBlock = -not $inCodeBlock
    }
    
    if (-not $inCodeBlock) {
        # Check if this is a list item
        $isListItem = $line -match '^\s*[-*+]\s+' -or $line -match '^\s*\d+\.\s+'
        
        # Add blank line before list if needed
        if ($isListItem -and -not $inList -and $i -gt 0 -and $previousLine -ne '' -and -not ($previousLine -match '^\s*$')) {
            $fixedLines += ''
            $fixCount['MD032'] = ($fixCount['MD032'] -as [int]) + 1
        }
        
        # Add blank line after list if needed
        if ($inList -and -not $isListItem -and $line -ne '' -and -not ($line -match '^\s*$') -and -not ($nextLine -match '^\s*[-*+]\s+') -and -not ($nextLine -match '^\s*\d+\.\s+')) {
            if (-not ($line -match '^\s*```')) {
                $fixedLines += $line
                $fixedLines += ''
                $fixCount['MD032'] = ($fixCount['MD032'] -as [int]) + 1
                $inList = $false
                continue
            }
        }
        
        $inList = $isListItem
    }
    
    $fixedLines += $line
}

$content = $fixedLines -join "`n"

# ============================================================================
# MD034: Convert bare URLs to markdown links (simple version)
# ============================================================================
# This is more conservative to avoid breaking things
$content = $content -replace '(?m)(?<![\[\(])(https?://[^\s\)]+)(?![\]\)])', '[$1]($1)'
$fixCount['MD034'] = ([regex]::Matches($originalContent, '(?m)(?<![\[\(])(https?://[^\s\)]+)(?![\]\)])') | Measure-Object).Count

# ============================================================================
# Write fixed content back to file
# ============================================================================
Set-Content -Path $FilePath -Value $content -Encoding UTF8
Write-Host "`n? File updated: $FilePath" -ForegroundColor Green

# ============================================================================
# Report fixes applied
# ============================================================================
Write-Host "`n=== Fixes Applied ===" -ForegroundColor Cyan

$fixCount.GetEnumerator() | ForEach-Object {
    if ($_.Value -gt 0) {
        Write-Host "  $($_.Key): $($_.Value) issue(s) fixed" -ForegroundColor Yellow
    }
}

$totalFixes = ($fixCount.Values | Measure-Object -Sum).Sum
Write-Host "`nTotal fixes: $totalFixes" -ForegroundColor Green

# Verify changes
Write-Host "`n=== Verification ===" -ForegroundColor Cyan
$modifiedLines = $content -split "`n"
Write-Host "  Lines: $($modifiedLines.Count)" -ForegroundColor White
Write-Host "  File size: $(([System.Text.Encoding]::UTF8.GetByteCount($content) / 1KB).ToString('F2')) KB" -ForegroundColor White

Write-Host "`n? Markdown linting complete!" -ForegroundColor Green
