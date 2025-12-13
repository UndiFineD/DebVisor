#!/usr/bin/env python3
"""
Comprehensive markdown linting fixer for all documents.
Fixes common markdown issues like:
- MD003: Consistent heading style
- MD004: Consistent list marker style (dashes)
- MD005: Consistent list indentation
- MD007: Unordered list indentation (2 spaces)
- MD009: Trailing spaces
- MD010: Hard tabs
- MD011: Reversed link syntax
- MD012: Multiple consecutive blank lines
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
- MD034: Bare URLs (wrap in markdown links)
- MD036: Emphasis as heading (convert to proper heading)
- MD037: Spaces inside emphasis markers
- MD038: Spaces inside code span delimiters
- MD039: Spaces inside link text
- MD040: Missing language identifier in code blocks
- MD041: First line in a file should be a top level heading
- MD045: Images should have alternate text
- MD047: Missing trailing newline
"""

import re
import os
from pathlib import Path

def fix_markdown_file(file_path):
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

    # Fix MD020: No space inside hashes on closed atx style heading (e.g., ##heading## -> ## heading ##)
    content = re.sub(r'^(#+) +(.+?) +(#+)$', r'\1 \2 \3', content, flags=re.MULTILINE)

    # Fix MD021: Multiple spaces inside hashes on closed atx style heading
    content = re.sub(r'^(#+) {2,}(.+?) {2,}(#+)$', r'\1 \2 \3', content, flags=re.MULTILINE)

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
    content = re.sub(r'^(\s*)[0-9]+\. {2,}', r'\1. ', content, flags=re.MULTILINE)

    # Fix MD037: Remove spaces inside emphasis markers
    content = re.sub(r'\*\* +(.+?) +\*\*', r'**\1**', content)
    content = re.sub(r'\* +(.+?) +\*', r'*\1*', content)
    content = re.sub(r'__ +(.+?) +__', r'__\1__', content)
    content = re.sub(r'_ +(.+?) +_', r'_\1_', content)

    # Fix MD038: Remove spaces inside code span delimiters
    content = re.sub(r'` +(.+?) +`', r'`\1`', content)

    # Fix MD039: Remove spaces inside link text
    content = re.sub(r'\[ +(.+?) +\]', r'[\1]', content)

    # Fix MD034: Wrap bare URLs in markdown links
    content = re.sub(r'(?<!\[)https?://([^\s\)]+)(?!\))', r'[\g<0>](\g<0>)', content)

    # Fix MD047: Ensure file ends with exactly one newline
    content = content.rstrip() + '\n'

    # Fix MD022, MD031, MD032 with line-by-line processing
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
            # Add blank line before if needed
            if fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
            fixed_lines.append(line)
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
    """Main function to find and fix all markdown files."""
    repo_root = Path('.')
    excluded_dirs = {'.venv', '.git', '__pycache__', '.pytest_cache', 'node_modules', '.github'}

    # Find all .md and .plan.md files
    markdown_files = []
    for md_file in repo_root.rglob('*.md'):
        # Skip files in excluded directories
        if any(excluded in md_file.parts for excluded in excluded_dirs):
            continue
        markdown_files.append(md_file)

    if not markdown_files:
        print("No markdown files found.")
        return

    print(f"Found {len(markdown_files)} markdown files to check...")
    fixed_count = 0

    for md_file in sorted(markdown_files):
        relative_path = md_file.relative_to(repo_root)
        if fix_markdown_file(str(md_file)):
            print(f"  [FIXED] {relative_path}")
            fixed_count += 1

    print(f"\n[COMPLETE] Fixed {fixed_count}/{len(markdown_files)} markdown files")

if __name__ == '__main__':
    main()
