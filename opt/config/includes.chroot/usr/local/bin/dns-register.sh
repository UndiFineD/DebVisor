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


# Node dynamic DNS registration using TSIG

set -euo pipefail

ZONE="debvisor.local"
DNS="10.10.0.1"
KEYFILE="/etc/debvisor/nsupdate-node.key"
TTL=300
HOSTNAME="$(hostname -s)"
IP="$(hostname -I | awk '{print $1}')"

if [[ -z "${IP}" ]]; then
	echo "dns-register: no IP address found, skipping" >&2
	exit 0
fi

if [[ ! -f "${KEYFILE}" ]]; then
	echo "dns-register: TSIG key file ${KEYFILE} not found, skipping" >&2
	exit 0
fi

cat <<EOF | nsupdate -k "${KEYFILE}"
server ${DNS}
zone ${ZONE}
update delete ${HOSTNAME}.${ZONE} A
update add ${HOSTNAME}.${ZONE} ${TTL} A ${IP}
send
EOF

logger "DebVisor: Registered ${HOSTNAME}.${ZONE} -> ${IP} via TSIG"
