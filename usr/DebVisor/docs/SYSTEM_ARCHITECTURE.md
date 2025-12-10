# DebVisor System Architecture: Tools & Services

This document outlines the core custom tooling and systemd services that make up the DebVisor operating system. Unlike standard Debian, DebVisor comes with a "Batteries Included" control plane designed for hyper-converged infrastructure.

## 1. Core Tooling (`/opt`)

The `/opt` directory contains the Python-based control plane that differentiates DebVisor from a generic Linux distribution.

### `dvctl` (Unified Control Plane)

**Location:** `/opt/dvctl.py`
**Purpose:** The primary CLI for administrators, designed to rival `talosctl`. It unifies management of:

- **Kubernetes**: Wraps `k8sctl` for cluster operations.
- **Storage**: Wraps `cephctl` and ZFS management.
- **Hypervisor**: Wraps `hvctl` for KVM/Libvirt VM management.
- **OS Lifecycle**: Manages A/B partition upgrades and drift detection.

### `netcfg-tui` (Day 0 Networking)

**Location:** `/opt/netcfg_tui_app.py`
**Purpose:** A text-based user interface (TUI) that launches automatically on the physical console if no network is detected.

- **Features:** Bond creation, VLAN tagging, Static IP/DHCP configuration.
- **Tech Stack:** Python `urwid` + `iproute2`.
- **Console:** Runs on `kmscon` (GPU-accelerated terminal) with UTF-8 support.

### `upgrade_manager` (A/B Updates)

**Location:** `/opt/system/upgrade_manager.py`
**Purpose:** Implements "Soft Immutability" by managing dual boot partitions (Slot A / Slot B).

- **Function:** Downloads new OS images, writes them to the inactive slot, and updates the GRUB bootloader.
- **Rollback:** Automatically reverts to the previous slot if the new version fails to boot/health-check.

### `zerotouch` (Discovery)

**Location:** `/opt/discovery/zerotouch.py`
**Purpose:** Enables automatic cluster formation without manual IP entry.

- **Tech Stack:** mDNS / Avahi (`zeroconf`).
- **Function:** Broadcasts node presence and listens for other DebVisor nodes to form a mesh.

---

## 2. Systemd Services

DebVisor uses `systemd` for service orchestration. Custom units are located in `/etc/systemd/system/`.

### `debvisor-firstboot.service`

- **Type:** `oneshot`
- **Exec:** `/usr/local/sbin/debvisor-firstboot.sh`
- **Purpose:** Runs exactly once on the very first boot of a new installation.

- Generates unique SSH host keys.
- Resizes the root filesystem to fill the disk.
  - Triggers the `netcfg-tui` if network is down.
  - Initializes the Kubernetes/Ceph cluster if configured via Preseed.

### `debvisor-rpcd.service`

- **Type:** `simple` (Daemon)
- **Purpose:** The RPC daemon that `dvctl` talks to remotely.
- **Function:** Exposes a secure gRPC/REST API for remote management of the node.

### `debvisor-panel.service`

- **Type:** `simple` (Daemon)
- **Purpose:** Serves the web-based management UI (Cockpit plugin backend).
- **Function:** Provides a lightweight web server for the "Day 0" landing page and status dashboard.

### `debvisor-backup.service` & `.timer`

- **Type:** `oneshot` (Timer triggered)
- **Purpose:** Automated configuration backup.
- **Function:** Snapshots `/etc` and critical data to a backup location (local or S3) based on schedule.

### `tsig-rotate.service` & `.timer`

- **Type:** `oneshot` (Timer triggered)
- **Purpose:** Security rotation for DNS TSIG keys.
- **Function:** Rotates the shared secrets used for secure DNS updates in the cluster.

### `kmscon` (Console Service)

- **Type:** `simple` (Daemon)
- **Purpose:** Replaces the standard `getty` (text login) on the physical screen.
- **Function:** Provides a high-resolution, GPU-accelerated terminal with full UTF-8 support, essential for the `netcfg-tui`.

---

## 3. Helper Scripts

Located in `/usr/local/bin` and `/usr/local/sbin`, these scripts glue the system together.

- `debvisor-firstboot.sh`: The heavy lifter for initialization logic.
- `validate-components.sh`: A health-check script used by the watchdog.
- `fix-runner-path.ps1`: (Dev) Fixes paths for GitHub Actions runners.
