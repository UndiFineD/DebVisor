# opt/ansible/ - Ansible Automation Framework

## Overview
The `opt/ansible/` directory contains Ansible playbooks, roles, and inventory for DebVisor infrastructure deployment and configuration management.
## Quick Start
## Validate inventory syntax
    python3 opt/ansible/validate-inventory.py -i inventory.yaml
## Lint playbooks for best practices
    ansible-lint opt/ansible/playbooks/
## Run playbook in check mode (dry-run)
    ansible-playbook playbooks/site.yml --check --diff
## Execute playbook
    ansible-playbook playbooks/site.yml
## Directory Structure
- **inventory.yaml**- Main inventory file with all hosts and groups

- **inventory.example**- Template for new deployments

- **inventory.lab**- Pre-configured for lab environments

- **inventory.prod**- Pre-configured for production

- **playbooks/**- Main automation playbooks

- **roles/**- Reusable role modules

- **ansible.cfg**- Ansible configuration

- **.ansible-lint**- Code quality rules (NEW)

- **molecule.yml**- Role testing framework (NEW)

- **validate-inventory.py**- Inventory validation script (NEW)
## Inventory Templates
### Grouping Strategy
All hosts are organized by functional role:
    all:
      children:
        dns_servers:
          children:
            dns_primaries: [dns1]
            dns_secondaries: [dns2, dns3]
        ceph_cluster:
          children:
            ceph_mons: [ceph1, ceph2, ceph3]
            ceph_osds: [osd1, osd2, osd3]
        kubernetes:
          children:
            k8s_controlplane: [k8s-master1]
            k8s_workers: [k8s-worker1, k8s-worker2]
        hypervisors: [hvr1, hvr2]
### Host Variables Requirements
- *DNS Servers**require:

- `dns_zone` - Primary zone for server

- `dns_mode` - primary or secondary

- *Ceph Monitors**require:

- `ceph_mon_ip` - Monitor IP address

- `ceph_fsid` - Cluster FSID

- *Kubernetes**require:

- `k8s_role` - controlplane or worker

- `pod_network_cidr` - Network CIDR for pods
## Playbook Execution
### Dependency Order
1.**bootstrap.yml**- Initial node setup (ALL nodes)
1.**dns-setup.yml**- DNS/DHCP configuration
1.**ceph.yml**- Ceph cluster deployment
1.**kubernetes.yml**- Kubernetes setup
1.**monitoring.yml**- Prometheus/Grafana
### Common Commands
## Full deployment
    ansible-playbook playbooks/site.yml
## Lab environment
    ansible-playbook -i inventory.lab playbooks/site.yml
## Specific playbook
    ansible-playbook playbooks/dns-setup.yml
## Dry-run
    ansible-playbook playbooks/site.yml --check --diff
## Specific hosts/groups
    ansible-playbook playbooks/site.yml -l dns_servers
## By tags
    ansible-playbook playbooks/site.yml --tags dns,ceph
## Testing & Validation
### Ansible Linting
## Check all playbooks
    ansible-lint opt/ansible/playbooks/
## Check specific playbook
    ansible-lint opt/ansible/playbooks/site.yml
## Molecule Role Testing
## Test role in isolation
    cd opt/ansible/roles/debvisor-common
    molecule test
## Run specific scenario
    molecule test -s default
## Debug failed test
    molecule converge && molecule login
## Best Practices
- **Always use --check first**: `ansible-playbook --check --diff`

- **Use inventory templates**: Start with inventory.lab or inventory.prod

- **Validate before running**: `validate-inventory.py`and`ansible-lint`

- **Test in non-prod**: Always test changes on lab environment first

- **Document custom variables**: Add comments in group_vars/ files

- **Use version control**: Track all changes in Git
## Troubleshooting
## Test connectivity
    ansible all -m ping
## Check inventory
    ansible-inventory -i inventory.yaml --list
## Verbose output
    ansible-playbook playbooks/site.yml -vvv
## Start from specific task
    ansible-playbook playbooks/site.yml --start-at-task "Task Name"
## Related Documentation
- Deployment guide: `opt/docs/install/`

- Architecture: `opt/docs/architecture.md`

- Operations: `opt/docs/operations.md`
