#!/usr/bin/env python3
"""
Rename all remaining 'l' variables to 'line' or 'item' for clarity.
This fixes E741 ambiguous variable names.
"""

import subprocess
import re

def get_e741_issues():
    result = subprocess.run(
        ['python', '-m', 'flake8', 'scripts/agent', '--max-line-length = 120'],
        capture_output = True,
        text = True
    )
    
    issues = {}
    for line in result.stdout.split('\n'):
        if 'E741' not in line:
            continue
        
        parts = line.split(':')
        if len(parts) >= 5:
            filepath = parts[0]
            lineno = int(parts[1])
            
            if filepath not in issues:
                issues[filepath] = set()
            issues[filepath].add(lineno)
    
    return issues

def fix_file(filepath, line_numbers):
    try:
        with open(filepath, 'r', encoding = 'utf-8') as f:
            lines = f.readlines()
    except:
        return 0
    
    fixed = 0
    
    for lineno in sorted(line_numbers, reverse = True):
        idx = lineno - 1
        if idx >= len(lines):
            continue
        
        line = lines[idx]
        
        # Replace [l for l in ...] with [line for line in ...]
        new_line = re.sub(r'\[l\s+for\s+l\s+in\s+', '[line for line in ', line)
        # Replace (l for l in ...) with (line for line in ...)
        new_line = re.sub(r'\(l\s+for\s+l\s+in\s+', '(line for line in ', new_line)
        # Replace ,l for l in with ,line for line in
        new_line = re.sub(r',l\s+for\s+l\s+in\s+', ',line for line in ', new_line)
        # Replace with 'item' for other contexts
        new_line = re.sub(r'\bl\b(?=\s+for\s+\w+\s+in\s+)', 'item', new_line) if 'for' in new_line else new_line
        
        if new_line != line:
            lines[idx] = new_line
            fixed += 1
    
    if fixed > 0:
        try:
            with open(filepath, 'w', encoding = 'utf-8') as f:
                f.writelines(lines)
        except:
            return 0
    
    return fixed

def main():
    print("E741 FINAL RENAMER (l → line/item)")
    print("=" * 50)
    
    issues = get_e741_issues()
    total = 0
    
    for filepath in sorted(issues.keys()):
        fixed = fix_file(filepath, issues[filepath])
        if fixed > 0:
            print(f"  {filepath}: {fixed} fixed")
            total += fixed
    
    print(f"\nTotal fixed: {total}")

if __name__ == '__main__':
    main()
