# usr/ Directory - Helper Scripts & Operational Tools

## Overview

The `usr/` directory contains runtime tools, systemd services, and helper scripts for operational use.

## Quick Tool Reference

| Tool | Purpose | Example |
|------|---------|---------|
| `cephctl`| Ceph cluster management |`cephctl status` |
| `hvctl`| Hypervisor/VM management |`hvctl list` |
| `k8sctl`| Kubernetes operations |`k8sctl nodes` |
| `debvisor-migrate.sh`| VM migration |`debvisor-migrate.sh vm1 hvr-02` |
| `debvisor-dns-update.sh`| DNS records |`debvisor-dns-update.sh host1 192.168.1.100` |
| `debvisor-netcfg`| Network configuration |`debvisor-netcfg` |

## Script Improvements

### Universal Features (All Scripts)

- **Documentation**: `--help` prints comprehensive usage

- **Error Handling**: Consistent error reporting and exit codes

- **Logging**: Audit trail of all operations

- **Validation**: Pre-flight checks before execution

- **Rollback**: Recovery procedures on failure

- **Examples**: Common usage examples in help text

### Helper Script Documentation

### debvisor-migrate.sh

- Pre-migration validation

- Bandwidth rate limiting

- Progress monitoring

- Rollback support

- Post-migration validation

### debvisor-dns-update.sh

- TSIG validation

- DNS propagation verification

- TTL management

- Rollback capability

- Multiple DNS server support

### debvisor-cloudinit-iso.sh

- cloud-init syntax validation

- Size constraints warnings

- Template library

- Provisioning documentation

### debvisor-netcfg

- Interactive validation

- Rollback mechanism

- Multiple backend support

- VLAN/bonding templates

- IPv6 support

### CLI Wrapper Tools

### cephctl

- Cluster health summary

- OSD status and management

- Pool operations

- PG statistics

- Performance metrics

- Alert integration

### hvctl

- VM resource tracking

- Migration helpers

- Snapshot management

- Console access

- Resource validation

### k8sctl

- Node health summary

- Workload status

- Pod log access

- Debug capabilities

- Addon management

## Output Formatting

All tools support multiple output formats:
    cephctl status --format json
    cephctl status --format yaml
    cephctl status --format table  # default

## Health Check

- *debvisor-health-check.sh**(NEW)

Universal pre-flight validation:
    debvisor-health-check.sh

## Checks: binaries, services, connectivity, filesystem

## Systemd Services

### debvisor-firstboot.service

- Initial node setup

- Retry on failure

- Status reporting

- Pre-flight checks

### debvisor-rpcd.service

- RPC service

- Security hardening

- Resource limits

- Health monitoring

### debvisor-panel.service

- Web UI service

- Dependency on RPC

- TLS configuration

- Log aggregation

## Audit Logging

All operational scripts log to audit trail:

## View audit logs

    journalctl --grep debvisor -o json | jq '.MESSAGE'

## Error Codes

Standardized exit codes:

- 0: Success

- 1: General error

- 2: Invalid arguments

- 3: Resource not found

- 4: Connection failed

- 5: Operation failed

- 6: Validation failed

## Troubleshooting

- *Common Issues**:

- Connectivity: Check SSH keys and network access

- Permissions: Verify sudo privileges and file permissions

- Services: Check systemd status and logs

- Configuration: Validate preseed and inventory files

## Safety Features

- Pre-flight validation before destructive operations

- Dry-run/check mode support

- Rollback procedures documented

- Mutex/lock mechanisms to prevent concurrent conflicts

- Maintenance mode support

## Documentation

Each script includes:

- Usage examples

- Common scenarios

- Troubleshooting guide

- Man pages (select scripts)

## Integration

All tools integrate with:

- Ceph cluster status

- Kubernetes API

- libvirt hypervisor

- systemd services

- Audit logging framework
