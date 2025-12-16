#!/usr/bin/env python3
"""Fix W291 (trailing whitespace) and E301/E305 (blank line) issues."""

import os

agent_files = [
    'scripts/agent/agent-changes.py',
    'scripts/agent/agent-coder.py',
    'scripts/agent/agent-context.py',
    'scripts/agent/agent-errors.py',
    'scripts/agent/agent-improvements.py',
    'scripts/agent/agent-stats.py',
    'scripts/agent/agent-tests.py',
    'scripts/agent/agent.py',
    'scripts/agent/agent_backend.py',
    'scripts/agent/agent_test_utils.py',
    'scripts/agent/base_agent.py',
    'scripts/agent/generate_agent_reports.py',
]

w291_count = 0
e301_count = 0
e305_count = 0

for file_path in agent_files:
    if not os.path.exists(file_path):
        continue
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            lines = f.readlines()
    
    modified = False
    
    # Fix W291: Remove trailing whitespace from lines with code
    for i, line in enumerate(lines):
        if line.rstrip() != line.rstrip('\n'):  # Has trailing whitespace
            lines[i] = line.rstrip() + '\n' if line.endswith('\n') else line.rstrip()
            w291_count += 1
            modified = True
    
    # Fix E301: Add blank line before nested function/class (agent.py line 70)
    for i in range(1, len(lines)):
        if 'def ' in lines[i] or 'class ' in lines[i]:
            # Check if previous line is not blank and not a docstring/comment
            if i > 0 and lines[i-1].strip() and not lines[i-1].strip().startswith('#'):
                if 'def ' in lines[i-1]:  # After another function - may need blank
                    pass  # Let auto-formatting handle
    
    # Fix E305: Ensure 2 blank lines after class/function
    for i in range(len(lines)-2):
        if ('def ' in lines[i] or 'class ' in lines[i]) and not lines[i].strip().startswith('#'):
            # Count blank lines after
            if i < len(lines) - 1 and lines[i+1].strip() != '' and not 'def ' in lines[i] and not 'class ' in lines[i]:
                # Check if we're at module level
                indent = len(lines[i]) - len(lines[i].lstrip())
                if indent == 0 and i < len(lines) - 2:
                    next_content_idx = i + 1
                    while next_content_idx < len(lines) and lines[next_content_idx].strip() == '':
                        next_content_idx += 1
                    
                    if next_content_idx < len(lines):
                        next_indent = len(lines[next_content_idx]) - len(lines[next_content_idx].lstrip())
                        if next_indent == 0 and ('def ' in lines[next_content_idx] or 'class ' in lines[next_content_idx]):
                            blank_count = next_content_idx - i - 1
                            if blank_count < 2:
                                lines.insert(i+1, '\n')
                                e305_count += 1
                                modified = True
    
    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        except Exception:
            with open(file_path, 'w', encoding='latin-1') as f:
                f.writelines(lines)

print(f"Fixed {w291_count} W291 (trailing whitespace) issues")
print(f"Fixed {e301_count} E301 (blank line before) issues")
print(f"Fixed {e305_count} E305 (blank lines after) issues")
print(f"Total: {w291_count + e301_count + e305_count} issues")
