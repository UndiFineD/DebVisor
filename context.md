# DebVisor Context\n\n## Structure\n\nTab size is 4 spaces\n\n## Overall

Purpose\n\nDebVisor is a

Debian 13-based mini hyper-converged hypervisor distro.\nIt is containers-first
(Docker/Kubernetes),
with VMs supported for\nlegacy and special-case workloads. The goal is a turnkey ISO that
you\nboot,
install via a curses (ncurses) installer, and end up with:\nKVM/libvirt + bridges +
Cockpit web
UI\nCephFS-first (with optional ZFS or mixed Ceph+ZFS)\nDocker + Kubernetes (kubeadm,
containerd,
Calico)\nOpinionated defaults and automated first-boot provisioning.\nKey entry
points:\nREADME.md -
high-level description, profiles, and ISO build quickstart.\nMakefile + build-debvisor.sh

- one-shot
live-build wrapper to produce the ISO.\nDebVisor_initial.md - now just a stub table
listing
canonical file locations.\n\n## Installer & Image Build\n
