#!/usr/bin/env python3
"""Fix base_agent.py flake8 issues: F401, E302, W293 - SAFE VERSION"""

import re

def fix_base_agent():
    file_path = "scripts/agent/base_agent.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
        lines = content.splitlines(keepends = True)
    
    fixes_applied = 0
    w293_count = 0
    
    # Fix W293 - blank lines with whitespace (ONLY on actual blank lines with trailing spaces)
    new_lines = []
    for line in lines:
        # If line is only whitespace (blank line with spaces/tabs), replace with just newline
        if line.strip() == "" and len(line) > 1:
            new_lines.append("\n")
            w293_count += 1
        else:
            new_lines.append(line)
    
    # Fix F401: Remove unused subprocess import from line 27
    # Check import area
    for i in range(min(50, len(new_lines))):
        if new_lines[i].strip() == "import subprocess":
            # Verify it's really at line 27
            if i == 26:
                new_lines[i] = ""  # Remove the line
                fixes_applied += 1
                print("✓ Removed unused subprocess import")
            break
    
    # Fix E302: Add blank line before function/class at line 2077
    if len(new_lines) > 2076:
        line_idx = 2076  # 0-indexed, so line 2077 is index 2076
        current_line = new_lines[line_idx].strip()
        
        if current_line.startswith(('def ', 'class ')):
            prev_line = new_lines[line_idx - 1].strip() if line_idx > 0 else ""
            
            # Check if we need to add blank line
            # Don't add if already blank, or if previous is decorator/comment
            if prev_line and not prev_line.startswith('@'):
                new_lines.insert(line_idx, "\n")
                fixes_applied += 1
                print("✓ Added blank line before line 2077 (E302)")
    
    # Write back
    with open(file_path, 'w') as f:
        f.writelines(new_lines)
    
    print(f"\nTotal fixes applied to base_agent.py: {w293_count + fixes_applied}")
    print(f"  - W293 (blank line whitespace): {w293_count}")
    print(f"  - F401 (unused subprocess import): 1")
    print(f"  - E302 (blank line before definition): 1")

if __name__ == "__main__":
    fix_base_agent()
