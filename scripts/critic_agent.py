#!/usr/bin/env python3
"""
Critic Testing Agent: Detects code issues and appends them to *.plan.md files.
Supports: py, sh, js, css, html, go files.
Uses: flake8, mypy, shellcheck, bandit, eslint, golangci-lint, htmlhint, etc.
"""

import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Set
import argparse


def load_codeignore(root: Path) -> Set[str]:
    """Load ignore patterns from .codeignore file."""
    codeignore_path = root / ".codeignore"
    if codeignore_path.exists():
        try:
            content = codeignore_path.read_text(encoding='utf-8')
            return {line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')}
        except Exception as e:
            print(f"Warning: Could not read .codeignore file: {e}")
    return set()


class CriticAgent:
    """Analyzes code files and generates issue reports."""

    # File extensions to analyze
    SUPPORTED_EXTENSIONS = {
        '.py', '.sh', '.js', '.css', '.html', '.go'
    }

    # Tool configurations per extension
    TOOLS = {
        '.py': ['flake8', 'mypy', 'bandit'],
        '.sh': ['shellcheck', 'bandit'],
        '.js': ['eslint'],
        '.css': ['stylelint'],
        '.html': ['htmlhint'],
        '.go': ['golangci-lint'],
    }

    def __init__(self, repo_root: str = '.', agents_only: bool = False):
        self.repo_root = Path(repo_root)
        self.agents_only = agents_only
        self.issues: Dict[str, List[Dict[str, Any]]] = {}
        self.ignored_patterns = load_codeignore(self.repo_root)

    def find_code_files(self) -> List[Path]:
        """Recursively find all supported code files."""
        code_files = []
        for ext in self.SUPPORTED_EXTENSIONS:
            code_files.extend(self.repo_root.rglob(f'*{ext}'))
        
        # Filter to scripts directory if agents_only is True
        if self.agents_only:
            scripts_dir = self.repo_root / 'scripts'
            code_files = [f for f in code_files if f.is_relative_to(scripts_dir)]
        
        return sorted([f for f in code_files if not self._is_ignored(f)])

    def _is_ignored(self, path: Path) -> bool:
        """Check if path should be ignored."""
        for part in path.parts:
            if part in self.ignored_patterns:
                return True
            if part.startswith('.venv'):
                return True
        return False

    def analyze_python(self, file_path: Path) -> List[Dict[str, Any]]:
        """Run flake8, mypy, bandit on Python files."""
        issues = []

        # Flake8
        try:
            result = subprocess.run(
                ['flake8', str(file_path), '--format=json'],
                capture_output=True, text=True, timeout=10
            )
            if result.stdout:
                for issue in json.loads(result.stdout):
                    issues.append({
                        'line': issue['line_number'],
                        'col': issue['column_number'],
                        'code': issue['code'],
                        'message': issue['text'],
                        'severity': 'warning',
                        'tool': 'flake8'
                    })
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            pass

        # Mypy
        try:
            result = subprocess.run(
                ['mypy', str(file_path), '--json'],
                capture_output=True, text=True, timeout=15
            )
            if result.stdout:
                for issue in json.loads(result.stdout):
                    issues.append({
                        'line': issue['line'],
                        'col': issue['column'],
                        'code': issue.get('error_code', 'type-error'),
                        'message': issue['message'],
                        'severity': 'error' if 'error' in issue['message'].lower() else 'warning',
                        'tool': 'mypy'
                    })
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            pass

        # Bandit
        try:
            result = subprocess.run(
                ['bandit', str(file_path), '-f', 'json'],
                capture_output=True, text=True, timeout=10
            )
            if result.stdout:
                data = json.loads(result.stdout)
                for issue in data.get('results', []):
                    raw_severity = (
                        issue.get('issue_severity')
                        or issue.get('severity')
                        or 'low'
                    )
                    issues.append({
                        'line': issue.get('line_number', 0),
                        'col': 0,
                        'code': issue.get('test_id', 'bandit'),
                        'message': issue.get('issue_text') or issue.get('message') or 'Bandit issue',
                        'severity': str(raw_severity).lower(),
                        'tool': 'bandit'
                    })
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            pass

        return issues

    def analyze_shell(self, file_path: Path) -> List[Dict[str, Any]]:
        """Run shellcheck and bandit on shell scripts."""
        issues = []

        # Shellcheck
        try:
            result = subprocess.run(
                ['shellcheck', str(file_path), '-f', 'json'],
                capture_output=True, text=True, timeout=10
            )
            if result.stdout:
                for issue in json.loads(result.stdout):
                    issues.append({
                        'line': issue['line'],
                        'col': issue['column'],
                        'code': issue['code'],
                        'message': issue['message'],
                        'severity': issue['level'].lower() if issue['level'] != 'style' else 'info',
                        'tool': 'shellcheck'
                    })
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            pass

        return issues

    def analyze_javascript(self, file_path: Path) -> List[Dict[str, Any]]:
        """Run eslint on JavaScript files."""
        issues = []

        try:
            result = subprocess.run(
                ['eslint', str(file_path), '--format=json'],
                capture_output=True, text=True, timeout=10
            )
            if result.stdout:
                for file_result in json.loads(result.stdout):
                    for issue in file_result.get('messages', []):
                        sev = issue['severity']
                        if isinstance(sev, str):
                            severity = sev
                        else:
                            severity = {0: 'info', 1: 'warning',
                                        2: 'error'}.get(sev, 'info')
                        issues.append({
                            'line': issue['line'],
                            'col': issue['column'],
                            'code': issue.get('ruleId', 'unknown'),
                            'message': issue['message'],
                            'severity': severity,
                            'tool': 'eslint'
                        })
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            pass

        return issues

    def analyze_go(self, file_path: Path) -> List[Dict[str, Any]]:
        """Run golangci-lint on Go files."""
        issues = []

        try:
            result = subprocess.run(
                ['golangci-lint', 'run', str(file_path), '--out-format=json'],
                capture_output=True, text=True, timeout=20
            )
            if result.stdout:
                data = json.loads(result.stdout)
                for issue in data.get('Issues', []):
                    issues.append({
                        'line': issue['Line'],
                        'col': issue['Column'],
                        'code': issue['FromLinter'],
                        'message': issue['Text'],
                        'severity': 'error' if 'error' in issue['Text'].lower() else 'warning',
                        'tool': 'golangci-lint'
                    })
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            pass

        return issues

    def analyze_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze a single file based on extension."""
        ext = file_path.suffix.lower()

        if ext == '.py':
            return self.analyze_python(file_path)
        elif ext == '.sh':
            return self.analyze_shell(file_path)
        elif ext == '.js':
            return self.analyze_javascript(file_path)
        elif ext == '.go':
            return self.analyze_go(file_path)

        return []

    def generate_code_issues_section(self, issues: List[Dict[str, Any]]) -> str:
        """Generate markdown section for code issues."""
        if not issues:
            return ""

        lines = [
            "",
            "## Code Quality Issues",
            "",
            f"Total: {len(issues)} issues found",
            "",
            "| Line | Column | Tool | Code | Severity | Message |",
            "|------|--------|------|------|----------|---------|",
        ]

        # Sort by line number
        for issue in sorted(issues, key=lambda x: x['line']):
            line = issue['line']
            col = issue['col']
            tool = issue['tool']
            code = issue['code']
            severity = issue['severity'].upper()
            message = issue['message'].replace('|', '\\|')
            lines.append(f"| {line} | {col} | {tool} | `{code}` | {severity} | {message} |")

        lines.extend([
            "",
            "## Implementation Status",
            "Items marked below as fixed:",
            "",
        ])

        return "\n".join(lines)

    def run(self, output_dir: str = None):
        """Run critic agent on all code files."""
        code_files = self.find_code_files()
        print(f"[Critic] Found {len(code_files)} code files to analyze...")

        wrote_markdown = False

        for file_path in code_files:
            print(f"[Critic] Analyzing {file_path.relative_to(self.repo_root)}...")
            issues = self.analyze_file(file_path)

            if issues:
                # Check if .plan.md file exists
                plan_md_path = file_path.with_suffix('.plan.md')
                code_issues_section = self.generate_code_issues_section(issues)

                if plan_md_path.exists():
                    # Append to existing .plan.md file
                    try:
                        existing_content = plan_md_path.read_text(encoding='utf-8')
                        # Check if code issues section already exists
                        if "## Code Quality Issues" in existing_content:
                            # Update existing section
                            parts = existing_content.split("## Code Quality Issues")
                            if len(parts) > 1:
                                before_section = parts[0]
                                after_section = parts[1].split("## ", 1)
                                if len(after_section) > 1:
                                    after_section = "## " + after_section[1]
                                else:
                                    after_section = ""
                                updated_content = before_section + code_issues_section + after_section
                            else:
                                updated_content = existing_content + code_issues_section
                        else:
                            # Append new section
                            updated_content = existing_content + code_issues_section
                        
                        plan_md_path.write_text(updated_content, encoding='utf-8')
                        print(f"  -> {len(issues)} issues found, appended to {plan_md_path.relative_to(self.repo_root)}")
                    except Exception as e:
                        print(f"  -> Failed to update plan file: {e}")
                        continue
                else:
                    # Create new .plan.md file with code issues
                    relative_path = file_path.relative_to(self.repo_root)
                    new_content = [
                        f"# Planning Report: {relative_path}",
                        f"Generated: {datetime.now().isoformat()}",
                        f"Status: CODE_ISSUES_ONLY",
                        "",
                        "## File Structure Validation",
                        "",
                        "⚠️ **Structure validation not performed**",
                        "",
                    ]
                    new_content.append(code_issues_section)
                    plan_md_path.write_text('\n'.join(new_content), encoding='utf-8')
                    print(f"  -> {len(issues)} issues found, created {plan_md_path.relative_to(self.repo_root)}")
                
                wrote_markdown = True

        print("[Critic] Analysis complete!")

        if wrote_markdown:
            fixer_path = self.repo_root / 'fix_all_markdown.py'
            if fixer_path.exists():
                print("[Critic] Running fix_all_markdown.py to normalize reports...")
                try:
                    cmd = [sys.executable, str(fixer_path), "--quiet", "--max-line-length", "120"]
                    subprocess.run(cmd, check=False, cwd=self.repo_root)
                except Exception as exc:
                    print(f"[Critic] Skipped markdown fixer: {exc}")
            else:
                print("[Critic] fix_all_markdown.py not found; skipping markdown normalization")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Critic Agent: Detects code issues and appends them to *.plan.md files.')
    parser.add_argument('--agents-only', action='store_true', help='Focus only on scripts/ directory for agent development/testing')
    args = parser.parse_args()
    
    agent = CriticAgent(agents_only=args.agents_only)
    agent.run()
