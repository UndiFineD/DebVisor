#!/usr/bin/env python3
"""Fix easy flake8 issues: E712 (boolean comparisons) and E741 (ambiguous names)"""

import re
from pathlib import Path

def process_files():
    """Process all Python files in scripts/agent/"""
    
    agent_dir = Path('scripts/agent')
    total_fixes = 0
    
    for py_file in sorted(agent_dir.glob('*.py')):
        if not py_file.is_file():
            continue
        
        try:
            content = py_file.read_text(encoding='utf-8')
        except Exception:
            continue
        
        original = content
        fixes = 0
        
        # Fix E712 - Boolean comparisons
        # Replace == True/False/None with is True/False/None
        initial_count = len(re.findall(r'==\s*True\b', content))
        content = re.sub(r'==\s*True\b', 'is True', content)
        fixes += initial_count
        
        initial_count = len(re.findall(r'==\s*False\b', content))
        content = re.sub(r'==\s*False\b', 'is False', content)
        fixes += initial_count
        
        initial_count = len(re.findall(r'==\s*None\b', content))
        content = re.sub(r'==\s*None\b', 'is None', content)
        fixes += initial_count
        
        initial_count = len(re.findall(r'!=\s*True\b', content))
        content = re.sub(r'!=\s*True\b', 'is not True', content)
        fixes += initial_count
        
        initial_count = len(re.findall(r'!=\s*False\b', content))
        content = re.sub(r'!=\s*False\b', 'is not False', content)
        fixes += initial_count
        
        initial_count = len(re.findall(r'!=\s*None\b', content))
        content = re.sub(r'!=\s*None\b', 'is not None', content)
        fixes += initial_count
        
        # Fix E741 - Ambiguous variable name 'l'
        lines = content.split('\n')
        e741_fixes = 0
        
        for i, line in enumerate(lines):
            # Only fix if 'l' appears as standalone variable
            # Match patterns like: l = , for l in, (l,  etc.
            if re.search(r'\bl\s*=', line) or re.search(r'\bfor\s+l\s+in\b', line):
                # Avoid replacing inside strings (simple heuristic)
                # Only proceed if the line doesn't have many quotes
                quote_count = line.count('"') + line.count("'")
                if quote_count <= 2:  # Allow 1 pair of quotes
                    # Replace 'l' variable assignments and usages
                    new_line = re.sub(r'\bl\s*=', 'lst =', line)
                    new_line = re.sub(r'\bfor\s+l\s+in\b', 'for lst in', new_line)
                    
                    if new_line != line:
                        lines[i] = new_line
                        e741_fixes += 1
        
        # Join back if E741 fixes were made
        if e741_fixes > 0:
            content = '\n'.join(lines)
            fixes += e741_fixes
        
        if content != original:
            try:
                py_file.write_text(content, encoding='utf-8')
                print(f"{py_file.name}: {fixes} fixes")
                total_fixes += fixes
            except Exception as e:
                print(f"Error writing {py_file.name}: {e}")
    
    print(f"\nTotal fixes applied: {total_fixes}")

if __name__ == '__main__':
    process_files()
