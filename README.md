# DebVisor

DebVisor is a Debian?based mini hyper?converged hypervisor distro focused on:

- Virtualization (KVM/QEMU + libvirt + Cockpit)
- Storage (CephFS?first, optional ZFS, Mixed mode)
- Containers (Docker + Compose) and Kubernetes (kubeadm + containerd)
- Low?friction installer (ncurses) with minimal choices
- Automated first?boot provisioning (Ceph/ZFS/K8s/Docker/libvirt/bridge networking)

## Project Layout

    README.md                              - Overview
    DebVisor_initial.md                    - Raw brainstorming (legacy source)
    context.md                             - Session history & progress tracking
    improvements.md                        - Enhancement roadmap & completed work
    IMPROVEMENTS_SUMMARY.md                - Detailed summary of completed improvements
    docs/architecture.md                   - High level architecture & stack
    docs/core-components.md               - Packages & roles
    docs/profiles.md                      - Storage / deployment profiles
    docs/operations.md                    - Operational defaults & safeguards
    docs/network-config-tui.md            - Network Config TUI (usage & features)
    docs/install/ISO_BUILD.md             - ISO build & installer integration
    etc/README.md                         - System configuration & maintenance tasks
      etc/debvisor/                       - Blocklist validation & examples
      etc/default/                        - Service environment variables
      etc/systemd/system/                 - Systemd services & timers (Ceph, ZFS)
    opt/README.md                         - Build automation & operational infrastructure
      opt/ansible/                        - Configuration management & orchestration
      opt/build/                          - ISO building scripts
      opt/config/                         - Live-build configuration
      opt/docker/addons/                  - Container & Kubernetes addons
      opt/docs/                           - Comprehensive documentation
      opt/grafana/                        - Monitoring dashboards
      opt/monitoring/                     - Prometheus & observability
      opt/services/rpc/                   - gRPC RPC service
    usr/README.md                         - Operational tools & system services
      usr/local/bin/                      - Operational scripts & CLIs
      usr/lib/systemd/system/             - Systemd service units
      usr/libexec/                        - Helper scripts for services
      usr/share/debvisor/                 - Static data & configuration
    device/ (future hardware specific overrides)
    config/preseed.cfg                    - Debian Installer preseed (curses + profile)
    config/package-lists/debvisor.list.chroot - Live?build package manifest
    config/hooks/normal/*.sh              - Hook scripts to ensure components
    config/includes.chroot/usr/local/sbin/debvisor-firstboot.sh - First boot provisioning
    config/includes.chroot/etc/systemd/system/debvisor-firstboot.service - Systemd unit
    build/build-debvisor.sh               - One?shot ISO build script
    Makefile                              - Convenience wrapper
    tests/                                - Unit & integration tests
    .github/workflows/                    - CI/CD pipelines

## Quick Start (Build ISO)

    sudo apt update
    sudo apt install -y live-build debootstrap xorriso squashfs-tools git
    ./build/build-debvisor.sh

## Result: live-image-amd64.hybrid.iso

The `build/build-debvisor.sh` script automatically runs
`build/sync-addons-playbook.sh` before creating the ISO. This keeps
the embedded `bootstrap-addons.yml`in`config/includes.chroot` in
sync with the source Ansible playbook so that addon enablement during
first boot always matches the repository.

## Profiles

- ceph (default): All non?OS disks become Ceph OSDs; CephFS mounted at /srv/cephfs; RBD pool for VM disks
- zfs: Non?OS disks aggregated into ZFS pool `tank`; datasets for vm/docker/k8s
- mixed: CephFS for shared (RWX) + ZFS for local performance datasets

## First Boot

Systemd unit sources `/etc/debvisor-profile` (written by installer). Script provisions:

- Bridge `br0`, KVM modules, libvirt default pool
- Ceph (MON/MGR/OSD/MDS, rbd & CephFS pools) if ceph/mixed
- ZFS pool + datasets if zfs/mixed
- Docker daemon defaults
- Kubernetes single-node (Calico CNI, control-plane taint removal)
- Firewall: SSH(22), Cockpit(9090), K8s API(6443)

## Maintenance & Operations

DebVisor includes automated maintenance services for system health and longevity:

### Ceph Health Checking

-__Service:__`ceph-health.service`(oneshot) +`ceph-health.timer` (hourly)
-__Function:__Periodically checks Ceph cluster health status
-__Logs:__Systemd journal (`journalctl -u ceph-health.service`)
-__Management:__See [etc/README.md](etc/README.md) for configuration and troubleshooting

### ZFS Pool Scrubbing

-__Service:__`zfs-scrub-weekly.service`(oneshot) +`zfs-scrub-weekly.timer` (weekly, Sunday 2 AM)
-__Function:__Performs data integrity checks, detects silent corruption
-__Configuration:__`/etc/default/debvisor-zfs-scrub` (includes detailed tuning guide)
-__Timeout:__Configurable per pool size (default 2 hours, suitable for 1-10 TB pools)
-__Logs:__Systemd journal (`journalctl -u zfs-scrub-weekly.service`)

---

## [U+1F512] Supply Chain Security

DebVisor implements comprehensive software supply chain security following **SLSA Build Level 3** and industry best practices:

### Security Features

- **[U+1F50F] Cryptographic Signing**: GPG-signed release artifacts and container images
- **[U+1F4CB] Dual SBOM Formats**: CycloneDX + SPDX for maximum compatibility
- **? Policy Enforcement**: OPA/Conftest validates SBOM quality (?10 components, versions, licenses)
- **[U+1F517] Cosign Attestations**: Keyless signing with Rekor transparency log
- **[U+1F3D7]? SLSA Provenance**: Verifiable build provenance with source/tag matching
- **[U+1F6E1]? VEX Documents**: Vulnerability Exploitability eXchange for security context
- **[U+1F504] Continuous Verification**: Nightly re-verification of release integrity
- **[U+1F4CA] Predicate Digests**: Cryptographic anchors for attestation validation

### Quick Verification

```bash
# Download release
gh release download v1.0.0

# Verify GPG signature
gpg --verify debvisor-1.0.0.tar.gz.asc debvisor-1.0.0.tar.gz

# Check SHA256 checksums
sha256sum -c debvisor-1.0.0.tar.gz.sha256

# Verify container provenance
slsa-verifier verify-image ghcr.io/undefind/debvisor:1.0.0 \
  --source-uri github.com/UndiFineD/DebVisor

# Verify SBOM attestations
cosign verify-attestation --type cyclonedx ghcr.io/undefind/debvisor:1.0.0
```text

**Full Documentation**: [docs/SUPPLY_CHAIN_SECURITY.md](docs/SUPPLY_CHAIN_SECURITY.md)

---
-__Management:__See [etc/README.md](etc/README.md) for customization and monitoring

### Blocklist Management

-__Validation:__`etc/debvisor/validate-blocklists.sh` (CIDR syntax, overlap detection)
-__Integrity:__`etc/debvisor/verify-blocklist-integrity.sh` (checksums, format verification)
-__Examples:__`blocklist-example.txt`,`blocklist-whitelist-example.txt`
-__Testing:__GitHub Actions validates all blocklists on commit
-__Details:__See [etc/debvisor/](etc/debvisor/) for configuration formats and usage

### Production Deployment Checklist

- [ ] Enable maintenance timers: `systemctl enable ceph-health.timer zfs-scrub-weekly.timer`
- [ ] Configure ZFS timeout for your pool size in `/etc/default/debvisor-zfs-scrub`
- [ ] Customize timer schedules if not aligned with your maintenance window
- [ ] Set up log aggregation or alerts for service failures
- [ ] For multi-node clusters, stagger scrub schedules to prevent simultaneous I/O
- [ ] Test manual execution: `systemctl start zfs-scrub-weekly.service`
- [ ] Monitor service logs during first automated run

### Modes

- `/etc/debvisor-mode` controls behavior:
- `lab`(default): ensures`root`,`node`,`monitor` users exist (non-root locked), convenience defaults.
- `prod`: only ensures`root` user; create additional accounts via your own workflow.

### Addons

- Global config: `/etc/debvisor-addons.conf` with flags:
- `ADDON_RPC_SERVICE`,`ADDON_WEB_PANEL`,`ADDON_VNC_CONSOLE`,`ADDON_MONITORING_STACK`(`yes`/`no`).
- Profile defaults: `/etc/debvisor-addons.d/.conf` provide sensible per-profile defaults if no global file exists.
- On first boot, an Ansible playbook (`bootstrap-addons.yml`) runs locally (when present) to apply addon roles:
- `rpc-service`,`web-panel`,`vnc-console`,`monitoring-stack` (shipped as safe stubs you can extend).

### Dry Run

- You can test the first boot logic non-destructively with:
- `debvisor-firstboot.sh --dry-run`
- In dry-run mode, provisioning steps only log intended actions; no disks/users/services are modified.

## Improvements & Operational Excellence

DebVisor includes comprehensive improvements across all system components to ensure production-readiness:

### Phase 1: Documentation & Configuration (? Complete)

- Enhanced systemd unit files with timeout protection, retry logic, and security sandboxing
- Comprehensive README files for `etc/`,`opt/`, and`usr/` directories
- Production deployment checklists and troubleshooting guides
- ZFS pool sizing formulas and multi-pool configuration support
- See [SESSION_COMPLETION_REPORT.md](SESSION_COMPLETION_REPORT.md) for details

### Phase 2: Operational Scripts & CI/CD (? Complete)

-__Shared bash library__(`usr/local/bin/debvisor-lib.sh`) with 50+ reusable functions

- Consistent logging, error handling, retry logic
- Infrastructure validation (Ceph, Kubernetes, ZFS)
- Safe operation patterns (dry-run, confirm, execute)

-__Enhanced scripts__with `--dry-run`,`--check`,`--verbose` modes

- `debvisor-join.sh`: Join nodes to cluster with comprehensive validation
- `debvisor-upgrade.sh`: Orchestrated cluster upgrades with checkpoints
- Full audit logging and error recovery

-__CI/CD validation workflow__(`.github/workflows/validate-syntax.yml`)

- systemd unit validation with `systemd-analyze`
- Shell script linting with `shellcheck`
- Ansible playbook syntax checking
- Cross-component consistency validation

-__Component validator__(`opt/validate-components.sh`)

- Validates Ansible inventory, package lists, Docker addons
- Checks file permissions and executable status
- Optional auto-fix for common issues

See [PHASE_2_SUMMARY.md](PHASE_2_SUMMARY.md) for implementation details and usage examples.

### Phase 3: RPC Service & Web Panel (Planned)

- gRPC service implementation with authentication, authorization, TLS
- Web management panel with security hardening
- Integration tests and advanced monitoring

---

## Contributing

1. Propose doc changes in `docs/`
1. Use the shared library (`debvisor-lib.sh`) in new scripts for consistency
1. All scripts should support `--dry-run`,`--check`,`--verbose`,`--log-file` flags
1. Include comprehensive error handling and audit logging
1. Keep scripts idempotent and non-destructive beyond initial provisioning
1. Avoid embedding passwords/keys; rely on installer prompts & environment variables
1. Run validation before submitting: `opt/validate-components.sh`

## Roadmap (High-Level)

- Cluster expansion scripts (join additional nodes for Ceph + K8s)
- Ceph CSI & ZFS LocalPV Helm charts under `docker\addons\`
- Metrics stack (Prometheus/Grafana) profile
- Upgrade orchestration (Ansible playbooks)

## Rate Limiting

- Web Panel (Flask):
- Set a global default via `RATELIMIT_DEFAULT` in the Flask config (e.g., `"100 per minute"`).
- Use `@limiter.limit("<N> per <period>")` per route for granular control (see `opt/web/panel/routes/auth.py`).
  - Login/Register routes include per-IP and per-user limits with lightweight backoff.

- RPC Server (gRPC):
- Configure `/etc/debvisor/rpc/config.json` -> `rate_limit` block:
- `window_seconds`: sliding window duration (seconds)
  - `max_calls`: max calls per principal per method within the window
  - `method_limits`: per-method overrides, e.g.:

        {
          "rate_limit": {
            "window_seconds": 60,
            "max_calls": 120,
            "method_limits": {
              "/debvisor.StorageService/CreateSnapshot": { "window_seconds": 60, "max_calls": 30 },
              "/debvisor.StorageService/DeleteSnapshot": { "window_seconds": 60, "max_calls": 20 }
            }
          }
        }

- `method_limits_prefix`: prefix-based defaults for groups of methods, e.g.:

        {
          "rate_limit": {
            "method_limits_prefix": {
              "/debvisor.StorageService/": { "window_seconds": 60, "max_calls": 30 },
              "/debvisor.MigrationService/": { "window_seconds": 60, "max_calls": 40 }
            }
          }
        }

- `method_limits_patterns`: regex-based matching for automatic stricter limits on mutating RPCs, e.g.:

        {
          "rate_limit": {
            "method_limits_patterns": [
              { "pattern": "/debvisor\\.[A-Za-z]+Service/(Create|Delete|Update|Migrate|Plan)$", "window_seconds": 60, "max_calls": 20 }
            ]
          }
        }

- Implemented by `RateLimitingInterceptor` in `opt/services/rpc/server.py`.

## License

Apache License Version 2.0, January 2004 `license.md`
