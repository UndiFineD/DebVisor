#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${REPO_ROOT}/ansible/playbooks/bootstrap-addons.yml"
DST="${REPO_ROOT}/config/includes.chroot/usr/local/share/debvisor/ansible/bootstrap-addons.yml"

if [[ ! -f "$SRC" ]]; then
    echo "[sync-addons-playbook] Source playbook not found: $SRC" >&2
    exit 1
fi

DST_DIR="$(dirname "$DST")"
mkdir -p "$DST_DIR"

if [[ -f "$DST" ]] && cmp -s "$SRC" "$DST"; then
    echo "[sync-addons-playbook] No changes; destination already up to date: $DST"
    exit 0
fi

install -m 0644 "$SRC" "$DST"
echo "[sync-addons-playbook] Synced addons playbook to includes.chroot: $DST"