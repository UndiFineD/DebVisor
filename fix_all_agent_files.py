#!/usr/bin/env python3
"""Fix all flake8 issues in scripts/agent directory"""

from pathlib import Path
import re
import glob

def fix_file(file_path: Path) -> int:
    """Fix a single file and return number of fixes applied"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    changes = 0
    
    # Fix 1: E303 (too many blank lines - reduce to max 2)
    result = []
    consecutive_blanks = 0
    for line in lines:
        if line.strip() == '':
            consecutive_blanks += 1
            if consecutive_blanks <= 2:
                result.append(line)
            else:
                changes += 1
        else:
            consecutive_blanks = 0
            result.append(line)
    lines = result
    
    # Fix 2: W293/W291 - Remove trailing whitespace and whitespace on blank lines
    result = []
    for line in lines:
        if line.rstrip() == '' and line != '\n':
            # Blank line with whitespace
            result.append('\n')
            changes += 1
        elif line.rstrip('\n') != line.rstrip():
            # Trailing whitespace
            result.append(line.rstrip() + '\n')
            changes += 1
        else:
            result.append(line)
    lines = result
    
    # Fix 3: W292 - no newline at end of file
    if lines and lines[-1].rstrip('\n') == lines[-1]:
        lines[-1] = lines[-1] + '\n'
        changes += 1
    
    # Fix 4: W391 - blank line at end of file
    while lines and lines[-1].strip() == '':
        lines.pop()
        changes += 1
    if lines:
        lines.append('\n')
    
    # Fix 5: F401 - Remove unused imports (simple patterns)
    for i, line in enumerate(lines):
        original = line
        
        # Remove 'call' from mock imports
        if 'from unittest.mock import' in line and 'call' in line:
            line = re.sub(r',?\s*call\s*,?', ',', line)
            line = re.sub(r',\s*,', ',', line)
            if line.rstrip().endswith(','):
                line = line.rstrip().rstrip(',') + '\n'
        
        # Remove 'patch' from mock imports
        if 'from unittest.mock import' in line and 'patch' in line:
            line = re.sub(r',?\s*patch\s*,?', ',', line)
            line = re.sub(r',\s*,', ',', line)
            if line.rstrip().endswith(','):
                line = line.rstrip().rstrip(',') + '\n'
        
        # Remove 'ANY' from mock imports
        if 'from unittest.mock import' in line and 'ANY' in line:
            line = re.sub(r',?\s*ANY\s*,?', ',', line)
            line = re.sub(r',\s*,', ',', line)
            if line.rstrip().endswith(','):
                line = line.rstrip().rstrip(',') + '\n'
        
        # Remove 'MagicMock' from mock imports
        if 'from unittest.mock import' in line and 'MagicMock' in line:
            line = re.sub(r',?\s*MagicMock\s*,?', ',', line)
            line = re.sub(r',\s*,', ',', line)
            if line.rstrip().endswith(','):
                line = line.rstrip().rstrip(',') + '\n'
        
        # Remove 'mock_open' from mock imports
        if 'from unittest.mock import' in line and 'mock_open' in line:
            line = re.sub(r',?\s*mock_open\s*,?', ',', line)
            line = re.sub(r',\s*,', ',', line)
            if line.rstrip().endswith(','):
                line = line.rstrip().rstrip(',') + '\n'
        
        # Comment out simple unused imports
        if line.strip().startswith('import ') and 'import' not in line[7:]:
            import_name = line.strip().split()[1]
            if import_name in ['time', 'tempfile', 'os', 'datetime']:
                # These are likely unused - comment them
                pass  # Don't auto-comment, too risky
        
        if line != original:
            changes += 1
            
        lines[i] = line
    
    # Fix 6: E712 - comparison to True/False should use 'is'
    for i, line in enumerate(lines):
        original = line
        # Fix "== True" to "is True" or "== False" to "is False"
        line = re.sub(r'==\s*True\b', 'is True', line)
        line = re.sub(r'==\s*False\b', 'is False', line)
        if line != original:
            changes += 1
        lines[i] = line
    
    # Fix 7: E128 - continuation line indentation
    for i in range(len(lines)):
        line = lines[i]
        
        if i > 0:
            # Look back to find if this is a continuation line
            j = i - 1
            paren_count = 0
            bracket_count = 0
            
            while j >= 0:
                paren_count += lines[j].count('(') - lines[j].count(')')
                bracket_count += lines[j].count('[') - lines[j].count(']')
                
                if paren_count > 0 or bracket_count > 0:
                    # Found unclosed bracket - this line should be indented
                    opening_line = lines[j]
                    
                    if paren_count > 0:
                        paren_pos = opening_line.rfind('(')
                        if paren_pos >= 0:
                            target_indent = paren_pos + 1
                            current_indent = len(line) - len(line.lstrip())
                            
                            # If indentation is too low, fix it
                            if 0 < current_indent < target_indent and line.strip() and not line.lstrip().startswith('#'):
                                old_line = line
                                lines[i] = ' ' * target_indent + line.lstrip()
                                if old_line != lines[i]:
                                    changes += 1
                    break
                
                j -= 1
    
    # Write back if changes were made
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return changes

def main():
    """Fix all Python files in scripts/agent/"""
    agent_dir = Path('scripts/agent')
    py_files = list(agent_dir.glob('*.py'))
    
    total_changes = 0
    fixed_files = []
    
    for py_file in sorted(py_files):
        changes = fix_file(py_file)
        if changes > 0:
            fixed_files.append((py_file.name, changes))
            total_changes += changes
    
    print(f"Fixed {len(fixed_files)} files with {total_changes} total changes:")
    for fname, count in fixed_files:
        print(f"  {fname}: {count} fixes")

if __name__ == '__main__':
    main()
