#!/usr/bin/env python3
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

"""
Unified Error Fixer for DebVisor.

Merges functionality from:
- fix_whitespace.py / fix_crlf.py
- fix_markdown_lint.py
- license_header_check.py
- fix_security_scan.py
- auto_fix_mypy.py
- fix_shellcheck.sh

Usage:
    python scripts/fix_all_errors.py --dry-run
    python scripts/fix_all_errors.py --apply
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Callable

# ==============================================================================
# Configuration & Constants
# ==============================================================================

SKIP_DIRS = {
    ".git", ".github", "node_modules", "dist", "build", "venv", ".venv",
    "__pycache__", "target", ".idea", ".vscode", "coverage", ".mypy_cache",
    ".pytest_cache", "tests"
}

LICENSE_HEADER = [
    "Copyright (c) 2025 DebVisor contributors",
    "Licensed under the Apache License, Version 2.0 (the \"License\");",
    "you may not use this file except in compliance with the License.",
    "You may obtain a copy of the License at",
    "    http://www.apache.org/licenses/LICENSE-2.0",
    "Unless required by applicable law or agreed to in writing, software",
    "distributed under the License is distributed on an \"AS IS\" BASIS,",
    "WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.",
    "See the License for the specific language governing permissions and",
    "limitations under the License.",
]

# ==============================================================================
# Data Structures
# ==============================================================================

@dataclass
class Issue:
    file_path: str
    issue_type: str
    line: int = 0
    message: str = ""
    fixed: bool = False

@dataclass
class RunStats:
    issues: List[Issue] = field(default_factory=list)
    summary: Dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def add(self, file_path: str, issue_type: str, line: int = 0, message: str = "", fixed: bool = False):
        self.issues.append(Issue(file_path, issue_type, line, message, fixed))
        self.summary[issue_type] += 1
        status = "FIXED" if fixed else "FOUND"
        # Print to console for immediate feedback
        print(f"[{status}] {issue_type}: {file_path}:{line} - {message}")

# ==============================================================================
# Fixer Implementations
# ==============================================================================

class BaseFixer:
    def __init__(self, root: Path, apply: bool):
        self.root = root
        self.apply = apply

    def run(self, stats: RunStats):
        raise NotImplementedError

    def should_skip(self, path: Path) -> bool:
        return any(part in SKIP_DIRS for part in path.parts)

class WhitespaceFixer(BaseFixer):
    def run(self, stats: RunStats):
        extensions = {'.py', '.sh', '.md', '.json', '.yaml', '.yml', '.txt', '.js', '.ts'}
        for path in self.root.rglob("*"):
            if path.is_file() and path.suffix in extensions and not self.should_skip(path):
                self.fix_file(path, stats)

    def fix_file(self, path: Path, stats: RunStats):
        try:
            content_bytes = path.read_bytes()
            original_bytes = content_bytes
            
            # Fix CRLF
            if b'\r\n' in content_bytes:
                stats.add(str(path), "CRLF", 0, "CRLF line endings found")
                if self.apply:
                    content_bytes = content_bytes.replace(b'\r\n', b'\n')

            try:
                content = content_bytes.decode('utf-8')
            except UnicodeDecodeError:
                return # Skip binary files

            original_content = content
            modified = False

            # Fix trailing whitespace and blank lines
            lines = content.split('\n')
            
            # Remove trailing blank lines
            while lines and not lines[-1].strip():
                lines.pop()
                modified = True
            
            # Ensure one newline at end
            if lines:
                lines.append('') 
            
            for i, line in enumerate(lines[:-1]): # Skip the last empty string we just added
                stripped = line.rstrip()
                if stripped != line:
                    stats.add(str(path), "Whitespace", i+1, "Trailing whitespace")
                    if self.apply:
                        lines[i] = stripped
                        modified = True
            
            if self.apply and (modified or content_bytes != original_bytes):
                new_content = '\n'.join(lines[:-1]) + '\n' # Reconstruct
                path.write_text(new_content, encoding='utf-8', newline='\n')
                stats.add(str(path), "Whitespace", 0, "Applied whitespace fixes", fixed=True)

        except Exception as e:
            print(f"Error processing {path}: {e}")

class MarkdownFixer(BaseFixer):
    def run(self, stats: RunStats):
        for path in self.root.rglob("*.md"):
            if not self.should_skip(path):
                self.fix_file(path, stats)

    def fix_file(self, path: Path, stats: RunStats):
        try:
            content = path.read_text(encoding='utf-8')
            original = content
            
            content = self.fix_list_numbering(content, path, stats)
            
            if self.apply and content != original:
                path.write_text(content, encoding='utf-8')
                stats.add(str(path), "Markdown", 0, "Applied markdown fixes", fixed=True)

        except Exception as e:
            print(f"Error processing {path}: {e}")

    def fix_list_numbering(self, content: str, path: Path, stats: RunStats) -> str:
        lines = content.split("\n")
        result = []
        for i, line in enumerate(lines):
            match = re.match(r"^(\s*)\d+\.\s+(.*)", line)
            if match:
                indent, text = match.groups()
                # MD029: Ordered list item prefix
                new_line = f"{indent}1. {text}"
                if new_line != line:
                     stats.add(str(path), "Markdown", i+1, "MD029: Ordered list item prefix")
                     if self.apply:
                         line = new_line
            result.append(line)
        return "\n".join(result)

class LicenseFixer(BaseFixer):
    def run(self, stats: RunStats):
        extensions = {'.py', '.sh'}
        for path in self.root.rglob("*"):
            if path.is_file() and path.suffix in extensions and not self.should_skip(path):
                self.check_license(path, stats)

    def check_license(self, path: Path, stats: RunStats):
        try:
            content = path.read_text(encoding='utf-8')
            # Check if first few lines contain "Copyright" and "Licensed under"
            header_found = False
            lines = content.splitlines()
            for i in range(min(10, len(lines))):
                if "Copyright" in lines[i] and "DebVisor" in lines[i]:
                    header_found = True
                    break
            
            if not header_found:
                stats.add(str(path), "License", 0, "Missing license header")
                if self.apply:
                    # Add header
                    new_content = ""
                    if lines and lines[0].startswith("#!"):
                        new_content += lines[0] + "\n"
                        remaining = lines[1:]
                    else:
                        remaining = lines
                    
                    # Add license
                    comment_char = "#"
                    for line in LICENSE_HEADER:
                        new_content += f"{comment_char} {line}\n"
                    
                    new_content += "\n" + "\n".join(remaining)
                    path.write_text(new_content, encoding='utf-8')
                    stats.add(str(path), "License", 0, "Added license header", fixed=True)

        except Exception:
            pass

class ShellCheckFixer(BaseFixer):
    def run(self, stats: RunStats):
        sh_files = [p for p in self.root.rglob("*.sh") if not self.should_skip(p)]
        
        if not shutil.which("shellcheck"):
            print("Warning: shellcheck not found in PATH. Skipping ShellCheck fixes.")
            return

        for sh_file in sh_files:
            try:
                # Get JSON output for reporting
                proc = subprocess.run(
                    ["shellcheck", "-f", "json", str(sh_file)],
                    capture_output=True, text=True
                )
                
                if proc.stdout.strip():
                    try:
                        issues = json.loads(proc.stdout)
                        for issue in issues:
                            stats.add(str(sh_file), "ShellCheck", issue.get('line', 0), 
                                      f"{issue.get('code', 'Unknown')}: {issue.get('message', '')}")
                    except json.JSONDecodeError:
                        pass

                if self.apply:
                    # Apply diffs
                    diff_proc = subprocess.run(
                        ["shellcheck", "-f", "diff", str(sh_file)],
                        capture_output=True, text=True
                    )
                    if diff_proc.stdout:
                        # Apply patch using git apply
                        try:
                            # git apply expects input from stdin
                            subprocess.run(
                                ["git", "apply", "-"],
                                input=diff_proc.stdout, text=True, check=True, cwd=self.root
                            )
                            stats.add(str(sh_file), "ShellCheck", 0, "Applied shellcheck auto-fixes", fixed=True)
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            # Fallback if git is not available or fails
                            print(f"Failed to apply shellcheck patch for {sh_file}")

            except Exception as e:
                print(f"Error running shellcheck on {sh_file}: {e}")

class MyPyFixer(BaseFixer):
    def run(self, stats: RunStats):
        # Only run if we have a mypy config
        if not (self.root / "mypy.ini").exists():
            return

        if not shutil.which("mypy"):
            print("Warning: mypy not found. Skipping MyPy fixes.")
            return

        print("Running MyPy scan...")
        try:
            # Run mypy
            proc = subprocess.run(
                [sys.executable, "-m", "mypy", "opt", "scripts", "--no-error-summary"],
                capture_output=True, text=True
            )
            
            # Parse output
            # Output format: file:line: error: message [code]
            for line in proc.stdout.splitlines():
                match = re.match(r"([^:]+):(\d+)(?::\d+)?: error: (.*) \[([^\]]+)\]", line)
                if match:
                    filepath, line_num, message, code = match.groups()
                    stats.add(filepath, "MyPy", int(line_num), f"{message} [{code}]")
            
        except Exception as e:
            print(f"Error running mypy: {e}")

# ==============================================================================
# Main Execution
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Fix all errors in the workspace.")
    parser.add_argument("--dry-run", action="store_true", help="Only report issues, do not fix.")
    parser.add_argument("--apply", action="store_true", help="Apply fixes.")
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("Please specify either --dry-run or --apply")
        sys.exit(1)

    root = Path.cwd()
    stats = RunStats()
    
    fixers = [
        WhitespaceFixer(root, args.apply),
        MarkdownFixer(root, args.apply),
        LicenseFixer(root, args.apply),
        ShellCheckFixer(root, args.apply),
        MyPyFixer(root, args.apply),
    ]

    for fixer in fixers:
        print(f"Running {fixer.__class__.__name__}...")
        fixer.run(stats)

    # Write report
    report_path = root / "fix_all_errors.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("Fix All Errors Report\n")
        f.write("=====================\n\n")
        f.write(f"Total Issues Found: {len(stats.issues)}\n")
        f.write("Summary by Type:\n")
        for k, v in stats.summary.items():
            f.write(f"  {k}: {v}\n")
        f.write("\nDetails:\n")
        for issue in stats.issues:
            status = "[FIXED]" if issue.fixed else "[OPEN]"
            f.write(f"{status} {issue.issue_type} | {issue.file_path}:{issue.line} | {issue.message}\n")

    print("\n" + "="*40)
    print(f"Run Complete. Report saved to {report_path}")
    print(f"Total Issues: {len(stats.issues)}")
    print("Summary:")
    for k, v in stats.summary.items():
        print(f"  {k}: {v}")
    print("="*40)

if __name__ == "__main__":
    main()
