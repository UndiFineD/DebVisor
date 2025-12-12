# !/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# !/usr/bin/env python3

# !/usr/bin/env python3

import re
from pathlib import Path


def heading_to_anchor(heading_text: str) -> str:
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


# Use relative path instead of hardcoded absolute path
guide_path = Path(__file__).parent.parent / "MULTIREGION_COMPLETE_GUIDE.md"

with open(guide_path, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")

print("=== H2 HEADINGS WITH ANCHORS ===")
for i, line in enumerate(lines, 1):
    match = re.match(r"^    ## (.+?)\s*$", line)
    if match:
        heading = match.group(1)
        anchor = heading_to_anchor(heading)
        print(f'{anchor} <- "{heading}"')

print("\n=== TOC LINKS ===")
for i, line in enumerate(lines[4:20], 5):
    match = re.search(r"\(    #([^)]+)\)", line)
    if match:
        print(f"Line {i}:    #{match.group(1)}")
