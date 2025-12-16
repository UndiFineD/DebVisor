#!/usr/bin/env python3
"""
F401 removal script using line-by-line analysis.
"""

import subprocess
import re

def get_f401_issues():
    """Get all F401 issues."""
    result = subprocess.run(
        ['python', '-m', 'flake8', 'scripts/agent', '--max-line-length=120'],
        capture_output=True,
        text=True
    )
    
    issues = {}
    for line in result.stdout.split('\n'):
        if 'F401' not in line:
            continue
        
        # Parse: "filepath:line:col: F401 'name' imported but unused"
        match = re.match(r"^([^:]+):(\d+):\d+:\s*F401\s+'([^']+)'", line)
        if match:
            filepath, lineno, fullname = match.groups()
            lineno = int(lineno)
            name = fullname.split('.')[-1]  # Just the class/function name
            
            if filepath not in issues:
                issues[filepath] = {}
            if lineno not in issues[filepath]:
                issues[filepath][lineno] = []
            issues[filepath][lineno].append(name)
    
    return issues

def remove_imports_from_line(line, names_to_remove):
    """Remove specific names from an import line."""
    # Try "from X import A, B, C" format
    match = re.match(r'^(\s*)from\s+(\S+)\s+import\s+(.*)$', line.rstrip())
    if match:
        indent, module, imports_str = match.groups()
        items = [item.strip() for item in imports_str.split(',')]
        
        # Filter out the names to remove
        filtered = []
        for item in items:
            base = item.split(' as ')[0].strip()
            if base not in names_to_remove:
                filtered.append(item)
        
        if not filtered:
            return None  # Remove entire line
        elif len(filtered) < len(items):
            return f'{indent}from {module} import {", ".join(filtered)}\n'
    
    # Try "import A, B, C" format
    match = re.match(r'^(\s*)import\s+(.*)$', line.rstrip())
    if match:
        indent, imports_str = match.groups()
        items = [item.strip() for item in imports_str.split(',')]
        
        filtered = []
        for item in items:
            base = item.split(' as ')[0].strip()
            if base not in names_to_remove:
                filtered.append(item)
        
        if not filtered:
            return None
        elif len(filtered) < len(items):
            return f'{indent}import {", ".join(filtered)}\n'
    
    return None  # No change

def fix_file(filepath, file_issues):
    """Fix all F401 issues in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return 0
    
    fixed = 0
    # Process in reverse to avoid index shifting
    for lineno in sorted(file_issues.keys(), reverse=True):
        names = file_issues[lineno]
        idx = lineno - 1
        
        if idx >= len(lines):
            continue
        
        new_line = remove_imports_from_line(lines[idx], names)
        
        if new_line is None:
            # Remove entire line
            lines.pop(idx)
            fixed += len(names)
        elif new_line != lines[idx]:
            # Replace line
            lines[idx] = new_line
            fixed += len(names)
    
    if fixed > 0:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        except:
            return 0
    
    return fixed

def main():
    print("F401 REMOVAL (Systematic)")
    print("=" * 50)
    
    issues = get_f401_issues()
    
    total = 0
    for filepath in sorted(issues.keys()):
        fixed = fix_file(filepath, issues[filepath])
        if fixed > 0:
            print(f"  {filepath}: {fixed} removed")
            total += fixed
    
    print(f"\nF401 total fixed: {total}")

if __name__ == '__main__':
    main()
