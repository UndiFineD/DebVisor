#!/usr/bin/env python3
"""
Smart F401 remover - handles multi-import statements.
"""

import subprocess
import re

def get_flake8_f401_issues():
    """Get F401 unused import issues from flake8."""
    result = subprocess.run(
        ['python', '-m', 'flake8', 'scripts/agent', '--max-line-length=120'],
        capture_output=True,
        text=True
    )
    
    issues = {}
    for line in result.stdout.split('\n'):
        if 'F401' not in line:
            continue
        parts = line.split(':')
        if len(parts) >= 5:
            filepath = parts[0]
            lineno = int(parts[1])
            msg = ':'.join(parts[4:]).strip()
            
            if filepath not in issues:
                issues[filepath] = {}
            if lineno not in issues[filepath]:
                issues[filepath][lineno] = []
            issues[filepath][lineno].append(msg)
    
    return issues

def extract_import_name(msg):
    """Extract the imported name from F401 message: 'typing.Callable' imported but unused"""
    match = re.search(r"'([^']+)'", msg)
    if match:
        return match.group(1).split('.')[-1]  # Get just the final name (Callable from typing.Callable)
    return None

def remove_from_import_line(line, import_name):
    """Remove import_name from a 'from X import A, B, C' line."""
    # Match: from X import A, B, C
    match = re.match(r'^(\s*)from\s+(\S+)\s+import\s+(.+)$', line)
    if not match:
        return None
    
    indent, module, imports_str = match.groups()
    
    # Split by comma and clean up
    items = [item.strip() for item in imports_str.split(',')]
    
    # Remove the unused import
    items = [item for item in items if item != import_name and not item.startswith(import_name + ' ')]
    
    if not items:
        # Entire import line becomes empty - remove it
        return None
    
    # Reconstruct
    return f'{indent}from {module} import {", ".join(items)}\n'

def fix_file_f401(filepath, file_issues):
    """Fix F401 issues in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0
    
    fixed = 0
    # Process lines in reverse order
    for lineno in sorted(file_issues.keys(), reverse=True):
        messages = file_issues[lineno]
        idx = lineno - 1
        
        if idx >= len(lines):
            continue
        
        line = lines[idx]
        import_names = [extract_import_name(msg) for msg in messages]
        import_names = [n for n in import_names if n]
        
        if not import_names:
            continue
        
        # Try to remove from multi-import
        for import_name in import_names:
            new_line = remove_from_import_line(line, import_name)
            if new_line is None:
                # Remove entire line
                lines.pop(idx)
                fixed += 1
                break
            elif new_line != line:
                # Replace with modified line
                lines[idx] = new_line
                line = new_line
                fixed += 1
    
    if fixed > 0:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return 0
    
    return fixed

def main():
    print("SMART F401 MULTI-IMPORT REMOVER")
    print("=" * 50)
    
    issues = get_flake8_f401_issues()
    
    if not issues:
        print("F401: 0 fixed")
        return
    
    total_fixed = 0
    for filepath in sorted(issues.keys()):
        fixed = fix_file_f401(filepath, issues[filepath])
        if fixed > 0:
            print(f"  {filepath}: {fixed} imports removed")
            total_fixed += fixed
    
    print(f"\nF401 total fixed: {total_fixed}")

if __name__ == '__main__':
    main()
