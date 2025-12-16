#!/usr/bin/env python3
"""Smart flake8 fixes for agent.py - only safe automatic fixes"""

from pathlib import Path
import re

def fix_agent_py():
    """Apply safe flake8 fixes"""
    file_path = Path("scripts/agent/agent.py")
    with open(file_path, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
    
    # Keep track of changes
    changes = []
    
    # Fix 1: E303 (too many blank lines - reduce to max 2)
    result = []
    consecutive_blanks = 0
    for line_num, line in enumerate(lines, 1):
        if line.strip() == '':
            consecutive_blanks += 1
            if consecutive_blanks <= 2:
                result.append(line)
            else:
                changes.append(f"Line {line_num}: Removed excess blank line (E303)")
        else:
            consecutive_blanks = 0
            result.append(line)
    lines = result
    
    # Fix 2: Remove trailing whitespace (W291) and fix blank lines with whitespace (W293)
    result = []
    for line_num, line in enumerate(lines, 1):
        if line.rstrip() == '' and line != '\n':
            # Blank line with whitespace
            result.append('\n')
            changes.append(f"Line {line_num}: Removed trailing whitespace from blank line (W293)")
        elif line.rstrip('\n') != line.rstrip():
            # Trailing whitespace
            result.append(line.rstrip() + '\n')
            changes.append(f"Line {line_num}: Removed trailing whitespace (W291)")
        else:
            result.append(line)
    lines = result
    
    # Fix 3: E713 - test for membership should be 'not in'
    for i, line in enumerate(lines):
        original = line
        # Pattern: "not variable in something" -> "variable not in something"
        # Be careful not to touch "not ... in ..." strings
        line = re.sub(r'\bnot\s+(\w+)\s+in\b', r'\1 not in ', line)
        if line != original:
            changes.append(f"Line {i+1}: Fixed membership test operator (E713)")
        lines[i] = line
    
    # Fix 4: Handle F821 undefined name 'e' - remove "as e" from except clauses
    # But only if we're sure it's not used in the except block
    for i, line in enumerate(lines):
        original = line
        if 'except ' in line and ' as e:' in line:
            # Check if 'e' is used in the next few lines
            e_used = False
            for j in range(i+1, min(i+5, len(lines))):
                if re.search(r'\be\b', lines[j]) and 'except' not in lines[j]:
                    e_used = True
                    break
                # Stop if we hit a dedent or new statement at same indent level
                if lines[j].strip() and not lines[j].startswith('    ') and not lines[j].startswith('\t'):
                    break
            
            if not e_used:
                lines[i] = line.replace(' as e:', ':')
                changes.append(f"Line {i+1}: Removed unused exception variable 'e' (F821)")
    
    # Fix 5: E301 - expected 1 blank line (only for clear cases)
    # This is tricky - only fix obvious cases
    result = []
    for i, line in enumerate(lines):
        result.append(line)
        # If current line is not blank and next line is a method def
        if (i + 1 < len(lines) and 
            line.strip() != '' and 
            lines[i+1].strip().startswith('def ') and
            len(lines[i+1]) - len(lines[i+1].lstrip()) > 0 and  # indented
            not line.strip().startswith(('def ', 'class ', '@', 'return', 'pass'))):
            result.append('\n')
            changes.append(f"Line {i+1}: Added blank line before method definition (E301)")
    lines = result
    
    # Fix 6: Simple E302 fixes - ensure 2 blank lines before top-level function/class
    result = []
    for i, line in enumerate(lines):
        # If this is a top-level def or class (no indentation)
        if (line.strip().startswith(('def ', 'class ')) and 
            len(line) - len(line.lstrip()) == 0):
            # Count preceding blank lines
            blank_count = 0
            j = i - 1
            while j >= 0 and lines[j].strip() == '':
                blank_count += 1
                j -= 1
            
            # Check if there's code before (not just comments/docstrings at start)
            if j >= 0:  # There's something before
                # Need 2 blank lines before top-level def/class
                if blank_count < 2:
                    # Add needed blank lines
                    for _ in range(2 - blank_count):
                        result.append('\n')
                        changes.append(f"Line {i+1}: Added blank line before {line.split()[0]} (E302)")
        
        result.append(line)
    lines = result
    
    # Write back
    with open(file_path, 'w', encoding = 'utf-8') as f:
        f.writelines(lines)
    
    print(f"Fixed {file_path}")
    print(f"Applied {len(changes)} fixes:")
    for change in changes[:20]:  # Show first 20
        print(f"  {change}")
    if len(changes) > 20:
        print(f"  ... and {len(changes) - 20} more fixes")

if __name__ == '__main__':
    fix_agent_py()
