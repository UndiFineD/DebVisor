#!/bin/bash
# DebVisor: ensure websockify console for a VM and print full URL

set -euo pipefail

VM=${1:-}
if [ -z "$VM" ]; then
  echo "Usage: $0 <vm-name>" >&2
  exit 1
fi

systemctl enable --now "debvisor-websockify@${VM}.service"

HOSTNAME=$(hostname -f 2>/dev/null || hostname)
PATH="/novnc/vnc.html?path=/vnc/${VM}"

echo "http://${HOSTNAME}${PATH}"
