# DebVisor ISO Building Guide

This guide describes how to build a custom bootable ISO for DebVisor.

## Prerequisites

Ensure you have the required packages installed:

```bash
apt-get update
apt-get install -y $(cat iso-requirements.txt)
```python

## Build Process

### 1. Prepare the Workspace

Create a working directory for the build:

```bash
mkdir -p build/chroot
mkdir -p build/image/isolinux
mkdir -p build/image/live
```python

### 2. Bootstrap the Base System

Use `debootstrap` to install a minimal Debian system into the chroot:

```bash
debootstrap --arch=amd64 bookworm build/chroot http://deb.debian.org/debian/
```python

### 3. Configure the Chroot

Mount necessary filesystems and enter the chroot:

```bash
mount --bind /dev build/chroot/dev
mount --bind /proc build/chroot/proc
mount --bind /sys build/chroot/sys

chroot build/chroot /bin/bash
```python

Inside the chroot:

1. Set the hostname.
1. Install the Linux kernel (`linux-image-amd64`).
1. Install `live-boot` and `systemd-sysv`.
1. Install DebVisor dependencies (Python, etc.).
1. Copy the DebVisor application code to `/opt/debvisor`.
1. Set the root password.

Exit the chroot and unmount:

```bash
exit
umount build/chroot/sys
umount build/chroot/proc
umount build/chroot/dev
```python

### 4. Create the Filesystem Image

Compress the chroot into a SquashFS filesystem:

```bash
mksquashfs build/chroot build/image/live/filesystem.squashfs -e boot
```python

### 5. Configure the Bootloader (ISOLINUX)

Create `build/image/isolinux/isolinux.cfg`:

```text
UI menu.c32
PROMPT 0
TIMEOUT 50

MENU TITLE DebVisor Installer

LABEL debvisor
    MENU LABEL Install DebVisor
    LINUX /live/vmlinuz
    INITRD /live/initrd.img
    APPEND boot=live components quiet
```python

Copy necessary syslinux modules (`isolinux.bin`, `menu.c32`, `ldlinux.c32`, etc.) to `build/image/isolinux/`.

### 6. Build the ISO

Use `xorriso` to generate the hybrid ISO:

```bash
xorriso -as mkisofs \
    -r -J --joliet-long \
    -l -iso-level 3 \
    -o debvisor-installer.iso \
    -b isolinux/isolinux.bin \
    -c isolinux/boot.cat \
    -no-emul-boot -boot-load-size 4 -boot-info-table \
    -eltorito-alt-boot -e boot/grub/efi.img -no-emul-boot \
    build/image
```python

## Verification

Test the ISO in a VM (QEMU/KVM):

```bash
qemu-system-x86_64 -m 2G -cdrom debvisor-installer.iso
```python
