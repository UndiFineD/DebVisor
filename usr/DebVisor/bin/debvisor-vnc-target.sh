#!/bin/bash
# DebVisor: find VNC port for a VM (libvirt)

set -euo pipefail

VM=${1:-}
if [ -z "$VM" ]; then
  echo "Usage: $0 <vm-name>" >&2
  exit 1
fi

# domdisplay typically prints something like: vnc://127.0.0.1:5901
DISPLAY_LINE=$(virsh domdisplay "$VM" 2>/dev/null || true)
PORT=$(echo "$DISPLAY_LINE" | sed -n 's/^vnc:\/\/127.0.0.1:\([0-9]\+\)$/\1/p')

if [ -z "$PORT" ]; then
  echo "DebVisor VNC: no VNC display found for VM $VM" >&2
  exit 1
fi

echo "$PORT"
