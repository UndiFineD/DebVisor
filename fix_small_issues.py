#!/usr/bin/env python3
"""
Low-risk small-issue fixer: W391, E266, E713
"""

import subprocess
import re

def get_issues():
    result = subprocess.run(
        ['python', '-m', 'flake8', 'scripts/agent', '--max-line-length=120'],
        capture_output=True,
        text=True
    )
    
    issues = {}
    for line in result.stdout.split('\n'):
        if not line:
            continue
        parts = line.split(':')
        if len(parts) >= 4:
            filepath = parts[0]
            lineno = int(parts[1])
            msg_start = parts[3].strip()
            code = msg_start.split()[0]
            
            if code in ['W391', 'E266', 'E713']:
                if filepath not in issues:
                    issues[filepath] = {}
                if lineno not in issues[filepath]:
                    issues[filepath][lineno] = []
                issues[filepath][lineno].append(code)
    
    return issues

def fix_file(filepath, file_issues):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return 0
    
    fixed = 0
    
    # Process in reverse
    for lineno in sorted(file_issues.keys(), reverse=True):
        codes = file_issues[lineno]
        idx = lineno - 1
        
        if idx >= len(lines):
            continue
        
        line = lines[idx]
        
        # W391: blank line at end of file
        if 'W391' in codes and idx == len(lines) - 1 and line.strip() == '':
            lines.pop(idx)
            fixed += 1
            continue
        
        # E266: too many leading # for block comment (should be ## with space)
        if 'E266' in codes:
            match = re.match(r'^(\s*)###(\s+)(.*)$', line.rstrip())
            if match:
                indent, spaces, content = match.groups()
                new_line = f'{indent}##  {content}\n'
                lines[idx] = new_line
                fixed += 1
                continue
        
        # E713: test for membership should be 'not in'
        if 'E713' in codes:
            # Match: not X in Y → X not in Y
            new_line = re.sub(r'\bnot\s+(\w+)\s+in\s+', r'\1 not in ', line)
            if new_line != line:
                # But be careful not to break imports
                if 'import' not in new_line:
                    lines[idx] = new_line
                    fixed += 1
    
    if fixed > 0:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        except:
            return 0
    
    return fixed

def main():
    print("SAFE SMALL ISSUE FIXER (W391, E266, E713)")
    print("=" * 50)
    
    issues = get_issues()
    total = 0
    
    for filepath in sorted(issues.keys()):
        fixed = fix_file(filepath, issues[filepath])
        if fixed > 0:
            print(f"  {filepath}: {fixed} fixed")
            total += fixed
    
    print(f"\nTotal fixed: {total}")

if __name__ == '__main__':
    main()
