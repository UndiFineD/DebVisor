#!/usr/bin/env python3
"""
E741 and F541 targeted fixer.
E741: ambiguous variable names (l, O, I)
F541: f-string without placeholders
"""

import subprocess
import re

def get_e741_f541_issues():
    result = subprocess.run(
        ['python', '-m', 'flake8', 'scripts/agent', '--max-line-length = 120'],
        capture_output = True,
        text = True
    )
    
    issues = {}
    for line in result.stdout.split('\n'):
        if 'E741' not in line and 'F541' not in line:
            continue
        
        parts = line.split(':')
        if len(parts) >= 5:
            filepath = parts[0]
            lineno = int(parts[1])
            col = int(parts[2])
            msg = ':'.join(parts[4:]).strip()
            code = msg.split()[0]
            
            if filepath not in issues:
                issues[filepath] = {}
            if lineno not in issues[filepath]:
                issues[filepath][lineno] = []
            issues[filepath][lineno].append((code, col, msg))
    
    return issues

def fix_file(filepath, file_issues):
    try:
        with open(filepath, 'r', encoding = 'utf-8') as f:
            lines = f.readlines()
    except:
        return 0
    
    fixed = 0
    
    for lineno in sorted(file_issues.keys(), reverse = True):
        issues_at_line = file_issues[lineno]
        idx = lineno - 1
        
        if idx >= len(lines):
            continue
        
        line = lines[idx]
        
        for code, col, msg in issues_at_line:
            
            if code == 'E741':
                # Replace 'l' with 'item' (common list variable)
                # Be careful with 'l' in strings
                # Simple approach: replace l in comprehensions/for loops
                
                # Pattern: [l for l in ... or for l in ...
                new_line = re.sub(r'\bl\s+for\s+l\s+in\b', 'item for item in', line)
                
                # Pattern: for l in ...
                new_line = re.sub(r'\bfor\s+l\s+in\b', 'for item in', new_line)
                
                # Also replace other 'l' references in same context
                # This is tricky, so be conservative
                
                if new_line != line:
                    lines[idx] = new_line
                    fixed += 1
            
            elif code == 'F541':
                # f-string without placeholders - remove f prefix
                # Pattern: f"string" or f'string'
                new_line = re.sub(r'\bf(["\'])', r'\1', line)
                
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
    print("E741 & F541 TARGETED FIXER")
    print("=" * 50)
    
    issues = get_e741_f541_issues()
    total = 0
    
    for filepath in sorted(issues.keys()):
        fixed = fix_file(filepath, issues[filepath])
        if fixed > 0:
            print(f"  {filepath}: {fixed} fixed")
            total += fixed
    
    print(f"\nTotal fixed: {total}")

if __name__ == '__main__':
    main()
