#!/usr/bin/env python3
"""Aggressive multi-issue flake8 fixer"""
import os
import re
import subprocess

agent_dir = r'c:\Users\kdejo\DEV\DebVisor\scripts\agent'

stats = {
    'e303': 0, 'e306': 0, 'e305': 0, 'e301': 0,
    'f401': 0, 'e999': 0, 'e501': 0, 'w391': 0
}

# Get flake8 output for F401 and E999 issues
result = subprocess.run(
    ['python', '-m', 'flake8', '--max-line-length = 120', 'scripts/agent/'],
    capture_output = True, text = True, cwd = r'c:\Users\kdejo\DEV\DebVisor'
)

# Parse F401 and E999
f401_lines = {}
e999_lines = {}
for line in (result.stderr + result.stdout).split('\n'):
    if 'F401' in line:
        match = re.match(r'scripts/agent/([^:]+):(\d+):', line)
        if match:
            fname, lnum = match.groups()
            f401_lines.setdefault(fname, set()).add(int(lnum) - 1)
    elif 'E999' in line:
        match = re.match(r'scripts/agent/([^:]+):(\d+):', line)
        if match:
            fname, lnum = match.groups()
            e999_lines.setdefault(fname, set()).add(int(lnum) - 1)

# Fix all files
for filename in os.listdir(agent_dir):
    if not filename.endswith('.py'):
        continue
    filepath = os.path.join(agent_dir, filename)
    with open(filepath, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
    
    modified = False
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # E303: Collapse 4+ blanks to 2
        if line.strip() == '':
            blank_count = 1
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                blank_count += 1
                j += 1
            if blank_count > 2:
                new_lines.append('\n\n')
                stats['e303'] += blank_count - 2
                i = j
                modified = True
                continue
        
        # E306: Expected blank line before nested definition
        if i > 0 and line.lstrip().startswith(('def ', 'class ', 'async ')):
            if new_lines[-1].strip() != '' and i > 0:
                # Check if inside another function/class
                indent = len(line) - len(line.lstrip())
                if indent > 0:
                    new_lines.append('\n')
                    stats['e306'] += 1
                    modified = True
        
        # E305: Expected 2 blank lines after class/function
        if i > 0 and line.lstrip().startswith(('def ', 'class ', '@')) and i > 0:
            prev_line = new_lines[-1] if new_lines else ''
            if prev_line.strip() != '':
                # Add blanks if needed
                prev_indent = len(prev_line) - len(prev_line.lstrip()) if prev_line.strip() else 0
                curr_indent = len(line) - len(line.lstrip())
                if curr_indent <= prev_indent and prev_line.strip():
                    blank_count = 0
                    j = i - 1
                    while j >= 0 and lines[j].strip() == '':
                        blank_count += 1
                        j -= 1
                    if blank_count < 2:
                        new_lines.append('\n')
                        stats['e305'] += 1
                        modified = True
        
        # W391: Remove blank line at end of file
        if i == len(lines) - 1 and line.strip() == '':
            # Skip last blank line
            stats['w391'] += 1
            modified = True
            i += 1
            continue
        
        # E501: Truncate long lines that exceed 120 chars (try to break them)
        if len(line.rstrip()) > 120:
            if '#' in line and line.strip()[0] != '#':
                parts = line.split('#', 1)
                code = parts[0].rstrip()
                comment = '#' + parts[1]
                if len(code) + 2 < 120:  # Code fits on its own line
                    new_lines.append(code + '\n')
                    new_lines.append(comment)
                    stats['e501'] += 1
                    modified = True
                    i += 1
                    continue
        
        # F401: Remove unused imports (skip if already marked)
        if filename in f401_lines and i in f401_lines[filename]:
            if re.match(r'^\s*(import|from)\s+', line):
                stats['f401'] += 1
                modified = True
                i += 1
                continue
        
        new_lines.append(line)
        i += 1
    
    if modified and new_lines != lines:
        with open(filepath, 'w', encoding = 'utf-8') as f:
            f.writelines(new_lines)

print("=" * 60)
print("FLAKE8 FIXES APPLIED")
print("=" * 60)
for code, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"{code.upper():6s}: {count:4d} fixed")
print("=" * 60)
print(f"Total: {sum(stats.values())} issues fixed")
