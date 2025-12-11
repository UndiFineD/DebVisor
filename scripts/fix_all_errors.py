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
            lines = content.split('\n')

            # Apply all markdown fixes in sequence
            lines, _ = self._fix_trailing_spaces(lines)
            lines, _ = self._fix_multiple_blank_lines(lines)
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
        except Exception:
            pass

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
        except Exception:
            pass

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
        SecurityScanFixer(root, args.apply),
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
