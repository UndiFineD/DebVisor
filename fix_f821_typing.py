#!/usr/bin/env python3
"""Fix F821 undefined names - restore missing imports"""
import os
import re
import subprocess

agent_dir = r'c:\Users\kdejo\DEV\DebVisor\scripts\agent'

# Get all F821 issues
result = subprocess.run(
    ['python', '-m', 'flake8', '--max-line-length = 120', 'scripts/agent/'],
    capture_output = True, text = True, cwd = r'c:\Users\kdejo\DEV\DebVisor'
)

# Map of common undefined names to their imports
COMMON_IMPORTS = {
    'Tuple': 'typing',
    'List': 'typing',
    'Dict': 'typing',
    'Set': 'typing',
    'Optional': 'typing',
    'Union': 'typing',
    'Any': 'typing',
    'Callable': 'typing',
    'Generator': 'typing',
    'Iterator': 'typing',
    'Protocol': 'typing',
    'Literal': 'typing',
    'TypedDict': 'typing',
    'Sequence': 'typing',
}

# Parse F821 errors
undefined_by_file = {}
for line in (result.stderr + result.stdout).split('\n'):
    if 'F821' not in line:
        continue
    match = re.match(r'scripts/agent/([^:]+):\d+:\d+: F821 undefined name \'([^\']+)\'', line)
    if match:
        filename, name = match.groups()
        if filename not in undefined_by_file:
            undefined_by_file[filename] = set()
        undefined_by_file[filename].add(name)

fixed = 0

for filename, undefined_names in undefined_by_file.items():
    # Only process typing-related imports for now
    typing_missing = {n for n in undefined_names if n in COMMON_IMPORTS}
    if not typing_missing:
        continue
    
    filepath = os.path.join(agent_dir, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
    
    # Find existing typing import
    typing_import_line = None
    typing_imports = set()
    
    for i, line in enumerate(lines):
        if re.match(r'^\s*from\s+typing\s+import', line):
            typing_import_line = i
            # Parse what's already imported
            match = re.search(r'from\s+typing\s+import\s+(.+)$', line)
            if match:
                imports_str = match.group(1).strip()
                for item in imports_str.split(','):
                    typing_imports.add(item.strip().split(' as ')[0])
            break
    
    # Determine what needs to be added
    to_add = typing_missing - typing_imports
    if not to_add:
        continue
    
    # Add the missing imports
    if typing_import_line is not None:
        # Modify existing import
        line = lines[typing_import_line]
        # Simple append for now
        if line.rstrip().endswith(')'):
            # Multi-line import
            insert_pos = line.rfind(')')
            lines[typing_import_line] = line[:insert_pos] + ', ' + ', '.join(sorted(to_add)) + line[insert_pos:]
        else:
            # Single-line import
            lines[typing_import_line] = line.rstrip() + ', ' + ', '.join(sorted(to_add)) + '\n'
        fixed += len(to_add)
    else:
        # Add new typing import
        # Find where to insert (after other imports)
        insert_pos = 0
        for i, line in enumerate(lines):
            if re.match(r'^\s*(import|from)\s+', line):
                insert_pos = i + 1
        
        import_statement = 'from typing import ' + ', '.join(sorted(to_add)) + '\n'
        lines.insert(insert_pos, import_statement)
        fixed += len(to_add)
    
    with open(filepath, 'w', encoding = 'utf-8') as f:
        f.writelines(lines)

print(f"F821 undefined names fixed (typing imports): {fixed}")
