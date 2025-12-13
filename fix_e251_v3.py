#!/usr/bin/env python3
"""Fix E251 keyword argument spacing - handles multiline function calls"""
import re
import glob


def fix_e251_aggressive(content):
    """
    Fix E251 spacing issues more aggressively.
    We look for patterns like '   _word = value' or '   word = value'
    These are almost certainly keyword arguments in multiline function calls.
    """
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        # Lines with only indentation + keyword args typically have multiple spaces at start
        # Pattern: ^spaces + _?word + spaces + = + spaces
        # These are almost always keyword args in function calls
        if re.match(r'^\s{4,}(_?\w+)\s+=\s+', line):
            fixed_line = re.sub(r'(\w+)\s+=\s+', r'\1=', line)
            fixed_lines.append(fixed_line)
        elif '(' in line or '[' in line:
            # Also handle inline function calls
            fixed_line = re.sub(r'([\(\[,]\s*)(_?\w+)\s+=\s+', r'\1\2=', line)
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


# Find all Python test files
fixed_count = 0
for filepath in glob.glob("tests/**/*.py", recursive=True):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    content = fix_e251_aggressive(content)
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        fixed_count += 1
        print(f"Fixed: {filepath}")

print(f"\nDone! Fixed {fixed_count} files with E251 errors")
