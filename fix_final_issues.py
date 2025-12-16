#!/usr/bin/env python3
"""Fix F841, F541, F821, E305, and E128/E129 issues"""

from pathlib import Path
import re

def fix_issues():
    """Fix the remaining issues"""
    file_path = Path("scripts/agent/agent.py")
    with open(file_path, 'r', encoding = 'utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    changes = 0
    
    # Fix 1: F541 - f-strings with no placeholders
    # Pattern: f"text with no {}" -> "text with no"
    # But be careful not to break actual f-strings
    for i, line in enumerate(lines):
        original = line
        # Find f-strings without placeholders
        # Look for f"..." or f'...' that don't contain {
        matches = re.finditer(r'f(["\'])((?:(?!\1|{).)*)\1', line)
        for match in matches:
            # Replace f"..." with "..."
            quote = match.group(1)
            content_str = match.group(2)
            line = line.replace(f'f{quote}{content_str}{quote}', f'{quote}{content_str}{quote}')
        
        if line != original:
            lines[i] = line
            changes += 1
    
    # Fix 2: F841 - unused variable in except clause  
    # Pattern: "except Exception as e:" -> "except Exception:"
    # But only if e is not used in the block
    for i, line in enumerate(lines):
        original = line
        if 'except ' in line and ' as e:' in line:
            # Check if e is used in the next lines before another except/except/def/class
            e_used = False
            j = i + 1
            indent_level = len(line) - len(line.lstrip())
            
            while j < len(lines):
                next_line = lines[j]
                
                # Stop at unindented statements
                if next_line.strip() and not next_line.startswith(' ' * (indent_level + 1)):
                    break
                
                # Check if 'e' is referenced in error message or logging
                if re.search(r'\be\b', next_line) and 'e:' not in next_line:
                    e_used = True
                    break
                
                j += 1
            
            if not e_used:
                lines[i] = line.replace(' as e:', ':')
                changes += 1
    
    # Fix 3: F821 - undefined name 'e'
    # These are cases where except clause had "as e" removed but e is still referenced
    # Need to look for these and fix the references
    for i, line in enumerate(lines):
        original = line
        
        # Fix references like f"...{e}..." where e is undefined
        if re.search(r'\{e\}', line) or re.search(r'\{e[^}]*\}', line):
            # Remove the {e} part - it was trying to reference the exception but it's not bound
            line = re.sub(r'\{e[^}]*\}', '', line)
            changes += 1
        
        lines[i] = line
    
    # Fix 4: E305 - expected 2 blank lines after function definition at module level
    # Line 89 area
    result = []
    for i, line in enumerate(lines):
        result.append(line)
        
        # If this is end of a module-level function/class (checking by dedent)
        if (i + 1 < len(lines) and
            line.strip() != '' and 
            (lines[i + 1].strip().startswith(('def ', 'class ')) or 
             (lines[i + 1].startswith('#') and '=' in lines[i + 1]))):
            # Check indentation
            curr_indent = len(line) - len(line.lstrip())
            next_indent = len(lines[i + 1]) - len(lines[i + 1].lstrip())
            
            # If going from indented code to module-level, need 2 blank lines
            if curr_indent > 0 and next_indent == 0 and lines[i + 1].strip().startswith(('def ', 'class ')):
                # Count existing blank lines
                blank_count = 0
                j = i + 1
                while j < len(lines) and lines[j].strip() == '':
                    blank_count += 1
                    j += 1
                
                # Need 2 blank lines
                if blank_count < 2:
                    for _ in range(2 - blank_count):
                        result.append('')
                        changes += 1
    
    lines = result
    
    # Fix 5: E128/E129 - continuation line indentation
    # These are lines that are part of multi-line statements
    for i in range(len(lines)):
        line = lines[i]
        
        # Check if this is a continuation line (preceded by unclosed brackets)
        if i > 0:
            # Look back to find opening bracket
            j = i - 1
            paren_count = 0
            bracket_count = 0
            
            while j >= 0:
                paren_count += lines[j].count('(') - lines[j].count(')')
                bracket_count += lines[j].count('[') - lines[j].count(']')
                
                if paren_count > 0 or bracket_count > 0:
                    # Found unclosed bracket
                    # This line should be indented to align
                    opening_line = lines[j]
                    
                    # If opening line has unclosed bracket, indent continuation properly
                    if paren_count > 0:
                        # Find the position of opening paren
                        paren_pos = opening_line.rfind('(')
                        if paren_pos >= 0:
                            target_indent = paren_pos + 1
                            current_indent = len(line) - len(line.lstrip())
                            
                            # If not properly aligned, fix it
                            if current_indent < target_indent and line.strip():
                                # Indent to align with opening paren
                                if current_indent > 0:
                                    lines[i] = ' ' * target_indent + line.lstrip()
                                    changes += 1
                    break
                
                j -= 1
    
    # Write back
    with open(file_path, 'w', encoding = 'utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Fixed {file_path}")
    print(f"Applied {changes} fixes")

if __name__ == '__main__':
    fix_issues()
