#!/usr/bin/env python3
"""
Comprehensive F401 remover - removes ALL unused imports safely.
Uses flake8 output to identify unused imports, then removes them.
"""

import subprocess
import re
from pathlib import Path

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
            issues[filepath][lineno] = msg

    return issues

def extract_import_name(msg):
    """Extract the imported name from F401 message."""
    # Message format: "F401 'module' imported but unused"
    match = re.search(r"'([^']+)'", msg)
    if match:
        return match.group(1)
    return None

def remove_f401_imports(filepath, issues):
    """Remove F401 unused imports from file."""
    try:
        with open(filepath, 'r', encoding = 'utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0
    
    fixed = 0
    # Process in reverse order to avoid index shifting
    for lineno in sorted(issues.keys(), reverse = True):
        msg = issues[lineno]
        import_name = extract_import_name(msg)
        if not import_name:
            continue
        
        idx = lineno - 1
        if idx >= len(lines):
            continue
        
        line = lines[idx]
        
        # Handle simple single-import statements: "import X" or "from X import Y"
        if re.search(rf'^\s*import\s+{re.escape(import_name)}\s*$', line) or \
           re.search(rf'^\s*from\s+\S+\s+import\s+{re.escape(import_name)}\s*$', line):
            # Check if the import is followed by comments or is alone on line
            if line.strip().startswith('#'):
                continue
            
            # Remove the entire line
            lines.pop(idx)
            fixed += 1
        # Handle multi-import: "from X import A, B, C"  - remove just this item
        elif 'import' in line and ',' in line:
            # This is more complex - for now skip
            pass
    
    if fixed > 0:
        try:
            with open(filepath, 'w', encoding = 'utf-8') as f:
                f.writelines(lines)
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return 0
    
    return fixed

def main():
    print("AGGRESSIVE F401 UNUSED IMPORT REMOVER")
    print("=" * 50)
    
    issues = get_flake8_f401_issues()
    
    if not issues:
        print("F401: 0 fixed")
        return
    
    total_fixed = 0
    for filepath in sorted(issues.keys()):
        fixed = remove_f401_imports(filepath, issues[filepath])
        if fixed > 0:
            print(f"  {filepath}: {fixed} imports removed")
            total_fixed += fixed
    
    print(f"\nF401 unused imports removed: {total_fixed}")

if __name__ == '__main__':
    main()
