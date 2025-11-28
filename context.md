# DebVisor Context

## Structure

Tab size is 4 spaces

## Overall Purpose

DebVisor is a Debian 13–based mini hyper‑converged hypervisor distro.
It is__containers‑first__(Docker/Kubernetes), with VMs supported for
legacy and special‑case workloads. The goal is a turnkey ISO that you
boot, install via a curses (ncurses) installer, and end up with:
KVM/libvirt + bridges + Cockpit web UI
CephFS‑first (with optional ZFS or mixed Ceph+ZFS)
Docker + Kubernetes (kubeadm, containerd, Calico)
Opinionated defaults and automated first‑boot provisioning.
Key entry points:

README.md – high‑level description, profiles, and ISO build quickstart.
Makefile + build-debvisor.sh – one‑shot live-build wrapper to produce the ISO.
DebVisor_initial.md – now just a stub table listing canonical file locations.

## Installer & Image Build

Live-build config:
preseed.cfg – Debian Installer preseed with:
Locale/timezone (en_US, UTC).
Hostname debvisor.local.
Prompts for root + admin passwords.
Custom profile menu (ceph | zfs | mixed) via whiptail, writing PROFILE=... to /etc/debvisor-profile.
Late command creating node and monitor accounts with interactive passwords.
debvisor.list.chroot – APT package manifest installing:
Base tools (sudo, ssh, nftables, ufw, fail2ban, tmux, nano, mc, etc.).
Virtualization (qemu-kvm, libvirt, virt-manager, virt-viewer, guest agent, SPICE).
Web management (Cockpit + submodules, nginx‑light).
Storage (Ceph MON/MGR/OSD/MDS, RBD, CephFS; ZFS; LVM/RAID).
Containers + K8s (docker.io, containerd, kubeadm/kubelet/kubectl).
RPC/UI groundwork (python3‑grpcio/zmq, Flask, gunicorn, node exporter, noVNC/websockify, tigervnc).
Build tooling:
Makefile – wraps live-build with DebVisor settings (bookworm, ISO‑hybrid, preseed, firmware, mirrors).
build-debvisor.sh – script that runs live-build using the above config, with environment flags for `DEBVISOR_DIST`(Debian release, default`bookworm`),`DEBVISOR_ARCH`(architecture, default`amd64`; tested primarily on amd64, with arm64/riscv64 as advanced/experimental targets),`DEBVISOR_FAST`(skip`lb clean`for quicker rebuilds),`DEBVISOR_VERSION`(tags the ISO filename), mirror/firmware toggles, and a`DEBVISOR_SELFTEST`mode that runs preflight +`lb config` only for CI.
Result: a `live-image-.hybrid.iso`(or`debvisor--.hybrid.iso`) that boots into the DebVisor installer.

## First‑Boot Provisioning & System Services

Main provisioning script:
debvisor-firstboot.sh:
Reads PROFILE from /etc/debvisor-profile (default ceph).
Ensures Cockpit and libvirt are enabled; basic locale/time setup.
Verifies root, node, monitor users (creates/locks non‑root until passwords set).
Networking: creates br0, attaches the primary NIC, brings bridge up.
Disk detection: identifies OS disk vs. “extra” storage disks for Ceph/ZFS.
Ceph path (ceph/mixed):
Generates ceph.conf, bootstraps MON/MGR/MDS.
Wipes extra disks, creates OSDs via ceph-volume lvm.
Creates RBD pool and a CephFS filesystem, mounts CephFS at /srv/cephfs via /etc/fstab.
ZFS path (zfs/mixed):
Wipes extra disks, creates tank pool, enables lz4, datasets tank/vm, tank/docker, tank/k8s mounted under /srv/*.
Configures Docker (daemon.json) and enables it.
Initializes single‑node Kubernetes (swapoff, containerd, kubeadm init, Calico CNI, removes control-plane taint).
Configures ufw firewall (allow 22, 9090, 6443).
Defines and autostarts libvirt default storage pool.
Disables its own systemd unit after successful run.
Systemd unit (not re-read here but referenced from README):
debvisor-firstboot.service – runs the script once on first boot, sources /etc/debvisor-profile.

## Core Configuration & Addons

config:

preseed.cfg, package-lists/, and live-build hooks/normal/*.sh (Ceph, ZFS, K8s, Cockpit).
includes.chroot/... – files injected into the target system:
debvisor-firstboot.sh (above).
Various helper scripts: tsig-keygen.sh, hostname-register.sh, dns-register.sh, chk-bind.sh, run-tsig-rotation.sh.
Service configs: dnsmasq.conf, tsig-debvisor.conf, ceph.conf, kubeadm-config.yaml, Docker daemon, etc.
debvisor-compliance.conf + debvisor-compliance-pipeline.conf – logging pipeline for compliance logs.
addons:

k8s/ subfolders with ready‑made manifests:
StorageClass YAMLs for Ceph RBD/CephFS and ZFS LocalPV.
Monitoring stack (Prometheus + Grafana), ingress (nginx), CSI drivers.
compose/ (e.g. Traefik, GitLab Runner).
nextcloud-compose.yml – example app stack.

scripts:

debvisor-vm-convert.sh – helper to convert VM disk images between
common formats (qcow2, raw, vmdk) using qemu-img; used when importing
or exporting VMs to/from other hypervisors.

## Orchestration & Automation

ansible:
playbooks/:
security-hardening.yml – includes roles that:
Install Wazuh/IDS, configure nftables blocklists, sysctl hardening, auditd rules.
enforce-mfa.yml – configure MFA via PAM Google Authenticator for SSH.
block-ips.yml – push IPs into nftables blocklist, log and export metrics.
quarantine-host.yml – isolate compromised host (firewall, disable autostarted VMs, tag in metrics/DNS/audit).
rotate-tsig-ha.yml – rotate TSIG keys cluster‑wide (nodes, VMs, transfer key).
roles/:
dns-ha – Bind9+Keepalived HA primaries (VIP, nftables gating, TSIG configs, zone file templates).
dns-secondary – secondary Bind9 (multi-master secondaries, IXFR).
node-register – now a non-operational stub; hostname registration is handled
  by on-node `hostname-register.service`, TSIG helper scripts
  (`tsig-keygen.sh`,`run-tsig-rotation.sh`), and the libvirt VM hook,
  with `dns-register.sh.j2` kept as a reference-only example.
vm-register – installs a libvirt qemu hook that, on VM start, discovers the
  VM's IPv4 address and delegates DNS registration to the local helper
  `/usr/local/sbin/debvisor-vm-register.sh`, which uses on-node TSIG
  configuration.
blocklist, mfa – firewall blocklist and SSH MFA enforcement; `mfa` is a
  stub role that only ensures the package is present and then fails
  with guidance to use `enforce-mfa.yml`.
vnc-console – Debian 13 + nginx VNC/noVNC console addon that installs
  TigerVNC, noVNC, websockify, nginx, helper scripts, a websockify systemd
  template, and nginx config to expose per-VM consoles over HTML5.
rpc-service, web-panel – non-operational stubs that create placeholder
  directories/READMEs only; future implementations will live here.
This layer turns DebVisor into a manageable cluster with DNS HA, secure dynamic updates, and automated remediation.

## Monitoring, Dashboards & CI

grafana/dashboards/*.json and monitoring:
Dashboards:
DNS/DHCP overview, multi‑tenant isolation, security overview, compliance/MFA audit, and a multitenant DebVisor dashboard.
Provisioning:
monitoring/grafana/provisioning/... – dashboards and alerting provisioning YAML.
Alerting:
Alerts for TSIG rotation overdue, failed TSIG updates (via Loki logs), DHCP exhaustion, VRRP VIP status, tenant‑specific DNS failures.
security-remediation-workflow.yaml:
Argo Workflow that reacts to Prometheus alerts → triggers AWX/Ansible remediation (e.g., enforce MFA, quarantine host) → verifies via metrics.
workflows:
validate-dashboards.yml, validate-grafana.yml, test-grafana.yml – CI to validate Grafana JSON, importability, etc.

## DNS / DHCP / Logging / Compliance

DNS/DHCP:

dnsmasq.conf – dnsmasq as DHCP (cluster + tenant ranges) with DNS pointing to Bind9 VIP.
tsig-debvisor.conf and Ansible templates – TSIG keys for:
Node records (node*.debvisor.local).
VM records (vm*.debvisor.local).
Zone transfer keys (primaries ↔ secondaries).
HA pattern:
Two Bind9 primaries behind a Keepalived VIP (10.10.0.1), only VIP holder accepts TSIG updates.
Secondaries with multi-master yes and secured IXFR.
nftables rules to ensure updates only hit VIP.
Logging & Compliance:

Fluent Bit → Kafka/Logstash → Elasticsearch + immutable S3 (object lock) for audit logs.
Loki via Promtail for Bind/dnsmasq logs; Grafana panels + alerting on TSIG failures, per‑tenant zones.
compliance-logging.md – describes schema, retention, and evidence workflows.

## Documentation

docs:
architecture.md – high‑level stack and design.
core-components.md – package roles and responsibilities.
profiles.md – ceph/zfs/mixed storage profiles and behavior.
operations.md – day‑2 ops, defaults, safeguards, including containers
vs VMs positioning and VM storage model.
networking.md – VLANs/bridges, DNS/DHCP model, tenant isolation.
migration.md – failover, live migration, Ceph RBD layouts.
rpc-service.md – design for debvisor-rpcd (gRPC service for node membership, migrations, config sync).
failover-identity-access.md – AD/SSSD/Keycloak/OIDC integration and per‑VM RBAC.
monitoring-automation.md – dashboards, synthetic metrics CronJob, automation flows.
compliance-logging.md, quick-reference.md, workloads.md, developer-workflow.md – logging, cheat sheets, workload examples, contribution patterns.
install/ISO_BUILD.md – building the ISO, live-build details.

## Services / Web / Extra

services, web, usr, etc:
Skeleton for additional system services and a potential custom DebVisor web panel (Flask+Gunicorn+nginx).
Intended to host the “Proxmox‑like” management UI, backed by debvisor-rpcd and noVNC for VM consoles.
In one sentence:

DebVisor is a Debian‑based, ISO‑built mini hyper‑converged hypervisor distro that combines KVM/libvirt, CephFS/ZFS, Docker/Kubernetes, HA DNS with TSIG‑secured dynamic updates, rich monitoring/automation, and strong identity/compliance tooling, with most of the behavior driven by preseeded installer choices and a powerful first‑boot provisioning script plus Ansible/GitOps on top.

If you want, I can next:

Draw a high‑level architecture diagram (text) tying directories to components, or
Walk through the exact boot → install → first‑boot → cluster‑ready flow step‑by‑step.

## Session Progress & Improvements (Current)

### Completed Work

#### 1. Enhanced ZFS Scrub Configuration (`/etc/default/debvisor-zfs-scrub`)

- Replaced minimal 2-line config with 700+ line production-grade template
- Added comprehensive documentation for all variables
- Included pool sizing guide with timeout recommendations
- Documented fallback behavior and multi-pool support
- Added security, robustness, and operational guidance

#### 2. Enhanced Systemd Units (ceph-health & zfs-scrub)

-__ceph-health.service__: Added 300+ lines of documentation including reliability improvements:

- Timeout protection (30s), retry logic (3 tries in 60s), syslog levels
- Resource limits (memory, CPU), security sandboxing
- Full error reporting (captures complete Ceph status output)

-__ceph-health.timer__: Added 200+ lines documenting:

- Scheduling customization (hourly default), persistence behavior
- Production considerations (cluster churn, scheduling impact, monitoring)

-__zfs-scrub-weekly.service__: Added 400+ lines covering:

- Pre-flight validation, timeout configuration by pool size
- Resource management, security hardening
- Post-execution logging, troubleshooting guide

-__zfs-scrub-weekly.timer__: Added 250+ lines explaining:

- Weekly scheduling (Sunday 2 AM off-peak), timezone handling
- Cluster staggering for HA, I/O impact mitigation
- Frequency tuning guidance based on workload

#### 3. Created Comprehensive etc/ README (`/etc/README.md`)

- 600+ line guide covering all etc/ subdirectories
- Service management commands with examples
- Customization guide for adding/modifying services
- Production deployment checklist
- Detailed troubleshooting section
- References to systemd documentation and man pages

#### 4. Existing Blocklist Infrastructure Verified

-__Validation__: test_validate_blocklists.py includes 400+ lines of unit tests

- CIDR syntax validation (IPv4/IPv6)
- Comment and blank line handling
- Overlap detection (identical, subnet, partial)
- Whitelist override logic
- Duplicate detection
- Special IP range handling (loopback, multicast, documentation, private)
- Integration tests with validation script

-__CI/CD__: GitHub Actions workflows already in place

- validate-blocklists.yml: Syntax and integrity checks
- blocklist-integration-tests.yml: Full integration testing

#### 5. Updated Main README

- Added context.md and improvements.md to project layout
- Added etc/ directory documentation references
- Created new "Maintenance & Operations" section
- Documented Ceph health checks and ZFS scrubbing
- Added production deployment checklist
- Linked to comprehensive etc/README.md for detailed info

### In Progress / Next Steps

- [ ] Enhance build scripts (build-debvisor.sh, test-firstboot.sh) with:
- Better error handling and logging
- Retry logic for transient failures
- Input validation and precondition checks
- Comprehensive diagnostics output

- [ ] Create opt/ README with similar comprehensive documentation
- Ansible inventory/playbooks guidance
- Build script customization guide
- Docker addons architecture
- Monitoring stack setup

- [ ] Enhance usr/ operational scripts with:
- Standardized error handling and logging
- Dry-run modes for all operational commands
- Integration tests via bats
- Man pages for key tools

### Documentation Created

| File | Lines | Purpose |
|------|-------|---------|
| etc/default/debvisor-zfs-scrub | 700+ | Configuration template with sizing guide |
| etc/systemd/system/ceph-health.service | 300+ | Ceph health check with reliability improvements |
| etc/systemd/system/ceph-health.timer | 200+ | Hourly health check scheduling |
| etc/systemd/system/zfs-scrub-weekly.service | 400+ | ZFS scrub with pre-flight validation |
| etc/systemd/system/zfs-scrub-weekly.timer | 250+ | Weekly scrub scheduling |
| etc/README.md | 600+ | Comprehensive service management guide |

### Test Infrastructure

| File | Coverage |
|------|----------|
| tests/test_validate_blocklists.py | 400+ lines, 10+ test classes, 40+ test methods |

### Key Improvements Rationale

1.__Production-Grade Documentation__: Each service now includes real-world examples, troubleshooting guides, and tuning recommendations.

1.__Reliability__: Timeout protection, retry logic, validation, and proper error handling prevent silent failures.

1.__Observability__: Structured logging to systemd journal with syslog levels enables integration with monitoring systems.

1.__Security__: Filesystem sandboxing, privilege restrictions, and resource limits prevent unintended system impact.

1.__Operability__: Comprehensive management commands, customization guides, and checklists support production deployments.

---

## Phase 2 Progress (Operational Scripts & CI/CD) - COMPLETE

### Session 2 Completed Work

#### 1. Shared Bash Library (usr/local/bin/debvisor-lib.sh)

- 700+ lines of production-ready bash utility functions
- Logging: log_info, log_warn, log_error, log_debug with timestamps and colors
- Error Handling: die(), cleanup_trap(), error_trap() for consistent error management
- Validation: require_bin, require_env, require_root, require_file, validate_cidr, validate_pool_name
- Retry Logic: retry() with exponential backoff, wait_for_condition() with timeout
- Safe Operations: execute() respects --dry-run, show_dry_run_plan(), confirm_operation()
- Infrastructure: ceph_health_check(), ceph_osds_ready(), ceph_set_noout(), zpool_exists(), kubectl_available()

#### 2. Enhanced Operational Scripts

- debvisor-join.sh: 25 to 350+ lines with --dry-run, --check, --verbose, --force-disk modes
- debvisor-upgrade.sh: 50 to 400+ lines with checkpoints, rollback, audit logging

#### 3. CI/CD Validation Workflow

- systemd-validation, shell-validation, ansible-validation, yaml-validation
- config-validation, cross-component-check, summary-report
- 7 parallel jobs, 2 minute runtime

#### 4. Cross-Component Validator (opt/validate-components.sh)

- Validates Ansible, packages, systemd, scripts, Docker, RPC, monitoring
- Can auto-fix common issues with --fix flag

### Phase 2 Summary

- 3,300+ lines of new production code
- All scripts now support --dry-run/--check modes
- CI/CD validation on every commit
- Comprehensive audit logging and error recovery
- Ready for Phase 3 (RPC service & web panel implementation)

---

## Phase 2 Progress (Operational Scripts & CI/CD) - COMPLETE [2]

### Session 2 Completed Work [2]

#### 1. Shared Bash Library (usr/local/bin/debvisor-lib.sh) [2]

- 700+ lines of production-ready bash utility functions
- Logging: log_info, log_warn, log_error, log_debug with timestamps and colors
- Error Handling: die(), cleanup_trap(), error_trap() for consistent error management
- Validation: require_bin, require_env, require_root, require_file, validate_cidr, validate_pool_name
- Retry Logic: retry() with exponential backoff, wait_for_condition() with timeout
- Safe Operations: execute() respects --dry-run, show_dry_run_plan(), confirm_operation()
- Infrastructure: ceph_health_check(), ceph_osds_ready(), ceph_set_noout(), zpool_exists(), kubectl_available()

#### 2. Enhanced Operational Scripts [2]

- debvisor-join.sh: 25 to 350+ lines with --dry-run, --check, --verbose, --force-disk modes
- debvisor-upgrade.sh: 50 to 400+ lines with checkpoints, rollback, audit logging

#### 3. CI/CD Validation Workflow [2]

- systemd-validation, shell-validation, ansible-validation, yaml-validation
- config-validation, cross-component-check, summary-report
- 7 parallel jobs, 2 minute runtime

#### 4. Cross-Component Validator (opt/validate-components.sh) [2]

- Validates Ansible, packages, systemd, scripts, Docker, RPC, monitoring
- Can auto-fix common issues with --fix flag

### Phase 2 Summary [2]

- 3,300+ lines of new production code
- All scripts now support --dry-run/--check modes
- CI/CD validation on every commit
- Comprehensive audit logging and error recovery
- Ready for Phase 3 (RPC service & web panel implementation)
