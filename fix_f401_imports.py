#!/usr/bin/env python3
"""Fix F401 unused imports across agent files."""

import re
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
]

# Map of specific unused imports to remove
unused_imports = {
    'scripts/agent/agent-changes.py': [
        ('typing.Callable', 33),
        ('pathlib.Path', 41),
    ],
    'scripts/agent/agent-coder.py': [
        ('typing.Set', 49),
    ],
    'scripts/agent/agent-context.py': [
        ('typing.Callable', 47),
        ('typing.Set', 47),
    ],
    'scripts/agent/agent-errors.py': [
        ('pathlib.Path', 49),
        ('typing.Callable', 50),
    ],
    'scripts/agent/agent-improvements.py': [
        ('typing.Set', 49),
    ],
    'scripts/agent/agent-stats.py': [
        ('typing.Set', 48),
        ('numpy as np', 52),
    ],
    'scripts/agent/agent-tests.py': [
        ('random', 42),
        ('re', 43),
    ],
    'scripts/agent/agent.py': [
        ('typing.Union', 42),
        ('multiprocessing', 48),
        ('concurrent.futures.ProcessPoolExecutor', 50),
    ],
}

total_fixed = 0

for file_path, imports_to_remove in unused_imports.items():
    if not os.path.exists(file_path):
        continue
        
    try:
        with open(file_path, 'r', encoding = 'utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding = 'latin-1') as f:
            lines = f.readlines()
    
    for import_name, line_num in imports_to_remove:
        # Find and remove the import
        for i, line in enumerate(lines):
            if import_name in line and 'import' in line:
                # Check if it's a single import on the line
                if line.strip().endswith(import_name):
                    lines[i] = ''
                    print(f"{file_path}:{i+1}: Removed unused import '{import_name}'")
                    total_fixed += 1
                elif ', ' in line and f'({import_name}' in line or f', {import_name}' in line:
                    # Remove from middle of import
                    new_line = re.sub(f',?\s*{re.escape(import_name)}(?=,|\))', '', line)
                    lines[i] = new_line
                    print(f"{file_path}:{i+1}: Removed unused import '{import_name}'")
                    total_fixed += 1
                break
    
    # Write back
    try:
        with open(file_path, 'w', encoding = 'utf-8') as f:
            f.writelines(lines)
    except Exception:
        with open(file_path, 'w', encoding = 'latin-1') as f:
            f.writelines(lines)

print(f"\nTotal F401 (unused imports) fixed: {total_fixed}")
