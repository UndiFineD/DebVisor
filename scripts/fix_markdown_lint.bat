@echo off
REM ============================================================================
REM Markdown Linting Fixer - Batch Script
REM Fixes common markdown linting errors across multiple files
REM ============================================================================

setlocal enabledelayedexpansion

if "%~1"=="" (
    echo.
    echo Markdown Linting Fixer - Batch Script
    echo.
    echo Usage:
    echo   fix_markdown_lint.bat <filepath>
    echo   fix_markdown_lint.bat <directory>
    echo   fix_markdown_lint.bat <pattern>
    echo.
    echo Examples:
    echo   fix_markdown_lint.bat README.md
    echo   fix_markdown_lint.bat *.md
    echo   fix_markdown_lint.bat docs/
    echo.
    exit /b 1
)

echo.
echo ============================================================================
echo Markdown Linting Fixer
echo ============================================================================
echo.

set "input=%~1"
set "count=0"

REM Check if Python is available (preferred)
where python.exe >nul 2>&1
if !errorlevel! equ 0 (
    echo [INFO] Using Python fixer (preferred method)
    echo.

    REM Check if it's a file or directory/pattern
    if exist "%input%" (
        if "%~a1"=="d" (
            REM Directory - process all .md files
            for /r "%input%" %%F in (*.md) do (
                echo Processing: %%F
                python fix_markdown_lint.py "%%F" --no-backup
                set /a count+=1
            )
        ) else (
            REM Single file
            python fix_markdown_lint.py "%input%" --no-backup
            set /a count+=1
        )
    ) else (
        REM Pattern
        for %%F in (%input%) do (
            echo Processing: %%F
            python fix_markdown_lint.py "%%F" --no-backup
            set /a count+=1
        )
    )

    echo.
    echo ============================================================================
    echo Processed %count% file(s)
    echo ============================================================================
    echo.
    exit /b 0
)

REM Fallback to PowerShell
where powershell.exe >nul 2>&1
if !errorlevel! equ 0 (
    echo [INFO] Using PowerShell fixer
    echo.

    if exist "%input%" (
        if "%~a1"=="d" (
            REM Directory - process all .md files
            for /r "%input%" %%F in (*.md) do (
                echo Processing: %%F
                powershell -NoProfile -File fix_markdown_lint.ps1 -FilePath "%%F"
                set /a count+=1
            )
        ) else (
            REM Single file
            powershell -NoProfile -File fix_markdown_lint.ps1 -FilePath "%input%"
            set /a count+=1
        )
    ) else (
        REM Pattern
        for %%F in (%input%) do (
            echo Processing: %%F
            powershell -NoProfile -File fix_markdown_lint.ps1 -FilePath "%%F"
            set /a count+=1
        )
    )

    echo.
    echo ============================================================================
    echo Processed %count% file(s)
    echo ============================================================================
    echo.
    exit /b 0
)

echo [ERROR] Neither Python nor PowerShell found!
echo Please install Python 3 or enable PowerShell.
exit /b 1
