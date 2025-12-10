#!/bin/bash
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
