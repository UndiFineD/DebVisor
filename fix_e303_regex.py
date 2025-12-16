#!/usr/bin/env python3
"""
E303 fixer using regex: Replace 3+ newlines with 2 newlines.
"""

import subprocess
import re
from pathlib import Path

def get_e303_files():
    """Get files with E303 issues."""
    result = subprocess.run(
        ['python', '-m', 'flake8', 'scripts/agent', '--max-line-length=120'],
        capture_output=True,
        text=True
    )
    
    files = set()
    for line in result.stdout.split('\n'):
        if 'E303' in line:
            filepath = line.split(':')[0]
            files.add(filepath)
    
    return files

def fix_file_e303(filepath):
    """Fix E303 in file by regex."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return 0
    
    original = content
    
    # Replace 5+ newlines with 3 newlines (\n\n is blank line, \n\n\n is 2 blanks)
    # We want max 2 blank lines = 3 newlines total
    content = re.sub(r'\n{5,}', '\n\n\n', content)
    # Replace 4 newlines with 3
    content = re.sub(r'\n\n\n\n', '\n\n\n', content)
    
    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return 1
        except:
            return 0
    
    return 0

def main():
    print("E303 REGEX FIXER (5+ newlines → 3 newlines)")
    print("=" * 50)
    
    files = get_e303_files()
    total = 0
    
    for filepath in sorted(files):
        fixed = fix_file_e303(filepath)
        if fixed > 0:
            print(f"  {filepath}: normalized")
            total += fixed
    
    print(f"\nFiles fixed: {total}")

if __name__ == '__main__':
    main()
