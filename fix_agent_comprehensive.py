#!/usr/bin/env python3
"""Comprehensive flake8 fixes for agent.py"""

from pathlib import Path
import re

def fix_agent_py():
    """Fix all flake8 issues in agent.py"""
    file_path = Path("scripts/agent/agent.py")
    content = file_path.read_text()
    lines = content.split('\n')
    
    # Step 1: Fix E303 (too many blank lines - reduce to max 2)
    result = []
    consecutive_blanks = 0
    for line in lines:
        if line.strip() == '':
            consecutive_blanks += 1
            if consecutive_blanks <= 2:
                result.append(line)
        else:
            consecutive_blanks = 0
            result.append(line)
    lines = result
    
    # Step 2: Fix E301 (need 1 blank line before method)
    # Look at line 69 - should have blank line before "def"
    result = []
    for i, line in enumerate(lines):
        result.append(line)
        # If next line is a method definition and we're not at EOF
        if i + 1 < len(lines):
            next_line = lines[i + 1]
            # Check if next is a method definition (indented def)
            if (next_line.strip().startswith('def ') and 
                len(next_line) - len(next_line.lstrip()) > 0 and  # Has indentation
                line.strip() != '' and  # Current line is not blank
                not line.strip().startswith(('def ', 'class ', '@'))):  # Not a decorator/def/class
                # Need blank line
                result.append('')
    lines = result
    
    # Step 3: Fix F821 undefined name 'e' in except clauses
    # These are caused by "except X as e:" where e is referenced but e was removed
    # Pattern: ...except ... -> ref to {e} or .format(e=...) where e is undefined
    for i, line in enumerate(lines):
        # First remove "as e" from except clauses
        if 'except ' in line and ' as e' in line:
            lines[i] = line.replace(' as e:', ':').replace(' as e,', ',')
    
    # Step 4: Fix F841 - local variable assigned but never used
    # Lines to handle: 885 (signal_name), 1270 (status_symbol), 2973 (elapsed), 
    # 3227 (content_hash), 3231/3267 (rel_path), 3538/3673 (base)
    
    # For each problematic variable, comment out the assignment
    unused_assignments = [
        (r'^\s+signal_name\s*=', 'signal_name'),
        (r'^\s+status_symbol\s*=', 'status_symbol'),
        (r'^\s+elapsed\s*=', 'elapsed'),
        (r'^\s+content_hash\s*=', 'content_hash'),
        (r'^\s+rel_path\s*=', 'rel_path'),
        (r'^\s+base\s*=', 'base'),
    ]
    
    for i, line in enumerate(lines):
        for pattern, var_name in unused_assignments:
            if re.match(pattern, line):
                # Check if this is a pure assignment (not multi-statement)
                if '=' in line and not any(kw in line for kw in ['if ', 'for ', 'while ', 'and ', 'or ']):
                    indent = len(line) - len(line.lstrip())
                    # Comment it out
                    lines[i] = ' ' * indent + f'# {line.lstrip()}'
                break
    
    # Step 5: Fix E713 - test for membership should be 'not in'
    for i, line in enumerate(lines):
        # Pattern: "not variable in something" -> "variable not in something"
        lines[i] = re.sub(r'\bnot\s+(\w+)\s+in\b', r'\1 not in ', line)
    
    # Step 6: Fix E128/E129 - continuation line indentation
    # These need proper indentation alignment
    # Common pattern: opening paren on one line, args on next
    i = 0
    while i < len(lines):
        line = lines[i]
        # Count unclosed brackets/parens
        open_parens = line.count('(') - line.count(')')
        open_brackets = line.count('[') - line.count(']')
        open_braces = line.count('{') - line.count('}')
        total_open = open_parens + open_brackets + open_braces
        
        if total_open > 0:
            # This line has unclosed delimiters, check continuation
            base_indent = len(line) - len(line.lstrip())
            j = i + 1
            
            while j < len(lines) and total_open > 0:
                next_line = lines[j]
                
                if next_line.strip() == '':
                    j += 1
                    continue
                
                # Fix indentation of continuation line
                next_indent = len(next_line) - len(next_line.lstrip())
                required_indent = base_indent + 8  # Typical indent for continuation
                
                # If it's not properly indented, fix it
                if next_indent != required_indent and next_line.strip():
                    lines[j] = ' ' * required_indent + next_line.lstrip()
                
                # Update open count
                next_line = lines[j]
                open_parens -= next_line.count('(') - next_line.count(')')
                open_brackets -= next_line.count('[') - next_line.count(']')
                open_braces -= next_line.count('{') - next_line.count('}')
                total_open = open_parens + open_brackets + open_braces
                
                j += 1
        
        i += 1
    
    # Step 7: Remove trailing whitespace on all lines
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip()
    
    # Write result
    output = '\n'.join(lines)
    file_path.write_text(output)
    print(f"Fixed {file_path}")

if __name__ == '__main__':
    fix_agent_py()
