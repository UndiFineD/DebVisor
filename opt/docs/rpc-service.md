# DebVisor RPC Service Design

## Purpose

Coordinate node membership, health, migration, and configuration synchronization securely.

## Deployment

- **Service User**: `debvisor-rpc:debvisor-rpc` (system account, no interactive login)

- **Working Directory**: `/opt/debvisor/rpc`

- **Port**: TCP `9443`(defined as`rpc_port`in nftables; inbound disabled by default, enable via`debvisor.nft`or`debvisor-local.nft` as needed)

- **Systemd Unit**: `debvisor-rpcd.service`

- Depends on `network-online.target`

- Logs with `SyslogIdentifier=debvisor-rpcd`

- Restarts on failure

- **First-boot setup**: `debvisor-firstboot.sh`calls`debvisor-setup-rpc-user.sh`to create the service account and set ownership of`/opt/debvisor/rpc`

## Stack

- gRPC (mutual TLS)

- etcd (registry + coordination keys)

- Language: Python (gRPC)

## Certificates

- Issued by internal CA (cfssl or Keycloak). Stored under `/etc/debvisor/pki/`.

- Rotation: systemd timer calls renewal + distribution via secure RPC.

## Coordination & State (etcd)

`debvisor-rpc` uses etcd as the runtime coordination store. Desired state (policies, profiles) is managed via Git and rendered into versioned config blobs, while etcd holds fast-moving operational state:
At a high level, the node agent (implemented as part of `debvisor-rpcd` or a small companion) is responsible for:

- Writing `/debvisor/self/node_id` on each node to a stable identifier

- Maintaining `/debvisor/nodes//info`(including`fqdn`) and`/debvisor/nodes//mode`

- Ensuring these keys are updated whenever local configuration (hostname, IP, mode) changes

The hostname registration script (`/usr/local/bin/hostname-register.sh`) is a consumer of this data: it prefers the cluster-assigned FQDN from`/debvisor/nodes//info/fqdn` when present, but falls back to the local hostname if etcd or the key is unavailable.

### Nodes & Health

    /debvisor/nodes//info          # static info: hostname, IP, rack, version
    /debvisor/nodes//health        # latest Health snapshot from Heartbeat
    /debvisor/nodes//last_seen     # RFC3339 timestamp of last heartbeat
    /debvisor/nodes//status        # OK | DEGRADED | DOWN (derived by controller)
     /debvisor/nodes//mode          # standalone | clustered (influences hostname/DNS behavior)
     /debvisor/nodes//info/fqdn     # optional cluster-assigned FQDN used by hostname-register

### VM Placement & Locks

    /debvisor/vms//owner           # current authoritative node for the VM
    /debvisor/vms//lock            # ephemeral lock holder (node_id) with TTL lease
    /debvisor/vms//metadata        # JSON/YAML with policy flags (protected, HA group, etc.)

### Replication Jobs & Last Sync

    /debvisor/replication/jobs/         # job definition (source, target, backend, dataset, policy)
    /debvisor/replication/jobs//status # job state machine + last run metrics
    /debvisor/replication/zfs///last_snapshot   # last successfully replicated snapshot name
    /debvisor/replication/zfs///last_success_at # timestamp of last successful run

### Templates (Ceph RBD)

    /debvisor/templates/              # template metadata: backend=rbd, pool, image, default snapshot label

### Config Sync

    /debvisor/config/current_version              # desired config version (e.g. Git SHA or semantic version)
    /debvisor/config/blob                         # rendered desired-state blob or pointer to CephFS path
    /debvisor/nodes//config/version      # last applied config version on the node
    /debvisor/nodes//config/last_applied_at # timestamp of last successful apply
    /debvisor/nodes//config/status       # OK | STALE | ERROR (+ optional error details)

## Health Metrics

- libvirt reachable

- Ceph `ceph -s` status parsed -> HEALTH_OK / WARN / ERR

- CPU/RAM pressure thresholds

- Network latency (gRPC round-trip to peers)

## RPC Endpoints

| Method | Description |
|--------|-------------|
| RegisterNode(NodeInfo) | Add/update node metadata |
| Heartbeat(Health) | Push health snapshot |
| ListNodes(Empty) | Enumerate cluster nodes |
| PrepareMigration(VMRef, Target) | Validate migration readiness |
| MigrateVM(VMMigrateSpec) | Execute live migration (libvirt) |
| FailoverVM(VMRef) | Promote or restart VM on alternate node |
| SnapshotRBD(VMRef, Label) | Create snapshot for VM disk |
| RollbackRBD(VMRef, Label) | Restore snapshot |
| SyncDirectory(Empty) | Refresh LDAP/AD cache |
| DispatchConfig(ConfigBlob) | Push config to nodes (versioned) |

## Migration Flow

1. `PrepareMigration` checks CPU flags, shared RBD access, network.

1. `MigrateVM`issues`virsh migrate --live --p2p --tunnelled` command.

1. Monitors progress (libvirt events); updates etcd status.

1. Finalizes by updating active node reference.

## Failover Flow

1. Heartbeats fail for source node.

1. Determine protected VMs (policy list).

1. Attempt `virsh list --all` via last known connection (optional fence).

1. Start VM on healthy node referencing same RBD volume.

## Security

- mTLS for all RPC calls.

- Role checks: only `debvisor-operator`and`debvisor-admin` groups can invoke migration/failover endpoints.

- Audit log appended with request metadata (user, timestamp, VM UUID, action).

## Roadmap

- Phase 1: Node registry, heartbeat, migratevm (Implemented).

- Phase 2: Failover orchestration & snapshots (Implemented).

- Phase 3: Config distribution & certificate rotation automation (Planned).

- Phase 4: Multi-cluster federation (stretch / geo replication) (Planned).
