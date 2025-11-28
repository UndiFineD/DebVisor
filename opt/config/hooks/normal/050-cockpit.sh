#!/bin/sh
set -e
echo "[HOOK 050] Installing Cockpit and modules"
apt-get update
apt-get install -y cockpit cockpit-machines cockpit-networkmanager cockpit-storaged
