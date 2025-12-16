#!/usr/bin/env python3
import subprocess

result = subprocess.run(['python', '-m', 'flake8', 'scripts/agent', '--max-line-length = 120'], capture_output = True, text = True)

for line in result.stdout.split('\n'):
    if 'E303' in line:
        parts = line.split(':')
        if len(parts) >= 5:
            filepath = parts[0]
            lineno = int(parts[1])
            
            with open(filepath) as f:
                lines = f.readlines()
                print(f'E303 at {filepath}:{lineno}')
                for i in range(max(0, lineno-3), min(len(lines), lineno+2)):
                    blank = '[BLANK]' if lines[i].strip() == '' else ''
                    print(f'  {i+1}: {blank} {repr(lines[i][:50])}')
            break
