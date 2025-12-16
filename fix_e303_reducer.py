#!/usr/bin/env python3
"""
E303 fixer: Reduce sequences of more than 2 blank lines to exactly 2.
"""

import subprocess
import re

def get_e303_issues():
    result = subprocess.run(
        ['python', '-m', 'flake8', 'scripts/agent', '--max-line-length = 120'],
        capture_output = True,
        text = True
    )
    
    issues = {}
    for line in result.stdout.split('\n'):
        if 'E303' not in line:
            continue
        
        parts = line.split(':')
        if len(parts) >= 5:
            filepath = parts[0]
            lineno = int(parts[1])
            
            if filepath not in issues:
                issues[filepath] = set()
            issues[filepath].add(lineno)
    
    return issues

def fix_e303(filepath, line_numbers):
    """Fix E303 by reducing excessive blank lines to 2."""
    try:
        with open(filepath, 'r', encoding = 'utf-8') as f:
            lines = f.readlines()
    except:
        return 0
    
    fixed = 0
    processed = set()
    
    # Sort and process in reverse to avoid index issues
    for lineno in sorted(line_numbers, reverse = True):
        if lineno in processed:
            continue
        
        idx = lineno - 1
        if idx >= len(lines):
            continue
        
        # Count consecutive blank lines ending at this line
        blank_start = idx
        while blank_start > 0 and lines[blank_start - 1].strip() == '':
            blank_start -= 1
        
        blank_end = idx
        while blank_end < len(lines) - 1 and lines[blank_end + 1].strip() == '':
            blank_end += 1
        
        blank_count = blank_end - blank_start + 1
        
        # If more than 2, reduce to 2
        if blank_count > 2:
            to_remove = blank_count - 2
            for _ in range(to_remove):
                # Remove from blank_end working backwards
                if blank_end < len(lines):
                    lines.pop(blank_end)
                blank_end -= 1
            fixed += to_remove
        
        # Mark all lines in this sequence as processed
        for i in range(blank_start, min(blank_end + 1, len(lines))):
            processed.add(i + 1)
    
    if fixed > 0:
        try:
            with open(filepath, 'w', encoding = 'utf-8') as f:
                f.writelines(lines)
        except:
            return 0
    
    return fixed

def main():
    print("E303 REDUCER (Reduce >2 blanks to 2)")
    print("=" * 50)
    
    issues = get_e303_issues()
    total = 0
    
    for filepath in sorted(issues.keys()):
        fixed = fix_e303(filepath, issues[filepath])
        if fixed > 0:
            print(f"  {filepath}: {fixed} blank lines removed")
            total += fixed
    
    print(f"\nE303 total fixed: {total}")

if __name__ == '__main__':
    main()
