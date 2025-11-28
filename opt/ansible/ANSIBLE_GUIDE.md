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

-__inventory.yaml__- Main inventory file with all hosts and groups
-__inventory.example__- Template for new deployments
-__inventory.lab__- Pre-configured for lab environments
-__inventory.prod__- Pre-configured for production
-__playbooks/__- Main automation playbooks
-__roles/__- Reusable role modules
-__ansible.cfg__- Ansible configuration
-__.ansible-lint__- Code quality rules (NEW)
-__molecule.yml__- Role testing framework (NEW)
-__validate-inventory.py__- Inventory validation script (NEW)

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

__DNS Servers__require:

- `dns_zone` - Primary zone for server
- `dns_mode` - primary or secondary

__Ceph Monitors__require:

- `ceph_mon_ip` - Monitor IP address
- `ceph_fsid` - Cluster FSID

__Kubernetes__require:

- `k8s_role` - controlplane or worker
- `pod_network_cidr` - Network CIDR for pods

## Playbook Execution

### Dependency Order

1.__bootstrap.yml__- Initial node setup (ALL nodes)
1.__dns-setup.yml__- DNS/DHCP configuration
1.__ceph.yml__- Ceph cluster deployment
1.__kubernetes.yml__- Kubernetes setup
1.__monitoring.yml__- Prometheus/Grafana

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

-__Always use --check first__: `ansible-playbook --check --diff`
-__Use inventory templates__: Start with inventory.lab or inventory.prod
-__Validate before running__: `validate-inventory.py`and`ansible-lint`
-__Test in non-prod__: Always test changes on lab environment first
-__Document custom variables__: Add comments in group_vars/ files
-__Use version control__: Track all changes in Git

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
