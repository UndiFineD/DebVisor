# Failover, Identity & Access Architecture\n\n## Goals\n\n- Hot/live migration for minimal

downtime.\n\n- Unified global user/tenant model (LDAP/AD compatibility).\n\n-
Modern SSO
(OIDC) for
panel/API + per-VM console authorization.\n\n- Granular RBAC: admin, operator,
tenant.\n\n## Live
Migration & Failover\n\n- Libvirt/QEMU live migration (pre-copy + optional
post-copy).\n\n- Shared
block storage via Ceph RBD eliminates disk copy.\n\n- Consistent CPU baseline
(`host-model`across
nodes) and matching hugepage config.\n\n- Encrypted libvirt migration channel
(TLS
certificates per
node).\n\n- RPC service
orchestrates:`preparemigration`,`migratevm`,`failovervm`.\n\n-
Health checks
(libvirt, ceph, network) feed failover decision logic.\n\n## Storage
Alignment\n\n- Ceph
RBD: VM
disks (single-writer, migratable).\n\n- CephFS: templates, ISO images, shared
configuration.\n\n-
ZFS (mixed profile): local high?speed ephemeral datasets.\n\n## Identity
Stack\n\n-
LDAP/AD
integration via SSSD + realmd (join domain or run local Samba/389DS).\n\n-
Keycloak (OIDC)
federated
to AD/LDAP for web/API auth.\n\n- Group mapping:
`debvisor-admin`,`debvisor-operator`,`debvisor-tenant-*`.\n\n- VM ownership
table
(PostgreSQL/SQLite): `vm_uuid`,`tenant_group`,`created_at`.\n\n## Access
Control\n\n- All
API
requests carry OIDC token -> claims mapped to groups.\n\n- Console tickets:
short?lived
signed token
referencing `vm_uuid`+ expiry.\n\n- Panel enforces ownership before exposing
VNC/SPICE
websocket
endpoints.\n\n## RPC Service Overview\n\n### Transport & Security\n\n- gRPC +
mutual TLS,
certs
issued by internal CA (cfssl or Keycloak CA).\n\n- Node registry stored in etcd
(keys:`/debvisor/nodes/`).\n\n### Core RPCs (Draft)\n\n| RPC | Purpose
|\n|-----|---------|\n|
registernode(node_info) | Add/update node in registry |\n| heartbeat(status) | Liveness &
metrics
feed |\n| listnodes() | Enumerate cluster nodes |\n| preparemigration(vmid,target) |
Pre-flight
checks |\n| migratevm(vmid,target,mode) | Execute live migration |\n| failovervm(vmid) |
Automatic
recovery action |\n| snapshotrbd(vmid,label) | Create RBD snapshot |\n|
rollbackrbd(vmid,snap) |
Restore snapshot |\n| syncusersgroups() | Cache directory users for fast lookup |\n\n##
Observability & Audit\n\n- Prometheus exporters: node, libvirt, Ceph.\n\n- Audit
log
(append-only):
migration events, snapshot ops, console access.\n\n- Alert rules: failed
migration,
degraded host,
Ceph health warn/err.\n\n## Security Considerations\n\n- Enforce TLS everywhere
(migration, RPC,
web).\n\n- Limit tenant capabilities (no direct host shell; only VM
operations).\n\n-
Rotate mTLS
certs (systemd timer + RPC distribution).\n\n- Optional per?VM firewall
segmentation via
security
groups / nft sets.\n\n## Roadmap\n\n1. MVP: registry, heartbeat, migratevm
(pre-copy),
panel auth
via Keycloak.\n\n1. Add snapshot lifecycle + tenant self-service.\n\n1.
Implement failover
orchestration + health scoring.\n\n1. Integrate post-copy migration for large
memory
VMs.\n\n1.
Multi-region replication (stretch Ceph cluster or RBD mirroring).\n\n##
References\n\n-
Libvirt
migration:
\n\n-]([https://libvirt.org/migration.html>\n\n]([https://libvirt.org/migration.html>\n\]([https://libvirt.org/migration.html>\n]([https://libvirt.org/migration.html>\]([https://libvirt.org/migration.html>]([https://libvirt.org/migration.html]([https://libvirt.org/migration.htm]([https://libvirt.org/migration.ht]([https://libvirt.org/migration.h]([https://libvirt.org/migration.]([https://libvirt.org/migration]([https://libvirt.org/migratio]([https://libvirt.org/migrati]([https://libvirt.org/migrat]([https://libvirt.org/migra]([https://libvirt.org/migr]([https://libvirt.org/mig]([https://libvirt.org/mi]([https://libvirt.org/m]([https://libvirt.org/]([https://libvirt.org]([https://libvirt.or]([https://libvirt.o]([https://libvirt.]([https://libvirt]([https://libvir]([https://libvi]([https://libv]([https://lib]([https://li](https://li)b)v)i)r)t).)o)r)g)/)m)i)g)r)a)t)i)o)n).)h)t)m)l)>)\)n)\)n)-)
Ceph RBD:
\n\n-]([https://docs.ceph.com/en/latest/rbd/>\n\n]([https://docs.ceph.com/en/latest/rbd/>\n\]([https://docs.ceph.com/en/latest/rbd/>\n]([https://docs.ceph.com/en/latest/rbd/>\]([https://docs.ceph.com/en/latest/rbd/>]([https://docs.ceph.com/en/latest/rbd/]([https://docs.ceph.com/en/latest/rbd]([https://docs.ceph.com/en/latest/rb]([https://docs.ceph.com/en/latest/r]([https://docs.ceph.com/en/latest/]([https://docs.ceph.com/en/latest]([https://docs.ceph.com/en/lates]([https://docs.ceph.com/en/late]([https://docs.ceph.com/en/lat]([https://docs.ceph.com/en/la]([https://docs.ceph.com/en/l]([https://docs.ceph.com/en/]([https://docs.ceph.com/en]([https://docs.ceph.com/e]([https://docs.ceph.com/]([https://docs.ceph.com]([https://docs.ceph.co]([https://docs.ceph.c]([https://docs.ceph.]([https://docs.ceph]([https://docs.cep]([https://docs.ce]([https://docs.c]([https://docs.]([https://docs](https://docs).)c)e)p)h).)c)o)m)/)e)n)/)l)a)t)e)s)t)/)r)b)d)/)>)\)n)\)n)-)
SSSD/AD:
\n\n-]([https://sssd.io/>\n\n]([https://sssd.io/>\n\]([https://sssd.io/>\n]([https://sssd.io/>\]([https://sssd.io/>]([https://sssd.io/]([https://sssd.io]([https://sssd.i]([https://sssd.]([https://sssd]([https://sss]([https://ss]([https://s](https://s)s)s)d).)i)o)/)>)\)n)\)n)-)
Keycloak:
\n\n]([https://www.keycloak.org/>\n\]([https://www.keycloak.org/>\n]([https://www.keycloak.org/>\]([https://www.keycloak.org/>]([https://www.keycloak.org/]([https://www.keycloak.org]([https://www.keycloak.or]([https://www.keycloak.o]([https://www.keycloak.]([https://www.keycloak]([https://www.keycloa]([https://www.keyclo]([https://www.keycl]([https://www.keyc]([https://www.key]([https://www.ke]([https://www.k]([https://www.]([https://www]([https://ww]([https://w](https://w)w)w).)k)e)y)c)l)o)a)k).)o)r)g)/)>)\)n)\)n)
