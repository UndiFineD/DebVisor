#!/bin/sh
set -e
echo "[HOOK 040] Installing Kubernetes core"
apt-get update
apt-get install -y kubeadm kubelet kubectl containerd crictl
systemctl enable kubelet || true
