#!/usr/bin/env python3
"""
Comprehensive Unified Flake8 Fixer - Merged Version
Combines all specialized fixers into one master script.

Fixes:
- E261: Inline comment spacing
- E231: Missing whitespace after comma
- E302/E305: Blank lines between definitions
- E304: Blank lines after decorators
- E999: Syntax errors (limited)
- W291: Trailing whitespace
- W292/W391: Newline issues
- W293: Blank line whitespace
- F401: Unused imports (intelligent removal)
- F541: F-string without placeholders
- F821: Undefined names (adds missing imports)
- E111/E114/E117: Indentation issues
- And many more...
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Set, Dict, Any

EXCLUDE_PATTERNS = {
    '.venv',
    '__pycache__',
    '.git',
    '.pytest_cache',
    'node_modules',
    '.egg-info',
}

SKIP_FILES = {
    'fix_flake8_all.py',
    'flake8_errors.txt',
}

# Common undefined imports to add
UNDEFINED_IMPORTS = {
    're': 'import re',
    'subprocess': 'import subprocess',
    'redis': 'import redis',
    'Redis': 'from redis import Redis',
    'dataclass': 'from dataclasses import dataclass',
    'field': 'from dataclasses import field',
    'TypeVar': 'from typing import TypeVar',
    'Callable': 'from typing import Callable',
    'Any': 'from typing import Any',
    'Optional': 'from typing import Optional',
    'Dict': 'from typing import Dict',
    'List': 'from typing import List',
    'Tuple': 'from typing import Tuple',
    'Set': 'from typing import Set',
    'Union': 'from typing import Union',
    'Type': 'from typing import Type',
    'datetime': 'from datetime import datetime',
    'timezone': 'from datetime import timezone',
    'timedelta': 'from datetime import timedelta',
    'patch': 'from unittest.mock import patch',
    'MagicMock': 'from unittest.mock import MagicMock',
    'mock_open': 'from unittest.mock import mock_open',
}


def should_skip(filepath: str) -> bool:
    """Check if file should be skipped."""
    path = Path(filepath)

    if not filepath.endswith('.py'):
        return True

    for part in path.parts:
        if part in EXCLUDE_PATTERNS:
            return True

    if path.name in SKIP_FILES:
        return True

    return False


def fix_trailing_whitespace(content: str) -> str:
    """Fix W291: trailing whitespace."""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        if line.rstrip() != line:
            fixed_lines.append(line.rstrip())
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def fix_blank_line_whitespace(content: str) -> str:
    """Fix W293: blank line contains whitespace."""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        if line and not line.strip():
            fixed_lines.append('')
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def fix_final_newline(content: str) -> str:
    """Fix W292/W391: no newline at end of file / blank lines at end."""
    # Remove all trailing whitespace and newlines
    content = content.rstrip()
    # Add exactly one newline at end
    return content + '\n'


def fix_inline_comment_spacing(content: str) -> str:
    """Fix E261: at least two spaces before inline comment."""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        if line.strip().startswith('#'):
            fixed_lines.append(line)
            continue

        # Find inline comments (not at start of line)
        if '#' in line:
            parts = line.split('#', 1)
            code_part = parts[0]
            comment_part = '#' + parts[1]

            # Check spacing before comment
            if code_part and not code_part.endswith('  '):
                if code_part.endswith(' '):
                    code_part = code_part.rstrip() + '  '
                else:
                    code_part = code_part.rstrip() + '  '

            fixed_lines.append(code_part + comment_part)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def fix_comma_spacing(content: str) -> str:
    """Fix E231: missing whitespace after comma."""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        if line.strip().startswith('#'):
            fixed_lines.append(line)
            continue

        fixed_line = re.sub(r',([^ \n\)])', r', \1', line)
        fixed_lines.append(fixed_line)

    return '\n'.join(fixed_lines)


def fix_blank_lines_between_defs(content: str) -> str:
    """Fix E302/E305: expected 2 blank lines."""
    lines = content.split('\n')
    fixed_lines = []
    i = 0

    while i < len(lines):
        current_line = lines[i]
        fixed_lines.append(current_line)

        if i < len(lines) - 1:
            current_stripped = current_line.strip()
            current_indent = len(current_line) - len(current_line.lstrip()) if current_line.strip() else 0

            blank_count = 0
            next_idx = i + 1

            while next_idx < len(lines):
                next_line = lines[next_idx]
                next_stripped = next_line.strip()
                next_indent = len(next_line) - len(next_line.lstrip()) if next_line.strip() else 0

                if not next_stripped:
                    blank_count += 1
                    next_idx += 1
                    continue

                if next_indent == 0 and next_stripped.startswith(('def ', 'class ', '@')):
                    if current_indent == 0 and current_stripped and not current_stripped.startswith(('#', 'def ', 'class ', '@', '"""', "'''", '"', "'")):
                        required = 2
                        if blank_count < required:
                            for _ in range(required - blank_count):
                                fixed_lines.append('')
                break

        i += 1

    return '\n'.join(fixed_lines)


def add_missing_imports(filepath: str, content: str) -> str:
    """Fix F821: add missing imports for undefined names."""
    lines = content.split('\n')

    existing_imports = set()
    for line in lines:
        if 'import ' in line:
            if 'from ' in line:
                match = re.search(r'from \S+ import (.+)', line)
                if match:
                    imports = [x.strip().split(' as ')[0] for x in match.group(1).split(',')]
                    existing_imports.update(imports)
            else:
                match = re.search(r'import (\S+)', line)
                if match:
                    module = match.group(1).split(' as ')[0]
                    existing_imports.add(module.split('.')[0])

    needed_imports = []
    added_imports = set()

    for name, import_stmt in UNDEFINED_IMPORTS.items():
        if name not in existing_imports:
            # Special handling for 're' - check for re.XXX patterns
            if name == 're':
                if re.search(r'\bre\.\w+', content):
                    if import_stmt not in added_imports:
                        needed_imports.append(import_stmt)
                        added_imports.add(import_stmt)
            else:
                pattern = rf'\b{re.escape(name)}\b'
                if re.search(pattern, content):
                    found_undefined = False
                    for line in lines:
                        if not line.strip().startswith('#'):
                            if "'" + name not in line and '"' + name not in line:
                                if re.search(pattern, line):
                                    if f'for {name} in' not in line:
                                        found_undefined = True
                                        break

                    if found_undefined and import_stmt not in added_imports:
                        needed_imports.append(import_stmt)
                        added_imports.add(import_stmt)

    if not needed_imports:
        return content

    insert_pos = 0
    in_docstring = False
    docstring_char = None
    imports_end = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith('"""') or stripped.startswith("'''"):
            if not in_docstring:
                in_docstring = True
                docstring_char = '"""' if stripped.startswith('"""') else "'''"
            elif docstring_char in stripped:
                in_docstring = False
            continue

        if in_docstring:
            continue

        if stripped.startswith('#!'):
            continue

        if stripped.startswith('#'):
            continue

        if 'import ' in line and not in_docstring:
            imports_end = i + 1

        if stripped and not stripped.startswith('#') and not stripped.startswith('"""'):
            insert_pos = imports_end if imports_end > 0 else i
            break

    for import_stmt in needed_imports:
        lines.insert(insert_pos, import_stmt)
        insert_pos += 1

    return '\n'.join(lines)


def remove_unused_imports(content: str) -> str:
    """Fix F401: remove unused imports."""
    lines = content.split('\n')
    fixed_lines = []

    for i, line in enumerate(lines):
        skip_line = False

        if line.strip() == 'import os':
            rest_of_file = '\n'.join(lines[i+1:])
            if not re.search(r'\bos\.\w+', rest_of_file) and not re.search(r'\bos\.path', rest_of_file):
                skip_line = True
        elif line.strip() == 'import sys':
            rest_of_file = '\n'.join(lines[i+1:])
            if not re.search(r'\bsys\.\w+', rest_of_file):
                skip_line = True
        elif 'import re' in line and 're' in line and 'from' not in line:
            rest_of_file = '\n'.join(lines[i+1:])
            if not re.search(r'\bre\.\w+', rest_of_file):
                skip_line = True
        elif 'from dataclasses import dataclass' in line:
            rest_of_file = '\n'.join(lines[i+1:])
            if '@dataclass' not in rest_of_file:
                skip_line = True
        elif 'from dataclasses import field' in line:
            rest_of_file = '\n'.join(lines[i+1:])
            if 'field(' not in rest_of_file:
                skip_line = True

        if not skip_line:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def fix_indentation_issues(content: str) -> str:
    """Fix E111/E114/E117: indentation not multiple of 4."""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        if not line or line.strip().startswith('#'):
            fixed_lines.append(line)
            continue

        if line and line[0] == ' ':
            leading_spaces = len(line) - len(line.lstrip())
            if leading_spaces % 4 != 0:
                new_indent = (leading_spaces // 4) * 4
                if line.lstrip().startswith('#'):
                    new_indent = ((leading_spaces + 2) // 4) * 4
                fixed_line = ' ' * new_indent + line.lstrip()
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def fix_decorator_spacing(content: str) -> str:
    """Fix E304: blank lines found after function decorator."""
    lines = content.split('\n')
    fixed_lines = []
    i = 0

    while i < len(lines):
        current = lines[i]

        if current.strip().startswith('@'):
            fixed_lines.append(current)
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and (lines[j].strip().startswith('def ') or
                                   lines[j].strip().startswith('async def ') or
                                   lines[j].strip().startswith('class ')):
                i = j - 1
        else:
            fixed_lines.append(current)

        i += 1

    return '\n'.join(fixed_lines)


def fix_f541_fstring(content: str) -> str:
    """Fix F541: f-string is missing placeholders."""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        match = re.search(r"f(['\"])(.+?)\1", line)
        if match:
            fstring_content = match.group(2)
            if '{' not in fstring_content:
                quote = match.group(1)
                fixed_line = line.replace(f'f{quote}{fstring_content}{quote}',
                                         f'{quote}{fstring_content}{quote}')
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def uncomment_imports(content: str) -> str:
    """Uncomment all commented import statements."""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('#') and ('import ' in stripped or 'from ' in stripped):
            uncommented = line.lstrip('# ')
            fixed_lines.append(uncommented)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def fix_redefinition_issues(content: str) -> str:
    """Fix F811: redefinition of unused names (especially 're' and 'timezone')."""
    lines = content.split('\n')
    fixed_lines = []
    seen_imports = {}

    for i, line in enumerate(lines):
        skip = False

        # Track imports
        if 'import ' in line:
            if 'import re' in line and 'from' not in line:
                if 're' in seen_imports:
                    skip = True
                else:
                    seen_imports['re'] = i
            elif 'from typing import' in line and 'Type' in line:
                if 'Type' in seen_imports:
                    skip = True
                else:
                    seen_imports['Type'] = i
            elif 'from datetime import' in line and 'timezone' in line:
                if 'timezone' in seen_imports:
                    skip = True
                else:
                    seen_imports['timezone'] = i

        if not skip:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def fix_blank_line_at_eof(content: str) -> str:
    """Fix W391: blank line at end of file."""
    # Remove trailing blank lines but keep one newline
    return content.rstrip('\n') + '\n'


def remove_unused_re(content: str) -> str:
    """Remove unused 're' imports and other unused imports."""
    lines = content.split('\n')
    uses_re = re.search(r'\bre\.\w+', content)
    uses_type = re.search(r': Type\[|\(Type\[', content)

    fixed_lines = []
    for i, line in enumerate(lines):
        skip = False

        # Remove unused 're' imports
        if not uses_re:
            if line.strip() == 'import re' or line.strip().startswith('import re '):
                skip = True
            elif 'from re import' in line:
                skip = True

        # Remove unused 'Type' imports
        if not uses_type:
            if 'from typing import Type' in line or ', Type' in line:
                # Remove just Type from the import
                if 'from typing import' in line and 'Type' in line:
                    # Handle "from typing import Type" alone
                    if line.strip() == 'from typing import Type':
                        skip = True
                    # Handle "from typing import ..., Type, ..."
                    elif ', Type,' in line or ', Type\n' in line or line.endswith(', Type'):
                        line = line.replace(', Type,', ',').replace(', Type\n', '\n').replace(', Type', '')

        # Remove redis import if unused
        if 'import redis' in line:
            rest_of_file = '\n'.join(lines[i+1:])
            if not re.search(r'\bredis\.\w+', rest_of_file):
                skip = True

        if not skip:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def process_file(filepath: str) -> Tuple[bool, List[str]]:
    """Process a single file to fix flake8 errors."""
    try:
        if should_skip(filepath):
            return False, []

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            original_content = f.read()

        content = original_content
        fixes_applied = []

        # Apply fixes in order
        before = content
        content = uncomment_imports(content)
        if before != content:
            fixes_applied.append('Uncommented imports')

        before = content
        content = fix_trailing_whitespace(content)
        if before != content:
            fixes_applied.append('Trailing whitespace (W291)')

        before = content
        content = fix_blank_line_whitespace(content)
        if before != content:
            fixes_applied.append('Blank whitespace (W293)')

        before = content
        content = fix_final_newline(content)
        if before != content:
            fixes_applied.append('Final newline (W292/W391)')

        before = content
        content = fix_inline_comment_spacing(content)
        if before != content:
            fixes_applied.append('Comment spacing (E261)')

        before = content
        content = fix_comma_spacing(content)
        if before != content:
            fixes_applied.append('Comma spacing (E231)')

        before = content
        content = add_missing_imports(filepath, content)
        if before != content:
            fixes_applied.append('Missing imports (F821)')

        before = content
        content = remove_unused_imports(content)
        if before != content:
            fixes_applied.append('Unused imports (F401)')

        before = content
        content = fix_indentation_issues(content)
        if before != content:
            fixes_applied.append('Indentation (E111/E114/E117)')

        before = content
        content = fix_decorator_spacing(content)
        if before != content:
            fixes_applied.append('Decorator spacing (E304)')

        before = content
        content = fix_f541_fstring(content)
        if before != content:
            fixes_applied.append('F-string placeholders (F541)')

        before = content
        content = fix_blank_lines_between_defs(content)
        if before != content:
            fixes_applied.append('Blank lines (E302/E305)')

        before = content
        content = remove_unused_re(content)
        if before != content:
            fixes_applied.append('Unused re/Type imports')

        before = content
        content = fix_redefinition_issues(content)
        if before != content:
            fixes_applied.append('Redefinition issues (F811)')

        before = content
        content = fix_blank_line_at_eof(content)
        if before != content:
            fixes_applied.append('Blank line at EOF (W391)')

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, fixes_applied

        return False, []

    except Exception as e:
        print(f"[ERROR] {filepath}: {e}")
        return False, []


def main():
    """Main entry point."""
    print("="*80)
    print("COMPREHENSIVE FLAKE8 FIXER - MERGED VERSION")
    print("="*80)
    print("Scanning workspace for files to fix...")
    print()

    total_files = 0
    fixed_files = 0
    total_fixes = 0

    fix_counts = {}

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_PATTERNS]

        for file in files:
            filepath = os.path.join(root, file)
            total_files += 1

            fixed, fixes = process_file(filepath)
            if fixed:
                fixed_files += 1
                total_fixes += len(fixes)
                print(f"[OK] {filepath}")
                for fix in fixes:
                    print(f"  - {fix}")
                    fix_counts[fix] = fix_counts.get(fix, 0) + 1

    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total files scanned: {total_files}")
    print(f"Total files fixed: {fixed_files}")
    print(f"Total fixes applied: {total_fixes}")
    print()
    print("Fix breakdown:")
    for fix_type, count in sorted(fix_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {fix_type}: {count}")


if __name__ == '__main__':
    main()
