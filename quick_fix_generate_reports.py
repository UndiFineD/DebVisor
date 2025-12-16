#!/usr/bin/env python3
"""Fix E261 and W293 issues in generate_agent_reports.py"""
import re

filepath = r"c:\Users\kdejo\DEV\DebVisor\scripts\agent\generate_agent_reports.py"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

e261_count = 0
w293_count = 0
new_lines = []

for line in lines:
    # W293: blank lines with whitespace
    if line.strip() == '':
        if line != '\n':
            new_lines.append('\n')
            w293_count += 1
        else:
            new_lines.append(line)
    else:
        # E261: comment spacing
        if '#' in line and not line.lstrip().startswith('#'):
            match = re.search(r'(\S)\s*#', line)
            if match:
                pos = match.end() - 1
                before = line[:pos]
                after = line[pos:]
                spaces = len(before) - len(before.rstrip())
                if spaces < 2:
                    before = before.rstrip() + '  '
                    line = before + after
                    e261_count += 1
        new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"E261 fixed: {e261_count}")
print(f"W293 fixed: {w293_count}")
print(f"Total: {e261_count + w293_count}")
