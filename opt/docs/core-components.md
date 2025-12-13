# Core Components\n\n## Virtualization\n\n- qemu-kvm\n\n- libvirt-daemon,

libvirt-daemon-system\n\n-

virt-manager (optional desktop usage)\n\n- ovmf, seabios\n\n- bridge-utils\n\n- cockpit,
cockpit-machines\n\nDebVisor supports VMs via KVM/libvirt, but the recommended
deployment\nmodel is
to run most application workloads as containers and reserve\nVMs for cases where a full
guest OS,
existing VM images, or strong\nOS-level isolation are required.\n\n## Storage\n\n-
ceph-mon,
ceph-mgr, ceph-osd, ceph-mds, ceph-common, ceph-fuse, radosgw (optional)\n\n- zfs-dkms,
zfsutils-linux\n\n- lvm2, mdadm\n\n- xfsprogs, btrfs-progs\n\n## Containers\n\n-
docker.io,
docker-compose-plugin\n\n- containerd, crictl\n\n## Kubernetes\n\n- kubeadm, kubelet,
kubectl\n\n-
calicoctl (default CNI tooling)\n\n- (optional future) cilium-cli\n\n- CSI drivers
deployed via
manifests (Ceph CSI, ZFS LocalPV)\n\nDebVisor is containers-first: Docker and Kubernetes
are
expected to\nhost the majority of workloads (microservices, web apps, controllers),\nwith
VMs used
when kernel customization, legacy appliances, or\nnon-containerized OS images are
needed.\n\n##
System & Tooling\n\n- openssh-server, cloud-init, chrony, rsyslog\n\n- nftables, ufw,
fail2ban\n\n-
vim, tmux, htop, jq, curl, git, ethtool, iproute2, net-tools\n\n- parted, lsblk, lshw,
pciutils,
usbutils\n\n## Rationale Highlights\n\n- CephFS first: shared RWX + RBD for performant VM
disks\n\n-
ZFS optional: local snapshot efficiency and compression\n\n- Calico chosen for mature
networking &
policy model\n\n- Hook scripts ensure DKMS and service enablement inside chroot\n\n
