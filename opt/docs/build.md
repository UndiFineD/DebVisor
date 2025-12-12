# DebVisor ISO Build

This document explains how to build the DebVisor ISO using the helper script.
## Prerequisites
- A Debian-based build environment with `live-build`(`lb`) installed.

- This repository checked out on the build machine.
## Basic build
From the project root:
    ./build/build-debvisor.sh
This will:

- Clean any previous build artifacts.

- Configure `live-build` for the default Debian distribution and architecture.

- Build an ISO named `live-image-amd64.hybrid.iso` in the project root (by default).
## Environment variables
The build script can be customized via environment variables.
### `DEBVISOR_DIST`
Target Debian distribution for the ISO.

- **Default:**`bookworm`

- **Example:**
    DEBVISOR_DIST=trixie ./build/build-debvisor.sh
### `DEBVISOR_FAST`
Control whether the build script runs `lb clean` before building.

- `0` (default): Perform a full clean before configuring and building.

- `1`: Skip`lb clean` to speed up iterative builds.

- **Example:**
    DEBVISOR_FAST=1 ./build/build-debvisor.sh
You can combine both variables:
    DEBVISOR_DIST=trixie DEBVISOR_FAST=1 ./build/build-debvisor.sh
### `DEBVISOR_ARCH`
Target architecture for the ISO.

- **Default:**`amd64`

- **Examples:**
    DEBVISOR_ARCH=arm64 ./build/build-debvisor.sh
    DEBVISOR_ARCH=riscv64 ./build/build-debvisor.sh
Actual success depends on `live-build` and Debian support for that architecture on your build host (amd64 is the primary, best-tested target).
### `DEBVISOR_VERSION`
Optional version tag used to construct a more descriptive ISO filename.

- **Default:**empty (keeps the original `live-image-amd64.hybrid.iso` name)

- **Example:**
    DEBVISOR_VERSION=0.2.0 ./build/build-debvisor.sh
This will produce an ISO named `debvisor-0.2.0-amd64.hybrid.iso`(or`debvisor-0.2.0-.hybrid.iso`if you also set`DEBVISOR_ARCH`).
### Mirror and firmware options
These toggle where packages come from and whether firmware is included:

- `DEBVISOR_MIRROR_BOOTSTRAP`- Bootstrap mirror URL (default:`[http://deb.debian.org/debian/](http://deb.debian.org/debian/)`).

- `DEBVISOR_MIRROR_BINARY`- Binary mirror URL (default:`[http://deb.debian.org/debian/](http://deb.debian.org/debian/)`).

- `DEBVISOR_FIRMWARE_CHROOT`-`true`/`false`, include firmware in chroot (default:`true`).

- `DEBVISOR_FIRMWARE_BINARY`-`true`/`false`, include firmware in binary (default:`true`).
Example overriding mirrors only:
    DEBVISOR_MIRROR_BOOTSTRAP=[http://deb.debian.org/debian/](http://deb.debian.org/debian/) \
    DEBVISOR_MIRROR_BINARY=[http://deb.debian.org/debian/](http://deb.debian.org/debian/) \
    ./build/build-debvisor.sh
### `DEBVISOR_SELFTEST`
Enable a quick self-test mode that runs configuration and preflight checks but skips the expensive ISO build.

- `0` (default): Full build (config + ISO).

- `1`: Run preflight and`lb config`, then exit before`lb build`.
Example (useful for CI):
    DEBVISOR_SELFTEST=1 ./build/build-debvisor.sh
## Helper scripts
The build script is aware of a couple of optional helper scripts:

- `build/sync-addons-playbook.sh` (optional):

- If present and executable, it is run automatically before `lb build`.

- Use this to keep the embedded Ansible addons playbook in sync.

- `build/test-firstboot.sh` (optional):

- If present and executable, the build script will print a hint after a successful build.

- Use this to run any post-build smoke tests for the `debvisor-firstboot.sh` logic.
## Output
On success, the script prints the path to the generated ISO:
    [DebVisor] Build complete: /path/to/live-image-amd64.hybrid.iso
You can then write this ISO to a USB stick using your preferred tool (e.g. `dd`,`balenaEtcher`,`Rufus`).
