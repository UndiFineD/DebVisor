# Architecture

DebVisor is a containers?first, hyper?converged node: it treats
containers and Kubernetes workloads as the default way to run
applications, with VMs available alongside them when needed.
Use containers when:

- You are deploying stateless or horizontally scalable services.

- You want Kubernetes-native automation, rolling updates, and self-healing.

- You need fast iteration and simple rollbacks for application code.
Use VMs when:

- You are running legacy or appliance-style workloads that cannot be containerized yet.

- You need strong isolation boundaries or custom guest kernels.

- You are hosting operating-system-level environments (e.g. lab images, special-purpose appliances).
## Base
- Debian minimal (netinst/live-build base; default target release: bookworm)

- English (US) locale, UTC timezone
## Virtualization Layer
- KVM/QEMU + libvirt (daemon + system integration)

- OVMF (UEFI guest firmware) + SeaBIOS (legacy)

- Cockpit (machines/network/storage dashboards)

- Optional LXD (future consideration)
## Storage Layer
- Ceph (MON, MGR, OSD, MDS) for shared storage (CephFS, RBD)

- ZFS for local performance datasets (vm, docker, k8s) - optional or mixed

- LVM2 / mdadm fallback support; xfs, btrfs utilities
## Container & Orchestration Layer
- Docker Engine + Compose plugin (classic workloads)

- Kubernetes: kubeadm, kubelet, kubectl

- Container runtime: containerd (for K8s) + crictl tooling

- CNI default: Calico (Cilium optional future)

- CSI: Ceph CSI (RBD & CephFS) + optional ZFS LocalPV
## Networking
- Primary bridge `br0` for VMs and services

- VLAN / bonding support (future dynamic detection)

- Calico pod network; potential BGP for multi-node expansion
## Management & Automation
- Systemd first?boot service invoking provisioning script

- Cockpit for web-based visualization & control

- Configuration seeded via preseed + profile selection
## Security & Resilience
- Fail2ban, nftables/ufw, unattended upgrades

- Optional rootless Docker mode (future enhancement)

- ZFS scrub + Ceph health checks (timers)
## Expansion (Roadmap)
- Multi-node Ceph and Kubernetes join scripts

- Metrics/observability stack (Prometheus/Grafana)

- Upgrade orchestration (Ansible playbooks)
