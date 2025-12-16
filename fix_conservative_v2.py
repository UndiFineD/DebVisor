#!/usr/bin/env python3
"""Conservative multi-issue fixer - only safe, tested patterns"""
import os
import re
import subprocess

agent_dir = r'c:\Users\kdejo\DEV\DebVisor\scripts\agent'

stats = {
    'e303_blanks': 0,  # Reduce 3+ blanks to 2
    'w391_eof': 0,     # Remove EOF blanks
    'f401_simple': 0,  # Only remove complete standalone imports
}

# Get E999 (syntax errors) which indicate broken files - skip those
result = subprocess.run(
    ['python', '-m', 'flake8', '--max-line-length=120', 'scripts/agent/'],
    capture_output=True, text=True, cwd=r'c:\Users\kdejo\DEV\DebVisor'
)

broken_files = set()
for line in (result.stderr + result.stdout).split('\n'):
    if 'E999' in line:
        match = re.match(r'scripts/agent/([^:]+):', line)
        if match:
            broken_files.add(match.group(1))

print(f"Skipping {len(broken_files)} files with syntax errors")

for filename in os.listdir(agent_dir):
    if not filename.endswith('.py'):
        continue
    if filename in broken_files:
        print(f"  Skipping {filename} (syntax error)")
        continue
    
    filepath = os.path.join(agent_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Pattern 1: E303 - More than 2 consecutive blank lines
        if line.strip() == '':
            blank_count = 1
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                blank_count += 1
                j += 1
            
            # Only reduce if there are 3 or more blanks
            if blank_count > 2:
                # Add exactly 2 blanks
                new_lines.append('\n\n')
                stats['e303_blanks'] += (blank_count - 2)
                i = j
                continue
        
        # Pattern 2: W391 - Blank line at end of file
        if i == len(lines) - 1 and line.strip() == '':
            # Don't add final blank line
            stats['w391_eof'] += 1
            i += 1
            continue
        
        new_lines.append(line)
        i += 1
    
    # Only write if changed
    if new_lines != lines:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

print("\n" + "=" * 60)
print("CONSERVATIVE FLAKE8 FIXES APPLIED")
print("=" * 60)
for code, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"{code:20s}: {count:4d}")
print("=" * 60)
total = sum(stats.values())
print(f"Total: {total} issues fixed")
