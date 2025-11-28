#!/bin/sh
set -e
echo "[HOOK 020] Installing ZFS packages"
apt-get update
apt-get install -y --no-install-recommends zfs-dkms zfsutils-linux
