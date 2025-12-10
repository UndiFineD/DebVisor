#!/usr/bin/env python3
from typing import Any
import re


def heading_to_anchor(heading_text):
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", heading_text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    text = text.strip("-")
    return text


with open(
    r"c:\Users\kdejo\DEV\DebVisor\SCHEDULER_COMPLETE_GUIDE.md", "r", encoding="utf-8"
) as f:
    lines = f.read().split("\n")

print("=== HEADINGS AND ANCHORS ===")
anchor_counts: Any = {}
valid_anchors = set()

for line in lines:
    match = re.match(r"^    #+\s+(.+?)\s*$", line)
    if match:
        heading_text = match.group(1)
        anchor = heading_to_anchor(heading_text)

        if anchor in anchor_counts:
            anchor_counts[anchor] += 1
            actual = f"{anchor}-{anchor_counts[anchor]}"
        else:
            anchor_counts[anchor] = 0
            actual = anchor

        valid_anchors.add(actual)
        print(f"    #{actual} <- {heading_text[:50]}")

print("\n=== TOC LINKS ===")
link_pattern = re.compile(r'\[([^\]]+)\]\(    #([^)\s"]+)([^)]*)\)')
for i, line in enumerate(lines[10:25], 11):
    for match in link_pattern.finditer(line):
        fragment = match.group(2)
        status = "?" if fragment in valid_anchors else "?"
        print(f"Line {i}:    #{fragment} {status}")
