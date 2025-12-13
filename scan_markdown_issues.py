#!/usr/bin/env python3
"""
Scan markdown files for common linting issues.
Reports on issues not yet fixed by fix_all_markdown.py
"""

import re
from pathlib import Path
from collections import defaultdict

def scan_markdown_file(file_path):
    """Scan a single markdown file for issues."""
    issues = defaultdict(int)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return issues

    lines = content.split('\n')

    # MD001: Multiple top-level headings
    h1_count = sum(1 for line in lines if re.match(r'^#\s+', line))
    if h1_count > 1:
        issues['MD001_multiple_h1'] += 1

    # MD005: Inconsistent indentation of list items
    list_items = [line for line in lines if re.match(r'^\s*[-*+]\s', line)]
    if list_items:
        indents = set(len(line) - len(line.lstrip()) for line in list_items)
        if len(indents) > 1:
            issues['MD005_inconsistent_list_indent'] += 1

    # MD006: Start of unordered list not at beginning of line
    for line in lines:
        if re.match(r'^\s+[-*+]\s', line) and not re.match(r'^\s{2}[-*+]\s', line):
            issues['MD006_list_not_at_start'] += 1
            break

    # MD007: Unordered list indentation
    for match in re.finditer(r'^\s+[-*+]\s', '\n'.join(lines), re.MULTILINE):
        spaces = len(match.group()) - len(match.group().lstrip())
        if spaces % 2 != 0:
            issues['MD007_list_bad_indent'] += 1
            break

    # MD008: Unordered list markers inconsistent
    markers = set()
    for line in lines:
        m = re.match(r'^\s*([-*+])\s', line)
        if m:
            markers.add(m.group(1))
    if len(markers) > 1:
        issues['MD008_inconsistent_markers'] += 1

    # MD013: Line too long (>120 chars for code, >80 for regular)
    in_code_block = False
    for i, line in enumerate(lines):
        if line.startswith('```'):
            in_code_block = not in_code_block
        elif not in_code_block and len(line) > 80 and line.strip() and not line.strip().startswith('http'):
            if i == 0 or (i > 0 and not lines[i-1].startswith('`')):
                issues['MD013_line_too_long'] += 1
                break

    # MD015: Unordered list markers inconsistent (variant)
    for line in lines:
        if re.match(r'^\s*\d+\.\s', line):
            # Found ordered list
            for check_line in lines:
                if re.match(r'^\s*[-*]\s', check_line):
                    # Mixed markers
                    issues['MD015_mixed_list_types'] += 1
                    break
            break

    # MD033: Inline HTML
    if re.search(r'<[^>]+>', content):
        issues['MD033_inline_html'] += 1

    # MD035: Horizontal rule style
    for line in lines:
        if re.match(r'^[-_*]{3,}$', line.strip()):
            # Found hr but check if consistent
            if not re.match(r'^---+$', line.strip()):
                issues['MD035_hr_style'] += 1
                break

    # MD044: Proper names (capitalization)
    # This is harder to detect, skip for now

    return issues

def main():
    """Scan all markdown files."""
    workspace_root = Path(__file__).parent
    excluded_dirs = {'.venv', '.git', '__pycache__', '.pytest_cache', 'node_modules', '.github', '.vscode'}

    # Find all markdown files
    markdown_files = []
    for pattern in ['**/*.md', '**/*.plan.md']:
        for md_file in workspace_root.glob(pattern):
            if not any(excluded in md_file.parts for excluded in excluded_dirs):
                markdown_files.append(md_file)

    print(f"Scanning {len(markdown_files)} markdown files for issues...")
    print("-" * 80)

    all_issues = defaultdict(int)
    files_with_issues = defaultdict(list)

    for md_file in sorted(markdown_files):
        issues = scan_markdown_file(md_file)
        if issues:
            relative_path = md_file.relative_to(workspace_root)
            for issue_type, count in issues.items():
                all_issues[issue_type] += count
                files_with_issues[issue_type].append(str(relative_path))

    print("\nMarkdown Linting Issues Found:")
    print("-" * 80)
    for issue_type in sorted(all_issues.keys()):
        count = all_issues[issue_type]
        print(f"\n{issue_type}: {count} files affected")
        # Show first 5 files
        for file_path in files_with_issues[issue_type][:5]:
            print(f"  - {file_path}")
        if len(files_with_issues[issue_type]) > 5:
            print(f"  ... and {len(files_with_issues[issue_type]) - 5} more")

    print("-" * 80)
    print(f"\nTotal issues found: {sum(all_issues.values())}")
    print("\nSummary by rule:")
    for rule in sorted(all_issues.keys()):
        print(f"  {rule}: {all_issues[rule]}")

if __name__ == '__main__':
    main()
