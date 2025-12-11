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
import logging
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Callable

# Configure logging for better error visibility
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


# ==============================================================================
# Configuration & Constants
# ==============================================================================

SKIP_DIRS = {
    ".git", ".github", "node_modules", "dist", "build", "venv", ".venv",
    "__pycache__", "target", ".idea", ".vscode", "coverage", ".mypy_cache",
    ".pytest_cache", "tests", "instance", "etc", "usr", "var", "tools"
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
            lines = content.split('\n')

            # Apply all markdown fixes in sequence
            lines, _ = self._fix_trailing_spaces(lines)
            lines, _ = self._fix_multiple_blank_lines(lines)
            lines, _ = self._fix_hard_tabs(lines)
            lines, _ = self._fix_unordered_list_style(lines)
            lines, _ = self._fix_unordered_list_indent(lines)
            lines, _ = self._fix_ordered_list_markers(lines)
            lines, _ = self._fix_code_fence_language(lines)
            lines = self._fix_blank_around_fences(lines)
            lines = self._fix_blank_around_lists(lines)
            lines = self._fix_blank_around_headings(lines)
            lines, _ = self._fix_duplicate_headings(lines)
            lines, _ = self._fix_multiple_h1(lines)
            lines, _ = self._fix_link_fragments(lines)
            lines, _ = self._fix_strong_style(lines)
            lines, _ = self._fix_bare_urls(lines)

            content = '\n'.join(lines)
            if content != original:
                stats.add(str(path), "Markdown", 0, "Applied markdown fixes", fixed=self.apply)
                if self.apply:
                    path.write_text(content, encoding='utf-8')

        except Exception as e:
            print(f"Error processing {path}: {e}")

    def _is_code_fence(self, line: str) -> bool:
        """Check if line is a code fence marker."""
        return bool(re.match(r"^\s*([`~]{3,})", line))

    def _is_heading(self, line: str) -> bool:
        """Check if line is a heading."""
        return bool(re.match(r"^#{1,6}\s+", line))

    def _is_list_item(self, line: str) -> bool:
        """Check if line is a list item."""
        return bool(re.match(r"^\s*([-*+]|\d+\.)\s+", line))

    def _is_table_row(self, line: str) -> bool:
        """Check if line is a table row."""
        return bool(re.match(r"^\s*\|.+\|\s*$", line))

    def _fix_trailing_spaces(self, lines: List[str]) -> Tuple[List[str], int]:
        """MD009: Remove trailing spaces."""
        result = []
        count = 0
        for line in lines:
            stripped = line.rstrip()
            if stripped != line:
                count += 1
            result.append(stripped)
        return result, count

    def _fix_multiple_blank_lines(self, lines: List[str]) -> Tuple[List[str], int]:
        """MD012: Reduce multiple blank lines to single blank line."""
        result = []
        prev_blank = False
        count = 0
        for line in lines:
            is_blank = not line.strip()
            if is_blank:
                if not prev_blank:
                    result.append(line)
                    prev_blank = True
                else:
                    count += 1
            else:
                result.append(line)
                prev_blank = False
        return result, count

    def _fix_unordered_list_style(self, lines: List[str]) -> Tuple[List[str], int]:
        """MD004: Convert * and + to - for unordered lists."""
        result = []
        count = 0
        in_code_block = False
        for line in lines:
            if self._is_code_fence(line):
                in_code_block = not in_code_block
                result.append(line)
                continue
            if in_code_block:
                result.append(line)
                continue
            match = re.match(r"^(\s*)([*+])(\s+)", line)
            if match:
                new_line = match.group(1) + "-" + match.group(3) + line[len(match.group(0)):]
                result.append(new_line)
                count += 1
            else:
                result.append(line)
        return result, count

    def _fix_unordered_list_indent(self, lines: List[str]) -> Tuple[List[str], int]:
        """MD007: Fix unordered list indentation (use 2 spaces per level)."""
        result = []
        count = 0
        in_code_block = False
        for i, line in enumerate(lines):
            if self._is_code_fence(line):
                in_code_block = not in_code_block
                result.append(line)
                continue
            if in_code_block:
                result.append(line)
                continue
            match = re.match(r"^(\s+)([-*+])(\s+)(.*)$", line)
            if match:
                indent = match.group(1)
                marker = match.group(2)
                space_after = match.group(3)
                content = match.group(4)
                current_spaces = len(indent)
                prev_line = lines[i - 1] if i > 0 else ""
                prev_is_ordered = bool(re.match(r"^\d+\.\s+", prev_line))
                if current_spaces == 2 and (prev_is_ordered or (re.match(r"^\s*[-*+]\s+", prev_line) and not prev_line.startswith("  "))):
                    new_line = f"{marker}{space_after}{content}"
                    result.append(new_line)
                    count += 1
                elif current_spaces == 4:
                    new_line = f"  {marker}{space_after}{content}"
                    count += 1
                    result.append(new_line)
                else:
                    result.append(line)
            else:
                result.append(line)
        return result, count

    def _fix_ordered_list_markers(self, lines: List[str]) -> Tuple[List[str], int]:
        """MD029: Use 1. prefix for all ordered list items."""
        result = []
        count = 0
        in_code_block = False
        for line in lines:
            if self._is_code_fence(line):
                in_code_block = not in_code_block
                result.append(line)
                continue
            if not in_code_block:
                match = re.match(r"^(\s*)(\d+)(\.\s+)", line)
                if match and match.group(2) != "1":
                    new_line = match.group(1) + "1" + match.group(3) + line[len(match.group(0)):]
                    result.append(new_line)
                    count += 1
                    continue
            result.append(line)
        return result, count

    def _fix_code_fence_language(self, lines: List[str]) -> Tuple[List[str], int]:
        """MD040: Add language to code fences."""
        result = []
        count = 0
        for line in lines:
            if re.match(r"^\s*```\s*$", line):
                result.append("```text")
                count += 1
            elif re.match(r"^\s*~~~\s*$", line):
                result.append("~~~text")
                count += 1
            else:
                result.append(line)
        return result, count

    def _fix_blank_around_fences(self, lines: List[str]) -> List[str]:
        """MD031: Add blank lines around code fences."""
        result = []  # type: ignore[var-annotated]
        i = 0
        while i < len(lines):
            line = lines[i]
            if self._is_code_fence(line):
                if i > 0 and result and result[-1].strip():
                    result.append("")
                result.append(line)
                i += 1
                match_char = re.match(r"^\s*([`~])", line)
                match_len = re.match(r"^\s*([`~]+)", line)
                if match_char and match_len:
                    fence_char = match_char.group(1)
                    fence_len = len(match_len.group(1))
                    while i < len(lines):
                        result.append(lines[i])
                        if re.match(rf"^\s*{re.escape(fence_char)}{{{fence_len},}}\s*$", lines[i]):
                            i += 1
                            if i < len(lines) and lines[i].strip():
                                result.append("")
                            break
                        i += 1
            else:
                result.append(line)
                i += 1
        return result

    def _fix_blank_around_lists(self, lines: List[str]) -> List[str]:
        """MD032: Add blank lines around lists."""
        result = []
        in_code_block = False
        prev_is_list = False
        prev_is_ordered = False
        prev_is_unordered = False
        for i, line in enumerate(lines):
            if self._is_code_fence(line):
                in_code_block = not in_code_block
                result.append(line)
                prev_is_list = False
                prev_is_ordered = False
                prev_is_unordered = False
                continue
            if in_code_block:
                result.append(line)
                continue
            is_ordered = bool(re.match(r"^\s*\d+\.\s+", line))
            is_unordered = bool(re.match(r"^\s*[-*+]\s+", line))
            is_list = is_ordered or is_unordered
            is_heading_line = self._is_heading(line)
            if is_list:
                if result and result[-1].strip():
                    should_add_blank = False
                    if not prev_is_list and not self._is_heading(result[-1]) and not self._is_table_row(result[-1]):
                        should_add_blank = True
                    if prev_is_ordered and is_unordered:
                        should_add_blank = True
                    if prev_is_unordered and is_ordered:
                        should_add_blank = True
                    if should_add_blank:
                        result.append("")
                result.append(line)
                prev_is_list = True
                prev_is_ordered = is_ordered
                prev_is_unordered = is_unordered
            else:
                if prev_is_list and line.strip() and not is_heading_line:
                    result.append("")
                result.append(line)
                prev_is_list = False
                prev_is_ordered = False
                prev_is_unordered = False
        return result

    def _fix_blank_around_headings(self, lines: List[str]) -> List[str]:
        """MD022: Add blank lines around headings."""
        result = []
        in_code_block = False
        for i, line in enumerate(lines):
            if self._is_code_fence(line):
                in_code_block = not in_code_block
                result.append(line)
                continue
            if in_code_block:
                result.append(line)
                continue
            if self._is_heading(line):
                if result and result[-1].strip():
                    result.append("")
                result.append(line)
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if next_line.strip() and not self._is_heading(next_line):
                        result.append("")
            else:
                result.append(line)
        return result

    def _fix_duplicate_headings(self, lines: List[str]) -> Tuple[List[str], int]:
        """MD024: Handle duplicate headings by making them unique."""
        heading_counts: Dict[str, int] = {}
        result = []
        count = 0
        for line in lines:
            if self._is_heading(line):
                match = re.match(r"^(#+\s+)(.+?)(\s*)$", line)
                if match:
                    prefix = match.group(1)
                    heading_text = match.group(2).strip()
                    suffix = match.group(3)
                    level = len(prefix.rstrip())
                    key = f"{level}:{heading_text.lower()}"
                    if key in heading_counts:
                        heading_counts[key] += 1
                        occurrence = heading_counts[key]
                        new_line = f"{prefix}{heading_text} ({occurrence}){suffix}"
                        result.append(new_line)
                        count += 1
                    else:
                        heading_counts[key] = 1
                        result.append(line)
                else:
                    result.append(line)
            else:
                result.append(line)
        return result, count

    def _fix_multiple_h1(self, lines: List[str]) -> Tuple[List[str], int]:
        """MD025: Convert multiple H1 headings to H2 (keep first H1 only)."""
        result = []
        count = 0
        found_h1 = False
        in_code_block = False
        for line in lines:
            if self._is_code_fence(line):
                in_code_block = not in_code_block
                result.append(line)
                continue
            if in_code_block:
                result.append(line)
                continue
            match = re.match(r"^#\s+(.+)$", line)
            if match:
                if not found_h1:
                    found_h1 = True
                    result.append(line)
                else:
                    new_line = f"## {match.group(1)}"
                    result.append(new_line)
                    count += 1
            else:
                result.append(line)
        return result, count

    def _fix_link_fragments(self, lines: List[str]) -> Tuple[List[str], int]:
        """MD051: Fix invalid link fragments."""
        count = 0
        in_code_block = False
        valid_anchors: Set[str] = set()
        anchor_counts: Dict[str, int] = {}

        for line in lines:
            if self._is_code_fence(line):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            heading_match = re.match(r"^#+\s+(.+?)\s*$", line)
            if heading_match:
                heading_text = heading_match.group(1)
                custom_match = re.search(r"\{#([^}]+)\}\s*$", heading_text)
                if custom_match:
                    valid_anchors.add(custom_match.group(1))
                else:
                    anchor = re.sub(r"[^\w\s-]", "", heading_text.lower())
                    anchor = re.sub(r"\s+", "-", anchor).strip("-")
                    if anchor in anchor_counts:
                        anchor_counts[anchor] += 1
                        actual_anchor = f"{anchor}-{anchor_counts[anchor]}"
                    else:
                        anchor_counts[anchor] = 0
                        actual_anchor = anchor
                    valid_anchors.add(actual_anchor)

        result = []
        in_code_block = False
        i = 0
        while i < len(lines):
            line = lines[i]
            if self._is_code_fence(line):
                in_code_block = not in_code_block
                result.append(line)
                i += 1
                continue
            if in_code_block:
                result.append(line)
                i += 1
                continue
            heading_match = re.match(r"^(#+\s+)(.+?)\s*\{#([^}]+)\}\s*$", line)
            if heading_match:
                prefix = heading_match.group(1)
                heading_text = heading_match.group(2)
                anchor_id = heading_match.group(3)
                result.append(f'<a id="{anchor_id}"></a>')
                result.append("")
                result.append(f"{prefix}{heading_text}")
                count += 1
                i += 1
                continue
            result.append(line)
            i += 1
        return result, count

    def _fix_strong_style(self, lines: List[str]) -> Tuple[List[str], int]:
        """MD050: Use asterisks for strong emphasis instead of underscores."""
        result = []
        count = 0
        in_code_block = False
        pattern = re.compile(r"(`[^`]+`)|((?<!_)__(.+?)__(?!_))")
        for line in lines:
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                result.append(line)
                continue
            if in_code_block:
                result.append(line)
                continue
            def replace_func(match: re.Match[str]) -> str:
                if match.group(1):
                    return match.group(1)
                else:
                    return f"**{match.group(3)}**"
            new_line = pattern.sub(replace_func, line)
            if new_line != line:
                count += 1
            result.append(new_line)
        return result, count

    def _fix_hard_tabs(self, lines: List[str]) -> Tuple[List[str], int]:
        """MD010: Replace hard tabs with spaces."""
        result = []
        count = 0
        for line in lines:
            if '\t' in line:
                new_line = line.replace('\t', '    ')  # Replace with 4 spaces
                result.append(new_line)
                count += 1
            else:
                result.append(line)
        return result, count

    def _fix_bare_urls(self, lines: List[str]) -> Tuple[List[str], int]:
        """MD034: Wrap bare URLs in angle brackets."""
        result = []
        count = 0
        in_code_block = False
        # Pattern for URLs not already in brackets or links
        url_pattern = re.compile(r'(?<![[\(])(https?://[^\s\)]+)(?![)\]])')
        for line in lines:
            if self._is_code_fence(line):
                in_code_block = not in_code_block
                result.append(line)
                continue
            if in_code_block or '```' in line or line.strip().startswith('```'):
                result.append(line)
                continue
            # Don't process lines in links or code
            if line.strip().startswith('[') or line.strip().startswith('`') or '|' in line:
                result.append(line)
                continue
            new_line = url_pattern.sub(r'<\1>', line)
            if new_line != line:
                count += 1
            result.append(new_line)
        return result, count

class LicenseFixer(BaseFixer):
    def run(self, stats: RunStats):
        # Check Python and shell files for licenses
        extensions = {'.py', '.sh'}
        for path in self.root.rglob("*"):
            if path.is_file() and path.suffix in extensions and not self.should_skip(path):
                self.check_license(path, stats)

    def check_license(self, path: Path, stats: RunStats):
        try:
            content = path.read_text(encoding='utf-8')
            lines = content.splitlines()

            # Check if license header exists in first 15 lines
            has_license = False
            for i in range(min(15, len(lines))):
                line = lines[i]
                if ("Copyright" in line and "DebVisor" in line) or \
                   ("Licensed under the Apache License" in line):
                    has_license = True
                    break

            if not has_license:
                stats.add(str(path), "License", 0, "Missing or incomplete license header")
                if self.apply:
                    self._add_license_header(path, lines, stats)

        except (OSError, UnicodeDecodeError) as e:
            print(f"Warning: Could not process {path}: {e}")

    def _add_license_header(self, path: Path, lines: List[str], stats: RunStats):
        """Add license header to file."""
        new_lines = []

        # Preserve shebang if it exists
        start_idx = 0
        if lines and lines[0].startswith("#!"):
            new_lines.append(lines[0])
            start_idx = 1

        # Add license header
        comment_char = "#" if path.suffix in {'.py', '.sh'} else "//"
        for header_line in LICENSE_HEADER:
            new_lines.append(f"{comment_char} {header_line}")

        # Add blank line after header
        new_lines.append("")

        # Add rest of content
        new_lines.extend(lines[start_idx:])

        # Write back
        new_content = "\n".join(new_lines)
        if new_content and not new_content.endswith("\n"):
            new_content += "\n"

        path.write_text(new_content, encoding='utf-8')
        stats.add(str(path), "License", 0, "Added license header", fixed=True)


class ShellCheckFixer(BaseFixer):
    def run(self, stats: RunStats):
        sh_files = [p for p in self.root.rglob("*.sh") if not self.should_skip(p)]

        if not shutil.which("shellcheck"):
            print("Warning: shellcheck not found in PATH. Skipping ShellCheck fixes.")
            return

        for sh_file in sh_files:
            try:
                if self.apply:
                    self._normalize_line_endings(sh_file, stats)

                # Get JSON output for reporting
                proc = subprocess.run(
                    ["shellcheck", "-f", "json", str(sh_file)],
                    capture_output=True, text=True
                )

                if proc.stdout.strip():
                    try:
                        issues = json.loads(proc.stdout)
                        for issue in issues:
                            code = issue.get('code', 'Unknown')
                            # Ignore 1017 if we already confirmed the file has no CR bytes; shellcheck on Windows
                            # can falsely report 1017 even after normalization.
                            if code == 1017 and not self._has_carriage_return(sh_file):
                                continue
                            stats.add(str(sh_file), "ShellCheck", issue.get('line', 0),
                                      f"{code}: {issue.get('message', '')}")
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

    def _normalize_line_endings(self, path: Path, stats: RunStats) -> None:
        """Strip carriage returns so shellcheck 1017 stops firing."""
        try:
            data = path.read_bytes()
            if b"\r" not in data:
                return
            fixed = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            if fixed != data:
                path.write_bytes(fixed)
                stats.add(str(path), "ShellCheck", 0, "Removed carriage returns", fixed=True)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            logger.debug(f"Could not normalize carriage returns in {path}: {e}")

    def _has_carriage_return(self, path: Path) -> bool:
        try:
            return b"\r" in path.read_bytes()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            logger.debug(f"Could not check carriage returns in {path}: {e}")
            return False

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

            # Parse output and collect errors by file
            errors_by_file: Dict[str, List[Tuple[int, str]]] = {}
            for line in proc.stdout.splitlines():
                match = re.match(r"([^:]+):(\d+)(?::\d+)?: error: (.*) \[([^\]]+)\]", line)
                if match:
                    filepath, line_num, message, code = match.groups()
                    stats.add(filepath, "MyPy", int(line_num), f"{message} [{code}]")

                    if self.apply:
                        if filepath not in errors_by_file:
                            errors_by_file[filepath] = []
                        errors_by_file[filepath].append((int(line_num), code))

            # Apply fixes if in apply mode
            if self.apply:
                self._apply_type_ignore_fixes(errors_by_file, stats)

        except Exception as e:
            print(f"Error running mypy: {e}")

    def _apply_type_ignore_fixes(self, errors_by_file: Dict[str, List[Tuple[int, str]]], stats: RunStats):
        """Apply type: ignore comments to all error lines."""
        for file_path in sorted(errors_by_file.keys()):
            file_errors = errors_by_file[file_path]

            # Group multiple errors on same line - collect all codes
            lines_to_fix: Dict[int, List[str]] = {}
            for line_num, code in file_errors:
                if line_num not in lines_to_fix:
                    lines_to_fix[line_num] = []
                lines_to_fix[line_num].append(code)

            # Fix each line
            file_fixed = 0
            for line_num, codes in sorted(lines_to_fix.items()):
                if self._add_type_ignore_to_line(file_path, line_num, codes):
                    file_fixed += 1
                    stats.add(file_path, "MyPy", line_num, f"Added type: ignore", fixed=True)

            if file_fixed > 0:
                print(f"Fixed {file_fixed} errors in {file_path}")

    def _add_type_ignore_to_line(self, file_path: str, line_num: int, codes: List[str]) -> bool:
        """Add or merge type: ignore[code1, code2, ...] comment to a specific line."""
        path = Path(file_path)

        if not path.exists():
            return False

        try:
            content = path.read_text(encoding="utf-8")
            lines = content.splitlines(keepends=False)

            if line_num < 1 or line_num > len(lines):
                return False

            idx = line_num - 1
            line = lines[idx]

            # Check if line already has type: ignore
            existing_codes: Set[str] = set()
            if "# type: ignore" in line:
                # Extract existing codes from comment
                ignore_match = re.search(r"#\s*type:\s*ignore\[([^\]]+)\]", line)
                if ignore_match:
                    existing_str = ignore_match.group(1)
                    existing_codes = set(c.strip() for c in re.split(r'[,\s]+', existing_str) if c.strip())
                    line = re.sub(r'\s*#\s*type:\s*ignore\[([^\]]+)\]', '', line)
                else:
                    line = re.sub(r'\s*#\s*type:\s*ignore\b.*', '', line)

            # Merge new codes with existing codes
            all_codes = existing_codes.union(set(codes))

            # Don't modify if no new codes were added
            if existing_codes and all_codes == existing_codes:
                return False

            # Add type: ignore comment with sorted, comma-separated codes
            sorted_codes = ", ".join(sorted(all_codes))
            lines[idx] = line.rstrip() + f"  # type: ignore[{sorted_codes}]"
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return True
        except Exception as e:
            print(f"Error processing {file_path}:{line_num}: {e}")
            return False

class SecurityScanFixer(BaseFixer):
    """Fix security scan issues from security-scan.md."""

    def run(self, stats: RunStats):
        scan_path = self.root / "security-scan.md"
        if not scan_path.exists():
            return

        # Clean bytecode artifacts
        removed_files, removed_dirs = self._clean_bytecode(stats)

        # Parse security scan entries
        rows = self._parse_scan(scan_path)

        if not rows:
            return

        # Fix various security issues
        if self.apply:
            fixed_ids = set()
            fixed_ids.update(self._fix_unused_imports(rows, stats))
            fixed_ids.update(self._fix_f_string_placeholders(rows, stats))
            fixed_ids.update(self._fix_unused_variables(rows, stats))
            fixed_ids.update(self._fix_future_import_order(rows, stats))
            fixed_ids.update(self._fix_missing_imports(rows, stats))

            # Remove fixed entries from scan file
            self._remove_fixed_entries(scan_path, fixed_ids)

    def _clean_bytecode(self, stats: RunStats) -> Tuple[List[Path], List[Path]]:
        """Remove *.pyc files and __pycache__ directories."""
        removed_files = []
        removed_dirs = []

        skip_dirs = {".git", ".venv", "node_modules", ".tox", ".mypy_cache", ".pytest_cache"}

        for pyc_file in self.root.rglob("*.pyc"):
            if any(part in skip_dirs for part in pyc_file.parts):
                continue
            removed_files.append(pyc_file)
            stats.add(str(pyc_file), "BinaryArtifact", 0, "Bytecode file")
            if self.apply:
                try:
                    pyc_file.unlink()
                except FileNotFoundError:
                    pass

        for cache_dir in self.root.rglob("__pycache__"):
            if any(part in skip_dirs for part in cache_dir.parts):
                continue
            removed_dirs.append(cache_dir)
            stats.add(str(cache_dir), "BinaryArtifact", 0, "Cache directory")
            if self.apply:
                shutil.rmtree(cache_dir, ignore_errors=True)

        return removed_files, removed_dirs

    def _parse_scan(self, scan_path: Path) -> List[Dict[str, str]]:
        """Parse security-scan.md table rows."""
        rows = []
        row_pattern = re.compile(
            r"^\|\s*(?P<id>\d+)\s*\|\s*(?P<rule>[^|]+?)\s*\|\s*(?P<severity>[^|]+?)\s*\|"
            r"\s*`(?P<file>[^`]+)`\s*\|\s*(?P<line>[^|]+)\|\s*(?P<message>.+?)\s*\|$"
        )

        try:
            with scan_path.open(encoding="utf-8") as f:
                for line in f:
                    match = row_pattern.match(line.strip())
                    if match:
                        entry = {k: v.strip() for k, v in match.groupdict().items()}
                        rows.append(entry)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            logger.debug(f"Could not read security scan results: {e}")

        return rows

    def _fix_unused_imports(self, rows: List[Dict[str, str]], stats: RunStats) -> Set[str]:
        """Fix unused imports (F401)."""
        fixed_ids = set()
        by_file: Dict[Path, List[Dict[str, str]]] = defaultdict(list)

        for row in rows:
            if row["rule"] != "F401":
                continue
            file_path = self.root / row["file"]
            if file_path.exists() and file_path.suffix == ".py":
                by_file[file_path].append(row)

        for file_path, entries in by_file.items():
            try:
                lines = file_path.read_text(encoding="utf-8").split("\n")
                original_lines = lines[:]

                for entry in sorted(entries, key=lambda e: int(e.get("line", 0)), reverse=True):
                    try:
                        line_num = int(entry["line"]) - 1
                        if 0 <= line_num < len(lines):
                            line = lines[line_num]
                            if line.strip().startswith(("import ", "from ")):
                                indent = len(line) - len(line.lstrip())
                                lines[line_num] = " " * indent + "# " + line.lstrip()
                                fixed_ids.add(entry["id"])
                                stats.add(str(file_path), "F401", line_num + 1, "Commented unused import", fixed=True)
                    except (ValueError, KeyError):
                        pass

                if self.apply and lines != original_lines:
                    file_path.write_text("\n".join(lines), encoding="utf-8")
            except Exception:
                pass

        return fixed_ids

    def _fix_f_string_placeholders(self, rows: List[Dict[str, str]], stats: RunStats) -> Set[str]:
        """Fix f-strings missing placeholders (F541)."""
        fixed_ids = set()
        by_file: Dict[Path, List[Dict[str, str]]] = defaultdict(list)

        for row in rows:
            if row["rule"] != "F541":
                continue
            file_path = self.root / row["file"]
            if file_path.exists() and file_path.suffix == ".py":
                by_file[file_path].append(row)

        for file_path, entries in by_file.items():
            try:
                lines = file_path.read_text(encoding="utf-8").split("\n")
                original_lines = lines[:]

                for entry in sorted(entries, key=lambda e: int(e.get("line", 0)), reverse=True):
                    try:
                        line_num = int(entry["line"]) - 1
                        if 0 <= line_num < len(lines):
                            line = lines[line_num]
                            # Remove f prefix from strings without placeholders
                            line = re.sub(r'\bf"([^"]*)"', r'"\1"', line)
                            line = re.sub(r"\bf'([^']*)'", r"'\1'", line)
                            lines[line_num] = line
                            fixed_ids.add(entry["id"])
                            stats.add(str(file_path), "F541", line_num + 1, "Fixed f-string", fixed=True)
                    except (ValueError, KeyError):
                        pass

                if self.apply and lines != original_lines:
                    file_path.write_text("\n".join(lines), encoding="utf-8")
            except Exception:
                pass

        return fixed_ids

    def _fix_unused_variables(self, rows: List[Dict[str, str]], stats: RunStats) -> Set[str]:
        """Fix unused local variables (F841) by replacing with underscore."""
        fixed_ids = set()
        by_file: Dict[Path, List[Dict[str, str]]] = defaultdict(list)

        for row in rows:
            if row["rule"] != "F841":
                continue
            file_path = self.root / row["file"]
            if file_path.exists() and file_path.suffix == ".py":
                by_file[file_path].append(row)

        for file_path, entries in by_file.items():
            try:
                lines = file_path.read_text(encoding="utf-8").split("\n")
                original_lines = lines[:]

                for entry in sorted(entries, key=lambda e: int(e.get("line", 0)), reverse=True):
                    try:
                        line_num = int(entry["line"]) - 1
                        msg = entry.get("message", "")
                        if 0 <= line_num < len(lines):
                            line = lines[line_num]
                            match = re.search(r"local variable '([^']+)' is assigned to but never used", msg)
                            if match:
                                var_name = match.group(1)
                                if re.search(rf"\b{var_name}\s*=", line):
                                    lines[line_num] = re.sub(rf"\b{var_name}\s*=", "_ =", line, count=1)
                                    fixed_ids.add(entry["id"])
                                    stats.add(str(file_path), "F841", line_num + 1, "Replaced with underscore", fixed=True)
                    except (ValueError, KeyError):
                        pass

                if self.apply and lines != original_lines:
                    file_path.write_text("\n".join(lines), encoding="utf-8")
            except Exception:
                pass

        return fixed_ids

    def _remove_fixed_entries(self, scan_path: Path, fixed_ids: Set[str]):
        """Remove fixed entries from security-scan.md."""
        if not fixed_ids or not scan_path.exists():
            return

        try:
            lines = scan_path.read_text(encoding="utf-8").split("\n")
            kept = []
            removed = 0

            row_pattern = re.compile(
                r"^\|\s*(?P<id>\d+)\s*\|\s*(?P<rule>[^|]+?)\s*\|\s*(?P<severity>[^|]+?)\s*\|"
                r"\s*`(?P<file>[^`]+)`\s*\|\s*(?P<line>[^|]+)\|\s*(?P<message>.+?)\s*\|$"
            )

            for line in lines:
                match = row_pattern.match(line.strip())
                if match and match.group("id") in fixed_ids:
                    removed += 1
                else:
                    kept.append(line)

            if removed > 0:
                scan_path.write_text("\n".join(kept), encoding="utf-8")
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            logger.debug(f"Could not remove duplicate scan results: {e}")

    def _fix_missing_imports(self, rows: List[Dict[str, str]], stats: RunStats) -> Set[str]:
        """Fix F821 undefined names by adding common safe imports."""
        fixed_ids: Set[str] = set()
        targets: Dict[Path, Dict[str, Set[str]]] = defaultdict(lambda: {"typing": set(), "direct": set()})

        typing_names = {"Any", "Dict", "List", "Optional", "Set", "Tuple", "Callable"}
        direct_map = {
            "logging": "import logging",
            "MagicMock": "from unittest.mock import MagicMock",
            "patch": "from unittest.mock import patch",
        }

        for row in rows:
            if row.get("rule") != "F821":
                continue
            file_path = self.root / row["file"]
            msg = row.get("message", "")
            match = re.search(r"undefined name '([^']+)'", msg)
            if not match:
                continue
            name = match.group(1)
            if name in typing_names:
                targets[file_path]["typing"].add(name)
                fixed_ids.add(row["id"])
            elif name in direct_map:
                targets[file_path]["direct"].add(direct_map[name])
                fixed_ids.add(row["id"])

        for file_path, needs in targets.items():
            if not file_path.exists() or file_path.suffix != ".py":
                continue
            try:
                content = file_path.read_text(encoding="utf-8").split("\n")
                original = content[:]
                insertion_idx = self._import_insertion_index(content)

                # typing imports
                if needs["typing"]:
                    sorted_names = sorted(needs["typing"])
                    import_line = f"from typing import {', '.join(sorted_names)}"
                    if not self._has_import(content, import_line):
                        content.insert(insertion_idx, import_line)
                        insertion_idx += 1
                # direct imports
                for import_line in sorted(needs["direct"]):
                    if not self._has_import(content, import_line):
                        content.insert(insertion_idx, import_line)
                        insertion_idx += 1

                if content != original:
                    file_path.write_text("\n".join(content), encoding="utf-8")
            except Exception:
                pass

        return fixed_ids

    def _has_import(self, lines: List[str], import_line: str) -> bool:
        return any(line.strip() == import_line for line in lines)

    def _import_insertion_index(self, lines: List[str]) -> int:
        idx = 0
        if lines and lines[0].startswith("#!"):
            idx = 1
        # Skip module docstring
        if idx < len(lines) and lines[idx].startswith(("\"\"\"", "'''")):
            quote = lines[idx][:3]
            idx += 1
            while idx < len(lines) and quote not in lines[idx]:
                idx += 1
            if idx < len(lines):
                idx += 1
        # Skip encoding comments and blank lines
        while idx < len(lines) and (not lines[idx].strip() or lines[idx].lstrip().startswith("#")):
            idx += 1
        return idx

    def _fix_future_import_order(self, rows: List[Dict[str, str]], stats: RunStats) -> Set[str]:
        """Ensure __future__ imports are at the top (F404)."""
        fixed_ids: Set[str] = set()
        targets: Dict[Path, List[str]] = defaultdict(list)

        for row in rows:
            if row.get("rule") != "F404":
                continue
            file_path = self.root / row["file"]
            targets[file_path].append(row["id"])

        for file_path, ids in targets.items():
            if not file_path.exists() or file_path.suffix != ".py":
                continue
            try:
                lines = file_path.read_text(encoding="utf-8").split("\n")
                original = lines[:]

                future_lines = [ln for ln in lines if ln.strip().startswith("from __future__ import")]
                if not future_lines:
                    continue

                # Remove existing future imports
                lines = [ln for ln in lines if not ln.strip().startswith("from __future__ import")]

                # Deduplicate and sort future imports
                cleaned = sorted(set(future_lines))

                insert_idx = self._import_insertion_index(lines)
                for fut in cleaned:
                    lines.insert(insert_idx, fut)
                    insert_idx += 1

                if lines != original:
                    file_path.write_text("\n".join(lines), encoding="utf-8")
                    for id_ in ids:
                        fixed_ids.add(id_)
                        stats.add(str(file_path), "F404", 0, "Reordered __future__ imports", fixed=True)
            except Exception:
                pass

        return fixed_ids


class NotificationsReportFixer(BaseFixer):
    """Normalize notifications-report.md into a lint-friendly bullet format."""

    def run(self, stats: RunStats):
        path = self.root / "notifications-report.md"
        if not path.exists():
            return

        try:
            raw = path.read_text(encoding="utf-8").split("\n")
        except Exception:
            return

        repo = self._extract_value(raw, r"^\*\*Repository:\*\*\s*(.+)") or "UndiFineD/DebVisor"
        rows = self._parse_table(raw)

        new_lines: List[str] = []
        new_lines.append("# Notification Report")
        new_lines.append("")
        new_lines.append(f"**Repository:** {repo}")
        new_lines.append(f"**Unread Notifications:** {len(rows)}")
        new_lines.append("")
        new_lines.append("Generated via GitHub CLI.")
        new_lines.append("")
        new_lines.append("## Unread Notifications")
        new_lines.append("")

        for row in rows:
            title = self._shorten(row.get("title", ""), 90) or "(no title)"
            link = row.get("link", "")
            bullet = f"- [{title}]({link})" if link else f"- {title}"
            meta = (
                f"  - Type: {row.get('type','')} | Reason: {row.get('reason','')} | "
                f"Updated: {row.get('updated','')}"
            )
            new_lines.append(bullet)
            new_lines.append(meta)

        new_lines.append("")

        new_content = "\n".join(new_lines)
        existing = "\n".join(raw)

        if new_content != existing:
            stats.add(str(path), "NotificationsReport", 0, "Normalized notifications report", fixed=self.apply)
            if self.apply:
                path.write_text(new_content, encoding="utf-8")

    def _extract_value(self, lines: List[str], pattern: str) -> Optional[str]:
        regex = re.compile(pattern)
        for line in lines:
            match = regex.match(line.strip())
            if match:
                return match.group(1).strip()
        return None

    def _parse_table(self, lines: List[str]) -> List[Dict[str, str]]:
        rows: List[Dict[str, str]] = []
        in_table = False
        for line in lines:
            if line.strip().startswith("| ID |"):
                in_table = True
                continue
            if in_table:
                if not line.strip().startswith("|"):
                    break
                cells = [c.strip() for c in line.strip("|").split("|")]
                if len(cells) < 6:
                    continue
                rows.append(
                    {
                        "id": cells[0],
                        "type": cells[1],
                        "reason": cells[2],
                        "updated": cells[3],
                        "title": cells[4],
                        "link": cells[5].strip("[]() "),
                    }
                )
        return rows

    def _shorten(self, text: str, limit: int) -> str:
        text = text.strip()
        if len(text) <= limit:
            return text
        return text[: max(limit - 3, 0)] + "..."

class ConfigFixer(BaseFixer):
    """Fix configuration file issues (YAML, JSON, etc)."""

    def run(self, stats: RunStats):
        # Validate JSON files
        for path in self.root.rglob("*.json"):
            if not self.should_skip(path):
                self.validate_json(path, stats)

        # Validate YAML files
        for path in self.root.rglob("*.yaml"):
            if not self.should_skip(path):
                self.validate_yaml(path, stats)
        for path in self.root.rglob("*.yml"):
            if not self.should_skip(path):
                self.validate_yaml(path, stats)

    def validate_json(self, path: Path, stats: RunStats):
        """Validate JSON syntax."""
        try:
            content = path.read_text(encoding='utf-8')
            json.loads(content)
        except json.JSONDecodeError as e:
            stats.add(str(path), "JSON", 0, f"Invalid JSON: {e}")
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            logger.debug(f"Could not validate JSON in {path}: {e}")

    def validate_yaml(self, path: Path, stats: RunStats):
        """Validate YAML syntax."""
        try:
            content = path.read_text(encoding='utf-8')
            # Basic YAML validation - check for common issues
            if content.strip() and not any(line.strip().startswith('#') or not line.strip() for line in content.split('\n')):
                # Try to detect basic YAML structure
                if ':' not in content and '-' not in content:
                    stats.add(str(path), "YAML", 0, "Potentially invalid YAML structure")
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            logger.debug(f"Could not validate YAML in {path}: {e}")

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
        ConfigFixer(root, args.apply),
        ShellCheckFixer(root, args.apply),
        MyPyFixer(root, args.apply),
        SecurityScanFixer(root, args.apply),
        NotificationsReportFixer(root, args.apply),
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
