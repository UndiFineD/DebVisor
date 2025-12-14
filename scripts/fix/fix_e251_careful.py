#!/usr/bin/env python3
"""Carefully fix E251 keyword argument spacing"""

with open('opt/services/backup/backup_intelligence.py', 'r') as f:
    lines = f.readlines()

result_lines = []

for line in lines:
    # Only process lines that have function calls (parentheses)
    if '(' not in line or ')' not in line:
        result_lines.append(line)
        continue

    # Split by parentheses to handle multiple calls
    parts = []
    current_pos = 0

    for i, char in enumerate(line):
        if char == '(':
            # Found opening paren, collect everything until closing
            j = i + 1
            depth = 1
            func_content = []

            while j < len(line) and depth > 0:
                if line[j] == '(':
                    depth += 1
                elif line[j] == ')':
                    depth -= 1
                func_content.append(line[j])
                j += 1

            # Now fix the func_content - replace " = " with "="
            func_str = ''.join(func_content[:-1])  # Remove the closing paren

            # Replace spaces around = with just =
            # But be careful not to affect strings or type hints
            import re
            fixed_func = re.sub(r'(\w+)\s+=\s+', r'\1=', func_str)

            # Add back and continue
            line = (line[:i+1] + fixed_func + ')' + line[j:])
            break  # Only handle one call per line for safety

    result_lines.append(line)

with open('opt/services/backup/backup_intelligence.py', 'w') as f:
    f.writelines(result_lines)

print("Careful E251 fixes applied")
