# Deployment Matrix & CI/CD Pipeline

## Overview

This document defines the build matrix, test suite, and deployment pipeline for DebVisor.

## Build Matrix

### ISO Builds

| OS | Architecture | Status | Notes |
|----|--------------|--------|-------|
| Debian 13 | amd64 | Supported | Alternative |

### Docker Images

| Image | Tags | Platforms | Status |
|-------|------|-----------|--------|
| debvisor/rpcd | latest, v1.0, arm64v8 | amd64, arm64 | Production |
| debvisor/panel | latest, v1.0, arm64v8 | amd64, arm64 | Production |
| debvisor/health-check | latest, v1.0 | amd64, arm64 | Stable |

## CI/CD Pipeline

### Build Pipeline

    +-----------------+
    |   Git Event     |
    |   (push/PR)     |
    +--------+--------+
             |
        +----?----+
        | Lint    | (5 min)
        | Tests   |
        +----+----+
             |
        +----?----+
        | Build   | (parallelized)
        | Matrix  |
        +----+----+
             |
      +------+------+
      |      |      |
    +-?--+ +--?--+ +--?--+
    |ISO | |Dock-| | Pkg |
    |amd64 ||ers  | |List |
    +------++------++------+
             |      |
        +----?------?----+
        | Integration    | (20 min)
        | Tests (Docker) |
        +----+-----------+
             |
        +----?----+
        | Deploy  |
        | Staging | (15 min)
        +----+----+
             |
        +----?----+
        | E2E     |
        | Tests   | (30 min)
        +----+----+
             |
        +----?------------------------+
        | Approval (manual gate)       |
        | for production deployment    |
        +----+-------------------------+
             |
        +----?----+
        | Deploy  |
        | Prod    | (20 min)
        +---------+

### Parallel Build Jobs

| Job | Duration | Trigger | Artifacts |
|-----|----------|---------|-----------|
|**Lint**| 5 min | Commit | Report |
|**Unit Tests**| 10 min | Commit | Coverage |
|**Security Scan**| 5 min | Commit | Report |
|**ISO (amd64)**| 20 min | Tag | ISO + checksum |
|**ISO (arm64)**| 25 min | Tag | ISO + checksum |
|**Docker (amd64)**| 15 min | Commit | Image:tag |
|**Docker (arm64)**| 20 min | Commit | Image:tag |
|**Package Validation**| 5 min | Commit | Report |

### Test Suite

#### Unit Tests

## Language: Python

## Framework: pytest

## Coverage: >80%

    pytest opt/services/rpc/tests/
    pytest opt/web/panel/tests/
    pytest opt/build/tests/

## Coverage

- RPC: gRPC handlers, auth, rate limiting
- Panel: REST handlers, RBAC, audit logging
- Build: ISO generation, package validation
- Config: Preseed generation, variable substitution

### Integration Tests

## Method: Docker Compose

## Scope: Multi-container interactions

## RPC + Database + Monitoring

    docker-compose -f tests/docker-compose.yml up

## Test: RPC service responds to requests

## Test: Metrics exported to Prometheus

## Test: Audit logs written to database

## Ansible Tests

## Method: Molecule + Docker

## Scope: Playbook execution in isolated containers

    cd opt/ansible
    molecule test

## Platforms tested: ubuntu-22.04, debian-12

## Roles tested: all roles in opt/ansible/roles/

## Validation: Idempotence, service startup

## End-to-End Tests (Staging/Prod)

## Scope: Full system tests against deployed environment

## 1. Node provisioning

    debvisor-provision-node --host staging-node-1 --profile ceph

## 2. Cluster health

    cephctl health
    hvctl nodes
    k8sctl nodes

## 3. Web panel

    curl -u admin:password [https://staging-panel.local/api/health](https://staging-panel.local/api/health)

## 4. RPC service

    grpcurl -plaintext localhost:5000 debvisor.Node/Status

## 5. Backup/restore

    debvisor-backup --path /backup/staging-$(date +%Y%m%d)
    debvisor-restore --path /backup/staging-20240101

## Deployment Environments

### Staging Cluster

**Purpose:**Pre-production validation

### Configuration

- 3 nodes (ceph config: 1 mon, 2 osds)
- Kubernetes: 1 control plane, 2 workers
- Monitoring: Prometheus + Grafana

### Deployment

- Automatic on merge to main
- Manual promotion from main branch

### Testing

- Full E2E test suite
- Load testing (100 concurrent users)
- Chaos testing (kill pods, drain nodes)

### Production Cluster

**Purpose:**Production infrastructure

### Configuration [2]

- 5+ nodes minimum
- Ceph replication factor: 3
- Kubernetes: 3 control plane, N workers

### Deployment [2]

- Manual approval required
- Canary deployment (1 node first)
- Blue-green swap with health checks
- Automatic rollback on failure

### SLO

- 99.99% uptime
- <100ms p99 latency
- <1s recovery on node failure

## Release Process

### Versioning

Semantic versioning: `MAJOR.MINOR.PATCH`

-**MAJOR**: Breaking changes (API, storage format)
-**MINOR**: New features, backward compatible
-**PATCH**: Bug fixes

### Release Branches

    main
      +-- v1.0 (release branch)
      |    +-- v1.0.0 (tag - release)
      |    +-- v1.0.1 (patch)
      |    +-- v1.0.2 (patch)
      +-- v1.1
           +-- v1.1.0 (tag - release)
           +-- ...

### Release Checklist

- [ ] Changelog complete and reviewed
- [ ] All tests pass
- [ ] Security scanning: no critical issues
- [ ] Documentation updated
- [ ] Performance benchmarks documented
- [ ] Upgrade path tested
- [ ] Rollback procedure documented
- [ ] Tags created and signed
- [ ] Artifacts built and checksummed
- [ ] Release notes published
- [ ] Monitoring alerts configured
- [ ] Runbooks created

## Monitoring & Observability

### Prometheus Metrics

## Build metrics

    debvisor_build_duration_seconds{arch="amd64", os="ubuntu-22.04"}
    debvisor_build_status{arch="amd64", os="ubuntu-22.04", status="success"}
    debvisor_build_package_count{arch="amd64"}

## Deployment metrics

    debvisor_deployment_duration_seconds{environment="staging"}
    debvisor_deployment_status{environment="staging", status="success"}
    debvisor_deployment_rollback_total{environment="prod"}

## System metrics

    debvisor_node_count{cluster="prod"}
    debvisor_cluster_health{cluster="prod", status="healthy"}
    debvisor_rpc_request_duration_seconds{method="RegisterNode", quantile="0.99"}

## Alerting

### Critical Alerts

- Build failure rate > 10%
- Deployment failure
- Production cluster unhealthy
- RPC service latency > 1s p99

### Warnings

- Build duration > 30 min
- Test coverage < 80%
- Security scan: medium issues found

## Performance Benchmarks

### Build Performance

| Component | Duration | Target | Status |
|-----------|----------|--------|--------|
| ISO (amd64) | 20 min | <30 min | ? |
| ISO (arm64) | 25 min | <30 min | ? |
| Docker build | 15 min | <20 min | ? |
| Tests | 15 min | <20 min | ? |
|**Total pipeline**| ~45 min | <60 min | ? |

### RPC Service Performance

| Operation | Latency p99 | Throughput | Status |
|-----------|-------------|-----------|--------|
| RegisterNode | <100ms | 100 nodes/s | ? |
| GetStatus | <50ms | 1000 qps | ? |
| UpdateConfig | <200ms | 50 nodes/s | ? |

### Web Panel Performance

| Operation | Latency p99 | Connections | Status |
|-----------|-------------|-------------|--------|
| Login | <200ms | 100 concurrent | ? |
| List nodes (1000) | <500ms | 100 concurrent | ? |
| Dashboard render | <1s | 100 concurrent | ? |

## Scaling Capabilities

### Cluster Sizes

| Size | Nodes | Services | Status |
|------|-------|----------|--------|
| Small | 3-5 | Single zone | Supported |
| Medium | 5-20 | Multi-zone | Supported |
| Large | 20-100 | Multi-region | Supported |
|**XL**| 100-1000 | Large deployment | Experimental |

### Large cluster optimization (Phase 5)

- Virtual scrolling in UI
- Lazy loading of components
- Batch API operations
- Result pagination

## Disaster Recovery

### Backup Strategy

- Daily snapshots: RBD volumes
- Hourly: Configuration changes
- Real-time: Audit logs to external silo

### Recovery Targets

| Scenario | RTO | RPO |
|----------|-----|-----|
| Single node failure | <5 min | <1 min |
| Database failure | <15 min | <5 min |
| Cluster failure | <1 hour | <15 min |
| Data center failure | <4 hours | <1 hour |

### Testing [2]

- Backup validation: Weekly full restore test
- Failover drills: Monthly
- Chaos engineering: Continuous

## References

- ISO Build: `opt/build/README.md`
- Ansible: `opt/ansible/ANSIBLE_GUIDE.md`
- RPC Service: `opt/services/rpc/ADVANCED_FEATURES.md`
- Web Panel: `opt/web/panel/ADVANCED_FEATURES.md`
