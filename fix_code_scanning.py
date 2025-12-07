
import json
import os

def fix_file(file_path, alerts):
    print(f"Fixing {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    # Sort alerts by line number descending to avoid shifting issues
    alerts.sort(key=lambda x: x['line'], reverse=True)

    for alert in alerts:
        line_num = alert['line']
        rule = alert['rule']
        idx = line_num - 1

        if idx >= len(lines):
            continue

        if rule == 'W293':
            # Blank line contains whitespace
            if lines[idx].strip() == '':
                lines[idx] = '\n'
        
        elif rule in ['E302', 'E305']:
            # Expected 2 blank lines
            # Count existing blank lines before idx
            blanks = 0
            p = idx - 1
            while p >= 0 and lines[p].strip() == '':
                blanks += 1
                p -= 1
            
            needed = 2 - blanks
            if needed > 0:
                for _ in range(needed):
                    lines.insert(idx, '\n')
        
        elif rule == 'E306':
            # Expected 1 blank line
            blanks = 0
            p = idx - 1
            while p >= 0 and lines[p].strip() == '':
                blanks += 1
                p -= 1
            
            needed = 1 - blanks
            if needed > 0:
                for _ in range(needed):
                    lines.insert(idx, '\n')

        elif rule in ['E111', 'E117']:
            # Indentation issues
            # Specific fix for scripts/fix_markdown_lint_comprehensive.py line 53
            if 'fix_markdown_lint_comprehensive.py' in file_path and line_num == 53:
                # It has 21 spaces, needs 20
                if lines[idx].startswith('                     '):
                    lines[idx] = lines[idx].replace('                     ', '                    ', 1)
        
        elif rule == 'E501':
            # Line too long
            # Specific fix for scripts/fix_markdown_lint_comprehensive.py line 151
            if 'fix_markdown_lint_comprehensive.py' in file_path and line_num == 151:
                content = lines[idx]
                if 'if any(part.startswith' in content:
                    # Split the line
                    indent = content[:content.find('if')]
                    parts = content.split(' or ')
                    # Reconstruct with line breaks
                    # This is a bit hacky, let's just replace the specific known long line
                    new_lines = [
                        f"{indent}if any(part.startswith('.') or part in ['node_modules', 'venv', '__pycache__']\n",
                        f"{indent}       for part in filepath.parts):\n"
                    ]
                    lines[idx] = new_lines[0]
                    lines.insert(idx + 1, new_lines[1])

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def main():
    with open('alerts_details.json', 'r') as f:
        alerts = json.load(f)

    # Group by file
    files = {}
    for alert in alerts:
        path = alert['path']
        if path not in files:
            files[path] = []
        files[path].append(alert)

    for path, file_alerts in files.items():
        fix_file(path, file_alerts)

if __name__ == '__main__':
    main()
