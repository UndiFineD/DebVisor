# ISO Build & Installer Integration

## Build Host Prerequisites

A recent Debian-based build host is recommended; ideally match the target release (default: bookworm).

    sudo apt update
    sudo apt install -y live-build debootstrap xorriso squashfs-tools git

## Live-Build Configuration

Defined via `build/build-debvisor.sh`and`config/auto/config` (script form). Key flags:

- `--distribution bookworm`
- Hybrid ISO (`--binary-images iso-hybrid`)
- Installer integration (`--debian-installer live`)
- Firmware enabled (`--firmware-chroot true --firmware-binary true`)

## Package Manifest

Located at `config/package-lists/debvisor.list.chroot` - single source of truth for included packages.

- Core hypervisor, storage, and Kubernetes components are enabled by default.
- Optional stacks (RPC service, web panel, VNC console, monitoring) are present but commented out and are installed via addons rather than baked into the ISO.

## Installer Preseed

`config/preseed.cfg` is intentionally thin. It seeds locale, hostname, disk recipe, and invokes a curses profile menu:

- Writes profile choice to `/target/etc/debvisor-profile`(`ceph`,`zfs`, or`mixed`).
- Keeps OS on first disk; remaining disks are left untouched for first-boot provisioning.
- No complex late-commands; all smart logic happens at first boot.

For safety:

- Any placeholder or lab-only passwords in `preseed.cfg`**must**be

   overridden for real deployments. Treat the shipped file as an
   example, not production-ready credentials.

- For environments that require unattended installs, prefer keeping

   secrets in a private include file (for example
   `config/preseed.private.cfg` ignored by Git) and sourcing it from
   the main preseed, or inject sensitive values via CI at build time
   rather than committing them into this repository.

## Hooks

Placed under `config/hooks/normal/*.sh` (executed inside chroot build):

- Ensure ZFS DKMS builds
- Preinstall Ceph stack
- Preinstall Kubernetes components
- Cockpit console modules

## First Boot Provisioning

Systemd unit: `debvisor-firstboot.service`
Script: `debvisor-firstboot.sh`

Behavior:

1. Loads profile from `/etc/debvisor-profile` (ceph|zfs|mixed).
1. Loads mode from `/etc/debvisor-mode`(`lab`or`prod`, default`lab`).
1. Initializes logging under `/var/log/debvisor/*.status` (ceph, zfs, kubernetes, addons, etc.).
1. Ensures base services (cockpit, libvirtd, KVM modules) and locale/time.
1. Creates accounts depending on mode:

- `lab`: ensures`root`,`node`,`monitor` exist; non-root accounts are locked by default.
- `prod`: only ensures`root`; additional accounts are left to your workflow.

1. Configures bridge networking and libvirt default storage.
1. Detects disks; reserves first disk for OS; treats others as candidate storage disks.
1. Provisioning is idempotent and guarded:

- Ceph: skipped if `ceph status` already works; avoids wiping disks with existing data.
- ZFS: skipped if `zpool list tank` succeeds; avoids wiping disks with existing data.
- Kubernetes: skipped if `/etc/kubernetes/admin.conf` already exists.

1. Configures Docker, initializes single-node Kubernetes + Calico, and applies ufw firewall rules (logging the active mode).
1. Runs addons via Ansible (see below) and disables the first-boot service.

If any major step fails, a corresponding `*.status`marker under`/var/log/debvisor/`is set to`failed` for easy diagnosis.

## Addons and Modes

-**Mode control**: `/etc/debvisor-mode`

- `lab`(default): convenience defaults, auto-create`node`/`monitor` users (locked), suitable for labs.
- `prod`: minimal user changes; better suited for hardened environments.

-**Addons config**:

- Global flag file: `/etc/debvisor-addons.conf` with keys:
- `ADDON_RPC_SERVICE`,`ADDON_WEB_PANEL`,`ADDON_VNC_CONSOLE`,`ADDON_MONITORING_STACK`(`yes`/`no`).
- Profile defaults: `/etc/debvisor-addons.d/.conf`(e.g.`ceph.conf`,`zfs.conf`,`mixed.conf`).
- On first boot, if `/etc/debvisor-addons.conf`is missing, a profile default is copied from`/etc/debvisor-addons.d/` when available.

-**Addons execution**:

- Ansible playbook: `ansible/playbooks/bootstrap-addons.yml`(mirrored into the image at`/usr/local/share/debvisor/ansible/bootstrap-addons.yml`).
- First boot will run this playbook locally (if Ansible and the playbook are present), which conditionally applies roles:
- `rpc-service`,`web-panel`,`vnc-console`,`monitoring-stack`.
- Roles currently ship as stubs that create `/opt/debvisor-*/` placeholders and README notes; extend them to deploy real services.

## Build Flow

    ./build/build-debvisor.sh   # cleans, configures, builds
    ls -lh live-image-amd64.hybrid.iso

As part of the build, `build/build-debvisor.sh` runs
`build/sync-addons-playbook.sh` to mirror
`ansible/playbooks/bootstrap-addons.yml` into
`config/includes.chroot/usr/local/share/debvisor/ansible/`. This keeps
the in-image addons playbook aligned with the repository version
without requiring manual copies.

## Test Flow (VM or Bare Metal)

1. Boot ISO
1. Follow minimal installer prompts (locale, passwords, profile)
1. Reboot -> first boot provisioning executes
1. Validate:

- Cockpit: <<<<<<https://host:9090>->>>>> `ceph -s` healthy (ceph/mixed)
- `zpool status` (zfs/mixed)
- `kubectl get nodes` Ready

## Extending

- Add Helm charts under `docker\addons\`
- Add cluster join script under `scripts/`
- Pin versions via custom APT repo file under `config/includes.chroot/etc/apt/sources.list.d/`
- Use `/etc/debvisor-addons.conf` and addons roles to introduce new optional stacks without changing the ISO package list.

## Troubleshooting

- Inspect build logs: `live-build.log`
- Chroot failures: verify hook script shebangs and executable bit
- Missing modules: confirm kernel flavor matches architecture (`amd64`)
