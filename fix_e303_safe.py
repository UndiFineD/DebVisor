#!/usr/bin/env python3
"""
Safe E303 blank line remover - handles multiple consecutive blank lines.
E303: too many blank lines (more than 2)
"""

import subprocess
import re

def get_flake8_issues():
    """Get E303 issues from flake8."""
    result = subprocess.run(
        ['python', '-m', 'flake8', 'scripts/agent', '--max-line-length=120'],
        capture_output=True,
        text=True
    )
    
    issues = {}
    for line in result.stdout.split('\n'):
        if 'E303' not in line:
            continue
        parts = line.split(':')
        if len(parts) >= 4:
            filepath = parts[0]
            lineno = int(parts[1])
            if filepath not in issues:
                issues[filepath] = set()
            issues[filepath].add(lineno)
    
    return issues

def fix_e303_safe(filepath):
    """Fix E303 by replacing 3+ blank lines with 2 blank lines."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0
    
    original = content
    
    # Replace 5+ blank lines with 2
    content = re.sub(r'\n\n\n\n\n+', '\n\n\n', content)
    # Replace 4 blank lines with 2
    content = re.sub(r'\n\n\n\n', '\n\n\n', content)
    # Replace 3 blank lines with 2
    content = re.sub(r'\n\n\n', '\n\n', content)
    
    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return 1
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return 0
    
    return 0

def main():
    print("SAFE E303 BLANK LINE REDUCER")
    print("=" * 50)
    
    issues = get_flake8_issues()
    
    if not issues:
        print("E303: 0 fixed")
        return
    
    total_fixed = 0
    for filepath in sorted(issues.keys()):
        fixed = fix_e303_safe(filepath)
        if fixed > 0:
            print(f"  {filepath}: normalized blank lines")
            total_fixed += fixed
    
    print(f"\nE303 files normalized: {total_fixed}")

if __name__ == '__main__':
    main()
