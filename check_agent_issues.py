import subprocess
from collections import Counter

result = subprocess.run(['python', '-m', 'flake8', 'scripts/agent', '--max-line-length=120'], 
                       capture_output=True, text=True)
issues = Counter()
for line in result.stdout.split('\n'):
    if ':' in line and ': ' in line:
        parts = line.split(': ', 1)
        if len(parts) == 2:
            code = parts[1].split()[0]
            issues[code] += 1

print("Issue Summary for scripts/agent:")
print("-" * 40)
for code, count in sorted(issues.items(), key=lambda x: -x[1]):
    print(f"{code:6} : {count:4} issues")
print("-" * 40)
print(f"Total: {sum(issues.values())} issues")
