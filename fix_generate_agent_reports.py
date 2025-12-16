#!/usr/bin/env python3
"""
Fix E261 (comment spacing) and W293 (blank line whitespace) issues in generate_agent_reports.py
"""
import re

filepath = r"c:\Users\kdejo\DEV\DebVisor\scripts\agent\generate_agent_reports.py"

# Read file
with open(filepath, 'r', encoding = 'utf-8') as f:
    lines = f.readlines()

e261_fixed = 0
w293_fixed = 0

# Process each line
for i, line in enumerate(lines):
    # Fix W293: Remove whitespace from blank lines (but keep the newline)
    if line.strip() == '':
        if line != '\n':
            lines[i] = '\n'
            w293_fixed += 1
    
    # Fix E261: Ensure at least 2 spaces before inline comment
    # Only process lines with inline comments (have both code and comment)
    if '#' in line and not line.strip().startswith('#'):
        # Find the comment start position
        # Need to be careful about # in strings
        code_part = line.rstrip('\n')
        
        # Simple approach: look for # that's not at the start, after non-whitespace
        match = re.search(r'[^\s#]\s*#', code_part)
        if match:
            comment_pos = match.end() - 1  # Position of #
            code_end = comment_pos
            
            # Get content before comment
            before_comment = code_part[:code_end]
            comment_part = code_part[code_end:]
            
            # Check spaces before comment
            spaces_before = len(before_comment) - len(before_comment.rstrip())
            if spaces_before < 2:
                # Add spaces to make it 2
                before_comment = before_comment.rstrip() + '  '
                lines[i] = before_comment + comment_part + '\n'
                e261_fixed += 1

# Write file
with open(filepath, 'w', encoding = 'utf-8') as f:
    f.writelines(lines)

print(f"Fixed {e261_fixed} E261 (comment spacing) issues")
print(f"Fixed {w293_fixed} W293 (blank line whitespace) issues")
print(f"Total: {e261_fixed + w293_fixed} issues")
print(f"Successfully wrote fixed file to {filepath}")
