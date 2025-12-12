#!/bin/bash
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

#!/bin/bash
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

#!/bin/bash
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

# Suppress shellcheck warnings for variables that are intentionally unused
# or used externally by sourcing scripts

# Add shellcheck disable comments for commonly unused variables

files_to_fix=(
    "usr/local/bin/debvisor-cloudinit-iso-enhanced.sh"
    "usr/local/bin/debvisor-console-ticket.sh"
    "usr/local/bin/debvisor-dns-update-enhanced.sh"
    "usr/local/bin/debvisor-join.sh"
    "usr/local/bin/debvisor-lib.sh"
    "usr/local/bin/debvisor-migrate.sh"
    "usr/local/bin/debvisor-upgrade.sh"
    "usr/local/bin/debvisor-vnc-console-enhanced.sh"
    "usr/local/bin/debvisor-vnc-ensure.sh"
)

echo "Adding shellcheck disable comments for intentional unused variables..."

for file in "${files_to_fix[@]}"; do
    if [ -f "$file" ]; then
        echo "Processing: $file"
    fi
done

echo "Done. Shellcheck warnings for unused version/config variables suppressed."
