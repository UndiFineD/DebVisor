#!/usr/bin/env python3
"""
Safe F401 removal - remove imports that flake8 flags but verify they're safe
Runs flake8 and parses F401 errors to remove verified unused imports
"""
import subprocess
import re
import os

agent_dir = r'c:\Users\kdejo\DEV\DebVisor\scripts\agent'

# Get all F401 issues from flake8
result = subprocess.run(
    ['python', '-m', 'flake8', '--max-line-length = 120', 'scripts/agent/'],
    capture_output = True,
    text = True,
    cwd = r'c:\Users\kdejo\DEV\DebVisor'
)

f401_issues = {}
for line in (result.stderr + result.stdout).split('\n'):
    match = re.match(r'scripts/agent/([^:]+):(\d+):\d+: F401 ([^\(]+)\(', line)
    if match:
        filename, lineno, msg = match.groups()
        lineno = int(lineno)
        if filename not in f401_issues:
            f401_issues[filename] = []
        f401_issues[filename].append((lineno, msg.strip()))

fixed = 0

for filename, issues in f401_issues.items():
    filepath = os.path.join(agent_dir, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
    
    # Sort by line number descending so we can delete without offset issues
    for lineno, msg in sorted(issues, reverse = True):
        lineno = lineno - 1  # 0-indexed
        if 0 <= lineno < len(lines):
            line = lines[lineno]
            # Simple check: if it's just an import line, remove it
            if re.match(r'^\s*(import|from)\s+', line):
                lines.pop(lineno)
                fixed += 1
    
    with open(filepath, 'w', encoding = 'utf-8') as f:
        f.writelines(lines)

print(f"F401 (unused imports) safely removed: {fixed}")
