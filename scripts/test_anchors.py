#!/usr/bin/env python3
import re

def heading_to_anchor(heading_text):
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', heading_text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text

with open(r'c:\Users\kdejo\DEV\DebVisor\MULTIREGION_COMPLETE_GUIDE.md', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

print('=== H2 HEADINGS WITH ANCHORS ===')
for i, line in enumerate(lines, 1):
    match = re.match(r'^## (.+?)\s*$', line)
    if match:
        heading = match.group(1)
        anchor = heading_to_anchor(heading)
        print(f'{anchor} <- "{heading}"')

print('\n=== TOC LINKS ===')
for i, line in enumerate(lines[4:20], 5):
    match = re.search(r'\(#([^)]+)\)', line)
    if match:
        print(f'Line {i}: #{match.group(1)}')
