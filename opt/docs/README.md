# DebVisor Documentation

DebVisor is a Debian-based, containers-first hypervisor distribution optimized for running Kubernetes and containerized workloads at the edge, with optional VM support.

## Getting Started

**New here?__Start with [__00-START.md**](00-START.md) for guided navigation, decision trees, and role-based documentation paths.

__Need a term defined?__See the [Glossary](GLOSSARY.md).

__Looking for a specific task?__Use the [Quick Reference](quick-reference.md) for common commands.

## Key Documents

| Document | Purpose |
|----------|---------|
| [00-START.md](00-START.md) |__Start here!__Navigation guide, decision trees, and role-based paths |
| [GLOSSARY.md](GLOSSARY.md) | DebVisor-specific terminology and concepts |
| [Architecture](architecture.md) | High-level system design, layers, and major components |
| [Operations](operations.md) | Day-2 operations, safety rails, and containers vs VMs guidance |
| [Profiles](profiles.md) | Storage profiles (Ceph, ZFS, mixed) and behavior |
| [Security](security.md) | Security posture, hardening, and threat model references |
| [Installation Guide](install/ISO_BUILD.md) | How to build and deploy the DebVisor ISO |
| [Networking](networking.md) | Network configuration, DNS, VLAN, and troubleshooting |
| [Workloads](workloads.md) | Container vs VM guidance with practical examples |
| [Monitoring & Automation](monitoring-automation.md) | Prometheus, Grafana, and alert automation setup |

Additional documentation covers migration/failover, RPC API design, compliance logging, developer workflows, and more.

**All documents reviewed and current as of 2025-11-26**?

## Build-time vs. first-boot vs. Ansible

At a high level:

- `config/preseed.cfg`- controls the Debian Installer experience (locale, disks, initial users, and a storage profile selector that writes`/etc/debvisor-profile`).
- `config/package-lists/` - defines which packages are baked into the DebVisor image by live-build.
- `config/hooks/` - shell hooks that run during the image build; they prepare files and defaults inside the chroot but do not replace day-2 configuration.
- Example hooks:
- `ZZ-debvisor-perms.chroot` ensures helper scripts are executable.
- `99-debvisor-firstboot-enable.chroot` installs/enables the first-boot unit.
- `config/includes.chroot/`- static files copied into the target filesystem (for example`debvisor-firstboot.sh`, systemd units, helper scripts, and base configs).
- Example includes:
- `/usr/local/sbin/debvisor-firstboot.sh` - main first-boot script.
- `/usr/local/sbin/debvisor-profile-summary.sh` - writes profile summary files.
- `/opt/debvisor/systemd/debvisor-firstboot.service` - staged unit installed by hook.
- `config/includes.installer/` - helpers used only at install time (for example profile/addon selection scripts) and not present on the running system.
- `debvisor-firstboot.sh` - the main first-boot provisioning script that turns a freshly installed node into a DebVisor hypervisor based on the chosen profile.
- At the end of the run, it calls `debvisor-profile-summary.sh`to produce`/var/log/debvisor/profile-summary.{txt,json}` for automation.
- `ansible/` - day-2 configuration, hardening, and addons, intended to be safe to re-apply as the cluster evolves.

All supported builds should go through `build/build-debvisor.sh`rather than calling live-build directly. The legacy`config/auto/config` entry point is intentionally deprecated.
