#!/usr/bin/env python3
"""Remove duplicate datetime imports."""

import re
from pathlib import Path


def deduplicate_datetime_imports(content: str) -> tuple[str, bool]:
    """Merge duplicate datetime import statements."""
    lines = content.split('\n')
    new_lines = []
    datetime_imports = []
    skip_until_line = -1
    modified = False

    for i, line in enumerate(lines):
        if i <= skip_until_line:
            continue

        if line.startswith('from datetime import'):
            # Found a datetime import, collect it
            current_import = line
            datetime_imports.append(current_import)

            # Look ahead for more datetime imports on next line
            j = i + 1
            while j < len(lines) and lines[j].startswith('from datetime import'):
                datetime_imports.append(lines[j])
                j += 1

            # If we found multiple imports, merge them
            if len(datetime_imports) > 1:
                # Parse and merge all imports
                all_items = set()
                for imp in datetime_imports:
                    # Extract imports after 'from datetime import'
                    match = re.search(r'from datetime import (.+)', imp)
                    if match:
                        items = match.group(1)
                        # Split by comma
                        for item in items.split(','):
                            item = item.strip()
                            if item:
                                all_items.add(item)

                # Create merged import
                merged = 'from datetime import ' + ', '.join(sorted(all_items))
                new_lines.append(merged)
                skip_until_line = j - 1
                modified = True
                datetime_imports = []
            else:
                new_lines.append(line)
                datetime_imports = []
        else:
            new_lines.append(line)

    return '\n'.join(new_lines), modified


def main():
    """Process all Python files."""
    repo_root = Path(__file__).parent.parent
    python_files = list(repo_root.rglob('*.py'))

    files_modified = 0
    total_merges = 0

    for filepath in sorted(python_files):
        if '.venv' in str(filepath):
            continue

        try:
            content = filepath.read_text(encoding='utf-8')
            new_content, modified = deduplicate_datetime_imports(content)

            if modified:
                filepath.write_text(new_content, encoding='utf-8')
                files_modified += 1
                total_merges += 1
                print(f"Deduped: {filepath.relative_to(repo_root)}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    print(f"\nTotal files modified: {files_modified}")
    print(f"Total deduplication operations: {total_merges}")


if __name__ == '__main__':
    main()
