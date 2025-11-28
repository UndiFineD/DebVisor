#!/bin/bash
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
