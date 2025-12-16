#!/usr/bin/env python3
"""
Aggressive E303 blank line remover.
E303: too many blank lines (more than 2)
This removes extra blank lines to reduce to maximum 2 blank lines.
"""

import re
import json
import subprocess
import sys

def get_flake8_issues():
    """Get E303 issues from flake8."""
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
        if len(parts) >= 4:
            filepath = parts[0]
            lineno = int(parts[1])
            if filepath not in issues:
                issues[filepath] = []
            issues[filepath].append(lineno)
    
    return issues

def fix_e303(filepath, line_numbers):
    """Fix E303 issues in a file by removing excess blank lines."""
    try:
        with open(filepath, 'r', encoding = 'utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0
    
    fixed = 0
    # Sort line numbers in reverse to avoid index shifting
    for lineno in sorted(set(line_numbers), reverse = True):
        idx = lineno - 1
        if idx >= len(lines):
            continue
        
        # Count consecutive blank lines starting from this line
        blank_count = 0
        start_idx = idx
        
        # Move backwards to find the start of blank line sequence
        while start_idx > 0 and lines[start_idx - 1].strip() == '':
            start_idx -= 1
            blank_count += 1
        
        blank_count += 1  # Count the current line
        
        # Move forward to count all consecutive blanks
        check_idx = idx + 1
        while check_idx < len(lines) and lines[check_idx].strip() == '':
            check_count = 1
            check_idx += 1
            blank_count += check_count
        
        # Remove excess blank lines (keep maximum 2)
        if blank_count > 2:
            # Remove blank_count - 2 lines
            to_remove = blank_count - 2
            for _ in range(to_remove):
                if idx < len(lines):
                    if lines[idx].strip() == '':
                        lines.pop(idx)
                    else:
                        idx -= 1
            fixed += to_remove
    
    # Write back
    if fixed > 0:
        try:
            with open(filepath, 'w', encoding = 'utf-8') as f:
                f.writelines(lines)
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return 0
    
    return fixed

def main():
    print("AGGRESSIVE E303 BLANK LINE REMOVER")
    print("=" * 50)
    
    issues = get_flake8_issues()
    
    if not issues:
        print("E303: 0 fixed")
        return
    
    total_fixed = 0
    for filepath in sorted(issues.keys()):
        line_numbers = issues[filepath]
        fixed = fix_e303(filepath, line_numbers)
        if fixed > 0:
            print(f"  {filepath}: {fixed} blanks removed")
            total_fixed += fixed
    
    print(f"\nE303 blank lines reduced: {total_fixed}")
    print(f"Total: {total_fixed}")

if __name__ == '__main__':
    main()
