# usr/ Directory - DebVisor Operational Tools & Services

## Overview

The `usr/` directory contains runtime binaries, systemd services, and operational helper scripts deployed on DebVisor systems. This directory provides the day-2 management interface: operational CLIs, automation scripts, and system daemons that operators interact with to manage clusters, VMs, networking, and storage.

- *Key Responsibility:**Provide reliable, well-documented operational tools with comprehensive error handling, logging, and safety mechanisms.

## Directory Structure

    usr/
    +-- README.md                          # This file
    +-- local/bin/                         # Operational scripts and CLI wrappers
    |   +-- debvisor-join.sh              # Join node to cluster
    |   +-- debvisor-upgrade.sh           # Orchestrated cluster upgrades
    |   +-- debvisor-migrate.sh           # VM live migration
    |   +-- debvisor-dns-update.sh        # Dynamic DNS record updates
    |   +-- debvisor-cloudinit-iso.sh     # Generate cloud-init ISO
    |   +-- debvisor-vnc-ensure.sh        # VNC port management
    |   +-- debvisor-vnc-target.sh        # VNC target configuration
    |   +-- debvisor-vm-register.sh       # VM registration helper
    |   +-- debvisor-console-ticket.sh    # Console access token generation
    |   +-- debvisor-vm-convert.sh        # VM disk image conversion
    |   +-- debvisor-health-check.sh      # Cluster health verification
    |   +-- cephctl                       # Ceph cluster management CLI
    |   +-- hvctl                         # Hypervisor management CLI
    |   +-- k8sctl                        # Kubernetes management CLI
    |   +-- debvisor-netcfg               # Network configuration interface
    |   +-- debvisor-lib.sh               # Shared bash library (functions)
    |
    +-- lib/systemd/debvisor/             # Systemd service support files
    |   +-- debvisor-firstboot            # First-boot helper module
    |
    +-- lib/systemd/system/               # Systemd service/timer units
    |   +-- debvisor-firstboot.service    # First-boot provisioning
    |   +-- debvisor-rpcd.service         # gRPC RPC service daemon
    |   +-- debvisor-panel.service.example # Web panel service template
    |   +-- ...
    |
    +-- libexec/debvisor/                 # Helper scripts (called by services)
    |   +-- firstboot.d/                  # First-boot modules
    |   |   +-- 01-network-setup.sh       # Network initialization
    |   |   +-- 02-disk-setup.sh          # Disk/storage setup
    |   |   +-- 03-ceph-setup.sh          # Ceph cluster setup
    |   |   +-- 04-zfs-setup.sh           # ZFS pool setup
    |   |   +-- 05-docker-setup.sh        # Docker daemon setup
    |   |   +-- 06-k8s-setup.sh           # Kubernetes setup
    |   |   +-- 99-completion.sh          # Completion reporting
    |   +-- hooks/                        # Lifecycle hooks
    |       +-- libvirt-qemu.sh           # libvirt hook for VM events
    |       +-- ...
    |
    +-- share/debvisor/                   # Static data and configs
    |   +-- templates/                    # Configuration templates
    |   |   +-- compose/                  # Docker Compose templates
    |   |   +-- k8s/                      # Kubernetes manifests
    |   +-- defaults/                     # Default configuration values
    |   +-- examples/                     # Example configs
    |
    +-- share/hypervisor/                 # Hypervisor documentation
        +-- README.md                     # Quick reference guide

## Component Descriptions

### usr/local/bin/ - Operational Scripts

### General Script Improvements (applies to all)

#### Error Handling

## All scripts should have

    set -eEuo pipefail  # Exit on error, undefined vars, pipe failures

## Trap errors with context

    trap 'echo "ERROR at line $LINENO"; exit 1' ERR

## Validate preconditions

    if ! command -v ceph &> /dev/null; then
        echo "ERROR: ceph command not found"
        exit 1
    fi

## Logging & Diagnostics

- Prefix output with `[INFO]`,`[WARN]`,`[ERROR]`

- Add `--verbose` flag for detailed output

- Add `--log-file` option for capturing output

- Support `--json` for machine parsing

### Dry-Run Mode

- `--dry-run` shows what would happen without making changes

- `--check` validates prerequisites without executing

#### Documentation

- `--help` prints usage and examples

- Man pages for major tools

- Inline comments in code

- Documented preconditions and rollback procedures

#### Testing

- Unit tests via `bats` (bash test framework)

- Integration tests in containers

- CI matrix for different scenarios

- --

#### debvisor-join.sh

- *Purpose:**Join a new node to DebVisor cluster (Ceph OSDs, K8s workers, storage tiers).

### Features (Join)

- Disk discovery and provisioning

- Ceph OSD initialization

- Kubernetes node joining

- Idempotence check (node already joined)

- Pre-flight checks (network connectivity to monitors/control plane)

- Safer disk discovery (confirm user selection before provisioning)

- Ceph CRUSH map updates (proper placement, weight)

- K8s node labeling and taint verification

- Log OSD/node IDs created

- Rollback support (graceful node removal if join fails)

- Cluster health pre-check

### Usage (Join)

    debvisor-join.sh --mode=ceph          # Join as Ceph OSD
    debvisor-join.sh --mode=k8s           # Join as K8s worker
    debvisor-join.sh --dry-run            # Preview changes
    debvisor-join.sh --verbose            # Detailed output

#### debvisor-upgrade.sh

- *Purpose:**Orchestrated cluster-wide upgrades (APT packages, Ceph, Kubernetes).

### Features (Upgrade)

- APT update orchestration

- Service restarts

- Pre-upgrade validation (cluster health, no degraded PGs, K8s ready)

- Ceph noout during upgrades (protect against rebalancing)

- K8s drain verification (pods can be rescheduled)

- Rollback guidance (undo if something fails)

- Kernel upgrade handling (verify new kernel boots)

- ZFS/Ceph version compatibility checks

- `--pause` flag for manual verification points

- Detailed timing (log duration per phase)

- Log before/after cluster snapshots

### Usage (Upgrade)

    debvisor-upgrade.sh                   # Upgrade entire cluster
    debvisor-upgrade.sh --node=node1      # Upgrade single node
    debvisor-upgrade.sh --check --diff    # Preview changes
    debvisor-upgrade.sh --pause           # Pause at checkpoints

#### debvisor-migrate.sh

- *Purpose:**Live migrate VMs between hypervisor nodes (with downtime optimization).

### Features (Migrate)

- Pre-migration checks (source/target healthy, sufficient resources)

- Bandwidth rate limiting (prevent network saturation)

- Progress monitoring (% transferred, ETA)

- Rollback support (abort and recover if fails)

- Post-migration validation (runs on target, reachable)

- Downtime estimation (warn if noticeable)

- Document connection requirements (TLS/auth material)

- Support shared storage vs NAS scenarios

### Usage (Migrate)

    debvisor-migrate.sh vm-name target-node      # Migrate VM
    debvisor-migrate.sh --bandwidth=100Mbps ...  # Rate limit
    debvisor-migrate.sh --dry-run ...            # Preview

#### debvisor-dns-update.sh

- *Purpose:**Dynamic DNS record updates with TSIG authentication.

### Features (DNS)

- TSIG validation (key/secret loaded)

- DNS propagation verification (poll servers)

- TTL considerations (lower TTL before update)

- Rollback (log old values, restore if needed)

- Support multiple DNS servers (primaries + secondaries)

- DNSSEC validation

- Audit logging (changes with timestamp, operator, old/new)

### Usage (DNS)

    debvisor-dns-update.sh vm-name 192.168.1.100    # Register A record
    debvisor-dns-update.sh --ttl=300 ...            # Short TTL
    debvisor-dns-update.sh --rollback    # Rollback changes

#### debvisor-cloudinit-iso.sh

- *Purpose:**Generate cloud-init ISOs for VM provisioning.

### Features (ISO)

- Validation (user-data/meta-data syntax)

- Size constraints (warn if too large)

- Support vendor-data and network-config

- Template library (common user-data examples)

- Document ISO usage during provisioning

#### VNC & Console Tools

- *debvisor-vnc-ensure.sh:**Ensure VNC ports are listening

- Consistency checks (ports actually listening)

- Document TLS/auth options

- Security hardening

- *debvisor-vnc-target.sh:**Configure VNC targets

- Validation (VNC reachable)

- Document port assignment

- Firewall integration

- *debvisor-vm-register.sh:**Register VMs for management

- Registration validation

- Document verification steps

- *debvisor-console-ticket.sh:**Generate console access tokens

- Token verification (print token, show usage)

- TTL enforcement

- Audit logging (VM, requester, TTL)

- Support read-only vs admin tickets

- *debvisor-vm-convert.sh:**Convert VM disk formats

- Auto-detect source format

- Progress indication

- Compression options

- Integrity checks (checksums)

- Support resume for interrupted conversions

- Document performance tuning

#### Management CLIs

- *cephctl**- Ceph cluster management

    cephctl status                    # Cluster health summary
    cephctl osd list                  # OSD status with suggestions
    cephctl pool capacity             # Capacity planning
    cephctl pg balance                # PG balancing recommendations
    cephctl alerts                    # Show critical alerts

- *hvctl**- Hypervisor management

    hvctl list                        # List VMs (running, stopped)
    hvctl list --filter running       # Filter by state
    hvctl migrate vm1 node2           # Live migration
    hvctl snapshot vm1 create         # Create snapshot
    hvctl console vm1                 # Access VM console
    hvctl resources vm1               # Show CPU/RAM/I/O

- *k8sctl**- Kubernetes management

    k8sctl nodes                      # Node health & resources
    k8sctl workloads                  # Workload status
    k8sctl logs pod-name              # Pod log tailing
    k8sctl debug pod-name             # Debug pod
    k8sctl addon list                 # Available addons
    k8sctl addon enable monitoring    # Enable addon

- *debvisor-netcfg**- Network configuration

    debvisor-netcfg interactive       # Interactive TUI
    debvisor-netcfg --apply           # Apply with confirmation
    debvisor-netcfg --rollback        # Rollback to previous

#### debvisor-lib.sh - Shared Library

Reusable bash functions for all scripts:

## Logging functions

    log_info "Message"       # Info level
    log_warn "Warning"       # Warning level
    log_error "Error"        # Error level

## Error handling [2]

    die "Error message"      # Exit with error
    trap_error               # Error trap handler

## Validation

    require_bin "ceph"       # Verify binary exists
    require_env "ZFS_POOL"   # Verify env variable
    require_root             # Verify running as root

## Retry logic

    retry 3 "command"        # Retry command up to 3 times

## Output formatting

    json_output '{"key": "value"}'  # JSON output
    table_output               # Table formatting

## usr/lib/systemd/system/ - Service Units

### debvisor-firstboot.service

- *Purpose:**Run first-boot provisioning on system startup.

### Features (Firstboot)

- Runs once on first boot

- Sets up networking, storage, services

- Disables itself after completion

- `Restart=on-failure` with RetartSec=10

- TimeoutSec=3600 (prevent infinite hangs)

- Structured logging (StandardOutput=journal)

- RemainAfterExit=yes (service stays active)

- ConditionFirstBoot=yes verification

- Generate status report (`/var/log/debvisor/firstboot-report.json`)

- Pre-firstboot checks

#### debvisor-rpcd.service

- *Purpose:**gRPC RPC service daemon for API access.

### Features (RPC)

- Python-based gRPC service

- Listens on network socket

- Authentication (OAuth2, mTLS, API keys)

- Authorization (RBAC per method)

- TLS by default

- Request validation (schema, rate limiting, timeout)

- Audit logging (caller, timestamp)

- Security sandboxing (ProtectSystem=strict, etc.)

- Resource limits (memory, CPU)

- Health check endpoint

#### debvisor-panel.service.example

- *Purpose:**Web management UI service template.

### Features (Panel)

- Same security recommendations as debvisor-rpcd.service

- After=debvisor-rpcd.service dependency

- Document HTTPS/TLS certificate configuration

- Resource limits

### usr/share/hypervisor/README.md

Quick reference guide for operators.

### Features (Docs)

- Quick-reference for each helper command

- Cluster state prerequisites

- Troubleshooting section

- Architecture overview

## Operational Patterns

### Health Checking

## Quick cluster health check

    debvisor-health-check.sh

## Verbose diagnostics

    debvisor-health-check.sh --verbose

## Collect diagnostics (logs, configs)

    debvisor-health-check.sh --collect-diagnostics

## Safe Operations Pattern

## 1. Dry-run to preview

    command --dry-run

## 2. Check prerequisites

    command --check

## 3. Execute with confirmation

    command --confirm

## 4. Verify result

    command status

## 5. Rollback if needed

    command --rollback

## Maintenance Mode

## Enable maintenance mode (prevents new operations)

    debvisor-maintenance.sh enable

## Perform maintenance

## Section

## Disable maintenance mode

    debvisor-maintenance.sh disable

## Production Deployment Checklist

- [ ] Test all operational scripts in staging environment

- [ ] Verify `--help` works for all scripts

- [ ] Test `--dry-run` mode for destructive operations

- [ ] Enable and test all systemd services

- [ ] Verify logging to systemd journal

- [ ] Set up log aggregation (fluentd, logstash, etc.)

- [ ] Configure monitoring for service failures

- [ ] Create runbooks for common operations

- [ ] Document custom scripts/extensions

- [ ] Set up audit logging for state-changing operations

## Testing [2]

### Unit Tests

## Using bats (bash test framework)

    bats tests/*.bats

## Test specific script

    bats tests/debvisor-join.bats

## Integration Tests

## Full cluster operation

    docker-compose -f tests/integration.yml up

## Dry-Run Testing

## Preview without changes

    debvisor-join.sh --dry-run
    debvisor-upgrade.sh --check --diff

## Security & Safety

### Audit Logging

All operational scripts should log:

- Who (user) ran the command

- When (timestamp) it ran

- What (command, arguments) was executed

- Result (success/failure)

### Privilege Requirements

Document which scripts require sudo/special permissions:

- debvisor-join.sh: root (disk provisioning)

- debvisor-upgrade.sh: root (system updates)

- debvisor-dns-update.sh: ceph/dns group (TSIG keys)

### Rollback Procedures

Each operational script should document:

- What changes it makes

- How to undo them if something goes wrong

- Recovery procedures

## References

- [systemd Documentation](https://www.freedesktop.org/wiki/Software/systemd/)

- [Bash Strict Mode](http://redsymbol.net/articles/unofficial-bash-strict-mode/)

- [BATS Testing Framework](https://github.com/bats-core/bats-core)

## Related Documentation

- See [/etc/README.md](../etc/README.md) for system maintenance services

- See [/opt/README.md](../opt/README.md) for build and automation tools

- See [README.md](../README.md) for project overview
