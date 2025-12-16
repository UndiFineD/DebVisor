#!/usr/bin/env python3
"""Fix remaining safe issues in agent files"""

from pathlib import Path
import re

def fix_remaining_issues():
    """Fix W391, F541, and simple issues"""
    agent_dir = Path('scripts/agent')
    py_files = list(agent_dir.glob('*.py'))
    
    total_fixes = 0
    
    for py_file in py_files:
        with open(py_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        changes = 0
        
        # Fix W391 - blank line at end of file
        while lines and lines[-1].strip() == '':
            lines.pop()
            changes += 1
        
        if lines:
            # Ensure file ends with newline
            if lines[-1] and not lines[-1].endswith('\n'):
                lines[-1] = lines[-1] + '\n'
                changes += 1
        
        # Fix F541 - f-strings missing placeholders
        for i, line in enumerate(lines):
            original = line
            # Find f-strings without {} and convert to regular strings
            # Match f"..." or f'...' that don't have any {}
            line = re.sub(r'f(["\'])((?:(?!\1|{).)*)\1', r'\1\2\1', line)
            
            if line != original:
                changes += 1
                lines[i] = line
        
        # Write back if changes
        if changes > 0:
            with open(py_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            total_fixes += changes
            print(f"{py_file.name}: {changes} fixes")
    
    print(f"\nTotal fixes applied: {total_fixes}")

if __name__ == '__main__':
    fix_remaining_issues()
