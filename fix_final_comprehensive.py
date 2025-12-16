#!/usr/bin/env python3
"""Final comprehensive fixer for multiple small issues"""
import os
import re
import subprocess

agent_dir = r'c:\Users\kdejo\DEV\DebVisor\scripts\agent'

result = subprocess.run(
    ['python', '-m', 'flake8', '--max-line-length = 120', 'scripts/agent/'],
    capture_output = True, text = True, cwd = r'c:\Users\kdejo\DEV\DebVisor'
)

stats = {'e266': 0, 'e301': 0, 'e305': 0}

# Parse issues
e266_lines = {}  # E266: inline comment should start with '# '
e301_lines = {}  # E301: expected 1 blank line
e305_lines = {}  # E305: expected 2 blank lines after class/function

for line in (result.stderr + result.stdout).split('\n'):
    if 'E266' in line:
        match = re.match(r'scripts/agent/([^:]+):(\d+):', line)
        if match:
            f, l = match.groups()
            e266_lines.setdefault(f, set()).add(int(l) - 1)
    elif 'E301' in line:
        match = re.match(r'scripts/agent/([^:]+):(\d+):', line)
        if match:
            f, l = match.groups()
            e301_lines.setdefault(f, set()).add(int(l) - 1)
    elif 'E305' in line:
        match = re.match(r'scripts/agent/([^:]+):(\d+):', line)
        if match:
            f, l = match.groups()
            e305_lines.setdefault(f, set()).add(int(l) - 1)

# Fix files
for filename in os.listdir(agent_dir):
    if not filename.endswith('.py'):
        continue
    
    has_issues = (filename in e266_lines or filename in e301_lines or filename in e305_lines)
    if not has_issues:
        continue
    
    filepath = os.path.join(agent_dir, filename)
    with open(filepath, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
    
    modified = False
    
    # Fix E266: ##comment -> # comment
    if filename in e266_lines:
        for lineno in e266_lines[filename]:
            if lineno < len(lines):
                line = lines[lineno]
                # Replace ## with # (only at line level comments)
                if '#' in line and not line.strip().startswith('#'):
                    # Inline comment
                    new_line = re.sub(r'(\s)#+\s*', r'\1# ', line)
                    if new_line != line:
                        lines[lineno] = new_line
                        stats['e266'] += 1
                        modified = True
    
    if modified:
        with open(filepath, 'w', encoding = 'utf-8') as f:
            f.writelines(lines)

print(f"E266 (comment format) fixed: {stats['e266']}")
print(f"E301 (blank line) fixed: {stats['e301']}")
print(f"E305 (blank lines after) fixed: {stats['e305']}")
print(f"Total: {sum(stats.values())}")
