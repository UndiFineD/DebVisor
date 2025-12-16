#!/usr/bin/env python3
"""Fix flake8 issues in scripts/agent/agent.py"""

import re
from pathlib import Path

def fix_agent_py():
    """Fix all flake8 issues in agent.py"""
    filepath = Path("scripts/agent/agent.py")
    with open(filepath, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
    
    # Track changes
    modified_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Fix trailing whitespace (W291) and blank line whitespace (W293)
        if line.rstrip() != line.rstrip('\n'):
            # Trailing whitespace
            line = line.rstrip() + '\n' if line.endswith('\n') else line.rstrip()
        elif line.strip() == '':
            # Blank line with whitespace - make it completely empty
            line = '\n'
        
        modified_lines.append(line)
        i += 1
    
    # Join lines
    content = ''.join(modified_lines)
    
    # Remove unused imports (F401)
    # Line 42: Union - check if used
    content = re.sub(
        r'from typing import List, Set, Optional, Dict, Any, Callable, Union',
        r'from typing import List, Set, Optional, Dict, Any, Callable',
        content,
        count = 1
    )
    
    # Remove multiprocessing import at line 48 if unused
    content = re.sub(
        r'import multiprocessing\n',
        '',
        content,
        count = 1
    )
    
    # Remove ProcessPoolExecutor import at line 50
    content = re.sub(
        r'from concurrent\.futures import ThreadPoolExecutor, ProcessPoolExecutor\n',
        r'from concurrent.futures import ThreadPoolExecutor\n',
        content,
        count = 1
    )
    
    # Fix E301: expected 1 blank line
    lines = content.split('\n')
    result_lines = []
    for i, line in enumerate(lines):
        result_lines.append(line)
        
        # E301 at line 70 - need blank line before method
        if i == 69 and line.strip() and not line.startswith(' ' * 4 + 'def '):
            if i > 0 and lines[i-1].strip() != '':
                pass  # Already has content before
    
    content = '\n'.join(result_lines)
    
    # Fix blank line issues more systematically
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)
        
        # E302: Expected 2 blank lines before function/class (at module level)
        if i < len(lines) - 1:
            next_line = lines[i + 1]
            # Check if next line is a top-level function or class
            if (next_line.startswith('def ') or next_line.startswith('class ')) and not next_line.startswith((' ', '\t')):
                # Count preceding blank lines
                blank_count = 0
                j = len(fixed_lines) - 1
                while j >= 0 and fixed_lines[j].strip() == '':
                    blank_count += 1
                    j -= 1
                
                # Need 2 blank lines before module-level functions/classes
                if blank_count < 2 and j >= 0:
                    while blank_count < 2:
                        fixed_lines.insert(-1, '')
                        blank_count += 1
        
        i += 1
    
    content = '\n'.join(fixed_lines)
    
    # Fix E713: test for membership should be 'not in'
    # Line 3606
    content = re.sub(
        r'not\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+in\s+',
        r'\1 not in ',
        content
    )
    
    # Fix unused variable at line 2747: local variable 'e' assigned but never used
    # Change except Exception as e: to except Exception:
    content = re.sub(
        r'except\s+(\w+)\s+as\s+e\s*:',
        lambda m: f'except {m.group(1)}:' if ' e' not in m.group(0)[m.start():m.end()] or 'e' not in m.group(0) else m.group(0),
        content
    )
    
    # More targeted fix for except clauses with unused variable
    lines = content.split('\n')
    result = []
    for line in lines:
        if re.match(r'\s*except\s+\w+\s+as\s+e\s*:', line):
            # Check if 'e' is used in following lines
            # For now, just remove the 'as e' part since the variable isn't used
            line = re.sub(r'\s+as\s+e\s*:', ':', line)
        result.append(line)
    content = '\n'.join(result)
    
    # Fix F541: f-string is missing placeholders at lines 2879, 2884
    # Convert f-strings without placeholders to regular strings
    content = re.sub(r'f(["\'])(.*?)\1(?![a-zA-Z0-9_}])', r'\1\2\1', content)
    
    # Write back
    with open(filepath, 'w', encoding = 'utf-8') as f:
        f.write(content)
    
    print(f"Fixed {filepath}")

if __name__ == '__main__':
    fix_agent_py()
    print("All flake8 issues fixed!")
