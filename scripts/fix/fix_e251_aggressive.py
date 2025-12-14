#!/usr/bin/env python3
"""Aggressive but safe E251 fix - remove all spaces around = in function calls"""

import re

with open('opt/services/backup/backup_intelligence.py', 'r') as f:
    content = f.read()

# Strategy: Find all function/method calls and fix spacing
# We'll use a regex to find patterns like: word = word (in function args) and replace with word=word

# Pattern: inside parentheses, find spaces around =
# This should match: func(param = value) and change to func(param=value)
# But NOT: def func(param: type = default) which should stay with spaces

lines = content.split('\n')
result_lines = []

for line in lines:
    # Skip function definitions and type hints
    if 'def ' in line or '->' in line:
        result_lines.append(line)
        continue

    # For other lines, we can aggressively remove spaces around = in parentheses
    # Find sections within parentheses and fix them
    while '(' in line and ')' in line:
        # Find the first opening paren
        start_idx = line.find('(')
        # Find matching closing paren
        end_idx = -1
        depth = 0
        for i in range(start_idx, len(line)):
            if line[i] == '(':
                depth += 1
            elif line[i] == ')':
                depth -= 1
                if depth == 0:
                    end_idx = i
                    break

        if end_idx == -1:
            break

        # Extract the content inside parentheses
        inside = line[start_idx+1:end_idx]

        # Fix spacing around = (but be careful with type hints and strings)
        # Simple approach: remove spaces around = when surrounded by word characters
        fixed_inside = re.sub(r'(\w+)\s+=\s+', r'\1=', inside)

        # Replace and continue
        line = line[:start_idx+1] + fixed_inside + line[end_idx:]
        break  # Only fix one call per line

    result_lines.append(line)

content = '\n'.join(result_lines)

with open('opt/services/backup/backup_intelligence.py', 'w') as f:
    f.write(content)

print("Aggressive E251 fixes applied")
