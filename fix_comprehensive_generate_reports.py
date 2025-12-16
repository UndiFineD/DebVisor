#!/usr/bin/env python3
"""
Comprehensive fix for E261 and W293 issues in generate_agent_reports.py
"""

filepath = r"c:\Users\kdejo\DEV\DebVisor\scripts\agent\generate_agent_reports.py"

# Read file in binary mode to preserve exact line endings
with open(filepath, 'rb') as f:
    content = f.read()

# Decode to get string, then process
text = content.decode('utf-8')
lines = text.split('\n')

e261_fixed = 0
w293_fixed = 0
updated_lines = []

for i, line in enumerate(lines, 1):
    original_line = line
    
    # Fix W293: Blank lines with whitespace
    if line.strip() == '':
        # This is a blank line - remove any whitespace
        line = ''
        if original_line != line:
            w293_fixed += 1
    
    # Fix E261: At least 2 spaces before inline comment
    # Skip lines that start with # (full-line comments)
    elif '#' in line and not line.lstrip().startswith('#'):
        # Has an inline comment
        # Find comment position - simple approach: split on #
        parts = line.split('#', 1)
        if len(parts) == 2:
            code_part = parts[0]
            comment_part = '#' + parts[1]
            
            # Count spaces at end of code_part
            spaces = len(code_part) - len(code_part.rstrip())
            
            # Need at least 2 spaces
            if spaces < 2 and code_part.rstrip():  # Only if there's actual code
                code_stripped = code_part.rstrip()
                line = code_stripped + '  ' + comment_part
                e261_fixed += 1
    
    updated_lines.append(line)

# Reconstruct content with original line ending style
result = '\n'.join(updated_lines)
# If original ended with newline, add it back
if text.endswith('\n'):
    result += '\n'

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(result)

print(f"Fixed {e261_fixed} E261 (comment spacing) issues")
print(f"Fixed {w293_fixed} W293 (blank line whitespace) issues")
print(f"Total: {e261_fixed + w293_fixed} issues")
print(f"Successfully wrote fixed file to {filepath}")
