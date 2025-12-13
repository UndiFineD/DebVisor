# DebVisor Ansible Directory\n\nThis directory contains Ansible playbooks, roles, and

inventory for

automating DebVisor cluster deployment and management.\n\n## Directory
Structure\n\n
opt/ansible/\n
+-- inventory.yaml # Primary inventory (YAML format with full schema)\n +--
inventory.lab

## Lab

environment overrides (copy and customize)\n +-- inventory.prod # Production
environment
overrides
(copy and customize)\n +-- inventory.example # Legacy INI format (deprecated,
for
reference)\n +--
ansible.cfg # Ansible configuration\n +-- playbooks/ # Top-level playbooks for
orchestration\n | +--
site.yml # Master playbook: deploy full cluster\n | +-- dns-primary.yml # DNS primary
setup\n | +--
dns-secondary.yml # DNS secondary setup\n | +-- ceph-cluster.yml # Ceph cluster
deployment\n | +--
kubernetes-cluster.yml # Kubernetes cluster deployment\n | +-- security-hardening.yml #
Security
policy enforcement\n | +-- rotate-tsig-ha.yml # TSIG key rotation (HA DNS)\n | +--
bootstrap-addons.yml # Optional addon deployment\n +-- roles/ # Ansible roles
(atomic,
reusable
units)\n | +-- blocklist/ # Blocklist management role\n | +-- debvisor-blocklist/ #
DebVisor-specific blocklist role\n | +-- dns-ha/ # HA DNS setup (primary & secondary)\n |
+--
dns-secondary/ # Secondary DNS configuration\n | +-- mfa/ # MFA enforcement role\n | +--
monitoring-stack/ # Prometheus/Grafana deployment\n | +-- node-register/ # Node
registration role\n
| +-- rpc-service/ # DebVisor RPC service role\n | +-- vm-register/ # VM registration role\n | +--
vnc-console/ # VNC console access role\n | +-- web-panel/ # DebVisor web panel role\n |
+--
wireguard-mesh/ # WireGuard mesh networking role\n +-- group_vars/ # Group-level
variable
overrides\n +-- all.yml # Variables for all hosts\n +-- dns_primaries.yml # DNS
primary
variables\n
+-- dns_secondaries.yml # DNS secondary variables\n +-- ceph_mons.yml # Ceph
monitor
variables\n +--
ceph_osds.yml # Ceph OSD variables\n +-- k8s_controlplane.yml # Kubernetes
control plane
variables\n
+-- k8s_workers.yml # Kubernetes worker variables\n +-- hypervisors.yml #
Hypervisor
variables\n
host_vars/ # Host-specific variable overrides\n +-- dns01.debvisor.local.yml\n
+--
ceph-mon01.debvisor.local.yml\n +-- ... (per-host customizations)\n\n## Quick
Start\n\n###
1.
Prepare Inventory\n\n## Copy template to environment-specific file\n\n cp
inventory.yaml
inventory.lab\n\n## Edit for your lab environment\n\n vi inventory.lab\n\n##
Validate
inventory
syntax\n\n ansible-inventory -i inventory.lab --list\n\n## 2. Set Environment
Variables\n\n export
CEPH_FSID="a7f64e91-6f4a-4923-ab7e-1234567890ab"\n export ZFS_POOL="tank"\n
export
KUBERNETES_VERSION="1.28.0"\n\n### 3. Run Playbooks\n\n## Full cluster
deployment\n\n
ansible-playbook -i inventory.lab playbooks/site.yml\n\n## Individual
components\n\n
ansible-playbook -i inventory.lab playbooks/dns-primary.yml\n ansible-playbook
-i
inventory.lab
playbooks/ceph-cluster.yml\n ansible-playbook -i inventory.lab
playbooks/kubernetes-cluster.yml\n\n## Dry-run (check mode)\n\n ansible-playbook
-i
inventory.lab
playbooks/site.yml --check --diff\n\n## With specific tags\n\n ansible-playbook
-i
inventory.lab
playbooks/site.yml --tags "dns,ceph"\n\n## Verbose output\n\n ansible-playbook
-i
inventory.lab
playbooks/site.yml -vv\n\n## Playbook Tags\n\nAll playbooks use tags for
selective
execution. Common
tags:\n| Tag | Purpose | When to Use |\n|-----|---------|------------|\n| `dns`| DNS
configuration |
Updating DNS only |\n|`ceph`| Ceph operations | Updating Ceph cluster |\n|`k8s`|
Kubernetes
operations | Updating K8s cluster |\n|`security`| Security hardening | Applying security
policies
|\n|`monitoring`| Monitoring setup | Installing Prometheus/Grafana |\n|`mfa`| MFA enforcement |
Enabling MFA |\n|`validation`| Pre-flight checks | Verifying prerequisites
|\n|`idempotent`|
Repeatable operations | Safe to run multiple times |\n\n- *Example**: Run only DNS and
security
tasks:\n\n ansible-playbook -i inventory.lab playbooks/site.yml --tags
"dns,security"\n\n## Role
Dependency Order\n\nRoles should execute in this order to satisfy
dependencies:\n1.**blocklist**-
Ensure blocklist data is
available\n1.**dns-ha**/**dns-primary**/**dns-secondary**- DNS
must be up
for name resolution\n1.**node-register**- Register nodes with management
system\n1.**ceph-cluster**-
Storage backend (other services depend on it)\n1.**monitoring-stack**-
Prometheus/Grafana
for
observability\n1.**kubernetes-cluster**- K8s cluster (depends on
storage)\n1.**rpc-service**-
DebVisor RPC (depends on DNS, monitoring)\n1.**web-panel**- Web UI (depends on
RPC
service)\n1.**mfa**- MFA enforcement (last, non-blocking)\n\n### Enforced in
playbooks
via`roles:`and`pre_tasks/post_tasks`\n\n## Role Details\n\n### dns-ha\n\n-
*Purpose**:
Deploy HA DNS
with TSIG authentication\n\n- *Groups**: `dns_primaries`,`dns_secondaries`\n\n-
*Tasks**:\n\n-
Install bind9\n\n- Configure zone files\n\n- Set up TSIG keys\n\n- Enable zone
transfers\n\n-
Configure systemd service\n\n- *Variables**(see
`group_vars/dns_primaries.yml`):\n\n
bind_role:
"primary" # or "secondary"\n tsig_key_rotation: "monthly"\n dns_zones:\n\n-
"debvisor.local"\n\n-
"0.0.10.in-addr.arpa"\n\n### ceph-cluster\n\n- *Purpose**: Deploy Ceph storage
cluster\n\n-
*Groups**: `ceph_mons`,`ceph_osds`\n\n- *Tasks**:\n\n- Install Ceph
packages\n\n- Deploy
monitors\n\n- Deploy OSDs\n\n- Create pools\n\n- Enable health monitoring\n\n-
*Variables**:\n\n
ceph_version: "reef"\n ceph_cluster_name: "ceph"\n ceph_osd_pool_default_size:
3\n\n###
kubernetes-cluster\n\n- *Purpose**: Deploy Kubernetes cluster\n\n- *Groups**:
`k8s_controlplane`,`k8s_workers`\n\n- *Tasks**:\n\n- Install kubelet, kubeadm,
kubectl\n\n-
Initialize control plane\n\n- Deploy CNI (Calico)\n\n- Join worker nodes\n\n-
Deploy
CoreDNS\n\n-
*Variables**:\n\n kubernetes_version: "1.28.0"\n kubernetes_cni: "calico"\n
kubernetes_pod_network_cidr: "10.244.0.0/16"\n\n### monitoring-stack\n\n-
*Purpose**:
Deploy
Prometheus and Grafana\n\n- *Groups**: `management`\n\n- *Tasks**:\n\n- Deploy
Prometheus
server\n\n- Deploy Grafana\n\n- Configure scrape targets\n\n- Import
dashboards\n\n###
rpc-service\n\n- *Purpose**: Deploy DebVisor RPC service\n\n- *Groups**:
`management`\n\n-
*Depends
on**: DNS, monitoring\n\n- *Tasks**:\n\n- Deploy gRPC service\n\n- Configure
authentication\n\n- Set
up service discovery\n\n### web-panel\n\n- *Purpose**: Deploy DebVisor web
management
panel\n\n-
*Groups**: `management`\n\n- *Depends on**: RPC service\n\n- *Tasks**:\n\n-
Deploy
Flask/Django
application\n\n- Configure TLS\n\n- Set up reverse proxy\n\n## Idempotency &
Safety\n\n###
Idempotent Playbooks (Safe to re-run)\n\nThese playbooks are safe to run
multiple
times:\n\n-
`dns-primary.yml`- Configuration-only, no destructive
operations\n\n-`dns-secondary.yml`-
Configuration-only\n\n-`monitoring-stack.yml`- Idempotent service
deployment\n\n-`rpc-service.yml`-
Idempotent service deployment\n\n- *Re-run command**:\n\n ansible-playbook -i
inventory.lab
playbooks/.yml\n\n### Potentially Destructive Playbooks\n\nThese require careful
planning:\n\n-`ceph-cluster.yml`- Creates pools, initializes
storage\n\n-`kubernetes-cluster.yml`-
Initializes cluster, not easily reversible\n\n-`security-hardening.yml`- May
restrict
access; test
in lab first\n\n- *Recommended approach**:\n\n## Always dry-run first\n\n
ansible-playbook
-i
inventory.lab playbooks/.yml --check --diff\n\n## Review changes, then apply\n\n
ansible-playbook -i
inventory.lab playbooks/.yml\n\n## Dry-Run Workflow\n\nUse Ansible's check mode
to preview
changes
before applying:\n\n## Dry-run: show what would change (no actual changes)\n\n
ansible-playbook -i
inventory.lab playbooks/site.yml --check --diff\n\n## If satisfied, run for
real\n\n
ansible-playbook -i inventory.lab playbooks/site.yml\n\n## Debugging &
Troubleshooting\n\n###
Increase Verbosity\n\n## Show task names and results\n\n ansible-playbook -i
inventory.lab
playbooks/site.yml -v\n\n## Show variables, module args, and detailed output\n\n
ansible-playbook -i
inventory.lab playbooks/site.yml -vv\n\n## Show connection debugging\n\n
ansible-playbook
-i
inventory.lab playbooks/site.yml -vvv\n\n## Run Specific Hosts\n\n## Limit to
one host\n\n
ansible-playbook -i inventory.lab playbooks/site.yml --limit
dns01.debvisor.local\n\n##
Limit to a
group\n\n ansible-playbook -i inventory.lab playbooks/site.yml --limit
all_dns\n\n## Test
a Role in
Isolation\n\n## Run only dns-ha role\n\n ansible-playbook -i inventory.lab
playbooks/site.yml --tags
dns\n\n## Start from a specific task\n\n ansible-playbook -i inventory.lab
playbooks/site.yml
--start-at-task "Configure BIND zone"\n\n## Collect Diagnostics\n\nIf a playbook
fails:\n\n## Re-run
with debug output saved to file\n\n ansible-playbook -i inventory.lab
playbooks/site.yml
-vv >
/tmp/playbook.log 2>&1\n\n## Check Ansible logs\n\n grep -i error
/tmp/playbook.log\n\n##
SSH to
affected host for manual inspection\n\n ssh -i ~/.ssh/id_rsa
ansible@dns01.debvisor.local\n\n##
Ansible Configuration\n\nFile:`ansible.cfg`\n [defaults]\n inventory =
inventory.yaml\n
host_key_checking = False\n roles_path = roles\n collections_on_play_restart =
True\n
timeout = 60\n
[ssh_connection]\n ssh_args = -C -o ControlMaster=auto -o ControlPersist=60s\n
pipelining
=
True\n\n## Inventory Management\n\n### Environment-Specific
Inventories\n\nCreate
environment-specific copies:\n\n## Lab environment\n\n cp inventory.yaml
inventory.lab\n
vi
inventory.lab # Update IPs, hostnames, settings\n\n## Production environment\n\n
cp
inventory.yaml
inventory.prod\n vi inventory.prod # Production IPs, security hardening
settings\n\n##
Adding New
Hosts\n\n1. Edit inventory file (e.g., `inventory.lab`)\n\n1. Add host under
appropriate
group with
variables\n\n1. Validate:\n\n ansible-inventory -i inventory.lab --list | jq
'.all.hosts'\n\n 1. Run
playbook or role:\n\n ansible-playbook -i inventory.lab playbooks/.yml
--limit\n\n###
Modifying
Group Variables\n\n Edit `group_vars/`files:\nvi group_vars/ceph_osds.yml\n\n##
Change
osd_memory_target, recovery settings, etc\n\n Changes take effect next playbook
run:\nansible-playbook -i inventory.lab playbooks/ceph-cluster.yml\n\n## CI/CD
Integration\n\n###
Inventory Validation in CI\n\n## Validate YAML syntax\n\nyamllint
inventory.yaml\n\n##
Validate
Ansible inventory structure\n\nansible-inventory -i inventory.yaml --list >
/tmp/inv.json\npython3
-m json.tool /tmp/inv.json # Check JSON valid\n\n## Validate required groups and
hosts
exist\n\npython3 scripts/validate_inventory.py inventory.yaml\n\n## Playbook
Linting\n\n##
Lint all
playbooks\n\nansible-lint playbooks/\n\n## Fix common issues
automatically\n\nansible-lint
playbooks/ --fix\n\n## Test Playbooks in CI\n\n## Syntax check only
(fast)\n\nansible-playbook
playbooks/site.yml --syntax-check\n\n## Dry-run against lab inventory
(slow)\n\nansible-playbook -i
inventory.lab playbooks/site.yml --check\n\n## If available, test against
staging
environment\n\nansible-playbook -i inventory.staging playbooks/site.yml
--check\n\n## Best
Practices\n\n 1.**Use YAML inventory format**- More readable, supports nesting\n
1.**Separate
environments**- Always use environment-specific inventory copies\n 1.**Validate
before
applying**-
Always use`--check --diff`first\n 1.**Document variable changes**-
Update`group_vars/`comments when
modifying\n 1.**Use tags for flexibility**- Tag tasks for selective execution\n
1.**Test
idempotency**- Run playbooks twice to verify idempotency\n 1.**Version
control**- Commit
inventory
and playbooks to git\n 1.**Secrets management**- Use`ansible-vault`for sensitive
variables\n
1.**Meaningful host names**- Use FQDNs for DNS resolution
(e.g.,`dns01.debvisor.local`)\n
1.**Monitor compliance**- Use `--diff`to catch configuration drift\n\n##
Advanced
Topics\n\n###
Vault-Protected Secrets\n\n Store sensitive variables in encrypted vault
files:\n\n##
Create
encrypted vault\n\nansible-vault create group_vars/vault.yml\n\n## Edit
encrypted
vault\n\nansible-vault edit group_vars/vault.yml\n\n## Run playbook with
vault\n\nansible-playbook
-i inventory.lab playbooks/site.yml --ask-vault-pass\n\n## Dynamic Inventory\n\n
For large
or
dynamic environments, consider dynamic inventory scripts:\n\n## Use dynamic
inventory from
AWS,
Azure, etc\n\nansible-playbook -i scripts/dynamic_inventory.py
playbooks/site.yml\n\n##
Callback
Plugins\n\n Customize Ansible output (e.g., JSON, HTML reports):\n\n## In
ansible.cfg\n\n[defaults]\ncallback_whitelist = json\n\n## Support &
Contribution\n\n-
**Issue**:
Problems or questions? File an issue in the main DebVisor repo\n\n- **Pull
Request**:
Improvements?
Submit a PR with tests and documentation\n\n- **Changelog**: Document
significant changes
in`CHANGELOG.md`\n\n- --\n\n- *Last Updated**: 2025-11-26\n\n
