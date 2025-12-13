# DebVisor

DebVisor is a Debian-based mini hyper-converged hypervisor distro focused on:

- Virtualization (KVM/QEMU, libvirt, Cockpit)
- Storage (CephFS-first, optional ZFS, mixed mode)
- Containers (Docker + Compose) and Kubernetes (kubeadm + containerd)
- Low-friction ncurses installer with minimal choices
- Automated first-boot provisioning (Ceph/ZFS/K8s/Docker/libvirt/bridge networking)

## Project Layout

- README.md — Overview
- context.md — Session history and progress tracking
- improvements.md — Enhancement roadmap and completed work
- docs/ — Architecture, operations, profiles, install guides, TUI docs
- etc/ — System configuration, blocklists, service defaults, systemd units
- opt/ — Build automation, addons, observability, services, installer assets
- usr/ — Operational tools, service units, helpers
- build/ — ISO build scripts and hooks
- tests/ — Unit, integration, and validation
- .github/workflows/ — CI/CD pipelines

## Enterprise Features

- Multi-cluster management with failover and federation
- Advanced network configuration via `netcfg-tui` with rollback support
- Plugin architecture for custom storage, network, or monitoring providers
- End-to-end testing framework for deployments and upgrades
- ADRs and operational playbooks for production readiness

## Quick Start (Build ISO)

```bash
sudo apt update
sudo apt install -y live-build debootstrap xorriso squashfs-tools git
./build/build-debvisor.sh
```

## Result: live-image-amd64.hybrid.iso

The build script runs `build/sync-addons-playbook.sh` before creating the ISO so
`bootstrap-addons.yml` in `config/includes.chroot` stays in sync with the source
Ansible playbook.

## Developer Tasks (Docs/Lint)

- Activate the virtual environment, then run linters and fixers locally.
- Keep markdown formatting consistent to avoid CI failures.
- See improvements.md for more context and metrics.

```powershell
# Activate venv (PowerShell)
./.venv/Scripts/Activate.ps1

# Fix a single Markdown file
& ./.venv/Scripts/python.exe ./fix_markdown_lint.py ./docs/CONTRIBUTING.md

# Run full markdown lint scan
& ./.venv/Scripts/python.exe -m pymarkdown scan .

# Run fixer unit tests
& ./.venv/Scripts/python.exe ./scripts/test_fix_markdown_lint.py
```

## Profiles

- ceph (default): All non-OS disks become Ceph OSDs; CephFS at /srv/cephfs; RBD
  pool for VM disks
- zfs: Non-OS disks aggregated into ZFS pool `tank`; datasets for VM, Docker, and
  K8s
- mixed: CephFS for shared (RWX) plus ZFS for local performance datasets

## First Boot

The first-boot unit reads `/etc/debvisor-profile` (written by the installer) and
provisions:

- Bridge `br0`, KVM modules, libvirt default pool
- Ceph (MON/MGR/OSD/MDS, RBD and CephFS pools) if ceph or mixed
- ZFS pool and datasets if zfs or mixed
- Docker daemon defaults
- Kubernetes single-node (Calico CNI, control-plane taint removal)
- Firewall: SSH (22), Cockpit (9090), K8s API (6443)

## Maintenance and Operations

### Ceph Health Checking

- Service: `ceph-health.service` (oneshot) and `ceph-health.timer` (hourly)
- Logs: `journalctl -u ceph-health.service`
- Management: see etc/README.md

### ZFS Pool Scrubbing

- Service: `zfs-scrub-weekly.service` (oneshot) and `zfs-scrub-weekly.timer`
  (weekly, Sunday 2 AM)
- Config: `/etc/default/debvisor-zfs-scrub`
- Logs: `journalctl -u zfs-scrub-weekly.service`

## Supply Chain Security

### Security Features

- GPG-signed release artifacts and container images
- Dual SBOM formats (CycloneDX and SPDX) with policy enforcement
- Cosign attestations (keyless) with Rekor transparency log
- SLSA provenance with source and tag matching
- VEX documents for vulnerability context
- Continuous verification with nightly re-validation

### Quick Verification

```bash
# Download release
gh release download v1.0.0

# Verify GPG signature
gpg --verify debvisor-1.0.0.tar.gz.asc debvisor-1.0.0.tar.gz

# Check SHA256 checksums
sha256sum -c debvisor-1.0.0.tar.gz.sha256

# Verify container provenance
slsa-verifier verify-image ghcr.io/undefind/debvisor:1.0.0 --source-uri \
  github.com/UndiFineD/DebVisor

# Verify SBOM attestations
cosign verify-attestation --type cyclonedx ghcr.io/undefind/debvisor:1.0.0
```

## Network Configuration

- Management: see etc/README.md for customization and monitoring.

### Blocklist Management

- Validation: `etc/debvisor/validate-blocklists.sh` (CIDR syntax and overlap
  detection)
- Integrity: `etc/debvisor/verify-blocklist-integrity.sh` (checksums and format
  verification)
- Examples: `blocklist-example.txt`, `blocklist-whitelist-example.txt`
- Testing: GitHub Actions validates all blocklists on commit

### Production Deployment Checklist

- [ ] Enable maintenance timers: `systemctl enable ceph-health.timer
  zfs-scrub-weekly.timer`
- [ ] Configure ZFS timeout for your pool size in `/etc/default/debvisor-zfs-scrub`
- [ ] Align timer schedules with maintenance windows
- [ ] Set up log aggregation or alerts for service failures
- [ ] Stagger scrub schedules across nodes
- [ ] Test manual run: `systemctl start zfs-scrub-weekly.service`
- [ ] Monitor logs during the first automated run

## Modes

- `lab` (default): ensures `root`, `node`, and `monitor` users exist (non-root
  locked), convenience defaults
- `prod`: only ensures `root`; create other accounts via your workflow

## Addons

- Global config: `/etc/debvisor-addons.conf` with flags `ADDON_RPC_SERVICE`,
  `ADDON_WEB_PANEL`, `ADDON_VNC_CONSOLE`, `ADDON_MONITORING_STACK`
- Profile defaults: `/etc/debvisor-addons.d/*.conf`
- First boot runs `bootstrap-addons.yml` locally to apply addon roles

## Dry Run

Run `debvisor-firstboot.sh --dry-run` to log intended actions without modifying
users, disks, or services.

## Improvements and Operational Excellence

- Phase 1 (Complete): Documentation and configuration hardening; systemd units,
  directory READMEs, deployment checklists, ZFS sizing guidance
- Phase 2 (Complete): Shared bash library, validation scripts, CI workflow
  `.github/workflows/validate-syntax.yml`, component validator
  `opt/validate-components.sh`
- Phase 3 (Planned): gRPC service, web panel with hardening, integration tests,
  advanced monitoring

## Contributing

- Propose doc changes in docs/
- Use the shared library `debvisor-lib.sh` in new scripts
- Support `--dry-run`, `--check`, `--verbose`, and `--log-file` flags
- Include robust error handling and audit logging
- Keep scripts idempotent and non-destructive
- Run validation before submitting: `opt/validate-components.sh`

## Roadmap (High Level)

- Cluster expansion scripts (Ceph and Kubernetes)
- Ceph CSI and ZFS LocalPV Helm charts under docker/addons/
- Metrics stack (Prometheus and Grafana)
- Upgrade orchestration (Ansible playbooks)

## Rate Limiting

- Web Panel (Flask): set `RATELIMIT_DEFAULT` and use `@limiter.limit` per route
- RPC Server (gRPC): configure rate limits in `/etc/debvisor/rpc/config.json`;
  implemented by `RateLimitingInterceptor` in `opt/services/rpc/server.py`

## License

Apache License Version 2.0, January 2004 — see license.md.

## Monitoring

- Dashboards: see docs/monitoring-health-detail.md for Prometheus and Grafana
  setup using `/health/detail`
- Metrics: expose Prometheus metrics at `/metrics`
