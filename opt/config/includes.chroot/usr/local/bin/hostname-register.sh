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

# DebVisor hostname auto-registration for local dnsmasq,
# with optional cluster-aware behavior via etcd.
set -euo pipefail

DNSMASQ_HOSTS_DIR="/etc/dnsmasq.d/hosts"
DEFAULT_DOMAIN="debvisor.local"
ETCDCTL_BIN=${ETCDCTL_BIN:-/usr/bin/etcdctl}
ETCDCTL_ENDPOINTS=${ETCDCTL_ENDPOINTS:-}

HOSTNAME_SHORT=$(hostname -s)
HOSTNAME_FQDN=$(hostname -f || echo "${HOSTNAME_SHORT}.${DEFAULT_DOMAIN}")
IP=$(hostname -I | awk '{print $1}')   # first IP address

MODE="standalone"
FQDN="$HOSTNAME_FQDN"

# Try to determine node mode and cluster-assigned FQDN from etcd if available
if [[ -x "$ETCDCTL_BIN" && -n "${ETCDCTL_ENDPOINTS}" ]]; then
	if NODE_ID=$("$ETCDCTL_BIN" --endpoints="$ETCDCTL_ENDPOINTS" get /debvisor/self/node_id --print-value-only 2>/dev/null); then
		if [[ -n "$NODE_ID" ]]; then
			# Mode
			MODE=$("$ETCDCTL_BIN" --endpoints="$ETCDCTL_ENDPOINTS" get "/debvisor/nodes/${NODE_ID}/mode" --print-value-only 2>/dev/null || echo "standalone")
			# Cluster FQDN override, if present
			CLUSTER_FQDN=$("$ETCDCTL_BIN" --endpoints="$ETCDCTL_ENDPOINTS" get "/debvisor/nodes/${NODE_ID}/info/fqdn" --print-value-only 2>/dev/null || true)
			if [[ -n "$CLUSTER_FQDN" ]]; then
				FQDN="$CLUSTER_FQDN"
			fi
		fi
	fi
fi

DOMAIN=${FQDN#*.}
HOST=${FQDN%%.*}

mkdir -p "$DNSMASQ_HOSTS_DIR"
ENTRY="${IP} ${FQDN} ${HOST}"

# Write entry file for this host (local dnsmasq view)
echo "$ENTRY" > "${DNSMASQ_HOSTS_DIR}/${HOST}.conf"

# Reload dnsmasq to apply changes
systemctl reload dnsmasq || true
logger "DebVisor: Registered $FQDN (mode=$MODE) with IP $IP in dnsmasq"
