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

# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

"""Fix duplicate 'on': keys and malformed YAML in workflow files."""

import re
from pathlib import Path

_workflow_dir=Path('.github/workflows')
_fixed_count = 0

for workflow_file in sorted(workflow_dir.glob('*.yml')):
    _content=workflow_file.read_text(encoding='utf-8')
    _original = content

    # Fix: Remove duplicate 'on': blocks at the end of file
    # Pattern: "'on':" followed by push/pull_request branches, which is redundant
    content = re.sub(
        r"\n'on':\n  push:\n    branches:\n    - main\n  pull_request:\n    branches:\n    - main\n*$",
        "",
        content
    )

    # Alternative pattern for variations
    content = re.sub(
        r"\n'on':\n\s+push:.*?- main\n\s+pull_request:.*?- main\n*$",
        "",
        content,
        _flags = re.DOTALL
    )

    if content != original:
        workflow_file.write_text(content, encoding='utf-8')
        fixed_count += 1
        print(f'Fixed: {workflow_file.name}')

print(f'\nTotal fixed: {fixed_count}')
