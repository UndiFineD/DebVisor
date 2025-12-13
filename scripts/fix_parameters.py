#!/usr/bin/env python3
"""Fix parameter spacing issues"""

import re

with open('opt/services/backup/backup_intelligence.py', 'r') as f:
    lines = f.readlines()

result_lines = []
for i, line in enumerate(lines):
    # In function definitions (lines with def ...):
    # We want: param: type = default (with spaces)
    # Current wrong format: param: type=default (without spaces)

    # In function calls/class instantiation:
    # We want: ClassName(param=value) - NO spaces
    # Current wrong format might have spaces

    # Rule 1: If line is in function definition (contains 'def '),
    # ensure spaces around =
    if ' def ' in line:
        # Function definition - ensure spaces around = in parameters
        line = re.sub(r'(\w+):\s*(\w+)\s*=\s*', r'\1: \2 = ', line)

    # Rule 2: For class instantiation/function calls, remove spaces around =
    # Look for patterns like ClassName(param = value) and change
    # to ClassName(param=value)
    # But be careful not to affect assignment statements

    # Check if this is a class instantiation or function call
    if re.search(r'=\s*(.*?)\(', line):
        # This is like: test = RestoreTest(...)
        # Extract the part in parens and fix spacing
        match = re.search(r'(\w+)\s*=\s*([\w.]+)\((.*)\)', line)
        if match:
            var_name = match.group(1)
            class_name = match.group(2)
            params_str = match.group(3)

            # Fix parameter spacing: remove spaces around =
            params_str = re.sub(r'\s*=\s*', '=', params_str)

            ending = '\n' if line.endswith('\n') else ''
            line = f'{var_name} = {class_name}({params_str}){ending}'

    # Rule 3: Fix specific function call issues in named parameters
    # within function calls
    # Like: handler(vm_id = message, ...) should be handler(vm_id=message, ...)
    if '(' in line and ')' in line and ' = ' in line:
        # Check if this looks like a function call with keyword args
        # Pattern: word(keyword = value) -> word(keyword=value)
        line = re.sub(r'(\w+)\s*=\s*([^,)]+)(,|\))', r'\1=\2\3', line)

    result_lines.append(line)

with open('opt/services/backup/backup_intelligence.py', 'w') as f:
    f.writelines(result_lines)

print("Parameter spacing fixes applied")
