#!/usr/bin/env python3
"""
Smart F401 remover for multi-import typing statements.
"""

import subprocess
import re

def get_flake8_f401_issues():
    """Get F401 unused import issues from flake8."""
    result = subprocess.run(
        ['python', '-m', 'flake8', 'scripts/agent', '--max-line-length = 120'],
        capture_output = True,
        text = True
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

def extract_import_names(messages):
    """Extract imported names from F401 messages."""
    names = []
    for msg in messages:
        # Message: "'typing.Callable' imported but unused" or "'concurrent.futures.ProcessPoolExecutor' imported but unused"
        match = re.search(r"'([^']+)'", msg)
        if match:
            full_name = match.group(1)
            # Get just the class/function name (last part)
            name = full_name.split('.')[-1]
            names.append(name)
    return names

def fix_file_f401(filepath, file_issues):
    """Fix F401 issues in a file."""
    try:
        with open(filepath, 'r', encoding = 'utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return 0
    
    fixed = 0
    # Process lines in reverse order to avoid index shifting
    for lineno in sorted(file_issues.keys(), reverse = True):
        messages = file_issues[lineno]
        idx = lineno - 1
        
        if idx >= len(lines):
            continue
        
        line = lines[idx]
        import_names = extract_import_names(messages)
        
        if not import_names:
            continue
        
        # Check if this is a "from X import ..." line
        if 'from' in line and 'import' in line:
            # Extract imports
            match = re.match(r'^(\s*)from\s+(\S+)\s+import\s+(.+)$', line.rstrip())
            if match:
                indent, module, imports_part = match.groups()
                
                # Split imports, handling both "A, B" and "A as a, B as b"
                items = [item.strip() for item in imports_part.split(',')]
                original_count = len(items)
                
                # Remove unused imports
                filtered_items = []
                for item in items:
                    # Get the base name (before 'as')
                    base_name = item.split(' as ')[0].strip()
                    if base_name not in import_names:
                        filtered_items.append(item)
                
                if len(filtered_items) < original_count:
                    if filtered_items:
                        # Reconstruct with remaining imports
                        new_imports = ', '.join(filtered_items)
                        new_line = f'{indent}from {module} import {new_imports}\n'
                        lines[idx] = new_line
                    else:
                        # Remove entire line
                        lines.pop(idx)
                    
                    fixed += original_count - len(filtered_items)
        
        elif 'import' in line and not 'from' in line:
            # Handle simple "import X" statements
            match = re.match(r'^(\s*)import\s+(.+)$', line.rstrip())
            if match:
                indent, imports_part = match.groups()
                items = [item.strip() for item in imports_part.split(',')]
                original_count = len(items)
                
                filtered_items = []
                for item in items:
                    base_name = item.split(' as ')[0].strip()
                    if base_name not in import_names:
                        filtered_items.append(item)
                
                if len(filtered_items) < original_count:
                    if filtered_items:
                        new_imports = ', '.join(filtered_items)
                        new_line = f'{indent}import {new_imports}\n'
                        lines[idx] = new_line
                    else:
                        lines.pop(idx)
                    
                    fixed += original_count - len(filtered_items)
    
    if fixed > 0:
        try:
            with open(filepath, 'w', encoding = 'utf-8') as f:
                f.writelines(lines)
        except Exception:
            return 0
    
    return fixed

def main():
    print("SMART F401 REMOVAL (Multi-Import Aware)")
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
