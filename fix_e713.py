#!/usr/bin/env python3
"""Smart multi-fix: E128 indentation, E741 names, E713 comparison"""
import os
import re

agent_dir = r'c:\Users\kdejo\DEV\DebVisor\scripts\agent'

stats = {'e741': 0, 'e713': 0, 'renamed': 0}

for filename in os.listdir(agent_dir):
    if not filename.endswith('.py'):
        continue
    
    filepath = os.path.join(agent_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # E713: not x in y -> x not in y
    content = re.sub(r'\bnot\s+(\w+)\s+in\s+', r'\1 not in ', content)
    if content != original:
        stats['e713'] += content.count(' not in ') - original.count(' not in ')
    
    # E713: not x is y -> x is not y  
    original = content
    content = re.sub(r'\bnot\s+(\w+)\s+is\s+', r'\1 is not ', content)
    if content != original:
        stats['e713'] += 1
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print(f"E713 (comparison) fixed: {stats['e713']}")
print(f"Total: {sum(stats.values())}")
