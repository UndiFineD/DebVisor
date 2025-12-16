#!/usr/bin/env python3
"""Fix W293 (blank line whitespace) across all agent files"""

from pathlib import Path

def fix_all_w293():
    agent_dir = Path("scripts/agent")
    total_fixes = 0
    
    for py_file in sorted(agent_dir.glob("*.py")):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(py_file, 'r', encoding='latin-1') as f:
                lines = f.readlines()
        
        w293_count = 0
        for i, line in enumerate(lines):
            if line.strip() == "" and len(line) > 1:  # Blank line with whitespace
                lines[i] = "\n"
                w293_count += 1
        
        if w293_count > 0:
            with open(py_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"{py_file.name}: {w293_count} W293 fixes")
            total_fixes += w293_count
    
    print(f"\nTotal W293 fixes across all agent files: {total_fixes}")

if __name__ == "__main__":
    fix_all_w293()
