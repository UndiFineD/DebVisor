#!/usr/bin/env python3
"""Clean up duplicate timezone imports and unused datetime.timezone imports."""

import re
from pathlib import Path


def clean_duplicate_timezone_imports(content: str) -> tuple[str, int]:
    """Remove duplicate timezone imports."""
    lines = content.split('\n')
    seen_datetime_import = False
    modified = 0
    result_lines = []

    for line in lines:
        # Check for 'from datetime import' lines
        if line.startswith('from datetime import'):
            if seen_datetime_import and 'timezone' in line and line.strip().endswith('timezone'):
                # This is a duplicate timezone import on its own line
                continue
            seen_datetime_import = True

        result_lines.append(line)

    return '\n'.join(result_lines), modified


def fix_unused_datetime_timezone_imports(content: str) -> tuple[str, bool]:
    """
    Remove unused 'from datetime import timezone' lines.
    Keep only if timezone is actually used in the code.
    """
    modified = False

    # Check if timezone is actually used in the code (not in import statements)
    code_lines = content.split('\n')
    import_section_end = 0

    # Find where imports end
    for i, line in enumerate(code_lines):
        if line and not line.startswith(('import ', 'from ', '#', '"""', "'''")) and i > 5:
            import_section_end = i
            break

    # Check if timezone is used after imports
    code_after_imports = '\n'.join(code_lines[import_section_end:])
    timezone_used = bool(re.search(r'\btimezone\b', code_after_imports))

    if not timezone_used:
        # Remove 'from datetime import timezone' lines
        pattern = r'^from datetime import timezone\s*$'
        new_content = re.sub(pattern, '', content, flags=re.MULTILINE)
        if new_content != content:
            modified = True
        content = new_content

    # Also clean up W293 - blank lines with whitespace
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.strip() == '':
            new_lines.append('')
        else:
            new_lines.append(line)

    new_content = '\n'.join(new_lines)
    if new_content != content:
        modified = True

    return new_content, modified


def main():
    """Process all Python files."""
    repo_root = Path(__file__).parent.parent
    python_files = list(repo_root.rglob('*.py'))

    total_fixed = 0
    files_modified = 0

    for filepath in sorted(python_files):
        if '.venv' in str(filepath):
            continue

        try:
            content = filepath.read_text(encoding='utf-8')
            new_content, modified = fix_unused_datetime_timezone_imports(content)

            if modified:
                filepath.write_text(new_content, encoding='utf-8')
                files_modified += 1
                total_fixed += 1
                print(f"Cleaned: {filepath.relative_to(repo_root)}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    print(f"\nTotal files modified: {files_modified}")
    print(f"Total fixes applied: {total_fixed}")


if __name__ == '__main__':
    main()
