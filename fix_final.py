#!/usr/bin/env python3
"""Final comprehensive fixes"""

from pathlib import Path
import re

def final_fixes():
    """Apply final fixes"""
    file_path = Path("scripts/agent/agent.py")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Fix 1: Line 89 - E305 expected 2 blank lines after function def
    # Insert blank line before line 89 (after fix_markdown_content assignment)
    for i in range(len(lines)):
        if i == 88 and lines[i].strip() == '':  # Line 89 is blank
            # Check if we need another blank line before
            if i > 0 and lines[i-1].strip() != '':
                lines.insert(i, '\n')
                break
    
    # Fix 2: E713 - test for membership should be 'not in' (line 3613)
    for i, line in enumerate(lines):
        if i == 3612:  # Line 3613 (0-indexed)
            lines[i] = re.sub(r'\bnot\s+(\w+)\s+in\b', r'\1 not in ', line)
    
    # Fix 3: F541 - f-strings missing placeholders
    # Lines: 2892, 3092, 3431, 3518
    problematic_f_strings = [
        (2891, 2892),
        (3091, 3092),
        (3430, 3431),
        (3517, 3518),
    ]
    
    for f_line_start, f_line_num in problematic_f_strings:
        if f_line_start < len(lines):
            line = lines[f_line_start]
            # Find f-strings and remove the 'f' prefix if no placeholders
            # Match f"..." or f'...' without {
            line = re.sub(r'f(["\'])((?:(?!\1|{).)*)\1', r'\1\2\1', line)
            lines[f_line_start] = line
    
    # Fix 4: F841 - variable 'elapsed' never used (line 2943)
    # Just comment it out
    for i in range(len(lines)):
        if i == 2942 and 'elapsed' in lines[i] and '=' in lines[i]:
            indent = len(lines[i]) - len(lines[i].lstrip())
            lines[i] = ' ' * indent + '# ' + lines[i].lstrip()
    
    # Fix 5: F821 undefined name 'e' (line 1812)
    for i in range(len(lines)):
        if i == 1811:  # Line 1812
            # Remove reference to undefined 'e'
            lines[i] = re.sub(r'\{e[^}]*\}', '', lines[i])
            lines[i] = re.sub(r',\s*,', ',', lines[i])  # Clean double commas
    
    # Fix 6: E127/E122 - continuation line indentation issues
    # These are complex - let's try a different approach
    # Look for lines that have too much or too little indentation in continuation
    
    # Fix 7: E501 - line too long
    # Lines 1552, 3727, 3761
    # Can't easily auto-fix these without breaking code
    # Just leave them for now
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("Applied final fixes")

if __name__ == '__main__':
    final_fixes()
