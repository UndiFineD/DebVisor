#!/usr/bin/env python3
"""
Aggressive E303/E304 fixer - remove excess blank lines more thoroughly
"""
import os
import re

agent_dir = r'c:\Users\kdejo\DEV\DebVisor\scripts\agent'

total_fixed = 0

for filename in os.listdir(agent_dir):
    if not filename.endswith('.py'):
        continue
    
    filepath = os.path.join(agent_dir, filename)
    
    with open(filepath, 'r', encoding = 'utf-8') as f:
        content = f.read()
    
    original_length = len(content)
    
    # Pattern 1: More than 2 blank lines - replace with exactly 2
    while True:
        new_content = re.sub(r'\n\n\n\n+', '\n\n', content)
        if new_content == content:
            break
        content = new_content
    
    # Pattern 2: Blank lines immediately after @decorator
    lines = content.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # If this is a decorator line
        if line.lstrip().startswith('@'):
            # Check next line
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                # If next line is blank, skip it (E304)
                if next_line.strip() == '' and i + 2 < len(lines):
                    # Check if line after blank is def/class
                    line_after = lines[i + 2]
                    if line_after.lstrip().startswith(('def ', 'class ', 'async ', '@')):
                        # Skip the blank line
                        i += 2
                        continue
        
        i += 1
    
    content = '\n'.join(new_lines)
    
    # Count fixes
    if len(content) != original_length:
        fixed = (original_length - len(content)) // 1
        total_fixed += max(1, fixed // 2)  # Rough estimate
        
        with open(filepath, 'w', encoding = 'utf-8') as f:
            f.write(content)

print(f"E303/E304 blank line issues fixed: ~{total_fixed}")
