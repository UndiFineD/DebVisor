# DebVisor Ansible Directory

This directory contains Ansible playbooks, roles, and inventory for automating DebVisor cluster deployment and management.
## Directory Structure
    opt/ansible/
    +-- inventory.yaml                 # Primary inventory (YAML format with full schema)
    +-- inventory.lab                  # Lab environment overrides (copy and customize)
    +-- inventory.prod                 # Production environment overrides (copy and customize)
    +-- inventory.example              # Legacy INI format (deprecated, for reference)
    +-- ansible.cfg                    # Ansible configuration
    +-- playbooks/                     # Top-level playbooks for orchestration
    |   +-- site.yml                   # Master playbook: deploy full cluster
    |   +-- dns-primary.yml            # DNS primary setup
    |   +-- dns-secondary.yml          # DNS secondary setup
    |   +-- ceph-cluster.yml           # Ceph cluster deployment
    |   +-- kubernetes-cluster.yml     # Kubernetes cluster deployment
    |   +-- security-hardening.yml     # Security policy enforcement
    |   +-- rotate-tsig-ha.yml         # TSIG key rotation (HA DNS)
    |   +-- bootstrap-addons.yml       # Optional addon deployment
    +-- roles/                         # Ansible roles (atomic, reusable units)
    |   +-- blocklist/                 # Blocklist management role
    |   +-- debvisor-blocklist/        # DebVisor-specific blocklist role
    |   +-- dns-ha/                    # HA DNS setup (primary & secondary)
    |   +-- dns-secondary/             # Secondary DNS configuration
    |   +-- mfa/                       # MFA enforcement role
    |   +-- monitoring-stack/          # Prometheus/Grafana deployment
    |   +-- node-register/             # Node registration role
    |   +-- rpc-service/               # DebVisor RPC service role
    |   +-- vm-register/               # VM registration role
    |   +-- vnc-console/               # VNC console access role
    |   +-- web-panel/                 # DebVisor web panel role
    |   +-- wireguard-mesh/            # WireGuard mesh networking role
    +-- group_vars/                    # Group-level variable overrides
        +-- all.yml                    # Variables for all hosts
        +-- dns_primaries.yml          # DNS primary variables
        +-- dns_secondaries.yml        # DNS secondary variables
        +-- ceph_mons.yml              # Ceph monitor variables
        +-- ceph_osds.yml              # Ceph OSD variables
        +-- k8s_controlplane.yml       # Kubernetes control plane variables
        +-- k8s_workers.yml            # Kubernetes worker variables
        +-- hypervisors.yml            # Hypervisor variables
    host_vars/                         # Host-specific variable overrides
        +-- dns01.debvisor.local.yml
        +-- ceph-mon01.debvisor.local.yml
        +-- ... (per-host customizations)
## Quick Start
### 1. Prepare Inventory
## Copy template to environment-specific file
    cp inventory.yaml inventory.lab
## Edit for your lab environment
    vi inventory.lab
## Validate inventory syntax
    ansible-inventory -i inventory.lab --list
## 2. Set Environment Variables
    export CEPH_FSID="a7f64e91-6f4a-4923-ab7e-1234567890ab"
    export ZFS_POOL="tank"
    export KUBERNETES_VERSION="1.28.0"
### 3. Run Playbooks
## Full cluster deployment
    ansible-playbook -i inventory.lab playbooks/site.yml
## Individual components
    ansible-playbook -i inventory.lab playbooks/dns-primary.yml
    ansible-playbook -i inventory.lab playbooks/ceph-cluster.yml
    ansible-playbook -i inventory.lab playbooks/kubernetes-cluster.yml
## Dry-run (check mode)
    ansible-playbook -i inventory.lab playbooks/site.yml --check --diff
## With specific tags
    ansible-playbook -i inventory.lab playbooks/site.yml --tags "dns,ceph"
## Verbose output
    ansible-playbook -i inventory.lab playbooks/site.yml -vv
## Playbook Tags
All playbooks use tags for selective execution. Common tags:
| Tag | Purpose | When to Use |
|-----|---------|------------|
| `dns` | DNS configuration | Updating DNS only |
| `ceph` | Ceph operations | Updating Ceph cluster |
| `k8s` | Kubernetes operations | Updating K8s cluster |
| `security` | Security hardening | Applying security policies |
| `monitoring` | Monitoring setup | Installing Prometheus/Grafana |
| `mfa` | MFA enforcement | Enabling MFA |
| `validation` | Pre-flight checks | Verifying prerequisites |
| `idempotent` | Repeatable operations | Safe to run multiple times |

- *Example**: Run only DNS and security tasks:
    ansible-playbook -i inventory.lab playbooks/site.yml --tags "dns,security"
## Role Dependency Order
Roles should execute in this order to satisfy dependencies:
1.**blocklist**- Ensure blocklist data is available
1.**dns-ha**/**dns-primary**/**dns-secondary**- DNS must be up for name resolution
1.**node-register**- Register nodes with management system
1.**ceph-cluster**- Storage backend (other services depend on it)
1.**monitoring-stack**- Prometheus/Grafana for observability
1.**kubernetes-cluster**- K8s cluster (depends on storage)
1.**rpc-service**- DebVisor RPC (depends on DNS, monitoring)
1.**web-panel**- Web UI (depends on RPC service)
1.**mfa**- MFA enforcement (last, non-blocking)
### Enforced in playbooks via `roles:`and`pre_tasks/post_tasks`
## Role Details
### dns-ha
- *Purpose**: Deploy HA DNS with TSIG authentication

- *Groups**: `dns_primaries`,`dns_secondaries`

- *Tasks**:

- Install bind9

- Configure zone files

- Set up TSIG keys

- Enable zone transfers

- Configure systemd service

- *Variables**(see `group_vars/dns_primaries.yml`):
    bind_role: "primary"  # or "secondary"
    tsig_key_rotation: "monthly"
    dns_zones:

- "debvisor.local"

- "0.0.10.in-addr.arpa"
### ceph-cluster
- *Purpose**: Deploy Ceph storage cluster

- *Groups**: `ceph_mons`,`ceph_osds`

- *Tasks**:

- Install Ceph packages

- Deploy monitors

- Deploy OSDs

- Create pools

- Enable health monitoring

- *Variables**:
    ceph_version: "reef"
    ceph_cluster_name: "ceph"
    ceph_osd_pool_default_size: 3
### kubernetes-cluster
- *Purpose**: Deploy Kubernetes cluster

- *Groups**: `k8s_controlplane`,`k8s_workers`

- *Tasks**:

- Install kubelet, kubeadm, kubectl

- Initialize control plane

- Deploy CNI (Calico)

- Join worker nodes

- Deploy CoreDNS

- *Variables**:
    kubernetes_version: "1.28.0"
    kubernetes_cni: "calico"
    kubernetes_pod_network_cidr: "10.244.0.0/16"
### monitoring-stack
- *Purpose**: Deploy Prometheus and Grafana

- *Groups**: `management`

- *Tasks**:

- Deploy Prometheus server

- Deploy Grafana

- Configure scrape targets

- Import dashboards
### rpc-service
- *Purpose**: Deploy DebVisor RPC service

- *Groups**: `management`

- *Depends on**: DNS, monitoring

- *Tasks**:

- Deploy gRPC service

- Configure authentication

- Set up service discovery
### web-panel
- *Purpose**: Deploy DebVisor web management panel

- *Groups**: `management`

- *Depends on**: RPC service

- *Tasks**:

- Deploy Flask/Django application

- Configure TLS

- Set up reverse proxy
## Idempotency & Safety
### Idempotent Playbooks (Safe to re-run)
These playbooks are safe to run multiple times:

- `dns-primary.yml` - Configuration-only, no destructive operations

- `dns-secondary.yml` - Configuration-only

- `monitoring-stack.yml` - Idempotent service deployment

- `rpc-service.yml` - Idempotent service deployment

- *Re-run command**:
    ansible-playbook -i inventory.lab playbooks/.yml
### Potentially Destructive Playbooks
These require careful planning:

- `ceph-cluster.yml` - Creates pools, initializes storage

- `kubernetes-cluster.yml` - Initializes cluster, not easily reversible

- `security-hardening.yml` - May restrict access; test in lab first

- *Recommended approach**:
## Always dry-run first
    ansible-playbook -i inventory.lab playbooks/.yml --check --diff
## Review changes, then apply
    ansible-playbook -i inventory.lab playbooks/.yml
## Dry-Run Workflow
Use Ansible's check mode to preview changes before applying:
## Dry-run: show what would change (no actual changes)
    ansible-playbook -i inventory.lab playbooks/site.yml --check --diff
## If satisfied, run for real
    ansible-playbook -i inventory.lab playbooks/site.yml
## Debugging & Troubleshooting
### Increase Verbosity
## Show task names and results
    ansible-playbook -i inventory.lab playbooks/site.yml -v
## Show variables, module args, and detailed output
    ansible-playbook -i inventory.lab playbooks/site.yml -vv
## Show connection debugging
    ansible-playbook -i inventory.lab playbooks/site.yml -vvv
## Run Specific Hosts
## Limit to one host
    ansible-playbook -i inventory.lab playbooks/site.yml --limit dns01.debvisor.local
## Limit to a group
    ansible-playbook -i inventory.lab playbooks/site.yml --limit all_dns
## Test a Role in Isolation
## Run only dns-ha role
    ansible-playbook -i inventory.lab playbooks/site.yml --tags dns
## Start from a specific task
    ansible-playbook -i inventory.lab playbooks/site.yml --start-at-task "Configure BIND zone"
## Collect Diagnostics
If a playbook fails:
## Re-run with debug output saved to file
    ansible-playbook -i inventory.lab playbooks/site.yml -vv > /tmp/playbook.log 2>&1
## Check Ansible logs
    grep -i error /tmp/playbook.log
## SSH to affected host for manual inspection
    ssh -i ~/.ssh/id_rsa ansible@dns01.debvisor.local
## Ansible Configuration
File: `ansible.cfg`
    [defaults]
    inventory = inventory.yaml
    host_key_checking = False
    roles_path = roles
    collections_on_play_restart = True
    timeout = 60
    [ssh_connection]
    ssh_args = -C -o ControlMaster=auto -o ControlPersist=60s
    pipelining = True
## Inventory Management
### Environment-Specific Inventories
Create environment-specific copies:
## Lab environment
    cp inventory.yaml inventory.lab
    vi inventory.lab  # Update IPs, hostnames, settings
## Production environment
    cp inventory.yaml inventory.prod
    vi inventory.prod  # Production IPs, security hardening settings
## Adding New Hosts
1. Edit inventory file (e.g., `inventory.lab`)

1. Add host under appropriate group with variables

1. Validate:
       ansible-inventory -i inventory.lab --list | jq '.all.hosts'

    1. Run playbook or role:
   ansible-playbook -i inventory.lab playbooks/.yml --limit
### Modifying Group Variables
    Edit `group_vars/` files:
vi group_vars/ceph_osds.yml
## Change osd_memory_target, recovery settings, etc
    Changes take effect next playbook run:
ansible-playbook -i inventory.lab playbooks/ceph-cluster.yml
## CI/CD Integration
### Inventory Validation in CI
## Validate YAML syntax
yamllint inventory.yaml
## Validate Ansible inventory structure
ansible-inventory -i inventory.yaml --list > /tmp/inv.json
python3 -m json.tool /tmp/inv.json  # Check JSON valid
## Validate required groups and hosts exist
python3 scripts/validate_inventory.py inventory.yaml
## Playbook Linting
## Lint all playbooks
ansible-lint playbooks/
## Fix common issues automatically
ansible-lint playbooks/ --fix
## Test Playbooks in CI
## Syntax check only (fast)
ansible-playbook playbooks/site.yml --syntax-check
## Dry-run against lab inventory (slow)
ansible-playbook -i inventory.lab playbooks/site.yml --check
## If available, test against staging environment
ansible-playbook -i inventory.staging playbooks/site.yml --check
## Best Practices
    1.**Use YAML inventory format**- More readable, supports nesting
    1.**Separate environments**- Always use environment-specific inventory copies
    1.**Validate before applying**- Always use `--check --diff` first
    1.**Document variable changes**- Update `group_vars/` comments when modifying
    1.**Use tags for flexibility**- Tag tasks for selective execution
    1.**Test idempotency**- Run playbooks twice to verify idempotency
    1.**Version control**- Commit inventory and playbooks to git
    1.**Secrets management**- Use `ansible-vault` for sensitive variables
    1.**Meaningful host names**- Use FQDNs for DNS resolution (e.g., `dns01.debvisor.local`)
    1.**Monitor compliance**- Use `--diff` to catch configuration drift
## Advanced Topics
### Vault-Protected Secrets
    Store sensitive variables in encrypted vault files:
## Create encrypted vault
ansible-vault create group_vars/vault.yml
## Edit encrypted vault
ansible-vault edit group_vars/vault.yml
## Run playbook with vault
ansible-playbook -i inventory.lab playbooks/site.yml --ask-vault-pass
## Dynamic Inventory
    For large or dynamic environments, consider dynamic inventory scripts:
## Use dynamic inventory from AWS, Azure, etc
ansible-playbook -i scripts/dynamic_inventory.py playbooks/site.yml
## Callback Plugins
    Customize Ansible output (e.g., JSON, HTML reports):
## In ansible.cfg
[defaults]
callback_whitelist = json
## Support & Contribution
- **Issue**: Problems or questions? File an issue in the main DebVisor repo

- **Pull Request**: Improvements? Submit a PR with tests and documentation

- **Changelog**: Document significant changes in `CHANGELOG.md`

- --

- *Last Updated**: 2025-11-26
