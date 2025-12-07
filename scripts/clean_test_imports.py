#!/usr/bin/env python3
"""
Clean up test files by removing sys.path manipulation.

This script removes sys.path.insert statements from test files since
pytest.ini now configures pythonpath properly.
"""

import re
from pathlib import Path


def clean_test_file(filepath):
    """Remove sys.path.insert lines and related imports from test file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    lines = content.split('\n')
    cleaned_lines = []
    skip_next = False

    for i, line in enumerate(lines):
        # Skip sys.path.insert lines
        if 'sys.path.insert' in line or (skip_next and line.strip() == ''):
            skip_next = True
            continue

        # Skip variable definitions only used for sys.path
        if re.match(r'^\s*opt_path\s*=', line) or re.match(r'^\s*project_root\s*=', line):
            continue

        cleaned_lines.append(line)
        skip_next = False

    content = '\n'.join(cleaned_lines)

    # Remove import sys if it's only used for path manipulation
    if 'sys.' not in content.replace('sys.path', ''):
        content = re.sub(r'^import sys\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'\nimport sys\n', '\n', content)

    # Clean up multiple blank lines
    content = re.sub(r'\n\n\n+', '\n\n', content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    """Clean all test files."""
    test_dir = Path(__file__).parent.parent / 'tests'
    test_files = list(test_dir.glob('test_*.py'))

    cleaned_count = 0
    for test_file in test_files:
        if clean_test_file(test_file):
            print(f'✓ Cleaned {test_file.name}')
            cleaned_count += 1
        else:
            print(f'  Skipped {test_file.name} (no changes needed)')

    print(f'\n{cleaned_count} files cleaned')


if __name__ == '__main__':
    main()
