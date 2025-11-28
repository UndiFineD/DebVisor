#!/bin/sh
set -e
echo "[HOOK 030] Installing Ceph core stack"
apt-get update
apt-get install -y ceph-mon ceph-mgr ceph-osd ceph-mds ceph-common ceph-fuse radosgw
