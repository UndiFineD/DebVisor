# DebVisor ISO Building Guide\n\nThis guide describes how to build a custom bootable ISO

for

DebVisor.\n\n## Prerequisites\n\nEnsure you have the required packages
installed:\n\n```bash\napt-get update\napt-get install -y $(cat
iso-requirements.txt)\n\n```python\n\napt-get install -y $(cat
iso-requirements.txt)\n\n```python\napt-get update\napt-get install -y $(cat
iso-requirements.txt)\n\n```python\n\napt-get install -y $(cat
iso-requirements.txt)\n\n```python\napt-get update\napt-get install -y $(cat
iso-requirements.txt)\n\n```python\n\napt-get install -y $(cat
iso-requirements.txt)\n\n```python\napt-get install -y $(cat
iso-requirements.txt)\n\n```python\n\n```python\n## Build Process\n### 1.
Prepare the
Workspace\nCreate a working directory for the build:\n\n```bash\n\n### 1.
Prepare the
Workspace
(2)\n\nCreate a working directory for the build:\n\n```bash\n## Build Process
(2)\n\n###

1. Prepare
the Workspace (3)\n\nCreate a working directory for the build:\n\n```bash\n\n###
1.
Prepare the
Workspace (4)\n\nCreate a working directory for the build:\n\n```bash\n## Build
Process
(3)\n### 1.
Prepare the Workspace (5)\nCreate a working directory for the
build:\n\n```bash\n\n### 1.
Prepare
the Workspace (6)\n\nCreate a working directory for the build:\n\n```bash\n###

1. Prepare
the
Workspace (7)\n\nCreate a working directory for the build:\n\n```bash\n\nCreate
a working
directory
for the build:\n\n```bash\nmkdir -p build/chroot\nmkdir -p
build/image/isolinux\nmkdir -p
build/image/live\n\n```python\n\nmkdir -p build/image/isolinux\nmkdir -p
build/image/live\n\n```python\nmkdir -p build/chroot\nmkdir -p
build/image/isolinux\nmkdir
-p
build/image/live\n\n```python\n\nmkdir -p build/image/isolinux\nmkdir -p
build/image/live\n\n```python\nmkdir -p build/chroot\nmkdir -p
build/image/isolinux\nmkdir
-p
build/image/live\n\n```python\n\nmkdir -p build/image/isolinux\nmkdir -p
build/image/live\n\n```python\nmkdir -p build/image/isolinux\nmkdir -p
build/image/live\n\n```python\nmkdir -p build/image/live\n\n```python\n### 2.
Bootstrap
the Base
System\nUse `debootstrap`to install a minimal Debian system into the
chroot:\n\n```bash\nUse`debootstrap`to install a minimal Debian system into the
chroot:\n\n```bash\n### 2. Bootstrap the Base System (2)\n\nUse`debootstrap`to
install a
minimal
Debian system into the chroot:\n\n```bash\n\nUse`debootstrap`to install a
minimal Debian
system into
the chroot:\n\n```bash\n### 2. Bootstrap the Base System (3)\nUse`debootstrap`to
install a
minimal
Debian system into the chroot:\n\n```bash\n\nUse`debootstrap`to install a
minimal Debian
system into
the chroot:\n\n```bash\nUse`debootstrap`to install a minimal Debian system into
the
chroot:\n\n```bash\n\n```bash\ndebootstrap --arch=amd64 bookworm build/chroot
\n\n```python\n\n```python\ndebootstrap]([http://deb.debian.org/debian/>\n\n```python\n\n```python\ndebootstra]([http://deb.debian.org/debian/>\n\n```python\n\n```python\ndebootstr]([http://deb.debian.org/debian/>\n\n```python\n\n```python\ndebootst]([http://deb.debian.org/debian/>\n\n```python\n\n```python\ndeboots]([http://deb.debian.org/debian/>\n\n```python\n\n```python\ndeboot]([http://deb.debian.org/debian/>\n\n```python\n\n```python\ndeboo]([http://deb.debian.org/debian/>\n\n```python\n\n```python\ndebo]([http://deb.debian.org/debian/>\n\n```python\n\n```python\ndeb]([http://deb.debian.org/debian/>\n\n```python\n\n```python\nde]([http://deb.debian.org/debian/>\n\n```python\n\n```python\nd]([http://deb.debian.org/debian/>\n\n```python\n\n```python\n]([http://deb.debian.org/debian/>\n\n```python\n\n```python\]([http://deb.debian.org/debian/>\n\n```python\n\n```python]([http://deb.debian.org/debian/>\n\n```python\n\n```pytho]([http://deb.debian.org/debian/>\n\n```python\n\n```pyth]([http://deb.debian.org/debian/>\n\n```python\n\n```pyt]([http://deb.debian.org/debian/>\n\n```python\n\n```py]([http://deb.debian.org/debian/>\n\n```python\n\n```p]([http://deb.debian.org/debian/>\n\n```python\n\n```]([http://deb.debian.org/debian/>\n\n```python\n\n``]([http://deb.debian.org/debian/>\n\n```python\n\n`]([http://deb.debian.org/debian/>\n\n```python\n\n]([http://deb.debian.org/debian/>\n\n```python\n\]([http://deb.debian.org/debian/>\n\n```python\n]([http://deb.debian.org/debian/>\n\n```python\]([http://deb.debian.org/debian/>\n\n```python]([http://deb.debian.org/debian/>\n\n```pytho]([http://deb.debian.org/debian/>\n\n```pyth]([http://deb.debian.org/debian/>\n\n```pyt]([http://deb.debian.org/debian/>\n\n```py](http://deb.debian.org/debian/>\n\n```py)t)h)o)n)\)n)\)n)`)`)`)p)y)t)h)o)n)\)n)d)e)b)o)o)t)s)t)r)a)p)
--arch=amd64 bookworm build/chroot
[https://deb.debian.org/debian/\n\n```python\n\n```python\ndebootstrap]([https://deb.debian.org/debian/\n\n```python\n\n```python\ndebootstra]([https://deb.debian.org/debian/\n\n```python\n\n```python\ndebootstr]([https://deb.debian.org/debian/\n\n```python\n\n```python\ndebootst]([https://deb.debian.org/debian/\n\n```python\n\n```python\ndeboots]([https://deb.debian.org/debian/\n\n```python\n\n```python\ndeboot]([https://deb.debian.org/debian/\n\n```python\n\n```python\ndeboo]([https://deb.debian.org/debian/\n\n```python\n\n```python\ndebo]([https://deb.debian.org/debian/\n\n```python\n\n```python\ndeb]([https://deb.debian.org/debian/\n\n```python\n\n```python\nde]([https://deb.debian.org/debian/\n\n```python\n\n```python\nd]([https://deb.debian.org/debian/\n\n```python\n\n```python\n]([https://deb.debian.org/debian/\n\n```python\n\n```python\]([https://deb.debian.org/debian/\n\n```python\n\n```python]([https://deb.debian.org/debian/\n\n```python\n\n```pytho]([https://deb.debian.org/debian/\n\n```python\n\n```pyth]([https://deb.debian.org/debian/\n\n```python\n\n```pyt]([https://deb.debian.org/debian/\n\n```python\n\n```py]([https://deb.debian.org/debian/\n\n```python\n\n```p]([https://deb.debian.org/debian/\n\n```python\n\n```]([https://deb.debian.org/debian/\n\n```python\n\n``]([https://deb.debian.org/debian/\n\n```python\n\n`]([https://deb.debian.org/debian/\n\n```python\n\n]([https://deb.debian.org/debian/\n\n```python\n\]([https://deb.debian.org/debian/\n\n```python\n]([https://deb.debian.org/debian/\n\n```python\]([https://deb.debian.org/debian/\n\n```python]([https://deb.debian.org/debian/\n\n```pytho]([https://deb.debian.org/debian/\n\n```pyth]([https://deb.debian.org/debian/\n\n```pyt]([https://deb.debian.org/debian/\n\n```py](https://deb.debian.org/debian/\n\n```py)t)h)o)n)\)n)\)n)`)`)`)p)y)t)h)o)n)\)n)d)e)b)o)o)t)s)t)r)a)p)
--arch=amd64 bookworm build/chroot
[https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n```python\n###]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n```python\n##]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n```python\n#]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n```python\n]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n```python\]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n```python]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n```pytho]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n```pyth]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n```pyt]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n```py]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n```p]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n```]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n``]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n`]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\n]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n\]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\n]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python\]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```python]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```pytho]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```pyth]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```pyt]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```py]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```p]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n```]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n``]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n`]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\n]([https://deb.debian.org/debian/\n\n```python\n\n```python\n\]([https://deb.debian.org/debian/\n\n```python\n\n```python\n]([https://deb.debian.org/debian/\n\n```python\n\n```python\](https://deb.debian.org/debian/\n\n```python\n\n```python\)n)\)n)`)`)`)p)y)t)h)o)n)\)n)\)n)`)`)`)p)y)t)h)o)n)\)n)#)#)#)

1. Configure the Chroot\nMount necessary filesystems and enter the
chroot:\n\n```bash\nMount
necessary filesystems and enter the chroot:\n\n```bash\n### 3. Configure the
Chroot
(2)\n\nMount
necessary filesystems and enter the chroot:\n\n```bash\n\nMount necessary
filesystems and
enter the
chroot:\n\n```bash\n### 3. Configure the Chroot (3)\nMount necessary filesystems
and enter
the
chroot:\n\n```bash\n\nMount necessary filesystems and enter the
chroot:\n\n```bash\nMount
necessary
filesystems and enter the chroot:\n\n```bash\n\n```bash\nmount --bind /dev
build/chroot/dev\nmount
--bind /proc build/chroot/proc\nmount --bind /sys build/chroot/sys\nchroot
build/chroot
/bin/bash\n\n```python\n\nmount --bind /proc build/chroot/proc\nmount --bind
/sys
build/chroot/sys\nchroot build/chroot /bin/bash\n\n```python\nmount --bind /dev
build/chroot/dev\nmount --bind /proc build/chroot/proc\nmount --bind /sys
build/chroot/sys\nchroot
build/chroot /bin/bash\n\n```python\n\nmount --bind /proc
build/chroot/proc\nmount --bind
/sys
build/chroot/sys\nchroot build/chroot /bin/bash\n\n```python\nmount --bind /dev
build/chroot/dev\nmount --bind /proc build/chroot/proc\nmount --bind /sys
build/chroot/sys\nchroot
build/chroot /bin/bash\n\n```python\n\nmount --bind /proc
build/chroot/proc\nmount --bind
/sys
build/chroot/sys\nchroot build/chroot /bin/bash\n\n```python\nmount --bind /proc
build/chroot/proc\nmount --bind /sys build/chroot/sys\nchroot build/chroot
/bin/bash\n\n```python\n\nmount --bind /sys build/chroot/sys\nchroot
build/chroot
/bin/bash\n\n```python\nInside the chroot:\n\n1. Set the hostname.\n\n1. Install
the Linux
kernel
(`linux-image-amd64`).\n\n1. Install`live-boot`and`systemd-sysv`.\n\n1. Install
DebVisor
dependencies (Python, etc.).\n\n1. Copy the DebVisor application code to
`/opt/debvisor`.\n\n1. Set
the root password.\nExit the chroot and unmount:\n\n```bash\n\n1. Set the
hostname.\n\n1.
Install
the Linux kernel (`linux-image-amd64`).\n\n1. Install
`live-boot`and`systemd-sysv`.\n\n1.
Install
DebVisor dependencies (Python, etc.).\n\n1. Copy the DebVisor application code
to
`/opt/debvisor`.\n\n1. Set the root password.\n\nExit the chroot and
unmount:\n\n```bash\nInside the
chroot:\n\n1. Set the hostname.\n\n1. Install the Linux kernel
(`linux-image-amd64`).\n\n1. Install
`live-boot`and`systemd-sysv`.\n\n1. Install DebVisor dependencies (Python,
etc.).\n\n1.
Copy the
DebVisor application code to `/opt/debvisor`.\n\n1. Set the root password.\nExit
the
chroot and
unmount:\n\n```bash\n\n1. Set the hostname.\n\n1. Install the Linux kernel
(`linux-image-amd64`).\n\n1. Install `live-boot`and`systemd-sysv`.\n\n1. Install
DebVisor
dependencies (Python, etc.).\n\n1. Copy the DebVisor application code to
`/opt/debvisor`.\n\n1. Set
the root password.\n\nExit the chroot and unmount:\n\n```bash\nInside the
chroot:\n\n1.
Set the
hostname.\n\n1. Install the Linux kernel (`linux-image-amd64`).\n\n1. Install
`live-boot`and`systemd-sysv`.\n\n1. Install DebVisor dependencies (Python,
etc.).\n\n1.
Copy the
DebVisor application code to `/opt/debvisor`.\n\n1. Set the root password.\nExit
the
chroot and
unmount:\n\n```bash\n\n1. Set the hostname.\n\n1. Install the Linux kernel
(`linux-image-amd64`).\n\n1. Install `live-boot`and`systemd-sysv`.\n\n1. Install
DebVisor
dependencies (Python, etc.).\n\n1. Copy the DebVisor application code to
`/opt/debvisor`.\n\n1. Set
the root password.\n\nExit the chroot and unmount:\n\n```bash\n\n1. Set the
hostname.\n\n1. Install
the Linux kernel (`linux-image-amd64`).\n\n1. Install
`live-boot`and`systemd-sysv`.\n\n1.
Install
DebVisor dependencies (Python, etc.).\n\n1. Copy the DebVisor application code
to
`/opt/debvisor`.\n\n1. Set the root password.\nExit the chroot and
unmount:\n\n```bash\n\n1. Set the
hostname.\n\n1. Install the Linux kernel (`linux-image-amd64`).\n\n1. Install
`live-boot`and`systemd-sysv`.\n\n1. Install DebVisor dependencies (Python,
etc.).\n\n1.
Copy the
DebVisor application code to `/opt/debvisor`.\n\n1. Set the root
password.\n\nExit the
chroot and
unmount:\n\n```bash\nexit\numount build/chroot/sys\numount
build/chroot/proc\numount
build/chroot/dev\n\n```python\n\numount build/chroot/sys\numount
build/chroot/proc\numount
build/chroot/dev\n\n```python\nexit\numount build/chroot/sys\numount
build/chroot/proc\numount
build/chroot/dev\n\n```python\n\numount build/chroot/sys\numount
build/chroot/proc\numount
build/chroot/dev\n\n```python\nexit\numount build/chroot/sys\numount
build/chroot/proc\numount
build/chroot/dev\n\n```python\n\numount build/chroot/sys\numount
build/chroot/proc\numount
build/chroot/dev\n\n```python\numount build/chroot/sys\numount
build/chroot/proc\numount
build/chroot/dev\n\n```python\numount build/chroot/proc\numount
build/chroot/dev\n\n```python\n###

1. Create the Filesystem Image\nCompress the chroot into a SquashFS
filesystem:\n\n```bash\nCompress
the chroot into a SquashFS filesystem:\n\n```bash\n### 4. Create the Filesystem
Image
(2)\n\nCompress the chroot into a SquashFS filesystem:\n\n```bash\n\nCompress
the chroot
into a
SquashFS filesystem:\n\n```bash\n### 4. Create the Filesystem Image
(3)\nCompress the
chroot into a
SquashFS filesystem:\n\n```bash\n\nCompress the chroot into a SquashFS
filesystem:\n\n```bash\nCompress the chroot into a SquashFS
filesystem:\n\n```bash\n\n```bash\nmksquashfs build/chroot
build/image/live/filesystem.squashfs -e
boot\n\n```python\n\n```python\nmksquashfs build/chroot
build/image/live/filesystem.squashfs -e
boot\n\n```python\n\n```python\nmksquashfs build/chroot
build/image/live/filesystem.squashfs -e
boot\n\n```python\n\n```python\n\n```python\n\n```python\n### 5. Configure the
Bootloader
(ISOLINUX)\nCreate `build/image/isolinux/isolinux.cfg`:\n```text\nCreate
`build/image/isolinux/isolinux.cfg`:\n```text\n### 5. Configure the Bootloader
(ISOLINUX)
(2)\n\nCreate `build/image/isolinux/isolinux.cfg`:\n```text\n\nCreate
`build/image/isolinux/isolinux.cfg`:\n```text\n### 5. Configure the Bootloader
(ISOLINUX)
(3)\nCreate `build/image/isolinux/isolinux.cfg`:\n```text\n\nCreate
`build/image/isolinux/isolinux.cfg`:\n```text\nCreate
`build/image/isolinux/isolinux.cfg`:\n```text\n```text\nUI menu.c32\nPROMPT
0\nTIMEOUT
50\nMENU
TITLE DebVisor Installer\nLABEL debvisor\n MENU LABEL Install DebVisor\n LINUX
/live/vmlinuz\n
INITRD /live/initrd.img\n APPEND boot=live components
quiet\n\n```python\n\nPROMPT
0\nTIMEOUT
50\nMENU TITLE DebVisor Installer\nLABEL debvisor\n MENU LABEL Install
DebVisor\n LINUX
/live/vmlinuz\n INITRD /live/initrd.img\n APPEND boot=live components
quiet\n\n```python\nUI
menu.c32\nPROMPT 0\nTIMEOUT 50\nMENU TITLE DebVisor Installer\nLABEL debvisor\n
MENU LABEL
Install
DebVisor\n LINUX /live/vmlinuz\n INITRD /live/initrd.img\n APPEND boot=live
components
quiet\n\n```python\n\nPROMPT 0\nTIMEOUT 50\nMENU TITLE DebVisor Installer\nLABEL
debvisor\n MENU
LABEL Install DebVisor\n LINUX /live/vmlinuz\n INITRD /live/initrd.img\n APPEND
boot=live
components
quiet\n\n```python\nUI menu.c32\nPROMPT 0\nTIMEOUT 50\nMENU TITLE DebVisor
Installer\nLABEL
debvisor\n MENU LABEL Install DebVisor\n LINUX /live/vmlinuz\n INITRD
/live/initrd.img\n
APPEND
boot=live components quiet\n\n```python\n\nPROMPT 0\nTIMEOUT 50\nMENU TITLE
DebVisor
Installer\nLABEL debvisor\n MENU LABEL Install DebVisor\n LINUX /live/vmlinuz\n
INITRD
/live/initrd.img\n APPEND boot=live components quiet\n\n```python\nPROMPT
0\nTIMEOUT
50\nMENU TITLE
DebVisor Installer\nLABEL debvisor\n MENU LABEL Install DebVisor\n LINUX
/live/vmlinuz\n
INITRD
/live/initrd.img\n APPEND boot=live components quiet\n\n```python\n\nTIMEOUT
50\nMENU
TITLE DebVisor
Installer\nLABEL debvisor\n MENU LABEL Install DebVisor\n LINUX /live/vmlinuz\n
INITRD
/live/initrd.img\n APPEND boot=live components quiet\n\n```python\nCopy
necessary syslinux
modules
(`isolinux.bin`, `menu.c32`, `ldlinux.c32`, etc.) to
`build/image/isolinux/`.\n### 6.
Build the
ISO\nUse `xorriso`to generate the hybrid ISO:\n\n```bash\n\n### 6. Build the ISO
(2)\n\nUse`xorriso`to generate the hybrid ISO:\n\n```bash\nCopy necessary
syslinux modules
(`isolinux.bin`,`menu.c32`, `ldlinux.c32`, etc.) to
`build/image/isolinux/`.\n\n### 6.
Build the ISO
(3)\n\nUse `xorriso`to generate the hybrid ISO:\n\n```bash\n\n### 6. Build the
ISO
(4)\n\nUse`xorriso`to generate the hybrid ISO:\n\n```bash\nCopy necessary
syslinux modules
(`isolinux.bin`,`menu.c32`, `ldlinux.c32`, etc.) to
`build/image/isolinux/`.\n### 6. Build
the ISO
(5)\nUse `xorriso`to generate the hybrid ISO:\n\n```bash\n\n### 6. Build the ISO
(6)\n\nUse`xorriso`to generate the hybrid ISO:\n\n```bash\n### 6. Build the ISO
(7)\n\nUse`xorriso`to generate the hybrid ISO:\n\n```bash\n\nUse`xorriso` to
generate the
hybrid
ISO:\n\n```bash\nxorriso -as mkisofs \\n\n - r -J --joliet-long \\n\n - l
-iso-level 3
\\n\n - o
debvisor-installer.iso \\n\n - b isolinux/isolinux.bin \\n\n - c
isolinux/boot.cat \\n\n -
no-emul-boot -boot-load-size 4 -boot-info-table \\n\n - eltorito-alt-boot -e
boot/grub/efi.img
-no-emul-boot \\n build/image\n\n```python\n\n - r -J --joliet-long \\n\n - l
-iso-level 3
\\n\n - o
debvisor-installer.iso \\n\n - b isolinux/isolinux.bin \\n\n - c
isolinux/boot.cat \\n\n -
no-emul-boot -boot-load-size 4 -boot-info-table \\n\n - eltorito-alt-boot -e
boot/grub/efi.img
-no-emul-boot \\n\n build/image\n\n```python\nxorriso -as mkisofs \\n\n - r -J
--joliet-long \\n\n -
l -iso-level 3 \\n\n - o debvisor-installer.iso \\n\n - b isolinux/isolinux.bin
\\n\n - c
isolinux/boot.cat \\n\n - no-emul-boot -boot-load-size 4 -boot-info-table \\n\n
-
eltorito-alt-boot
-e boot/grub/efi.img -no-emul-boot \\n build/image\n\n```python\n\n - r -J
--joliet-long
\\n\n - l
-iso-level 3 \\n\n - o debvisor-installer.iso \\n\n - b isolinux/isolinux.bin
\\n\n - c
isolinux/boot.cat \\n\n - no-emul-boot -boot-load-size 4 -boot-info-table \\n\n
-
eltorito-alt-boot
-e boot/grub/efi.img -no-emul-boot \\n\n build/image\n\n```python\nxorriso -as
mkisofs
\\n\n - r -J
--joliet-long \\n\n - l -iso-level 3 \\n\n - o debvisor-installer.iso \\n\n - b
isolinux/isolinux.bin \\n\n - c isolinux/boot.cat \\n\n - no-emul-boot
-boot-load-size 4
-boot-info-table \\n\n - eltorito-alt-boot -e boot/grub/efi.img -no-emul-boot
\\n
build/image\n\n```python\n\n - r -J --joliet-long \\n\n - l -iso-level 3 \\n\n -
o
debvisor-installer.iso \\n\n - b isolinux/isolinux.bin \\n\n - c
isolinux/boot.cat \\n\n -
no-emul-boot -boot-load-size 4 -boot-info-table \\n\n - eltorito-alt-boot -e
boot/grub/efi.img
-no-emul-boot \\n\n build/image\n\n```python\n\n - r -J --joliet-long \\n\n - l
-iso-level
3 \\n\n -
o debvisor-installer.iso \\n\n - b isolinux/isolinux.bin \\n\n - c
isolinux/boot.cat \\n\n
-
no-emul-boot -boot-load-size 4 -boot-info-table \\n\n - eltorito-alt-boot -e
boot/grub/efi.img
-no-emul-boot \\n build/image\n\n```python\n\n - r -J --joliet-long \\n\n - l
-iso-level 3
\\n\n - o
debvisor-installer.iso \\n\n - b isolinux/isolinux.bin \\n\n - c
isolinux/boot.cat \\n\n -
no-emul-boot -boot-load-size 4 -boot-info-table \\n\n - eltorito-alt-boot -e
boot/grub/efi.img
-no-emul-boot \\n\n build/image\n\n```python\n## Verification\nTest the ISO in a
VM
(QEMU/KVM):\n\n```bash\nTest the ISO in a VM (QEMU/KVM):\n\n```bash\n##
Verification
(2)\n\nTest the
ISO in a VM (QEMU/KVM):\n\n```bash\n\nTest the ISO in a VM
(QEMU/KVM):\n\n```bash\n##
Verification
(3)\nTest the ISO in a VM (QEMU/KVM):\n\n```bash\n\nTest the ISO in a VM
(QEMU/KVM):\n\n```bash\nTest the ISO in a VM
(QEMU/KVM):\n\n```bash\n\n```bash\nqemu-system-x86_64
-m 2G -cdrom
debvisor-installer.iso\n\n```python\n\n```python\nqemu-system-x86_64 -m 2G
-cdrom
debvisor-installer.iso\n\n```python\n\n```python\nqemu-system-x86_64 -m 2G
-cdrom
debvisor-installer.iso\n\n```python\n\n```python\n\n```python\n\n```python\n\n
