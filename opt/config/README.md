# DebVisor image configuration (`config/`)

This directory contains the**image build-time**configuration used by
`build/build-debvisor.sh`and`live-build` to produce the DebVisor ISO.
It defines what is "baked into" the installer image versus what is
handled later by the first-boot provisioning script and Ansible.
In one sentence:

- `config/`+`build/` define the immutable base image;

- `debvisor-firstboot.sh` wires up a node on first boot; and

- Ansible playbooks/roles manage day-2 changes across nodes.
## Layout and responsibilities
- `preseed.cfg`

- Debian Installer preseed file controlling locale, time zone, disk
    layout, and non-interactive install defaults.

- Includes a menu to choose the DebVisor storage profile (for example
    `ceph`,`zfs`, or`mixed`), writing the selected profile to
    `/etc/debvisor-profile` on the installed system.

- Ships**no real passwords**; placeholders are intentionally blank
    and must be overridden for any production build.

- `package-lists/`

- Live-build package lists used during ISO creation.

- Decide which Debian packages are present on the installed system
    before any first-boot or Ansible automation runs (for example KVM,
    Ceph, ZFS, Docker, kubeadm/kubelet/kubectl, Cockpit, monitoring
    tooling).

- Changes here always require a**rebuild of the ISO**.

- `hooks/`

- Live-build hook scripts run inside the build chroot.

- Used for heavier build-time customization that cannot be expressed
    as simple package lists (for example seeding Kubernetes binaries,
    enabling Cockpit modules, or laying out directories).

- Hooks like `hooks/normal/040-k8s.sh` may install Kubernetes
    components unconditionally; future variants can gate this with
    environment flags such as `DEBVISOR_ENABLE_K8S` to produce
    Kubernetes-free images without editing the hook.

- `includes.chroot/`

- Files copied directly into the target filesystem of the installed
    system.

- Typical contents include:

- `usr/local/sbin/debvisor-firstboot.sh` and related helper scripts.

- Systemd unit files for first-boot, TSIG rotation, hostname
      registration, and monitoring.

- Base configuration files for Ceph, Docker/containerd, kubeadm,
      nftables, dnsmasq, and logging.

- These are**static defaults**; any configuration that must change
    across environments should ultimately be owned by Ansible or be
    explicitly overridden after install.
### Deprecated: `config/auto/config`
- The historical live-build entrypoint `config/auto/config` is kept as
  a small stub that exits with a deprecation notice.

- All supported builds must go through `build/build-debvisor.sh`, which
  wires in `preseed.cfg`,`package-lists/`, hooks, mirrors, firmware
  and self-test options.

- For more detail, see `install/ISO_BUILD.md` and the root
  `build/README` (if present).
## First-boot vs Ansible ownership
Once the image produced from `config/` is installed on a node, control
flows through two main layers:
1.**First-boot provisioning**

- `debvisor-firstboot.sh` (and its systemd unit
     `debvisor-firstboot.service`) run**once**on the first boot of an
     installed DebVisor node.

- Responsibilities include:

- Reading `/etc/debvisor-profile` and applying the chosen storage
       profile (CephFS-first, ZFS, or mixed).

- Creating core users and service accounts.

- Setting up networking (bridge `br0`, basic firewall)
       and wiring Cockpit + libvirt.

- Bootstrapping Ceph or ZFS pools and initial mounts.

- Laying down default Docker/Kubernetes configuration when
       enabled.

- The goal is to bring a single node from "freshly installed" to a
     usable, opinionated baseline.
1.**Ansible and day-2 automation**

- Playbooks and roles in `ansible/` assume a node has successfully
     completed first-boot.

- They are responsible for**cluster-wide**and**ongoing**tasks
     such as:

- Enforcing SSH MFA across many nodes.

- Rolling TSIG keys and updating DNS HA primaries/secondaries.

- Deploying monitoring stacks, VNC/noVNC consoles, and RPC
       services.

- Think of Ansible as the source of truth for configuration once a
     node is up and part of the cluster.
## What requires an ISO rebuild
As a rule of thumb:

- Changes under `config/`or`build/`**require**rebuilding the ISO.

- Changes to first-boot scripts, systemd units, or Ansible roles can
  often be rolled out to existing nodes without a reinstall (subject to
  safe re-run behavior).
When in doubt:

- If you are changing packages, filesystem layout, or installer
  behavior -> rebuild.

- If you are changing day-2 policies (firewall rules, monitoring,
  automation) -> prefer Ansible.
