#!/bin/sh
set -e

# DebVisor installer: collect addon choices via debconf and
# render /target/etc/debvisor-addons.conf for first boot.

OUT="/target/etc/debvisor-addons.conf"

# Defaults: all addons disabled for a minimal, secure core.
RPC="no"
WEB="no"
VNC="no"
MON="no"

# Read debconf answers if they exist (boolean yes/no)
if command -v debconf-communicate >/dev/null 2>&1; then
  if printf 'GET debvisor/addon-rpc\n' | debconf-communicate 2>/dev/null | grep -q '^0 '; then
    RPC=$(printf 'GET debvisor/addon-rpc\n' | debconf-communicate 2>/dev/null | awk '{print $2}' | tr 'A-Z' 'a-z')
  fi
  if printf 'GET debvisor/addon-webpanel\n' | debconf-communicate 2>/dev/null | grep -q '^0 '; then
    WEB=$(printf 'GET debvisor/addon-webpanel\n' | debconf-communicate 2>/dev/null | awk '{print $2}' | tr 'A-Z' 'a-z')
  fi
  if printf 'GET debvisor/addon-vncconsole\n' | debconf-communicate 2>/dev/null | grep -q '^0 '; then
    VNC=$(printf 'GET debvisor/addon-vncconsole\n' | debconf-communicate 2>/dev/null | awk '{print $2}' | tr 'A-Z' 'a-z')
  fi
  if printf 'GET debvisor/addon-monitoring\n' | debconf-communicate 2>/dev/null | grep -q '^0 '; then
    MON=$(printf 'GET debvisor/addon-monitoring\n' | debconf-communicate 2>/dev/null | awk '{print $2}' | tr 'A-Z' 'a-z')
  fi
fi

mkdir -p "$(dirname "$OUT")"
cat >"$OUT" <<EOF
# DebVisor optional addons configuration (generated at install time)
# Valid values: yes/no (case-insensitive). Default is "no" when unset.
# This file is read by debvisor-firstboot.sh on first boot.

ADDON_RPC_SERVICE=$RPC
ADDON_WEB_PANEL=$WEB
ADDON_VNC_CONSOLE=$VNC
ADDON_MONITORING_STACK=$MON
EOF

chmod 0644 "$OUT"
