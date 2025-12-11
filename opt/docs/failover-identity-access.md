# Failover, Identity & Access Architecture

## Goals

- Hot/live migration for minimal downtime.
- Unified global user/tenant model (LDAP/AD compatibility).
- Modern SSO (OIDC) for panel/API + per-VM console authorization.
- Granular RBAC: admin, operator, tenant.

## Live Migration & Failover

- Libvirt/QEMU live migration (pre-copy + optional post-copy).
- Shared block storage via Ceph RBD eliminates disk copy.
- Consistent CPU baseline (`host-model` across nodes) and matching hugepage config.
- Encrypted libvirt migration channel (TLS certificates per node).
- RPC service orchestrates: `preparemigration`,`migratevm`,`failovervm`.
- Health checks (libvirt, ceph, network) feed failover decision logic.

## Storage Alignment

- Ceph RBD: VM disks (single-writer, migratable).
- CephFS: templates, ISO images, shared configuration.
- ZFS (mixed profile): local high?speed ephemeral datasets.

## Identity Stack

- LDAP/AD integration via SSSD + realmd (join domain or run local Samba/389DS).
- Keycloak (OIDC) federated to AD/LDAP for web/API auth.
- Group mapping: `debvisor-admin`,`debvisor-operator`,`debvisor-tenant-*`.
- VM ownership table (PostgreSQL/SQLite): `vm_uuid`,`tenant_group`,`created_at`.

## Access Control

- All API requests carry OIDC token -> claims mapped to groups.
- Console tickets: short?lived signed token referencing `vm_uuid` + expiry.
- Panel enforces ownership before exposing VNC/SPICE websocket endpoints.

## RPC Service Overview

### Transport & Security

- gRPC + mutual TLS, certs issued by internal CA (cfssl or Keycloak CA).
- Node registry stored in etcd (keys: `/debvisor/nodes/`).

### Core RPCs (Draft)

| RPC | Purpose |
|-----|---------|
| registernode(node_info) | Add/update node in registry |
| heartbeat(status) | Liveness & metrics feed |
| listnodes() | Enumerate cluster nodes |
| preparemigration(vmid,target) | Pre-flight checks |
| migratevm(vmid,target,mode) | Execute live migration |
| failovervm(vmid) | Automatic recovery action |
| snapshotrbd(vmid,label) | Create RBD snapshot |
| rollbackrbd(vmid,snap) | Restore snapshot |
| syncusersgroups() | Cache directory users for fast lookup |

## Observability & Audit

- Prometheus exporters: node, libvirt, Ceph.
- Audit log (append-only): migration events, snapshot ops, console access.
- Alert rules: failed migration, degraded host, Ceph health warn/err.

## Security Considerations

- Enforce TLS everywhere (migration, RPC, web).
- Limit tenant capabilities (no direct host shell; only VM operations).
- Rotate mTLS certs (systemd timer + RPC distribution).
- Optional per?VM firewall segmentation via security groups / nft sets.

## Roadmap

1. MVP: registry, heartbeat, migratevm (pre-copy), panel auth via Keycloak.
1. Add snapshot lifecycle + tenant self-service.
1. Implement failover orchestration + health scoring.
1. Integrate post-copy migration for large memory VMs.
1. Multi-region replication (stretch Ceph cluster or RBD mirroring).

## References

- Libvirt migration: <<<https://libvirt.org/migration.html>>>
- Ceph RBD: <<<https://docs.ceph.com/en/latest/rbd/>>>
- SSSD/AD: <<<https://sssd.io/>>>
- Keycloak: <<<https://www.keycloak.org/>>>
