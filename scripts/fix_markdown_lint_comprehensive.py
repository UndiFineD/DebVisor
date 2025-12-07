#!/usr/bin/env python3
"""
Comprehensive markdown linting fixes for DebVisor project (v2).
Fixes markdownlint errors across all markdown files in the workspace.
"""

import re
from pathlib import Path


def fix_file(filepath: Path, fixes: list):
    """Apply a list of fix functions to a file."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        print(f"Skipping {filepath} due to encoding issues.")
        return False

    original = content

    for fix_func in fixes:
        content = fix_func(content)

    if content != original:
        filepath.write_text(content, encoding='utf-8')
        print(f"Fixed: {filepath}")
        return True
    return False


def fix_list_numbering(content: str) -> str:
    """
    Convert sequential numbered lists to all '1.' for auto-numbering (MD029).
    """
    lines = content.split('\n')
    result = []

    for line in lines:
        match = re.match(r'^(\s*)\d+\.(\s+.*)', line)
        if match:
            indent, rest = match.groups()
            line = f"{indent}1.{rest}"
        result.append(line)

    return '\n'.join(result)


def fix_blank_lines_around_headings(content: str) -> str:
    """Ensure headings have blank lines before and after (MD022)."""
    lines = content.split('\n')
    result = []

    for i, line in enumerate(lines):
        if re.match(r'^#{1,6}\s+', line):
            if i > 0 and result and result[-1].strip() != '':
                if not re.match(r'^#{1,6}\s+', result[-1]):
                    result.append('')
            result.append(line)
            if i < len(lines) - 1:
                next_line = lines[i + 1]
                if next_line.strip() != '':
                    result.append('')
        else:
            result.append(line)

    return re.sub(r'\n{3,}', '\n\n', '\n'.join(result))


def fix_blank_lines_around_lists(content: str) -> str:
    """Ensure lists have blank lines before and after (MD032)."""
    lines = content.split('\n')
    result = []
    in_list = False

    for i, line in enumerate(lines):
        is_list_item = re.match(r'^(\s*)([-*+]|\d+\.)\s+', line)

        if is_list_item:
            if not in_list:
                if result and result[-1].strip() != '' and not re.match(
                        r'^#{1,6}\s+', result[-1]):
                    result.append('')
                in_list = True
        elif line.strip() == '':
            pass
        else:
            if in_list:
                if result and result[-1].strip() != '':
                    result.append('')
                in_list = False

        result.append(line)

    return '\n'.join(result)


def fix_bare_urls(content: str) -> str:
    """Wrap bare URLs in angle brackets (MD034)."""
    pattern = r'(?<![<\(\[])(https?://[^\s\)<\]]+)(?![>\)\]])'

    def replace_url(match):
        url = match.group(1)
        return f'<{url}>'
    return re.sub(pattern, replace_url, content)


def fix_strong_style(content: str) -> str:
    """Convert __text__ to **text** for strong emphasis (MD050)."""
    return re.sub(r'(?<!\w)__(?!\s)(.+?)(?<!\s)__(?!\w)', r'**\1**', content)


def fix_fenced_code_language(content: str) -> str:
    """Add 'text' language to empty fenced code blocks (MD040)."""
    return re.sub(r'^```\s*$', '```text', content, flags=re.MULTILINE)


def fix_trailing_spaces(content: str) -> str:
    """Remove trailing spaces (MD009)."""
    lines = content.split('\n')
    result = []
    for line in lines:
        if line.endswith('  ') and not line.endswith('   '):
            result.append(line)
        else:
            result.append(line.rstrip())
    return '\n'.join(result)


def fix_fences_around_blocks_improved(content: str) -> str:
    """Ensure blank lines around fenced code blocks (MD031)."""
    lines = content.split('\n')
    result = []

    for i, line in enumerate(lines):
        is_fence = line.strip().startswith('```')

        if is_fence:
            if result and result[-1].strip() != '':
                result.append('')
            result.append(line)
            result.append('')
        else:
            result.append(line)

    return re.sub(r'\n{3,}', '\n\n', '\n'.join(result))


def process_all_files():
    """Process all markdown files in the workspace."""
    root_dir = Path('.')

    all_fixes = [
        fix_trailing_spaces,
        fix_list_numbering,
        fix_blank_lines_around_headings,
        fix_blank_lines_around_lists,
        fix_fenced_code_language,
        fix_strong_style,
        fix_fences_around_blocks_improved,
        fix_bare_urls,
    ]

    for filepath in root_dir.rglob('*.md'):
        if any(part.startswith('.') or part == 'node_modules' or part ==
               'venv' or part == '__pycache__' for part in filepath.parts):
            continue

        print(f"Processing {filepath}...")
        fix_file(filepath, all_fixes)


if __name__ == '__main__':
    print("Starting comprehensive markdown fix...")
    process_all_files()
    print("Done.")
