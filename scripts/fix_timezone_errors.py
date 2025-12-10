#!/usr/bin/env python3
"""Fix timezone F821 errors by adding timezone to datetime imports."""

import re
from pathlib import Path


def fix_timezone_import(content: str) -> tuple[str, bool]:
    """
    Fix F821 'undefined name timezone' errors.

    Strategy: If file uses timezone (either as timezone.utc or datetime.timezone)
    but only imports datetime, add timezone to the import.
    """
    # Check if file uses timezone in any form
    if 'timezone' not in content:
        return content, False

    modified = False

    # Pattern: from datetime import datetime  (with or without other imports)
    # Add timezone if it's not already there
    pattern = r'^from datetime import ([^\n]*?)(\n|$)'

    def add_timezone_to_import(match):
        nonlocal modified
        imports = match.group(1)

        # Check if timezone is already imported
        if 'timezone' in imports:
            return match.group(0)

        # Add timezone to the imports
        modified = True
        if imports.strip().endswith(')'):
            # Multi-line import - add before closing paren
            imports_stripped = imports.rstrip()
            if imports_stripped.endswith(')'):
                imports_stripped = imports_stripped[:-1].rstrip()
                if imports_stripped.endswith(','):
                    return f'from datetime import {imports_stripped}\n    timezone{match.group(2)}'
                else:
                    return f'from datetime import {imports_stripped},\n    timezone{match.group(2)}'
            return match.group(0)
        else:
            # Single line import - add timezone
            return f'from datetime import {imports}, timezone{match.group(2)}'

    content = re.sub(pattern, add_timezone_to_import, content, flags=re.MULTILINE)

    return content, modified


def main():
    """Process all Python files to fix timezone errors."""
    repo_root = Path(__file__).parent.parent
    python_files = list(repo_root.rglob('*.py'))

    total_fixed = 0
    files_modified = 0

    for filepath in sorted(python_files):
        # Skip venv
        if '.venv' in str(filepath):
            continue

        try:
            content = filepath.read_text(encoding='utf-8')
            new_content, modified = fix_timezone_import(content)

            if modified:
                filepath.write_text(new_content, encoding='utf-8')
                files_modified += 1
                total_fixed += 1
                print(f"Fixed: {filepath.relative_to(repo_root)}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    print(f"\nTotal files modified: {files_modified}")
    print(f"Total fixes applied: {total_fixed}")


if __name__ == '__main__':
    main()
