# DebVisor Architecture Overview

## System Design

### High-Level Architecture

    +--------------------------------------------------+
    |  User Layer                                       |
    |  +--------------------------------------------+  |
    |  |  Web UI (React)                            |  |
    |  |  Admin Dashboard * Cluster Management      |  |
    |  |  Real-time Notifications * Reports         |  |
    |  +--------------------------------------------+  |
    +--------------+-----------------------------------+
                   | HTTPS / WebSocket
    +--------------?-----------------------------------+
    |  API Layer                                        |
    |  +--------------------------------------------+  |
    |  |  REST API (Flask)                          |  |
    |  |  * Input validation & sanitization         |  |
    |  |  * RBAC & authentication                   |  |
    |  |  * Rate limiting & caching                 |  |
    |  |  * Audit logging                           |  |
    |  +--------------------------------------------+  |
    +--------------+-----------------------------------+
                   | gRPC / mTLS
    +--------------?-----------------------------------+
    |  Service Layer                                    |
    |  +--------------------------------------------+  |
    |  |  RPC Service (gRPC)                        |  |
    |  |  * Connection pooling                      |  |
    |  |  * Request compression                     |  |
    |  |  * API versioning                          |  |
    |  |  * Health checks                           |  |
    |  |  * Monitoring integration                  |  |
    |  +--------------------------------------------+  |
    +--------------+-----------------------------------+
                   | Native APIs
    +--------------?-----------------------------------+
    |  Infrastructure Layer                             |
    |  +--------------+ +--------------+ +---------+  |
    |  |    Ceph      | | Kubernetes   | | libvirt |  |
    |  |  (Storage)   | | (Orchestr.)  | | (VM)    |  |
    |  +--------------+ +--------------+ +---------+  |
    +----------------------------------------------------+

### Data Flow

### Example: Node Registration

    1. User clicks "Register Node" in Web Panel

       v

    1. Panel validates input

       v

    1. Panel sends REST request to API

       v

    1. API validates, audits, and calls RPC service

       v

    1. RPC service contacts Ceph, K8s, libvirt APIs

       v

    1. Results aggregated and returned via API

       v

    1. Web Panel updates UI with results

## Component Details

### 1. Web Panel (Frontend & API)

### Technology Stack

- Frontend: React, TypeScript

- Backend: Flask, SQLAlchemy

- Database: PostgreSQL / SQLite

- Cache: Redis

- Auth: OAuth2, LDAP/AD, local accounts

### Capabilities

- Cluster overview dashboard

- Node management (register, drain, reboot)

- Storage pool management (Ceph)

- VM management (libvirt)

- Kubernetes workload management

- User and RBAC management

- Audit log viewing

- Reports and exports (PDF, CSV)

### Security

- HTTPS with TLS 1.2+

- Input validation on all endpoints

- RBAC (admin, operator, viewer roles)

- CSRF protection

- Rate limiting (10 req/s per user)

- Session timeout (15 min idle)

- Audit logging of all operations

### 2. RPC Service

### Technology Stack [2]

- Framework: gRPC

- Language: Python

- Serialization: Protocol Buffers

- Transport: HTTP/2 with TLS

### Capabilities [2]

- Node management operations

- Status queries

- Configuration updates

- Batch operations

- Health monitoring

- Metrics export (Prometheus)

### Features

- mTLS authentication (node certs)

- Connection pooling (50 max)

- Request compression (GZIP/Brotli)

- API versioning (V1, V2, V3)

- Rate limiting per client

- Distributed tracing (OpenTelemetry)

### Monitoring

- Request latency metrics

- Error rate tracking

- Connection pool stats

- Compression ratios

### 3. Health Check Service

### Technology Stack [3]

- Language: Python

- Schedule: Systemd timer

### Monitors

- Service availability (RPC, Panel, cluster services)

- Network connectivity

- Storage health

- System resources

- DNS resolution

- Certificate expiration

### Actions

- Emit alerts to monitoring

- Log to audit trail

- Auto-remediation (restart services)

### 4. Storage Backend

### Supported Options

### Ceph (Recommended)

- Object storage (RBD)

- Filesystem (CephFS)

- Object Gateway (S3-compatible)

- Replication factor: 3 (configurable)

- Erasure coding support

### ZFS (Alternative)

- Local storage

- Copy-on-write semantics

- Snapshots and cloning

- RAID-Z (distributed parity)

- Single-node or HA configurations

### Hybrid

- Ceph for cluster-wide storage

- ZFS for local caching/performance

### 5. Orchestration (Kubernetes)

### Components

- Control plane: etcd, API server, scheduler, controller

- Worker nodes: kubelet, container runtime

- Networking: Calico, Flannel, or Weave

- Storage: Ceph RBD, CephFS, or local storage

- Ingress: nginx-ingress or HAProxy

### Workloads

- Stateless applications (deployments)

- Stateful applications (StatefulSets)

- Batch jobs (Jobs, CronJobs)

- Daemon workloads (DaemonSets)

### 6. Virtualization (libvirt)

### Hypervisor Options

- QEMU/KVM (Linux)

- Xen (alternative)

### Management

- Domain (VM) lifecycle

- Network bridge management

- Storage volume management

- Snapshot and cloning

- Live migration

### 7. Networking

### Network Architecture

    External Network (Internet)
        v VPN/Direct
    Public Zone (Firewall)
        +- Web Panel (HTTPS)
        +- SSH
        +- Ingress Controllers
        v Internal Network
    Internal Zone (OpenFlow)
        +- RPC Service (gRPC)
        +- Kubernetes API
        +- Ceph Network
        +- libvirt Network

### Features [2]

- VLANs for tenant isolation

- Bonding for HA

- VXLAN overlay networks

- IPv6 support

- DNS resolution (Bind9 HA)

- DHCP with PXE boot

### 8. Monitoring & Observability

### Metrics Collection

- Prometheus: Time-series metrics

- Node Exporter: System metrics

- Custom exporters: Application-specific

### Dashboards

- Grafana: Visualization and alerting

- Custom dashboards for each component

### Logging

- Systemd journal (local)

- Centralized log aggregation (optional)

- Audit trail for compliance

### Tracing

- OpenTelemetry instrumentation

- Jaeger or Zipkin for visualization

## Deployment Models

### Single-Node (Lab)

    Node: All-in-One
    +- Web Panel
    +- RPC Service
    +- Ceph MON + OSD
    +- Kubernetes (single node)
    +- libvirt (VMs)

- *Use Case:**Development, testing, small deployments

- *Limitations:**No HA, no geographic distribution

### Multi-Node Cluster (Standard)

    Control Nodes (3):         Worker Nodes (N):
    +- Web Panel               +- RPC Service
    +- RPC Service             +- Kubernetes
    +- Ceph MON                +- libvirt
    +- K8s Control Plane       +- Storage (Ceph OSD)
    +- DNS (Primary)
    Storage Nodes (optional):
    +- Ceph OSD (dedicated)

- *Use Case:**Production clusters, HA setup

- *Features:**Redundancy, load balancing, geographic expansion

### Multi-Site (Advanced)

    DC1:                       DC2:
    +- Control + Storage       +- Control + Storage
    +- Kubernetes              +- Kubernetes
    +- VMs                     +- VMs
        v Replication (Ceph)
        v Federation (K8s)

- *Use Case:**DR, geo-distribution, failover

- *Features:**Cross-site replication, automated failover

## Security Architecture

### Layers

    +-------------------------------------+
    | Application Layer                    |
    | * Input validation                   |
    | * RBAC enforcement                   |
    | * Audit logging                      |
    +-------------------------------------+
            v TLS/mTLS
    +-------------------------------------+
    | Transport Layer                      |
    | * Encryption (TLS 1.2+)             |
    | * Certificate validation             |
    | * Perfect forward secrecy           |
    +-------------------------------------+
            v Firewall rules
    +-------------------------------------+
    | Network Layer                        |
    | * Segmentation (VLANs)              |
    | * Access control lists              |
    | * DDoS protection                   |
    +-------------------------------------+

### Authentication & Authorization

### Authentication Methods

- Local accounts (username/password)

- OAuth2 (Google, GitHub, custom)

- LDAP/AD (enterprise)

- API keys (service accounts)

### Authorization (RBAC)

| Role | Permissions |
|------|-----------|
|**Admin**| All operations, user management |
|**Operator**| Cluster operations, no user/RBAC changes |
|**Viewer**| Read-only access to dashboards |
|**Developer**| Kubernetes workload deployment |

### Audit Trail

- All operations logged (user, timestamp, action)

- Immutable log storage

- Compliance-ready exports

## Performance Characteristics

### Scalability

| Metric | Value | Notes |
|--------|-------|-------|
| Max nodes | 1000+ | With large cluster optimization |
| Node registration rate | 100/sec | Batched operations |
| Status query rate | 1000 qps | Cached, <100ms latency |
| Config update rate | 50/sec | Per-node |
| Concurrent users | 100+ | Depends on cluster size |

### Latency (p99)

| Operation | Latency |
|-----------|---------|
| Web login | <200ms |
| Dashboard load | <1s |
| Node status | <100ms |
| Configuration apply | <500ms |
| Cluster query | <200ms |

### Resource Usage

### Per Node

- CPU: 1-2 cores (RPC service)

- RAM: 2-4 GB (Panel + RPC)

- Storage: 50 GB (logs, database, cache)

### Total HA Pair

- CPU: 4 cores

- RAM: 8 GB

- Storage: 200 GB

## High Availability

### Components [2]

### Stateless

- Web Panel (multiple instances, load balanced)

- RPC Service (multiple instances, gRPC LB)

- Health Check (distributed)

### Stateful

- Database (PostgreSQL HA with replication)

- Cache (Redis with Sentinel)

- Ceph (distributed, self-healing)

### Failover

### Automatic (< 1 second)

- Node health check failure

- Service unresponsive

- Network partition recovery

### Manual (< 5 minutes)

- Complete node failure

- Data center failure

- Planned maintenance

### Recovery

- Lost node: Rejoin with Ceph rebalancing

- Lost pod: Kubernetes reschedules

- Lost database: Restore from replicas

- Lost VM: Snapshot/clone recovery

## Integration Points

### External Systems

- **LDAP/AD**: User authentication

- **Webhook receivers**: Event notifications

- **Syslog servers**: Log forwarding

- **SNMP traps**: Legacy monitoring

- **S3 storage**: Backup destinations

- **Email/Slack**: Alerting

### APIs

- **gRPC**: Service-to-service communication

- **REST**: Client applications

- **Kubernetes API**: K8s workload management

- **Ceph API**: Storage operations

- **libvirt URI**: VM management

- **systemd D-Bus**: Service management

## References

- Component details: `opt/services/rpc/ADVANCED_FEATURES.md`

- Deployment: `opt/DEPLOYMENT_MATRIX.md`

- Networking: `opt/docs/networking.md`

- Security: Configuration audit guide
