#!/usr/bin/env python3
import subprocess

result = subprocess.run(['python', '-m', 'flake8', 'scripts/agent', '--max-line-length=120'], capture_output=True, text=True)
issues = {}
for line in result.stdout.split('\n'):
    if 'F401' not in line:
        continue
    parts = line.split(':')
    if len(parts) >= 5:
        filepath = parts[0]
        lineno = int(parts[1])
        if filepath not in issues:
            issues[filepath] = []
        issues[filepath].append((lineno, ':'.join(parts[4:]).strip()))

# Show first file's issues
for filepath in list(issues.keys())[:1]:
    print(f'{filepath}:')
    for lineno, msg in issues[filepath][:5]:
        print(f'  Line {lineno}: {msg}')
        with open(filepath) as f:
            lines = f.readlines()
            if lineno <= len(lines):
                print(f'    Code: {lines[lineno-1].rstrip()}')
