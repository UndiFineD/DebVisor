# DebVisor vs. Talos Linux: Strategic Roadmap

## Core Philosophy: Why DebVisor?

While **Talos Linux** is the gold standard for *Kubernetes-only, immutable infrastructure*, **DebVisor** aims to be the superior choice for **Hyper-Converged Infrastructure (HCI)** at the Edge and SME datacenter.

**Talos wins at:**

-   Pure Kubernetes clusters.
-   Stateless, immutable nodes.
-   Massive scale (1000+ nodes).

**DebVisor wins at:**

-   **Hybrid Workloads:** Running legacy VMs (Windows, Monoliths) alongside K8s containers.
-   **"Batteries Included" Storage:** Native ZFS/Ceph without needing a bootstrap cluster.
-   **Day 0 Usability:** TUI-based setup for technicians without a bootstrap machine.
-   **Hardware Intimacy:** Direct access to hardware for pass-through (GPU, USB, PCI) which is harder in purely API-driven OSes.

---

## Strategic Pillars to Outperform Talos

### 1. The "Unified Control Plane" (dvctl)

Talos has `talosctl` for the OS and `kubectl` for the cluster. DebVisor currently has fragmented scripts (`k8sctl`, `cephctl`, `hvctl`).
**Goal:** A single CLI (`dvctl`) that manages the *entire* stack: Hardware -> OS -> Storage -> Hypervisor -> Kubernetes.

### 2. "Soft" Immutability

Talos is immutable by default. DebVisor is mutable Debian.
**Goal:** Implement **Config Drift Detection**.

-   Use Ansible to enforce state every 15 minutes.
-   Alert on any file change in `/etc` that wasn't triggered by the controller.
-   *Future:* Offer an A/B partition update scheme (like OSTree) for the base OS.

### 3. Native Storage Supremacy

Talos relies on Rook/Longhorn running *inside* K8s. This creates a "chicken-and-egg" problem for cluster storage.
**Goal:** DebVisor provisions Ceph/ZFS *at the host level*.

-   K8s consumes it via CSI, but the storage layer survives K8s crashes.
-   VMs consume it directly via libvirt (faster than KubeVirt CSI).

### 4. The "Air-Gap" Advantage

Talos relies heavily on pulling images.
**Goal:** DebVisor ISOs should be fully self-contained.

-   Bundle all container images, debs, and helm charts.
-   Perfect for Defense, Space (NASA/ESA), and Maritime use cases.

---

## Feature Comparison Matrix

| Feature | Talos Linux | DebVisor (Target State) |
| :--- | :--- | :--- |
| **OS Architecture** | Immutable, API-only | Mutable (Managed), Hybrid |
| **Management** | `talosctl` (gRPC) | `dvctl` (Unified CLI + TUI) |
| **Workloads** | Kubernetes Only | **K8s + Native VMs (KVM)** |
| **Storage** | External / Rook (In-Cluster) | **Native ZFS/Ceph (Host-Level)** |
| **Access** | API Only (No SSH) | SSH + TUI + API |
| **Day 0 Setup** | Config file injection | **Interactive TUI / Preseed** |
| **Observability** | Metrics endpoint | **Built-in Prometheus/Grafana Stack** |

---

## Implementation Plan

### Phase 1: Unification (Current)

- [x] Create `dvctl` to wrap `k8sctl`, `cephctl`, `hvctl`.
- [x] Implement "Drift Detection" workflow.

### Phase 2: Hardening

- [x] Implement A/B partition updates for OS upgrades.
- [x] Lock down SSH (MFA/Key-only) by default.

### Phase 3: The "Edge" Experience

- [x] "Zero-Touch" clustering via mDNS/Avahi discovery.
- [x] Web-based "Cockpit" plugin for full cluster management.

### Phase 4: Day 0 Experience Refinement

- [x] **High-Performance Console**: Use `kmscon` with `fonts-terminus` to ensure a rich, UTF-8 capable TUI on the physical console, replacing the legacy VGA console.
- [x] **Interactive Network TUI**: Implemented `netcfg-tui` with `urwid` to allow IP/Gateway configuration on the physical console.
- [x] Interface List with Status Indicators
- [x] Edit Dialog for IP/Mask/Gateway
  - [x] Backend Integration (iproute2)
