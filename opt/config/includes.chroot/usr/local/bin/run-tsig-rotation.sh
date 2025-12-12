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

# DebVisor TSIG rotation helper
#
# This script is invoked by tsig-rotate.service. It is intentionally
# conservative and delegates the actual rotation logic to Ansible if
# a rotation playbook is present. If not, it logs a message and
# exits without error so the timer does not break the system.

set -euo pipefail

PLAYBOOK=/etc/ansible/rotate-tsig-ha.yml
INVENTORY=/etc/ansible/inventory

if [ -x /usr/bin/ansible-playbook ] && [ -f "$PLAYBOOK" ] && [ -f "$INVENTORY" ]; then
	ansible-playbook -i "$INVENTORY" "$PLAYBOOK" --limit dns_primaries,dns_secondaries
else
	logger "DebVisor TSIG rotate: playbook or inventory missing; skipping rotation run"
fi
