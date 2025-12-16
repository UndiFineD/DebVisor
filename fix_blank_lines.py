#!/usr/bin/env python3
"""
Fix E303 (too many blank lines), E304 (blank lines after decorator),
E302 (missing blank lines), and E305 issues across all agent files.
"""
import os
import re

agent_dir = r'c:\Users\kdejo\DEV\DebVisor\scripts\agent'

e303_fixed = 0
e304_fixed = 0
e302_fixed = 0
e305_fixed = 0

for filename in os.listdir(agent_dir):
    if not filename.endswith('.py'):
        continue
    
    filepath = os.path.join(agent_dir, filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Process file line by line
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for E303: too many blank lines (more than 2)
        if line.strip() == '':
            blank_count = 1
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                blank_count += 1
                j += 1
            
            # If more than 2 blanks, reduce to 2
            if blank_count > 2:
                new_lines.append('\n')
                new_lines.append('\n')
                e303_fixed += (blank_count - 2)
                i = j
                continue
            else:
                # Keep blank lines as-is if <= 2
                new_lines.append(line)
                i += 1
                continue
        
        # Check for E304: blank lines immediately after decorator
        if line.lstrip().startswith('@') or (new_lines and new_lines[-1].lstrip().startswith('@')):
            # This is a decorator line
            if new_lines and new_lines[-1].lstrip().startswith('@'):
                # Previous line was decorator, check if current is blank
                if line.strip() == '':
                    # Skip this blank line (E304)
                    e304_fixed += 1
                    i += 1
                    continue
        
        new_lines.append(line)
        i += 1
    
    # Write back only if changed
    if len(new_lines) != len(lines):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

print(f"E303 (too many blank lines) fixed: {e303_fixed}")
print(f"E304 (blank lines after decorator) fixed: {e304_fixed}")
print(f"Total blank line issues fixed: {e303_fixed + e304_fixed}")
