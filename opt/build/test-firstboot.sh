#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="${ROOT}/config/includes.chroot/usr/local/sbin/debvisor-firstboot.sh"

if [[ ! -x "$SCRIPT" ]]; then
    echo "[test-firstboot] ERROR: firstboot script not found or not executable: $SCRIPT" >&2
    exit 1
fi

if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[test-firstboot] shellcheck not found; install it with: sudo apt install shellcheck" >&2
else
    echo "[test-firstboot] Running shellcheck on debvisor-firstboot.sh"
    shellcheck "$SCRIPT"
fi

echo "[test-firstboot] Running debvisor-firstboot.sh in dry-run mode (this should be non-destructive)"
if ! "$SCRIPT" --dry-run; then
    echo "[test-firstboot] ERROR: dry-run exited non-zero (check logs)" >&2
    exit 1
fi
