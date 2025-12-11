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

# DebVisor: ensure websockify console for a VM and print full URL

set -euo pipefail

VM=${1:-}
if [ -z "$VM" ]; then
  echo "Usage: $0 <vm-name>" >&2
  exit 1
fi

systemctl enable --now "debvisor-websockify@${VM}.service"

HOSTNAME=$(hostname -f 2>/dev/null || hostname)
VNC_PATH="/novnc/vnc.html?path=/vnc/${VM}"

echo "http://${HOSTNAME}${VNC_PATH}"
