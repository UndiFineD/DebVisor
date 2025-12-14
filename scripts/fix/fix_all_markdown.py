#!/usr/bin/env python3
"""
Comprehensive markdown linting fixer for all documents.
Fixes common markdown issues like:
- MD001: Multiple top-level headings
- MD003: Consistent heading style
- MD004: Consistent list marker style (dashes)
- MD005: Consistent list indentation
- MD006: Start of unordered list not at beginning
- MD007: Unordered list indentation (2 spaces)
- MD008: Unordered list markers inconsistent
- MD009: Trailing spaces
- MD010: Hard tabs
- MD011: Reversed link syntax
- MD012: Multiple consecutive blank lines
- MD013: Line too long
- MD014: Dollar signs used before commands without showing output
- MD018: No space after hash on atx style heading
- MD019: Multiple spaces after hash on atx style heading
- MD020: No space inside hashes on closed atx style heading
- MD021: Multiple spaces inside hashes on closed atx style heading
- MD022: Blank lines around headings
- MD023: Heading must start with space
- MD024: Multiple headings with the same content
- MD025: Multiple top-level headings in the same document
- MD026: Trailing punctuation in headings
- MD027: Multiple spaces after blockquote symbol
- MD028: Blank line inside blockquote
- MD029: Ordered list item prefix
- MD030: Spaces after list markers
- MD031: Blank lines around code blocks
- MD032: Blank lines around lists
- MD033: Inline HTML
- MD034: Bare URLs (wrap in markdown links)
- MD036: Emphasis as heading (convert to proper heading)
- MD037: Spaces inside emphasis markers
- MD038: Spaces inside code span delimiters
- MD039: Spaces inside link text
- MD040: Missing language identifier in code blocks
- MD041: First line in a file should be a top level heading
- MD045: Images should have alternate text
- MD046: Code block style (indentation vs fenced)
- MD048: Code fence style (backticks vs tildes)
- MD049: Emphasis marker style (underscores vs asterisks)
- MD054: Relative links
- MD047: Missing trailing newline
"""

import re
import os
from pathlib import Path
import argparse
import json
import fnmatch

# Load optional wrapping configuration
def load_wrap_config(root: Path):
    cfg_path = root / 'md_wrap_config.json'
    if cfg_path.exists():
        try:
            return json.loads(cfg_path.read_text(encoding='utf-8'))
        except Exception:
            return {
                'default_limit': 80,
                'folder_limits': [],
                'file_limits': [],
                'skip_patterns': []
            }
    return {
        'default_limit': 80,
        'folder_limits': [],
        'file_limits': [],
        'skip_patterns': []
    }

def get_wrap_settings(root: Path, file_path: Path, cfg: dict):
    rel = str(file_path.relative_to(root)).replace('\\', '/')
    # skip check
    for pat in cfg.get('skip_patterns', []):
        if fnmatch.fnmatch(rel, pat):
            return True, None
    # file-specific limit
    for item in cfg.get('file_limits', []):
        pat = item.get('pattern')
        limit = item.get('limit')
        if pat and isinstance(limit, int) and fnmatch.fnmatch(rel, pat):
            return False, limit
    # folder-specific limit
    for item in cfg.get('folder_limits', []):
        pat = item.get('pattern')
        limit = item.get('limit')
        if pat and isinstance(limit, int) and fnmatch.fnmatch(rel, pat):
            return False, limit
    # default
    return False, int(cfg.get('default_limit', 80))

def fix_markdown_file(file_path, max_line_length: int | None = None):
    """Fix markdown linting errors in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  [ERROR] reading {file_path}: {e}")
        return False

    original_content = content

    # Fix MD009: Remove trailing spaces from lines
    lines = content.split('\n')
    lines = [line.rstrip() for line in lines]
    content = '\n'.join(lines)

    # Fix MD010: Replace hard tabs with spaces
    content = content.replace('\t', '    ')

    # Fix MD011: Reversed link syntax [text](url) not (text)[url]
    content = re.sub(r'\(([^\)]+)\)\[([^\]]+)\]', r'[\2](\1)', content)

    # Fix MD040: Add language identifier to code blocks
    content = re.sub(r'^```$', r'```python', content, flags=re.MULTILINE)

    # Fix MD012: Remove multiple consecutive blank lines
    content = re.sub(r'\n\n\n+', '\n\n', content)

    # Fix MD014: Remove leading $ from code blocks unless showing output
    content = re.sub(r'^(\s*)\$\s+', r'\1', content, flags=re.MULTILINE)

    # Fix MD018: Add space after hash on atx style heading
    content = re.sub(r'^(#+)([^ #])', r'\1 \2', content, flags=re.MULTILINE)

    # Fix MD019: Remove multiple spaces after hash on atx style heading
    content = re.sub(r'^(#+) {2,}', r'\1 ', content, flags=re.MULTILINE)

    # Fix MD020: No space inside hashes on closed atx style heading
    content = re.sub(r'^(#+) +(.+?) +(#+)$', r'\1 \2 \3', content, flags=re.MULTILINE)

    # Fix MD021: Multiple spaces inside hashes on closed atx style heading
    content = re.sub(r'^(#+) {2,}(.+?) {2,}(#+)$', r'\1 \2 \3', content, flags=re.MULTILINE)

    # Additional MD001 guard: demote extra H1 headings to H2
    lines = content.split('\n')
    h1_seen = False
    for idx, line in enumerate(lines):
        if line.startswith('# '):
            if h1_seen:
                lines[idx] = '#' + line
            else:
                h1_seen = True
    content = '\n'.join(lines)

    # Fix MD033: Remove or replace inline HTML (hard strip for remaining tags)
    content = re.sub(r'<br\s*/?>', '\n', content, flags=re.IGNORECASE)
    content = re.sub(r'<hr\s*/?>', '\n---\n', content, flags=re.IGNORECASE)
    content = re.sub(r'</?p[^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'</?div[^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'</?span[^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'</?(strong|b)>', '**', content, flags=re.IGNORECASE)
    content = re.sub(r'</?(em|i)>', '*', content, flags=re.IGNORECASE)
    content = re.sub(r'</?code>', '`', content, flags=re.IGNORECASE)
    content = re.sub(r'</?(table|thead|tbody|tr|th|td)[^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<[^>]+>', '', content)

    # Fix MD036: Convert emphasis as heading to proper heading
    content = re.sub(r'^\*\*(.+?):?\*\*$', r'### \1', content, flags=re.MULTILINE)

    # Fix MD026: Remove trailing punctuation from headings
    content = re.sub(r'^(#+\s+[^:\n]+):\s*$', r'\1', content, flags=re.MULTILINE)

    # Fix MD027: Remove multiple spaces after blockquote symbol
    content = re.sub(r'^(>\s) {2,}', r'\1', content, flags=re.MULTILINE)

    # Fix MD028: Remove multiple blank lines in blockquotes
    content = re.sub(r'(>\s*\n)\n+(>\s)', r'\1\2', content)

    # Fix MD030: Spaces after list markers (should be exactly 1)
    content = re.sub(r'^(\s*)[-*+] {2,}', r'\1- ', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)([0-9]+\.) {2,}', r'\1\2 ', content, flags=re.MULTILINE)
    # Fix MD050: Normalize ordered list prefixes (convert `1)` to `1.`)
    content = re.sub(r'^(\s*)[0-9]+\)\s+', r'\g<1>1. ', content, flags=re.MULTILINE)

    # Fix MD005, MD006, MD007, MD008, MD015: Normalize lists safely
    lines = content.split('\n')
    fixed_lines = []
    in_code_block = False
    indent_markers = {}
    for line in lines:
        if line.startswith('```'):
            in_code_block = not in_code_block
            fixed_lines.append(line)
            continue

        if in_code_block:
            fixed_lines.append(line)
            continue

        is_table = line.lstrip().startswith('|') or re.search(r'\|\s', line)
        if is_table:
            fixed_lines.append(line)
            continue

        match = re.match(r'^(\s*)([*\-+]|\d+\.)\s+(.*)', line)
        if not match:
            fixed_lines.append(line)
            continue

        indent, marker, text = match.groups()
        indent_level = len(indent) // 2
        normalized_indent = '  ' * indent_level

        marker_type = 'ordered' if marker[0].isdigit() else 'unordered'
        previous_type = indent_markers.get(indent_level)
        if previous_type and previous_type != marker_type:
            marker_type = 'unordered'

        indent_markers[indent_level] = marker_type
        marker_token = '-' if marker_type == 'unordered' else '1.'
        fixed_lines.append(f'{normalized_indent}{marker_token} {text}')

    content = '\n'.join(fixed_lines)

    # Fix MD013: Wrap long lines with smarter heuristics
    repo_root = Path(__file__).parent
    wrap_cfg = load_wrap_config(repo_root)
    skip_wrap, wrap_limit = get_wrap_settings(repo_root, Path(file_path), wrap_cfg)
    if max_line_length is not None:
        wrap_limit = max_line_length
    lines = content.split('\n')
    fixed_lines = []
    in_code_block = False
    in_list_paragraph = False
    last_list_indent = 0
    for line in lines:
        if skip_wrap:
            fixed_lines.append(line)
            continue
        if line.startswith('```'):
            in_code_block = not in_code_block
            fixed_lines.append(line)
            continue
        if in_code_block:
            fixed_lines.append(line)
            continue
        if line.startswith('    '):
            fixed_lines.append(line)
            continue
        if line.startswith('#'):
            fixed_lines.append(line)
            continue
        # Table lines only (not any '|' occurrence)
        stripped = line.lstrip()
        if stripped.startswith('|') or re.match(r'^\s*\|[-: ]+\|\s*$', stripped):
            fixed_lines.append(line)
            continue
        # Skip blockquotes and lines with inline code or URLs
        if line.lstrip().startswith('>'):
            fixed_lines.append(line)
            continue
        if '`' in line or 'http://' in line or 'https://' in line or '://' in line:
            fixed_lines.append(line)
            continue

        # Detect list items and continuation lines
        m_item = re.match(r'^(\s*)(?:[-*+]|\d+\.)\s', line)
        if m_item:
            in_list_paragraph = True
            last_list_indent = len(m_item.group(1))
            fixed_lines.append(line)
            continue
        if line.strip() == '':
            in_list_paragraph = False
            last_list_indent = 0
            fixed_lines.append(line)
            continue
        if in_list_paragraph:
            cont_indent = len(line) - len(line.lstrip(' '))
            if cont_indent >= last_list_indent:
                fixed_lines.append(line)
                continue

        # Skip lines that contain very long tokens (avoid mid-word wraps)
        long_token = any(len(tok) >= 40 for tok in re.split(r'\s+', line.strip()))
        limit = wrap_limit if wrap_limit is not None else 80
        if len(line) <= limit or long_token:
            fixed_lines.append(line)
            continue

        # Default wrapping for long lines
        words = line.split()
        current_line = ''
        indent_match = re.match(r'^(\s*)', line)
        indent = indent_match.group(1) if indent_match else ''
        for word in words:
            test_line = current_line + (' ' if current_line else '') + word
            if len(test_line) <= limit:
                current_line = test_line
            else:
                if current_line:
                    fixed_lines.append(indent + current_line)
                current_line = word
        if current_line:
            fixed_lines.append(indent + current_line)
    content = '\n'.join(fixed_lines)

    # Fix MD037: Remove spaces inside emphasis markers
    content = re.sub(r'\*\* +(.+?) +\*\*', r'**\1**', content)
    content = re.sub(r'\* +(.+?) +\*', r'*\1*', content)
    content = re.sub(r'__ +(.+?) +__', r'__\1__', content)
    content = re.sub(r'_ +(.+?) +_', r'_\1_', content)

    # Fix MD049: Normalize emphasis markers (prefer asterisks over underscores for bold)
    content = re.sub(r'__([^_]+)__', r'**\1**', content)
    content = re.sub(r'_([^_]+)_(?![a-zA-Z0-9])', r'*\1*', content)

    # Fix MD048: Normalize code fence style (prefer backticks over tildes)
    content = re.sub(r'^~~~+', '```', content, flags=re.MULTILINE)
    content = re.sub(r'~~~+$', '```', content, flags=re.MULTILINE)

    # Fix MD038: Remove spaces inside code span delimiters
    content = re.sub(r'` +(.+?) +`', r'`\1`', content)

    # Fix MD039: Remove spaces inside link text
    content = re.sub(r'\[ +(.+?) +\]', r'[\1]', content)

    # Fix MD046: Convert indented code blocks to fenced blocks
    lines = content.split('\n')
    fixed_lines = []
    in_fenced = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('```'):
            in_fenced = not in_fenced
            fixed_lines.append(line)
            i += 1
            continue

        if not in_fenced and line.startswith('    ') and line.strip() != '':
            # Start of a potential indented code block; collect consecutive indented lines
            block = []
            start_i = i
            while i < len(lines) and (lines[i].startswith('    ') or lines[i].strip() == ''):
                if lines[i].startswith('    '):
                    block.append(lines[i][4:])
                else:
                    block.append('')
                i += 1
            # Convert indented code blocks even if only a single non-empty line is present
            non_empty = sum(1 for b in block if b.strip() != '')
            if non_empty >= 1:
                if fixed_lines and fixed_lines[-1].strip() != '':
                    fixed_lines.append('')
                fixed_lines.append('```')
                fixed_lines.extend(block)
                fixed_lines.append('```')
                if i < len(lines) and lines[i].strip() != '':
                    fixed_lines.append('')
            else:
                # Not a real code block; emit original lines
                for j in range(start_i, i):
                    fixed_lines.append(lines[j])
            continue
        else:
            fixed_lines.append(line)
            i += 1
    content = '\n'.join(fixed_lines)

    # Fix MD034: Wrap bare URLs in markdown links
    content = re.sub(r'(?<!\[)https?://([^\s\)]+)(?!\))', r'[\g<0>](\g<0>)', content)

    # Fix MD047: Ensure file ends with exactly one newline
    content = content.rstrip() + '\n'

    # Fix MD001, MD022, MD031, MD032 with line-by-line processing
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    top_level_heading_found = False

    while i < len(lines):
        line = lines[i]

        # Check for code block opening
        if line.startswith('```'):
            # Add blank line before if needed
            if fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
            fixed_lines.append(line)
            # Process code block content
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                fixed_lines.append(lines[i])
                i += 1
            # Add closing fence
            if i < len(lines):
                fixed_lines.append(lines[i])
                # Add blank line after if next line exists and is not blank
                if i + 1 < len(lines) and lines[i + 1].strip() != '':
                    fixed_lines.append('')

        # Check for heading
        elif line.startswith('#') and not line.startswith('#!/'):
            # Check for top-level heading
            if line.startswith('# ') and not top_level_heading_found:
                top_level_heading_found = True
                current_heading = line
            elif line.startswith('# '):
                # Demote additional H1 to H2 for MD001
                current_heading = '#' + line
            else:
                current_heading = line
            # Add blank line before if needed
            if fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
            fixed_lines.append(current_heading)
            # Add blank line after if needed
            if i + 1 < len(lines) and lines[i + 1].strip() != '':
                fixed_lines.append('')

        # Check for list items (unordered and ordered)
        elif re.match(r'^\s*[-*+]\s', line) or re.match(r'^\s*[0-9]+\.\s', line):
            # Add blank line before if needed
            if fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
            fixed_lines.append(line)

        # Check for blockquote
        elif line.startswith('>'):
            # Add blank line before if needed
            if fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
            fixed_lines.append(line)

        else:
            fixed_lines.append(line)

        i += 1

    content = '\n'.join(fixed_lines)

    # Only write if content changed
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"  [ERROR] writing {file_path}: {e}")
            return False
    return False

def main():
    """Find and fix all markdown files in the repository."""
    parser = argparse.ArgumentParser(description="Normalize Markdown files across the repo")
    parser.add_argument("-q", "--quiet", action="store_true", help="suppress per-file [FIXED] lines")
    parser.add_argument("--max-line-length", type=int, default=None, help="override wrapping limit for MD013")
    args, _ = parser.parse_known_args()

    workspace_root = Path(__file__).parent

    # Directories to exclude
    excluded_dirs = {'.venv', '.venv-1', '.venv-2', '.venv-3', '.git', '__pycache__', '.pytest_cache', 'node_modules', '.github', '.vscode'}

    # Find all markdown files
    markdown_files = []
    for pattern in ['**/*.md', '**/*.plan.md']:
        for md_file in workspace_root.glob(pattern):
            # Check if file is in excluded directory
            if not any(excluded in md_file.parts for excluded in excluded_dirs):
                markdown_files.append(md_file)

    total_files = len(markdown_files)
    fixed_files = 0
    failed_files = 0

    print(f"Found {total_files} markdown files to process")
    print("-" * 60)

    for md_file in sorted(markdown_files):
        relative_path = md_file.relative_to(workspace_root)
        if fix_markdown_file(md_file, max_line_length=args.max_line_length):
            if not args.quiet:
                print(f"[FIXED] {relative_path}")
            fixed_files += 1
        else:
            failed_files += 1

    print("-" * 60)
    print(f"\nSummary:")
    print(f"  Total files:   {total_files}")
    print(f"  Fixed:         {fixed_files}")
    print(f"  Failed:        {failed_files}")
    print(f"  Unchanged:     {total_files - fixed_files - failed_files}")

if __name__ == '__main__':
    main()
