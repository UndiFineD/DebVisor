#!/usr/bin/env python3
"""Fix base_agent.py W293 issues - blank lines with whitespace"""

def fix_w293_only():
    file_path = "scripts/agent/base_agent.py"
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    w293_count = 0
    
    # Fix W293 - blank lines with whitespace
    for i, line in enumerate(lines):
        if line.strip() == "" and len(line) > 1:  # Blank line with whitespace
            lines[i] = "\n"
            w293_count += 1
    
    # Write back
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print(f"Fixed W293 issues in base_agent.py: {w293_count} blank lines cleaned")

if __name__ == "__main__":
    fix_w293_only()
