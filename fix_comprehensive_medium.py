#!/usr/bin/env python3
"""
Comprehensive fixer for E501, E741, F541, F811, F402, E713, and remaining F401.
Targets medium-difficulty issues that can be fixed with pattern matching.
"""

import subprocess
import re
from pathlib import Path

def get_issues():
    result = subprocess.run(
        ['python', '-m', 'flake8', 'scripts/agent', '--max-line-length = 120'],
        capture_output = True,
        text = True
    )
    
    issues = {}
    for line in result.stdout.split('\n'):
        if not line:
            continue
        parts = line.split(':')
        if len(parts) >= 5:
            filepath = parts[0]
            lineno = int(parts[1])
            msg = ':'.join(parts[4:]).strip()
            code = msg.split()[0]
            
            if code in ['E501', 'E741', 'F541', 'F811', 'F402', 'E713', 'F401']:
                if filepath not in issues:
                    issues[filepath] = {}
                if lineno not in issues[filepath]:
                    issues[filepath][lineno] = []
                issues[filepath][lineno].append((code, msg))
    
    return issues

def fix_file(filepath, file_issues):
    """Apply fixes to file."""
    try:
        with open(filepath, 'r', encoding = 'utf-8') as f:
            lines = f.readlines()
    except:
        return 0
    
    fixed = 0
    
    for lineno in sorted(file_issues.keys(), reverse = True):
        codes_and_msgs = file_issues[lineno]
        idx = lineno - 1
        
        if idx >= len(lines):
            continue
        
        line = lines[idx]
        
        for code, msg in codes_and_msgs:
            
            # F401: unused import
            if code == 'F401':
                # Extract import name from message
                match = re.search(r"'([^']+)'", msg)
                if match:
                    fullname = match.group(1)
                    name = fullname.split('.')[-1]
                    
                    # Try to remove from multi-import
                    import_match = re.match(r'^(\s*)from\s+(\S+)\s+import\s+(.+)$', line.rstrip())
                    if import_match:
                        indent, module, imports_str = import_match.groups()
                        items = [item.strip() for item in imports_str.split(',')]
                        
                        filtered = []
                        for item in items:
                            base = item.split(' as ')[0].strip()
                            if base != name:
                                filtered.append(item)
                        
                        if filtered and len(filtered) < len(items):
                            new_imports = ', '.join(filtered)
                            new_line = f'{indent}from {module} import {new_imports}\n'
                            lines[idx] = new_line
                            fixed += 1
                        elif not filtered:
                            lines.pop(idx)
                            fixed += 1
            
            # E741: ambiguous variable name (l, O, I) - rename to standard names
            elif code == 'E741':
                # Match: for l in ..., l =, etc
                new_line = re.sub(r'\bl\b(?!\s*=\s*\d)', 'item', line)  # l to item (but not l = number)
                new_line = re.sub(r'\bO\b', 'obj', new_line)
                new_line = re.sub(r'\bI\b', 'idx', new_line)
                if new_line != line:
                    lines[idx] = new_line
                    fixed += 1
            
            # F541: f-string without placeholder
            elif code == 'F541':
                # Message: "f-string without any placeholders"
                # Remove the f prefix
                new_line = re.sub(r'\bf(["\'])', r'\1', line)
                if new_line != line:
                    lines[idx] = new_line
                    fixed += 1
            
            # E713: test for membership should be 'not in'
            elif code == 'E713':
                # not X in Y → X not in Y (but avoid import lines)
                if 'import' not in line:
                    new_line = re.sub(r'\bnot\s+(\w+)\s+in\b', r'\1 not in', line)
                    if new_line != line:
                        lines[idx] = new_line
                        fixed += 1
            
            # F811: redefined while unused
            elif code == 'F811':
                # This is harder - usually means a function is defined twice
                # We can comment out the first one (conservative approach)
                # For now, skip - requires more context
                pass
            
            # F402: import shadowed by loop variable
            elif code == 'F402':
                # This is a logic issue, skip for safety
                pass
            
            # E501: line too long
            elif code == 'E501':
                # Try to split string literals or comments
                if 'http' in line or '#' in line:
                    # This is complex, skip for now
                    pass
    
    if fixed > 0:
        try:
            with open(filepath, 'w', encoding = 'utf-8') as f:
                f.writelines(lines)
        except:
            return 0
    
    return fixed

def main():
    print("COMPREHENSIVE MEDIUM-ISSUE FIXER")
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
