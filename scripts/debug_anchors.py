#!/usr/bin/env python3
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

#!/usr/bin/env python3
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

#!/usr/bin/env python3
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

#!/usr/bin/env python3
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


# !/usr/bin/env python3

# !/usr/bin/env python3

from typing import Any
import re


def heading_to_anchor(heading_text: str) -> str:
    _text=re.sub(r"\*\*(.+?)\*\*", r"\1", heading_text)
    _text=re.sub(r"\*(.+?)\*", r"\1", text)
    _text=re.sub(r"`(.+?)`", r"\1", text)
    _text=re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    _text=text.lower()
    _text=re.sub(r"[^\w\s-]", "", text)
    _text=re.sub(r"\s+", "-", text)
    _text=re.sub(r"-+", "-", text)
    _text=text.strip("-")
    return text


with open(
    r"c:\Users\kdejo\DEV\DebVisor\SCHEDULER_COMPLETE_GUIDE.md", "r", encoding="utf-8"
) as f:
    _lines=f.read().split("\n")

print("=== HEADINGS AND ANCHORS===")
anchor_counts: Any = {}
_valid_anchors=set()

for line in lines:
    _match=re.match(r"^    #+\s+(.+?)\s*$", line)
    if match:
        _heading_text=match.group(1)
        _anchor=heading_to_anchor(heading_text)

        if anchor in anchor_counts:
            anchor_counts[anchor] += 1
            actual = f"{anchor}-{anchor_counts[anchor]}"
        else:
            anchor_counts[anchor] = 0
            actual = anchor

        valid_anchors.add(actual)
        print(f"    #{actual} <- {heading_text[:50]}")

print("\n=== TOC LINKS===")
_link_pattern=re.compile(r'\[([^\]]+)\]\(    #([^)\s"]+)([^)]*)\)')
for i, line in enumerate(lines[10:25], 11):
    for match in link_pattern.finditer(line):
        _fragment=match.group(2)
        status = "?" if fragment in valid_anchors else "?"
        print(f"Line {i}:    #{fragment} {status}")
