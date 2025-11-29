# opt/ Directory - DebVisor Operational Workspace

## Overview

The `opt/` directory contains the core operational infrastructure for DebVisor, including build automation, Ansible orchestration, monitoring configuration, Docker addon definitions, and supporting tools. This directory transforms DebVisor from a single-node appliance into a deployable, manageable, and monitorable infrastructure platform.

__Key Responsibility:__Provide production-grade tooling for deployment, configuration management, monitoring, and lifecycle operations.

## Directory Structure

    opt/
    +-- README.md                          # This file
    +-- ansible/                           # Configuration management & orchestration
    |   +-- inventory.example              # Host inventory template
    |   +-- inventory                      # Actual inventory (not in git)
    |   +-- playbooks/                     # High-level orchestration playbooks
    |   |   +-- security-hardening.yml     # Security posture enforcement
    |   |   +-- enforce-mfa.yml            # SSH MFA configuration
    |   |   +-- block-ips.yml              # Dynamic IP blocklist management
    |   |   +-- quarantine-host.yml        # Host isolation (security response)
    |   |   +-- rotate-tsig-ha.yml         # TSIG key rotation (HA DNS)
    |   +-- roles/                         # Reusable Ansible roles
    |       +-- dns-ha/                    # Bind9+Keepalived HA DNS
    |       +-- dns-secondary/             # Secondary Bind9 servers
    |       +-- node-register/             # Node registration (stub)
    |       +-- vm-register/               # VM dynamic DNS registration
    |       +-- blocklist/                 # Firewall blocklist management
    |       +-- mfa/                       # SSH MFA setup (stub)
    |       +-- vnc-console/               # noVNC web console addon
    |       +-- rpc-service/               # gRPC RPC service (stub)
    |       +-- web-panel/                 # Web management UI (stub)
    |
    +-- argocd/                            # Kubernetes automation workflows
    |   +-- security-remediation-workflow.yaml # Alert -> remediation pipeline
    |
    +-- build/                             # ISO build and testing scripts
    |   +-- build-debvisor.sh              # Main ISO build script
    |   +-- sync-addons-playbook.sh        # Sync Ansible addons into ISO
    |   +-- test-firstboot.sh              # First-boot provisioning tests
    |   +-- test-profile-summary.sh        # Profile validation tests
    |
    +-- config/                            # Live-build configuration
    |   +-- preseed.cfg                    # Debian Installer preseed
    |   +-- package-lists/                 # APT package manifests
    |   |   +-- base.list                  # Base system packages
    |   |   +-- ceph.list                  # Ceph storage packages
    |   |   +-- zfs.list                   # ZFS storage packages
    |   |   +-- k8s.list                   # Kubernetes packages
    |   |   +-- docker.list                # Docker/container packages
    |   |   +-- virtualization.list        # KVM/libvirt packages
    |   |   +-- monitoring.list            # Prometheus/Grafana packages
    |   +-- hooks/                         # Live-build hook scripts
    |   |   +-- normal/                    # Normal phase hooks (executed)
    |   |   +-- ...
    |   +-- includes.chroot/               # Files injected into ISO
    |   |   +-- etc/                       # System configuration files
    |   |   +-- usr/                       # User binaries and libraries
    |   |   +-- ...
    |   +-- includes.installer/            # Debian Installer files
    |
    +-- docker/                            # Container addon definitions
    |   +-- addons/                        # Addon packages
    |   |   +-- compose/                   # Docker Compose applications
    |   |   |   +-- traefik-compose.yml    # Reverse proxy
    |   |   |   +-- gitlab-runner-compose.yml # CI/CD runner
    |   |   +-- k8s/                       # Kubernetes manifests
    |   |       +-- storage-classes/       # Storage (Ceph, ZFS)
    |   |       +-- monitoring/            # Prometheus, Grafana
    |   |       +-- networking/            # Ingress, CNI
    |   |       +-- system/                # Essential services
    |   +-- README.md                      # Addon architecture guide
    |
    +-- docs/                              # Project documentation
    |   +-- index.md                       # Documentation entry point
    |   +-- GLOSSARY.md                    # DebVisor terminology
    |   +-- architecture.md                # System design & components
    |   +-- core-components.md             # Package roles & responsibilities
    |   +-- profiles.md                    # Storage profiles (ceph/zfs/mixed)
    |   +-- operations.md                  # Day-2 operations & defaults
    |   +-- networking.md                  # Network configuration
    |   +-- migration.md                   # Failover & live migration
    |   +-- rpc-service.md                 # gRPC service design
    |   +-- failover-identity-access.md    # AD/SSSD/Keycloak integration
    |   +-- monitoring-automation.md       # Dashboards & automation
    |   +-- compliance-logging.md          # Audit trail & evidence
    |   +-- quick-reference.md             # Cheat sheet
    |   +-- workloads.md                   # Example workload configs
    |   +-- developer-workflow.md           # Contributing & development
    |   +-- install/                       # Installation guides
    |       +-- ISO_BUILD.md               # Building the ISO
    |
    +-- grafana/                           # Monitoring dashboards
    |   +-- dashboards/                    # Grafana JSON dashboards
    |   |   +-- overview.json              # System overview
    |   |   +-- dns-dhcp.json              # DNS/DHCP monitoring
    |   |   +-- security.json              # Security metrics
    |   |   +-- compliance.json            # Compliance audit
    |   |   +-- ceph.json                  # Ceph cluster metrics
    |   +-- provisioning/                  # Grafana provisioning configs
    |       +-- datasources/               # Prometheus, Loki, etc.
    |       +-- alerting/                  # Alert rules
    |       +-- notification-channels/     # Email, Slack, etc.
    |
    +-- monitoring/                        # Prometheus & observability
    |   +-- fixtures/                      # Test metrics & synthetic data
    |   |   +-- generator/                 # Metrics generator
    |   |   +-- *-ConfigMap.yaml           # Test data ConfigMaps
    |   |   +-- *-Deployment.yaml          # Test generators
    |   +-- prometheus/                    # Prometheus configuration
    |   |   +-- prometheus.yml             # Scrape configs
    |   |   +-- rules/                     # Recording & alerting rules
    |   |   +-- alerts/                    # Prometheus AlertManager configs
    |   +-- loki/                          # Loki log aggregation
    |       +-- loki-config.yaml           # Loki scrape configs
    |       +-- ...
    |
    +-- netcfg-tui/                        # Network configuration TUI
    |   +-- README.md                      # Usage guide
    |   +-- netcfg_tui.py                  # Python TUI application
    |   +-- ...
    |
    +-- services/
        +-- rpc/                           # gRPC RPC service
            +-- proto/                     # Protocol Buffer definitions
            |   +-- debvisor.proto         # RPC API schema
            |   +-- Makefile               # Proto compilation
            +-- Makefile                   # Build & testing
            +-- ...

## Component Descriptions

### ansible/ - Configuration Management

__Purpose:__Deploy, configure, and manage DebVisor clusters using Ansible playbooks and roles.

#### Inventory Management

### inventory.example

- Template showing expected host groups and variables
- Groups: `dns_primaries`,`dns_secondaries`,`ceph_mons`,`ceph_osds`,`k8s_controlplane`,`k8s_workers`
- Required variables per role (documented in file)

### inventory (not in git)

- Actual deployment inventory for your environment
- Should match inventory.example structure
- Sensitive data (passwords, API keys) stored in separate vault file

### Improvements to implement

- Convert to YAML format for better validation and templating
- Add `ansible-inventory --list` CI validation
- Document required variables per role
- Provide environment-specific examples (lab, prod, cluster)

#### Playbooks

### Key Playbooks

1.__security-hardening.yml__

- Installs Wazuh/IDS, configures nftables blocklists
- Applies sysctl hardening, auditd rules
- Enforces SELinux/AppArmor policies
- *Improvements:* Add check/diff modes, idempotence guarantees

1.__enforce-mfa.yml__

- Configures SSH MFA via PAM Google Authenticator
- Integrates with LDAP/AD if configured
- *Improvements:* Add rollback support, testing in CI

1.__block-ips.yml__

- Pushes IPs into nftables blocklist
- Logs and exports metrics for monitoring
- *Improvements:* Add dry-run, whitelist management, rate limiting

1.__quarantine-host.yml__

- Isolates compromised host (network, services)
- Disables autostarted VMs, tags in metrics/DNS
- *Improvements:* Add audit logging, emergency restore procedures

1.__rotate-tsig-ha.yml__

- Rotates TSIG keys cluster-wide (nodes, VMs, transfer key)
- *Improvements:* Add check/diff mode, rollback, audit logging

#### Roles

| Role | Purpose | Status | Improvements Needed |
|------|---------|--------|---------------------|
| dns-ha | Bind9+Keepalived HA primaries | Production | Document VIP setup, failover testing |
| dns-secondary | Secondary Bind9 servers | Production | Multi-master IXFR, zone validation |
| node-register | Node hostname registration | Stub | Integrate with on-node services |
| vm-register | VM dynamic DNS via libvirt hook | Production | Add IPv6, DNSSEC validation |
| blocklist | Firewall blocklist management | Production | Add granular rules, performance tuning |
| mfa | SSH MFA via PAM | Stub | Implement full MFA pipeline |
| vnc-console | noVNC web console addon | Production | Add TLS, websockify optimization |
| rpc-service | gRPC RPC service | Stub | Implement authentication, RBAC |
| web-panel | Web management UI | Stub | Implement full UI, backend integration |

### Usage Examples

## Run security hardening on all hosts

    ansible-playbook opt/ansible/playbooks/security-hardening.yml -i inventory

## Apply MFA enforcement to SSH servers

    ansible-playbook opt/ansible/playbooks/enforce-mfa.yml \
      -i inventory \
      -l ssh_servers \
      --tags ssh-mfa

## Dry-run: preview changes before applying

    ansible-playbook opt/ansible/playbooks/rotate-tsig-ha.yml \
      -i inventory \
      --check --diff

## build/ - ISO Building

__Purpose:__Automate ISO creation for DebVisor deployments.

### build-debvisor.sh

Main build script orchestrating live-build.

### Current Features

- Environment variable configuration (DEBVISOR_DIST, DEBVISOR_ARCH, DEBVISOR_VERSION)
- Mirror/firmware toggles
- Preseed and package list integration
- Addon synchronization (sync-addons-playbook.sh)
- ISO hybrid creation

### Improvements to implement [2]

- Add comprehensive logging (timestamp, severity levels)
- Add `--verbose` flag for detailed output
- Add mirror fallback if primary unavailable
- Add SHA256 checksum verification
- Preserve build artifacts on failure (for debugging)
- Add CI matrix for amd64, arm64, multiple Debian releases
- Add post-build smoke tests (mount, verify files)
- Create `.env.example` with all variables

#### sync-addons-playbook.sh

Synchronizes Ansible addons into ISO before building.

### Improvements to implement [3]

- Add error handling for missing source files
- Add `--dry-run` mode to preview changes
- Add checksumming (skip if identical)
- Document addon discovery process

#### test-firstboot.sh

Tests first-boot provisioning script.

### Improvements to implement [4]

- Expand test coverage (syntax + execution)
- Add tests for different Debian releases
- Add checks for required binaries (zfs, ceph, kubeadm)
- Generate JUnit test reports for CI

#### test-profile-summary.sh

Validates profile configuration.

### Improvements to implement [5]

- Document what is validated
- Add detailed error messages
- Add supported profile list output

### config/ - Live-Build Configuration

__Purpose:__Configure live-build to produce DebVisor ISO with all components.

#### preseed.cfg

Debian Installer preseeding for automated installation.

### Current Features [2]

- Locale/timezone/hostname
- Root + admin password prompts
- Profile selection menu (ceph/zfs/mixed)
- User account creation

### Improvements to implement [6]

- Add NTP/time synchronization settings
- Add language/locale selection options
- Document profile-specific vs universal settings
- Add inline comments explaining sections
- Review password/secret handling (no hardcoding)

#### package-lists/

APT package manifests for different component groups.

### Files

- base.list: Core system packages
- ceph.list: Ceph MON/MGR/OSD/MDS/RBD/CephFS
- zfs.list: ZFS storage
- k8s.list: Kubernetes (kubeadm/kubelet/kubectl)
- docker.list: Docker/containerd/compose
- virtualization.list: KVM/libvirt/virt-manager
- monitoring.list: Prometheus/Grafana/exporters

### Improvements to implement [7]

- Document purpose of each list file
- Add package validation CI: verify availability in target Debian
- Document conditional packages (profile-specific)
- Add size/security audit notes for high-impact packages

#### hooks/

Live-build hook scripts executed during ISO building.

### Improvements to implement [8]

- Document lifecycle: early, normal, late phases
- Add shellcheck linting in CI
- Add logging: each hook logs progress
- Document inter-hook dependencies

#### includes.chroot/ and includes.installer/

Files injected into ISO (system config, scripts, manifests).

### Improvements to implement [9]

- Create manifest of all files (ownership, purposes)
- Add CI validation: verify referenced files exist
- Document which files modified on first-boot vs at build time

### docker/addons/ - Container Addons

__Purpose:__Provide pre-built Docker Compose applications and Kubernetes manifests as optional addons.

#### compose/

Docker Compose application definitions.

### Examples

- Traefik reverse proxy
- GitLab Runner for CI/CD
- Custom application stacks

#### k8s/

Kubernetes manifests and addons.

### Categories

- storage-classes/: Ceph RBD, CephFS, ZFS LocalPV
- monitoring/: Prometheus, Grafana, node-exporter
- networking/: nginx-ingress, Calico CNI
- system/: Essential Kubernetes services

### Improvements to implement [10]

- Create `docker/README.md` explaining addon architecture
- Document addon metadata format (addon.yaml)
- Add CI validation: syntax, required fields, dependency consistency
- Support selective addon deployment (K8s-only, Ceph-only)

### docs/ - Documentation

__Purpose:__Comprehensive documentation for operators, developers, and users.

#### Documentation Structure

### Entry Points

- index.md: Main documentation index
- GLOSSARY.md: DebVisor-specific terminology
- quick-reference.md: Cheat sheet for common tasks

### Core Documentation

- architecture.md: System design, component interaction
- core-components.md: Package roles, responsibilities
- profiles.md: Storage profiles and behavior
- operations.md: Day-2 operations, defaults, safeguards

### Specialized Documentation

- networking.md: VLANs, bridges, tenant isolation
- migration.md: Failover, live migration, RBD layouts
- rpc-service.md: gRPC service architecture
- failover-identity-access.md: AD/SSSD/Keycloak integration
- monitoring-automation.md: Dashboards, automation flows
- compliance-logging.md: Audit trails, evidence workflows
- workloads.md: Example workload configurations
- developer-workflow.md: Contributing guidelines

### Installation

- install/ISO_BUILD.md: Building and booting ISO
- Step-by-step deployment guides

### Improvements to implement [11]

- Add index.md as entry point
- Create GLOSSARY.md for terminology
- Add navigation aids (breadcrumbs, table of contents)
- Audit all files for outdated info, broken links
- Add "last updated" timestamps
- Create decision trees for common scenarios

### grafana/ - Monitoring Dashboards

__Purpose:__Provide pre-built Grafana dashboards for monitoring DebVisor clusters.

#### Dashboards

### Key Dashboards

- overview.json: System overview (nodes, resources, services)
- dns-dhcp.json: DNS/DHCP health and performance
- security.json: Security metrics and firewall stats
- compliance.json: Compliance audit and MFA usage
- ceph.json: Ceph cluster health and performance

### Improvements to implement [12]

- Add datasource naming consistency (Prometheus UID: `prometheus-debvisor`)
- Document threshold choices (why specific values)
- Add CI validation: verify metrics exist in Prometheus
- Add dashboard variables for multi-cluster/multi-tenant reusability
- Add templating examples

#### Provisioning

Grafana provisioning configuration.

### Improvements to implement [13]

- Add provisioning for notification channels (email, Slack)
- Document datasource endpoint customization
- Add CI validation for YAML syntax

### monitoring/ - Prometheus & Observability

__Purpose:__Configure metrics collection and log aggregation.

#### fixtures/

Test metrics and synthetic data for lab/demo environments.

### Components

- generator/: Metrics generation for testing
- ConfigMaps/Deployments: Pre-configured test data

### Improvements to implement [14]

- Add configuration options for metric names, labels
- Add Helm charts or kustomize overlays
- Clarify which fixtures for testing vs never production
- Add auto-cleanup/retention policies

#### Prometheus Configuration

__prometheus.yml:__Scrape configurations for different component types
__rules/:__Recording and alerting rules
__alerts/:__AlertManager configuration

### netcfg-tui/ - Network Configuration TUI

__Purpose:__Terminal UI for interactive network configuration.

### Improvements to implement [15]

- Add unit tests for config generation (interface enumeration, IP validation, VLAN)
- Add error handling for edge cases (interface disappears, invalid CIDR)
- Add more backends: iproute2, nmcli (NetworkManager)
- Add `--apply` flag for direct application with confirmation
- Add pre-flight validation (systemd-networkd/netplan available)
- Expand documentation: bonding, LAGs, multi-bridge scenarios

### services/rpc/ - gRPC RPC Service

__Purpose:__Provide machine API for node management, migrations, config sync.

#### proto/debvisor.proto

Protocol Buffer definitions for RPC API.

### Improvements to implement [16]

- Add API versioning and deprecation guidance
- Document error codes and client handling
- Add request/response payload examples

#### Makefile

Proto compilation and build targets.

### Improvements to implement [17]

- Add targets for Go, TypeScript/Node.js
- Add protolint for proto files
- Add version pinning for grpcio-tools

#### Implementation

### Improvements to implement [18]

- Add authentication (OAuth2, mTLS, API keys)
- Add authorization (RBAC for different RPC methods)
- Add TLS by default (self-signed for lab, proper certs for prod)
- Add request validation (schema, rate limiting, timeouts)
- Add audit logging (caller identity, timestamp)
- Add integration tests in container
- Add load testing and chaos testing

## Management & Usage

### Building the ISO

## Standard build

    cd opt/build
    ./build-debvisor.sh

## With custom architecture

    DEBVISOR_ARCH=arm64 ./build-debvisor.sh

## Fast rebuild (skip clean)

    DEBVISOR_FAST=1 ./build-debvisor.sh

## Specific version

    DEBVISOR_VERSION=v1.0.0 ./build-debvisor.sh

## Verbose output

    DEBVISOR_VERBOSE=1 ./build-debvisor.sh

## Deploying with Ansible

## Verify inventory syntax

    ansible-inventory -i opt/ansible/inventory --list

## Run security hardening

    ansible-playbook opt/ansible/playbooks/security-hardening.yml \
      -i opt/ansible/inventory

## Dry-run playbook

    ansible-playbook opt/ansible/playbooks/rotate-tsig-ha.yml \
      -i opt/ansible/inventory \
      --check --diff

## Run with tags

    ansible-playbook opt/ansible/playbooks/security-hardening.yml \
      -i opt/ansible/inventory \
      --tags firewall,selinux

## Testing & Validation

## Test first-boot provisioning

    ./opt/build/test-firstboot.sh --profile ceph

## Validate profiles

    ./opt/build/test-profile-summary.sh

## Lint Ansible playbooks

    ansible-lint opt/ansible/playbooks/*.yml

## Validate systemd units in resulting ISO

## (after ISO boots)

    systemd-analyze verify /etc/systemd/system/*.service

## Production Deployment Checklist

### Pre-Deployment

- [ ] Review and customize `opt/ansible/inventory`
- [ ] Verify all `opt/config/package-lists/*.list` packages available
- [ ] Test ISO build: `./opt/build/build-debvisor.sh`
- [ ] Validate first-boot: `./opt/build/test-firstboot.sh`
- [ ] Review Ansible playbooks for your environment
- [ ] Test Ansible on staging: `--check --diff` dry-run

### ISO Building

- [ ] Build production ISO: `DEBVISOR_VERSION=v1.0.0 ./opt/build/build-debvisor.sh`
- [ ] Verify ISO checksums
- [ ] Boot ISO on test hardware
- [ ] Validate post-boot services

### Deployment

- [ ] Boot ISO on all target nodes
- [ ] Run through installer (profiles, networking, users)
- [ ] Verify first-boot completes successfully
- [ ] Run Ansible playbooks for cluster setup
- [ ] Validate cluster health (Ceph, K8s, networking)

### Post-Deployment

- [ ] Verify Grafana dashboards show metrics
- [ ] Confirm alert rules are firing correctly
- [ ] Test backup/restore procedures
- [ ] Document any custom configurations
- [ ] Set up monitoring alerts for critical metrics

## Cross-Component Validation

__Recommended:__Add CI job to validate compatibility:

## Check Ansible inventory matches expected groups

## Check build scripts reference valid package lists

## Check Kubernetes manifests reference valid images

## Check Grafana dashboards reference valid metrics

## Check RPC proto matches web panel implementation

## Advanced Improvements (Phase 3.5+)

### Services & Features

__RPC Service Enhancements__(`services/rpc/ADVANCED_FEATURES.md`)

- Connection pooling (50 max connections, configurable)
- Request/response compression (GZIP, Brotli)
- API versioning (V1.0, V2.0, V3.0)
- Large cluster optimization (1000+ nodes)

__Web Panel Enhancements__(`web/panel/ADVANCED_FEATURES.md`)

- Two-Factor Authentication (TOTP, WebAuthn)
- WebSocket real-time notifications
- PDF export and reporting
- Dark mode and themes
- Batch operations framework
- Large cluster performance optimization

### Infrastructure Components

__Ansible Automation__(`ansible/ANSIBLE_GUIDE.md`)

- Comprehensive Ansible framework guide
- Inventory templates and best practices
- Playbook patterns for scalability
- Molecule testing framework setup
- Ansible-lint quality assurance

__Configuration & Preseed__(`config/PRESEED_DOCUMENTATION.md`)

- Preseed.cfg customization guide
- Variable substitution templates
- Build hooks documentation
- Architecture support (amd64, arm64)
- Security hardening in preseed

__Systemd Services & Timers__(`../etc/CONFIGURATION_GUIDE.md`)

- Service file best practices
- Timer unit configuration
- Security hardening (PrivateTmp, ProtectSystem)
- Resource limits and restart policies
- Validation and troubleshooting

__Helper Scripts__(`../usr/HELPER_SCRIPTS_GUIDE.md`)

- CLI tool reference (cephctl, hvctl, k8sctl)
- Script improvements (error handling, logging, validation)
- Health check framework
- Standardized exit codes
- Audit logging integration

## Next Steps

1.__Short-term:__Create `docker/README.md` for addon architecture
1.__Short-term:__Add Ansible inventory validation to CI
1.__Short-term:__Implement advanced RPC features (connection pooling, compression)
1.__Medium-term:__Implement gRPC RPC service and web panel advanced features (2FA, WebSockets, PDF)
1.__Medium-term:__Add comprehensive testing framework
1.__Medium-term:__Large cluster optimization (1000+ nodes)
1.__Long-term:__Develop HA cluster automation

## References

- [Ansible Documentation](https://docs.ansible.com/)
- [Live-build Manual](https://live-team.pages.debian.net/live-manual/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

## Related Documentation

- See [/etc/README.md](../etc/README.md) for system services and maintenance
- See [/usr/README.md](../usr/README.md) for operational scripts and CLIs (planned)
- See [README.md](../README.md) for project overview
