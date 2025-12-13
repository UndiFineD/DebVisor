#!/usr/bin/env python3
"""
Extended markdown linting issue scanner.
Identifies additional markdown issues for fix_all_markdown.py
"""

import re
import json
import fnmatch
from pathlib import Path
from collections import defaultdict

def _load_wrap_config(root: Path):
    cfg_path = root / 'md_wrap_config.json'
    if cfg_path.exists():
        try:
            return json.loads(cfg_path.read_text(encoding='utf-8'))
        except Exception:
            return {}
    return {}

def _wrap_limit_for(root: Path, file_path: Path, cfg: dict, default_limit: int) -> int:
    rel = str(file_path.relative_to(root)).replace('\\', '/')
    for item in cfg.get('file_limits', []) or []:
        if fnmatch.fnmatch(rel, item.get('pattern', '')):
            return int(item.get('limit', default_limit))
    for item in cfg.get('folder_limits', []) or []:
        if fnmatch.fnmatch(rel, item.get('pattern', '')):
            return int(item.get('limit', default_limit))
    return int(cfg.get('default_limit', default_limit))

def scan_markdown_file(file_path, max_line_length: int | None = None):
    """Scan a single markdown file for issues."""
    issues = defaultdict(int)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return issues

    lines = content.split('\n')

    # MD001: Multiple top-level headings (fence-aware)
    in_fence = False
    h1_count = 0
    for line in lines:
        if line.startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.match(r'^#\s+', line):
            h1_count += 1
    if h1_count > 1:
        issues['MD001_multiple_h1'] += 1

    # MD005/MD006/MD007: Evaluate per nesting level and accept multiples of two
    in_code_block = False
    per_level_indents = {}
    md006_flagged = False
    md007_flagged = False

    for line in lines:
        if line.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        m_un = re.match(r'^(\s*)([-*+])\s', line)
        m_ord = re.match(r'^(\s*)(\d+\.)\s', line)
        if not (m_un or m_ord):
            continue

        indent_spaces = len((m_un or m_ord).group(1))
        level = indent_spaces // 2
        per_level_indents.setdefault(level, set()).add(indent_spaces)

        # MD006: accept multiples of two; only flag odd indentation
        if m_un and indent_spaces > 0 and (indent_spaces % 2 != 0):
            md006_flagged = True

        # MD007: bad indent if not multiple of two
        if m_un and (indent_spaces % 2 != 0):
            md007_flagged = True

    # MD005: inconsistent indents within same level
    for level, indent_set in per_level_indents.items():
        if len(indent_set) > 1:
            issues['MD005_inconsistent_list_indent'] += 1
            break

    if md006_flagged:
        issues['MD006_list_not_at_start'] += 1
    if md007_flagged:
        issues['MD007_list_bad_indent'] += 1

    # MD008: Unordered list markers inconsistent
    markers = set()
    for line in lines:
        m = re.match(r'^\s*([-*+])\s', line)
        if m:
            markers.add(m.group(1))
    if len(markers) > 1:
        issues['MD008_inconsistent_markers'] += 1

    # MD013: Line too long (threshold from config; skip code, headings, tables, lists, quotes, inline code, URLs, long tokens)
    in_code_block = False
    root = Path(__file__).parent
    cfg = _load_wrap_config(root)
    limit = _wrap_limit_for(root, Path(file_path), cfg, default_limit=100)
    if max_line_length is not None:
        limit = max_line_length
    prev_was_list = False
    for i, line in enumerate(lines):
        if line.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        stripped = line.lstrip()
        if not stripped:
            prev_was_list = False
            continue
        if stripped.startswith('#'):
            continue
        if stripped.startswith('>'):
            continue
        if re.match(r'^(?:[-*+]|\d+\.)\s', stripped):
            prev_was_list = True
            continue
        if prev_was_list and (len(line) - len(line.lstrip(' '))) >= 2:
            # list continuation
            continue
        if stripped.startswith('|') or re.match(r'^\|[-: ]+\|\s*$', stripped):
            continue
        if '`' in line or 'http://' in line or 'https://' in line or '://' in line:
            continue
        if any(len(tok) >= 40 for tok in re.split(r'\s+', stripped)):
            continue
        if len(line) > limit:
            issues['MD013_line_too_long'] += 1
            break

    # MD015: Mixed list types within the same list block and indentation level
    in_fence = False
    current_level_markers = {}
    for line in lines:
        if line.startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r'^(\s*)([-*+]|\d+\.|\d+\))\s', line)
        if not m:
            # reset context between list blocks
            current_level_markers.clear()
            continue
        indent_spaces = len(m.group(1))
        level = indent_spaces // 2
        marker_token = m.group(2)
        marker_type = 'ordered' if marker_token[0].isdigit() else 'unordered'
        prev = current_level_markers.get(level)
        if prev is None:
            current_level_markers[level] = marker_type
        elif prev != marker_type:
            issues['MD015_mixed_list_types'] += 1
            break

    # MD033: Inline HTML
    if re.search(r'<[^>]+>', content):
        issues['MD033_inline_html'] += 1

    # MD043: Required heading hierarchy
    h1_found = False
    h2_found = False
    for i, line in enumerate(lines):
        if line.startswith('# '):
            h1_found = True
        elif line.startswith('## '):
            h2_found = True
        elif line.startswith('### ') and not h2_found and h1_found:
            # H3 before H2
            issues['MD043_heading_hierarchy'] += 1
            break

    # MD046: Code block style (indentation vs fence)
    # Count true indented code blocks (>=2 consecutive indented lines) outside fences
    in_fence = False
    indented_block_found = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('```'):
            in_fence = not in_fence
            i += 1
            continue
        if in_fence:
            i += 1
            continue
        if line.startswith('    ') and line.strip():
            block_len = 0
            j = i
            while j < len(lines) and (lines[j].startswith('    ') or lines[j].strip() == ''):
                if lines[j].startswith('    ') and lines[j].strip():
                    block_len += 1
                j += 1
            if block_len >= 2:
                indented_block_found = True
                break
            i = j
            continue
        i += 1
    fenced_code_lines = sum(1 for line in lines if '```' in line)
    if indented_block_found and fenced_code_lines > 0:
        issues['MD046_code_block_style'] += 1

    # MD048: Code fence style (backticks vs tildes) - count only real fence markers
    backtick_count = len(re.findall(r'^```', content, flags=re.MULTILINE))
    tilde_count = len(re.findall(r'^~~~', content, flags=re.MULTILINE))
    if backtick_count > 0 and tilde_count > 0:
        issues['MD048_fence_style'] += 1

    # MD049: Emphasis marker style (underscores vs asterisks)
    underscore_bold = len(re.findall(r'__[^_]+__', content))
    asterisk_bold = len(re.findall(r'\*\*[^*]+\*\*', content))
    if underscore_bold > 0 and asterisk_bold > 0:
        issues['MD049_emphasis_style'] += 1

    # MD050: Ordered list item prefix style inconsistency
    period_prefixes = len(re.findall(r'^\s*\d+\.\s', '\n'.join(lines), re.MULTILINE))
    paren_prefixes = len(re.findall(r'^\s*\d+\)\s', '\n'.join(lines), re.MULTILINE))
    if period_prefixes > 0 and paren_prefixes > 0:
        issues['MD050_ol_prefix'] += 1

    # MD051: Link fragments (check for headings without proper IDs)
    # Check for links to internal anchors
    internal_links = re.findall(r'\[([^\]]+)\]\(#([^)]+)\)', content)
    if internal_links:
        # Check if heading with matching text exists
        for link_text, anchor in internal_links:
            if not any(anchor.lower() in line.lower() for line in lines):
                issues['MD051_link_fragments'] += 1
                break

    # MD054: Relative links (flag when mixing relative and absolute links on same page)
    relative_links = len(re.findall(r'\]\((\./|\.\./)[^)]+\)', content))
    absolute_links = len(re.findall(r'\]\(https?://[^)]+\)', content))
    if relative_links > 0 and absolute_links > 0:
        try:
            allowlist_path = Path(__file__).parent / 'md_link_allowlist.txt'
            allowlist = set()
            if allowlist_path.exists():
                allowlist = {line.strip() for line in allowlist_path.read_text(encoding='utf-8').splitlines() if line.strip()}
            rel = str(Path(file_path).relative_to(Path(__file__).parent)).replace('\\', '/')
            if rel not in allowlist:
                issues['MD054_relative_links'] += 1
        except Exception:
            issues['MD054_relative_links'] += 1

    return issues

def main():
    """Scan all markdown files."""
    import argparse
    parser = argparse.ArgumentParser(description="Scan markdown issues")
    parser.add_argument("--max-line-length", type=int, default=None, help="override MD013 threshold")
    args = parser.parse_args()

    workspace_root = Path(__file__).parent
    excluded_dirs = {'.venv', '.venv-1', '.venv-2', '.venv-3', '.git', '__pycache__', '.pytest_cache', 'node_modules', '.github', '.vscode'}

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
        issues = scan_markdown_file(md_file, max_line_length=args.max_line_length)
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
