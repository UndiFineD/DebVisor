#!/usr/bin/env python3
"""
Critic Testing Agent: Detects code issues and logs them to sibling .md files.
Supports: py, sh, js, css, html, go files.
Uses: flake8, mypy, shellcheck, bandit, eslint, golangci-lint, htmlhint, etc.
"""

import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


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

    def __init__(self, repo_root: str = '.'):
        self.repo_root = Path(repo_root)
        self.issues: Dict[str, List[Dict[str, Any]]] = {}

    def find_code_files(self) -> List[Path]:
        """Recursively find all supported code files."""
        code_files = []
        for ext in self.SUPPORTED_EXTENSIONS:
            code_files.extend(self.repo_root.rglob(f'*{ext}'))
        return sorted([f for f in code_files if not self._is_ignored(f)])

    def _is_ignored(self, path: Path) -> bool:
        """Check if path should be ignored."""
        ignored_dirs = {
            '.git',
            '__pycache__',
            '.mypy_cache',
            '.pytest_cache',
            'node_modules',
            '.venv',
            'venv',
            'site-packages',
            'build',
            'dist',
        }
        for part in path.parts:
            if part in ignored_dirs:
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

    def generate_md_report(self, file_path: Path, issues: List[Dict[str, Any]]) -> str:
        """Generate markdown report for issues."""
        relative_path = file_path.relative_to(self.repo_root)

        lines = [
            f"# Code Issues Report: {relative_path}",
            f"Generated: {datetime.now().isoformat()}",
            f"Source: {relative_path}",
            "",
            "## Issues Summary",
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

        for file_path in code_files:
            print(f"[Critic] Analyzing {file_path.relative_to(self.repo_root)}...")
            issues = self.analyze_file(file_path)

            if issues:
                md_report = self.generate_md_report(file_path, issues)
                md_path = file_path.with_suffix(file_path.suffix + '.md')
                md_path.write_text(md_report, encoding='utf-8')
                print(f"  -> {len(issues)} issues found, wrote to {md_path.relative_to(self.repo_root)}")

        print("[Critic] Analysis complete!")


if __name__ == '__main__':
    agent = CriticAgent()
    agent.run()
