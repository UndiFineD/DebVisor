#!/usr/bin/env python3
"""Targeted F401 unused import remover with safety checks"""
import os
import re
import subprocess

agent_dir = r'c:\Users\kdejo\DEV\DebVisor\scripts\agent'

# Get all F401 issues
result = subprocess.run(
    ['python', '-m', 'flake8', '--max-line-length=120', 'scripts/agent/'],
    capture_output=True, text=True, cwd=r'c:\Users\kdejo\DEV\DebVisor'
)

# Collect F401 issues by file and line
f401_map = {}
for line in (result.stderr + result.stdout).split('\n'):
    if 'F401' not in line:
        continue
    # Example: scripts/agent/agent-changes.py:33:1: F401 'typing.Callable' imported but unused
    match = re.match(r'scripts/agent/([^:]+):(\d+):\d+: F401 \'([^\']+)\'', line)
    if match:
        filename, lineno, module_name = match.groups()
        lineno = int(lineno)
        if filename not in f401_map:
            f401_map[filename] = {}
        if lineno not in f401_map[filename]:
            f401_map[filename][lineno] = []
        f401_map[filename][lineno].append(module_name)

fixed = 0

# Process only files with F401 issues
for filename, line_issues in f401_map.items():
    filepath = os.path.join(agent_dir, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Process in reverse so line numbers don't shift
    for lineno in sorted(line_issues.keys(), reverse=True):
        lineno_idx = lineno - 1  # Convert to 0-indexed
        if lineno_idx < len(lines):
            line = lines[lineno_idx]
            modules = line_issues[lineno]
            
            # Only remove if it's a simple import statement
            if re.match(r'^\s*(from|import)\s+', line):
                # Check if we can safely remove it
                # For now, remove only complete lines with single imports
                if re.match(r'^\s*import\s+\w+\s*$', line):
                    # Simple import like "import xyz"
                    lines[lineno_idx] = ''
                    fixed += 1
                elif re.match(r'^\s*from\s+[^\s]+\s+import\s+\w+\s*$', line):
                    # From import like "from x import y"
                    lines[lineno_idx] = ''
                    fixed += 1
    
    # Write back if modified
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)

print(f"F401 imports safely removed: {fixed}")
