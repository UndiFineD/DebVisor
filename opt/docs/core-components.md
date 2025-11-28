# Core Components

## Virtualization

- qemu-kvm
- libvirt-daemon, libvirt-daemon-system
- virt-manager (optional desktop usage)
- ovmf, seabios
- bridge-utils
- cockpit, cockpit-machines

DebVisor supports VMs via KVM/libvirt, but the recommended deployment
model is to run most application workloads as containers and reserve
VMs for cases where a full guest OS, existing VM images, or strong
OS-level isolation are required.

## Storage

- ceph-mon, ceph-mgr, ceph-osd, ceph-mds, ceph-common, ceph-fuse, radosgw (optional)
- zfs-dkms, zfsutils-linux
- lvm2, mdadm
- xfsprogs, btrfs-progs

## Containers

- docker.io, docker-compose-plugin
- containerd, crictl

## Kubernetes

- kubeadm, kubelet, kubectl
- calicoctl (default CNI tooling)
- (optional future) cilium-cli
- CSI drivers deployed via manifests (Ceph CSI, ZFS LocalPV)

DebVisor is containers-first: Docker and Kubernetes are expected to
host the majority of workloads (microservices, web apps, controllers),
with VMs used when kernel customization, legacy appliances, or
non-containerized OS images are needed.

## System & Tooling

- openssh-server, cloud-init, chrony, rsyslog
- nftables, ufw, fail2ban
- vim, tmux, htop, jq, curl, git, ethtool, iproute2, net-tools
- parted, lsblk, lshw, pciutils, usbutils

## Rationale Highlights

- CephFS first: shared RWX + RBD for performant VM disks
- ZFS optional: local snapshot efficiency and compression
- Calico chosen for mature networking & policy model
- Hook scripts ensure DKMS and service enablement inside chroot
