#!/usr/bin/env python3
"""Remove unused imports identified by flake8 F401"""
import subprocess
import re
import os

agent_dir = r'c:\Users\kdejo\DEV\DebVisor\scripts\agent'

# Get all F401 issues
result = subprocess.run(
    ['python', '-m', 'flake8', '--max-line-length = 120', 'scripts/agent/'],
    capture_output = True,
    text = True,
    cwd = r'c:\Users\kdejo\DEV\DebVisor'
)

f401_map = {}
for line in (result.stderr + result.stdout).split('\n'):
    if 'F401' not in line:
        continue
    # Format: scripts/agent/agent-changes.py:33:1: F401 'typing.Callable' imported but unused
    match = re.match(r'scripts/agent/([^:]+):(\d+):\d+: F401 \'([^\']+)\' imported but unused', line)
    if match:
        filename, lineno, module_name = match.groups()
        lineno = int(lineno) - 1  # Convert to 0-indexed
        key = (filename, lineno)
        f401_map[key] = module_name

fixed = 0

for (filename, lineno), module_name in f401_map.items():
    filepath = os.path.join(agent_dir, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
    
    if lineno < len(lines):
        line = lines[lineno]
        # Check if this line imports the module
        if module_name in line and re.match(r'^\s*(import|from)\s+', line):
            # Extract just the import part
            if 'from' in line:
                # from X import Y - remove Y if it's the unused import
                parts = line.split('import')
                if len(parts) == 2:
                    before_import = parts[0]
                    after_import = parts[1].strip()
                    
                    # Parse the item being imported
                    if 'as' in after_import:
                        item = after_import.split('as')[0].strip()
                    else:
                        item = after_import.rstrip()
                    
                    # If it matches the module_name, remove the line
                    if item == module_name.split('.')[-1]:
                        lines[lineno] = ''
                        fixed += 1
            else:
                # Simple import - just remove it
                lines[lineno] = ''
                fixed += 1
    
    with open(filepath, 'w', encoding = 'utf-8') as f:
        f.writelines(lines)

print(f"F401 (unused imports) removed: {fixed}")
