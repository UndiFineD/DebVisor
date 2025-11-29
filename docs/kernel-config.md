# DebVisor Kernel Configuration Guide

This document describes the required and recommended kernel options for building a custom kernel optimized for DebVisor.

## Overview

DebVisor requires specific kernel features for virtualization, storage, and networking. This guide covers options needed for:

- KVM/Xen hypervisor support
- Ceph storage integration
- ZFS compatibility
- Container isolation (namespaces, cgroups v2)
- Hardware passthrough (IOMMU, VFIO)
- Advanced networking (VXLAN, eBPF, nftables)

## Base Kernel Version

**Minimum:** Linux 5.15 LTS
**Recommended:** Linux 6.1 LTS or newer

## Required Kernel Options

### Virtualization (KVM)

```kconfig
# KVM Core
CONFIG_VIRTUALIZATION=y
CONFIG_KVM=m
CONFIG_KVM_INTEL=m          # For Intel CPUs
CONFIG_KVM_AMD=m            # For AMD CPUs

# Nested Virtualization
CONFIG_KVM_INTEL_NESTED=y   # Optional but recommended
CONFIG_KVM_AMD_NESTED=y     # Optional but recommended

# virtio Devices
CONFIG_VIRTIO=y
CONFIG_VIRTIO_PCI=y
CONFIG_VIRTIO_MMIO=y
CONFIG_VIRTIO_BLK=m
CONFIG_VIRTIO_NET=m
CONFIG_VIRTIO_CONSOLE=m
CONFIG_VIRTIO_BALLOON=m
CONFIG_VIRTIO_INPUT=m
CONFIG_VIRTIO_FS=m

# vhost for performance
CONFIG_VHOST=m
CONFIG_VHOST_NET=m
CONFIG_VHOST_SCSI=m
CONFIG_VHOST_VSOCK=m
```text

### Xen Support (Optional)

```kconfig
CONFIG_XEN=y
CONFIG_XEN_PV=y
CONFIG_XEN_PVHVM=y
CONFIG_XEN_512GB=y
CONFIG_XEN_SAVE_RESTORE=y
CONFIG_XEN_BALLOON=y
CONFIG_XEN_BLKDEV_FRONTEND=m
CONFIG_XEN_NETDEV_FRONTEND=m
CONFIG_XEN_PCIDEV_FRONTEND=m
```text

### IOMMU & Hardware Passthrough

```kconfig
# IOMMU Support
CONFIG_IOMMU_SUPPORT=y
CONFIG_IOMMU_API=y
CONFIG_INTEL_IOMMU=y        # Intel VT-d
CONFIG_INTEL_IOMMU_SVM=y
CONFIG_AMD_IOMMU=y          # AMD-Vi
CONFIG_AMD_IOMMU_V2=y

# VFIO for Device Passthrough
CONFIG_VFIO=m
CONFIG_VFIO_IOMMU_TYPE1=m
CONFIG_VFIO_PCI=m
CONFIG_VFIO_VIRQFD=y
CONFIG_VFIO_MDEV=m          # Mediated devices

# GPU Passthrough
CONFIG_DRM=m
CONFIG_DRM_VGEM=m
```text

### Container Support

```kconfig
# Namespaces
CONFIG_NAMESPACES=y
CONFIG_UTS_NS=y
CONFIG_IPC_NS=y
CONFIG_USER_NS=y
CONFIG_PID_NS=y
CONFIG_NET_NS=y
CONFIG_CGROUP_NS=y

# Control Groups v2
CONFIG_CGROUPS=y
CONFIG_CGROUP_FREEZER=y
CONFIG_CGROUP_DEVICE=y
CONFIG_CGROUP_CPUACCT=y
CONFIG_CGROUP_PERF=y
CONFIG_CGROUP_SCHED=y
CONFIG_CGROUP_HUGETLB=y
CONFIG_CGROUP_PIDS=y
CONFIG_CGROUP_RDMA=y
CONFIG_CGROUP_BPF=y
CONFIG_MEMCG=y
CONFIG_BLK_CGROUP=y
CONFIG_CGROUP_WRITEBACK=y

# OverlayFS for Container Images
CONFIG_OVERLAY_FS=m
CONFIG_OVERLAY_FS_INDEX=y
CONFIG_OVERLAY_FS_XINO_AUTO=y
```text

### Storage - Ceph

```kconfig
# Ceph Distributed Storage
CONFIG_CEPH_LIB=m
CONFIG_CEPH_FS=m
CONFIG_CEPH_FSCACHE=y
CONFIG_BLK_DEV_RBD=m        # RADOS Block Device

# Ceph Messenger
CONFIG_CEPH_LIB_USE_DNS_RESOLVER=y
```text

### Storage - ZFS Compatibility

```kconfig
# Required for ZFS (DKMS builds against these)
CONFIG_MODULES=y
CONFIG_MODULE_UNLOAD=y
CONFIG_ZLIB_DEFLATE=y
CONFIG_ZLIB_INFLATE=y
CONFIG_CRYPTO_DEFLATE=y

# Filesystem features ZFS benefits from
CONFIG_BLOCK=y
CONFIG_BLK_DEV=y
CONFIG_BLK_DEV_LOOP=m
CONFIG_BLK_DEV_NVME=m
CONFIG_ATA=y

# Encryption for ZFS native encryption
CONFIG_CRYPTO_AES=y
CONFIG_CRYPTO_SHA256=y
CONFIG_CRYPTO_GCM=y
```text

### Networking

```kconfig
# Core Networking
CONFIG_NET=y
CONFIG_INET=y
CONFIG_IPV6=y
CONFIG_NETFILTER=y

# Bridge & VLAN
CONFIG_BRIDGE=m
CONFIG_BRIDGE_NETFILTER=y
CONFIG_VLAN_8021Q=m
CONFIG_VLAN_8021Q_GVRP=y

# Overlay Networks (VXLAN/Geneve)
CONFIG_VXLAN=m
CONFIG_GENEVE=m
CONFIG_GRE=m

# nftables Firewall
CONFIG_NF_TABLES=m
CONFIG_NF_TABLES_INET=y
CONFIG_NF_TABLES_NETDEV=y
CONFIG_NFT_CT=m
CONFIG_NFT_MASQ=m
CONFIG_NFT_NAT=m
CONFIG_NFT_REJECT=m
CONFIG_NFT_LOG=m
CONFIG_NFT_LIMIT=m

# eBPF for Cilium CNI
CONFIG_BPF=y
CONFIG_BPF_SYSCALL=y
CONFIG_BPF_JIT=y
CONFIG_BPF_JIT_ALWAYS_ON=y
CONFIG_CGROUP_BPF=y
CONFIG_NET_CLS_BPF=m
CONFIG_NET_ACT_BPF=m
CONFIG_BPF_STREAM_PARSER=y
CONFIG_XDP_SOCKETS=y

# Traffic Control
CONFIG_NET_SCHED=y
CONFIG_NET_CLS=y
CONFIG_NET_SCH_HTB=m
CONFIG_NET_SCH_INGRESS=m

# SR-IOV
CONFIG_PCI_IOV=y
CONFIG_PCI_PRI=y
CONFIG_PCI_PASID=y
```text

### Security

```kconfig
# Kernel Hardening
CONFIG_SECURITY=y
CONFIG_SECURITYFS=y
CONFIG_SECURITY_NETWORK=y

# AppArmor (recommended for containers)
CONFIG_SECURITY_APPARMOR=y
CONFIG_DEFAULT_SECURITY_APPARMOR=y

# SELinux (alternative)
CONFIG_SECURITY_SELINUX=y

# Secure Computing
CONFIG_SECCOMP=y
CONFIG_SECCOMP_FILTER=y

# TPM Support
CONFIG_TCG_TPM=m
CONFIG_TCG_TIS=m
CONFIG_TCG_TIS_CORE=m
CONFIG_TCG_CRB=m
CONFIG_TCG_VTPM_PROXY=m

# Integrity
CONFIG_INTEGRITY=y
CONFIG_IMA=y
CONFIG_EVM=y
```text

### Hardware Support

```kconfig
# NUMA Support
CONFIG_NUMA=y
CONFIG_X86_64_ACPI_NUMA=y
CONFIG_ACPI_NUMA=y

# Huge Pages
CONFIG_HUGETLBFS=y
CONFIG_HUGETLB_PAGE=y
CONFIG_TRANSPARENT_HUGEPAGE=y

# NVMe
CONFIG_BLK_DEV_NVME=m
CONFIG_NVME_CORE=m
CONFIG_NVME_MULTIPATH=y

# IPMI for Hardware Management
CONFIG_IPMI_HANDLER=m
CONFIG_IPMI_DEVICE_INTERFACE=m
CONFIG_IPMI_SI=m
CONFIG_IPMI_SSIF=m
CONFIG_IPMI_WATCHDOG=m

# Hardware Watchdog
CONFIG_WATCHDOG=y
CONFIG_WATCHDOG_CORE=y
CONFIG_SOFT_WATCHDOG=m
CONFIG_ITCO_WDT=m           # Intel TCO
```text

## Kernel Command Line Parameters

Add to GRUB (`/etc/default/grub`):

```bash
# Intel systems
GRUB_CMDLINE_LINUX="intel_iommu=on iommu=pt default_hugepagesz=1G hugepagesz=1G hugepages=16"

# AMD systems
GRUB_CMDLINE_LINUX="amd_iommu=on iommu=pt default_hugepagesz=1G hugepagesz=1G hugepages=16"

# Common additions
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash kvm.ignore_msrs=1 kvm.report_ignored_msrs=0"
```text

## Building the Kernel

### From Source

```bash
# Install build dependencies
apt install build-essential libncurses-dev bison flex libssl-dev libelf-dev

# Download kernel source
wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.1.xx.tar.xz
tar xf linux-6.1.xx.tar.xz
cd linux-6.1.xx

# Start with distribution config
cp /boot/config-$(uname -r) .config

# Apply DebVisor requirements
scripts/config --enable KVM
scripts/config --module KVM_INTEL
scripts/config --module KVM_AMD
scripts/config --enable VFIO
scripts/config --module VFIO_PCI
# ... (apply all required options)

# Update config
make olddefconfig

# Build
make -j$(nproc)
make modules_install
make install

# Update bootloader
update-grub
```text

### Verification Script

```bash
#!/bin/bash
# verify-kernel-config.sh - Verify kernel has required features

check_config() {
    local opt=$1
    local required=$2

    if grep -q "CONFIG_${opt}=[ym]" /boot/config-$(uname -r); then
        echo "[OK] CONFIG_${opt}"
    else
        if [ "$required" = "required" ]; then
            echo "[FAIL] CONFIG_${opt} - REQUIRED"
        else
            echo "[WARN] CONFIG_${opt} - recommended"
        fi
    fi
}

echo "=== DebVisor Kernel Configuration Check ==="
echo "Kernel: $(uname -r)"
echo ""

echo "--- Virtualization ---"
check_config KVM required
check_config VFIO required
check_config VFIO_PCI required

echo ""
echo "--- Storage ---"
check_config CEPH_FS required
check_config BLK_DEV_RBD required

echo ""
echo "--- Networking ---"
check_config VXLAN required
check_config BPF_SYSCALL required
check_config NF_TABLES required

echo ""
echo "--- Containers ---"
check_config NAMESPACES required
check_config CGROUPS required
check_config OVERLAY_FS required

echo ""
echo "--- Security ---"
check_config SECCOMP required
check_config INTEGRITY optional
```text

## Module Loading

Ensure required modules are loaded at boot:

```bash
# /etc/modules-load.d/debvisor.conf
vfio
vfio_iommu_type1
vfio_pci
vhost_net
br_netfilter
overlay
```text

## sysctl Tuning

```bash
# /etc/sysctl.d/99-debvisor.conf

# Enable IP forwarding
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1

# Bridge netfilter
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1

# Memory overcommit for VMs
vm.overcommit_memory = 1

# Increase inotify limits for containers
fs.inotify.max_user_instances = 8192
fs.inotify.max_user_watches = 524288

# Network tuning
net.core.somaxconn = 32768
net.ipv4.tcp_max_syn_backlog = 32768

# File handles for many VMs
fs.file-max = 2097152
```text

## Troubleshooting

### IOMMU Not Enabled

```bash
# Check IOMMU groups
find /sys/kernel/iommu_groups/ -type l | head -20

# If empty, verify BIOS settings:
# - Intel: VT-d enabled
# - AMD: AMD-Vi / IOMMU enabled
```text

### KVM Performance Issues

```bash
# Verify nested virtualization
cat /sys/module/kvm_intel/parameters/nested  # Should be Y

# Check MSR handling
cat /sys/module/kvm/parameters/ignore_msrs
```text

### Container Networking Issues

```bash
# Verify eBPF
bpftool feature probe

# Check cgroup v2
mount | grep cgroup2
```text

## References

- [KVM Documentation](https://www.linux-kvm.org/page/Documents)
- [Ceph Kernel Client](https://docs.ceph.com/en/latest/cephfs/kernel/)
- [ZFS on Linux](https://openzfs.github.io/openzfs-docs/)
- [Cilium Requirements](https://docs.cilium.io/en/stable/operations/system_requirements/)
