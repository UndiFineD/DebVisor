#!/usr/bin/env python3
"""Fix E302 (missing blank lines) and E265 (block comments)."""

import re
from pathlib import Path


def fix_block_comment_format(content: str) -> tuple[str, bool]:
    """Fix E265: block comment should start with '# '."""
    lines = content.split('\n')
    modified = False
    new_lines = []

    for line in lines:
        if line.startswith('#') and not line.startswith('#!'):
            # This is a block/line comment
            if len(line) > 1 and line[1] not in (' ', '#', '\t', '\n'):
                # No space after # - add one
                new_line = '# ' + line[1:].lstrip()
                new_lines.append(new_line)
                modified = True
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    return '\n'.join(new_lines), modified


def fix_blank_lines_between_defs(content: str) -> tuple[str, bool]:
    """Fix E302: expected 2 blank lines before function/class definition."""
    lines = content.split('\n')
    new_lines = []
    modified = False
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this is a function/class definition at module level
        if re.match(r'^(def|class) ', line):
            # Count preceding blank lines
            blank_count = 0
            j = len(new_lines) - 1

            while j >= 0 and new_lines[j].strip() == '':
                blank_count += 1
                j -= 1

            # If we're not at the start of file and have < 2 blank lines, add them
            if j >= 0 and blank_count < 2:
                # Remove existing blanks
                for _ in range(blank_count):
                    new_lines.pop()
                # Add exactly 2 blank lines
                new_lines.append('')
                new_lines.append('')
                modified = True

        new_lines.append(line)
        i += 1

    return '\n'.join(new_lines), modified


def fix_blank_line_whitespace(content: str) -> tuple[str, bool]:
    """Fix W293: blank line contains whitespace."""
    lines = content.split('\n')
    modified = False
    new_lines = []

    for line in lines:
        if line.strip() == '':
            # Blank line - should have no whitespace
            if line != '':
                modified = True
            new_lines.append('')
        else:
            new_lines.append(line)

    return '\n'.join(new_lines), modified


def main():
    """Process all Python files."""
    repo_root = Path(__file__).parent.parent
    python_files = list(repo_root.rglob('*.py'))

    files_modified = 0
    total_fixes = 0

    for filepath in sorted(python_files):
        if '.venv' in str(filepath):
            continue

        try:
            content = filepath.read_text(encoding='utf-8')

            # Apply fixes in order
            new_content = content
            count = 0

            new_content, modified = fix_block_comment_format(new_content)
            if modified:
                count += 1

            new_content, modified = fix_blank_lines_between_defs(new_content)
            if modified:
                count += 1

            new_content, modified = fix_blank_line_whitespace(new_content)
            if modified:
                count += 1

            if count > 0:
                filepath.write_text(new_content, encoding='utf-8')
                files_modified += 1
                total_fixes += count
                print(f"Fixed: {filepath.relative_to(repo_root)} ({count} fixes)")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    print(f"\nTotal files modified: {files_modified}")
    print(f"Total fix categories applied: {total_fixes}")


if __name__ == '__main__':
    main()
