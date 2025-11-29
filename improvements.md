# DebVisor – Code Implementation Reference

**Last Updated:** November 29, 2025
**Status:** 20 service modules + 12 CI/CD workflows implemented. See `changelog.md` for history.

---

## Core Services

### RPC Service (`opt/services/rpc/`)

- `server.py` - gRPC server (mTLS, RBAC, audit logging)
- `auth.py`, `authz.py` - Authentication/authorization interceptors
- `proto/debvisor.proto` - API schema (NodeService, StorageService, MigrationService)

### Web Panel (`opt/web/panel/`)

- `app.py` - Flask application factory (CORS, CSP, rate limiting)
- `rbac.py` - Role-based access control (Admin/Operator/Developer/Viewer)
- `routes/` - Blueprints (nodes, storage, auth, passthrough)
- `models/` - SQLAlchemy ORM (User, Node, AuditLog)

### Multi-Region (`opt/services/multiregion/`)

- `core.py` - MultiRegionManager (replication, failover, health monitoring)
- `api.py` - Flask API (regions, resources, sync operations)
- `cli.py` - CLI commands (13 total: region/replication/failover management)

### Scheduler (`opt/services/scheduler/`)

- `core.py` - JobScheduler (cron expressions, dependencies, retry logic)
- `api.py` - REST API (job management, execution history)
- `cli.py` - CLI interface (schedule, execute, status, statistics)

### Anomaly Detection (`opt/services/anomaly/`)

- `core.py` - AnomalyDetectionEngine (ML baselines, trend analysis, alerts)
- `api.py` - Flask API (metrics, baselines, alerts, trends)
- `cli.py` - CLI (14 commands: metric/baseline/alert/system management)

### Backup Services

- `backup_manager.py` - BackupManager (ZFS/Ceph snapshots, policies, retention)
- `backup/backup_intelligence.py` - BackupIntelligence (dedup, SLA tracking, analytics)
- `backup/dedup_backup_service.py` - DedupBackupService (content-addressed storage)

### Cost Optimization (`opt/services/cost_optimization/`)

- `core.py` - CostOptimizer (resource cost tracking, recommendations)
- `api.py` - Flask API (cost reports, optimization suggestions)
- `cli.py` - CLI (analyze, report, optimize commands)

### Licensing (`opt/services/licensing/`)

- `licensing_server.py` - LicenseManager (hardware fingerprinting, feature gates)
- JWT-based license validation, expiration tracking

### Business Metrics (`opt/services/business_metrics.py`)

- BusinessMetrics class (counters, gauges, histograms)
- Prometheus exporter format

### Health Monitoring (`opt/services/health_check.py`)

- HealthCheckFramework (binaries, services, connectivity, resources)
- JSON/table report formats

---

## Infrastructure Components

### Network Configuration (`opt/netcfg-tui/`)

- `main.py` - NetworkConfigTUI (curses interface, systemd-networkd/netplan backends)
- `backends.py` - NetworkBackend abstraction (systemd-networkd, NetworkManager, netplan)
- `netcfg_tui.py` - Legacy TUI (bridge/bond/VLAN/WiFi configuration)

### Certificate Management (`opt/cert_manager.py`)

- CertificateAuthority - Internal CA creation/management
- CertificateManager - Service certificate issuance, rotation, reload hooks

### Configuration Distribution (`opt/config_distributor.py`)

- ConfigVersion - Versioned configuration with checksums
- Config synchronization across nodes

### Authentication (`opt/oidc_oauth2.py`)

- OIDCProvider - OAuth2/OIDC authentication
- JWTManager - Token generation/validation
- RBACManager - Role/permission management
- SessionManager - Session tracking

### Security Testing (`opt/security_testing.py`)

- OWASPTop10Checker - OWASP vulnerability scanning
- SecurityTestSuite - Comprehensive security validation

### Advanced Features (`opt/advanced_features.py`)

- IntegrationManager - External system integrations (Prometheus, ELK, Datadog)
- Health check functions, monitoring integrations

---

## Monitoring & Observability

### Grafana (`opt/grafana/`)

- `dashboards/*.json` - 7 dashboards (overview, DNS/DHCP, security, compliance, Ceph, multi-tenant)
- `provisioning/` - Datasources, alerting, notification channels

### Prometheus (`opt/monitoring/`)

- `prometheus/prometheus.yml` - Scrape configs
- `fixtures/generator/app.py` - Synthetic metrics generator
- `rules/` - Recording/alerting rules

### RPC Monitoring (`opt/services/rpc/monitoring.py`)

- Prometheus metrics (RPC requests, cache hits, TLS expiry, gRPC streams)

---

## Automation & CI/CD

### GitHub Workflows (`.github/workflows/`)

- `codeql.yml` - Python/JavaScript security scanning
- `secret-scan.yml` - TruffleHog secret detection (6h + PR)
- `test.yml` - Coverage gate (85%), mutation testing, parallel execution, health dashboard
- `lint.yml` - SARIF export (flake8, pylint, mypy)
- `release.yml` - Docker build, Trivy scan, GPG signing, SLSA attestation
- `performance.yml` - Benchmark regression detection (110% threshold)
- `release-please.yml` - Automated changelog generation

### Scripts

- `scripts/pylint_to_sarif.py` - pylint JSON → SARIF converter
- `scripts/action_audit.py` - GitHub Actions version auditing
- `scripts/sbom_diff.py` - SBOM dependency change detection
- `opt/validate-components.sh` - Component validator

---

## Data Models

### Multi-Region (`opt/services/multiregion/core.py`)

```python
Region(region_id, name, location, api_endpoint, status, capacity_vms, latency_ms)
ReplicatedResource(resource_id, type, primary_region, replica_regions)
FailoverEvent(event_id, from_region, to_region, strategy, success)
ReplicationConfig(source_region, target_region, resource_types, sync_interval)
```text

### Scheduler (`opt/services/scheduler/core.py`)

```python
ScheduledJob(job_id, name, command, cron_expression, priority, timeout, dependencies)
JobExecutionResult(job_id, start_time, end_time, status, exit_code, output)
JobDependency(job_id, dependency_id, type: REQUIRE|CONFLICT)
```text

### Anomaly Detection (`opt/services/anomaly/core.py`)

```python
Metric(id, name, type, value, timestamp, tags)
Baseline(metric_name, mean, std_dev, percentiles, samples, last_updated)
Alert(id, metric_name, severity, value, threshold, status)
TrendAnalysis(metric_name, direction, confidence, slope)
```text

---

## CLI Commands

**Scheduler**: `schedule`, `execute`, `status`, `history`, `stats`, `cancel`, `enable/disable`
**Anomaly**: `metric add/get/list/delete`, `baseline create/update/get/auto`, `alert list/ack/resolve`, `trend analyze/list`, `system stats/config/export/import`
**Multi-Region**: `region add/list/update/remove/health`, `replication setup/status/sync`, `failover execute/history/test`
**Cost**: `analyze`, `report`, `optimize`

---

## Configuration Files

- `/etc/debvisor-profile` - Storage profile (ceph/zfs/mixed)
- `/etc/debvisor-addons.conf` - Addon flags (RPC_SERVICE, WEB_PANEL, VNC_CONSOLE, MONITORING_STACK)
- `/etc/debvisor/rpc/config.json` - RPC server configuration
- `/etc/debvisor/regions/multiregion.db` - Multi-region state (SQLite)
- `/etc/systemd/system/debvisor-*.service` - Systemd services

---

## Future Enhancements

- AI-assisted operational runbooks
- Continuous compliance auto-remediation
- Carbon/energy telemetry (power + thermal sensors)
- Multi-hypervisor support (Xen integration)
- Marketplace governance & vulnerability scoring
- ACME Let's Encrypt certificates (auto-renewal)
- Customer DNS hosting (DebVisor.com domain)
- Enhanced SSH hardening profiles (MFA by default, root login prevention)

---

## 🔥 High-Priority Improvements (Session 12)

### Security Enhancements

**AUTH-001**: Implement API key rotation mechanism
- Location: `opt/services/rpc/auth.py`, `opt/oidc_oauth2.py`
- Add automatic key expiration (90 days)
- Implement key rotation workflow with overlap period
- Add audit logging for key usage and rotation

**AUTH-002**: Add rate limiting to authentication endpoints
- Location: `opt/web/panel/app.py`, `opt/services/rpc/server.py`
- Implement sliding window rate limiting
- Add exponential backoff on failed attempts
- Configure per-IP and per-user limits

**CRYPTO-001**: Upgrade to TLS 1.3 only
- Location: `opt/cert_manager.py`, `opt/services/rpc/server.py`
- Remove TLS 1.2 support
- Update cipher suites to TLS 1.3 only
- Add certificate transparency logging

**SECRET-001**: Implement secrets management service
- Location: New `opt/services/secrets/`
- HashiCorp Vault integration
- Encrypted secret storage
- Secret rotation automation
- Audit trail for secret access

**RBAC-001**: Add fine-grained permission system
- Location: `opt/web/panel/rbac.py`, `opt/services/rpc/authz.py`
- Implement resource-level permissions (beyond CRUD)
- Add conditional permissions (time-based, IP-based)
- Support permission inheritance

### Performance Optimizations

**PERF-001**: Add connection pooling to RPC client
- Location: `opt/web/panel/core/rpc_client.py`
- Implement gRPC channel pool (min: 2, max: 10)
- Add connection health checking
- Implement circuit breaker pattern

**PERF-002**: Add database query optimization
- Location: `opt/services/multiregion/core.py`, `opt/services/scheduler/core.py`
- Add indexes on frequently queried columns
- Implement query result caching (Redis)
- Add query execution time logging

**PERF-003**: Implement async operations for I/O-bound tasks
- Location: `opt/services/backup_manager.py`, `opt/services/multiregion/core.py`
- Convert sync database calls to async
- Add asyncio task queues for background jobs
- Implement batch processing for bulk operations

**CACHE-001**: Add distributed caching layer
- Location: New `opt/services/cache/`
- Redis integration for session storage
- Cache frequently accessed configuration
- Implement cache invalidation strategy

**METRICS-001**: Add performance metrics collection
- Location: All service modules
- Add request/response time tracking
- Implement percentile metrics (p50, p95, p99)
- Add slow query logging

### Testing & Quality

**TEST-001**: Increase unit test coverage to 90%
- Location: `tests/`
- Add tests for error paths
- Add edge case coverage
- Implement property-based testing (Hypothesis)

**TEST-002**: Add integration test suite
- Location: New `tests/integration/`
- Multi-service integration tests
- End-to-end workflow testing
- Database migration testing

**TEST-003**: Implement load testing framework
- Location: Enhance `tests/load_testing.js`
- Add realistic user scenarios
- Implement ramp-up/ramp-down patterns
- Add concurrent user simulation

**TEST-004**: Add contract testing
- Location: `tests/test_contracts.py`
- Implement NotImplementedError methods
- Add Pact consumer/provider testing
- Validate API compatibility

**CHAOS-001**: Enhance chaos engineering tests
- Location: `tests/test_chaos_engineering.py`
- Add network latency injection
- Implement partial outage scenarios
- Add dependency failure simulation

### Documentation

**DOC-001**: Add API versioning strategy
- Location: `opt/web/panel/`, `opt/services/rpc/`
- Document breaking change policy
- Add deprecation guidelines
- Implement sunset period (6 months)

**DOC-002**: Create troubleshooting runbooks
- Location: New `docs/runbooks/`
- Common failure scenarios
- Step-by-step resolution procedures
- Escalation paths

**DOC-003**: Add architecture decision records (ADRs)
- Location: New `docs/adr/`
- Document key technical decisions
- Rationale and tradeoffs
- Alternative approaches considered

**DOC-004**: Create deployment playbooks
- Location: `docs/deployment/`
- Production deployment checklist
- Rollback procedures
- Health check validation

### Observability

**OBS-001**: Add distributed tracing
- Location: `opt/distributed_tracing.py` (enhance)
- Implement OpenTelemetry instrumentation
- Add cross-service trace correlation
- Integrate with Jaeger/Zipkin

**OBS-002**: Enhance structured logging
- Location: All service modules
- Add correlation IDs to all logs
- Implement log level filtering per component
- Add structured fields (user_id, request_id, etc.)

**OBS-003**: Add custom Grafana dashboards
- Location: `opt/grafana/dashboards/`
- Service-level SLI/SLO dashboards
- Error rate and latency percentile dashboards
- Capacity planning dashboards

**ALERT-001**: Implement intelligent alerting
- Location: `opt/monitoring/prometheus/alerts/`
- Add alert fatigue reduction (deduplication)
- Implement alert severity levels
- Add on-call rotation integration

### Features

**FEAT-001**: Implement WebSocket real-time updates
- Location: `opt/web/panel/socketio_server.py` (enhance NotImplementedError)
- Real-time VM status updates
- Live metrics streaming
- Chat/notification system

**FEAT-002**: Add multi-tenancy support
- Location: `opt/core/unified_backend.py`
- Tenant isolation at data layer
- Per-tenant resource quotas
- Tenant-specific RBAC

**FEAT-003**: Implement backup compression
- Location: `opt/services/backup/dedup_backup_service.py`
- Add zstd compression algorithm
- Implement compression level tuning
- Add decompression streaming

**FEAT-004**: Add IPv6 support
- Location: `opt/netcfg-tui/`, `opt/services/security/firewall_manager.py`
- IPv6 address configuration
- Dual-stack support
- IPv6 firewall rules

**FEAT-005**: Implement plugin architecture
- Location: `opt/plugin_architecture.py` (complete stubs)
- Plugin discovery and loading
- Plugin lifecycle management
- Plugin API versioning

### Code Quality

**REFACTOR-001**: Remove code duplication
- Location: `opt/services/*/cli.py`
- Extract common CLI argument parsing
- Create shared table formatting utilities
- Standardize error handling

**REFACTOR-002**: Modernize Python code
- Location: All Python files
- Replace `datetime.utcnow()` with `datetime.now(timezone.utc)`
- Use `match` statements (Python 3.10+) where appropriate
- Add missing type hints

**REFACTOR-003**: Implement dependency injection
- Location: `opt/services/*/core.py`
- Remove hard-coded dependencies
- Add configuration injection
- Improve testability

**TYPE-001**: Achieve 100% type hint coverage
- Location: All Python modules
- Add missing return type annotations
- Add parameter type hints
- Use Protocol for duck typing

### Infrastructure

**INFRA-001**: Add health check endpoints
- Location: All service APIs
- Implement `/health/live` (liveness probe)
- Implement `/health/ready` (readiness probe)
- Add dependency health checks

**INFRA-002**: Implement graceful shutdown
- Location: `opt/web/panel/graceful_shutdown.py` (complete stubs)
- Drain in-flight requests before shutdown
- Close database connections gracefully
- Implement shutdown timeout (30s)

**INFRA-003**: Add configuration validation
- Location: All services
- Validate config on startup
- Fail fast on invalid configuration
- Add config schema documentation

**DB-001**: Implement database migrations
- Location: New `opt/migrations/`
- Use Alembic for schema migrations
- Add migration testing
- Implement rollback support

### Compliance & Audit

**AUDIT-001**: Enhanced audit logging
- Location: All services
- Add immutable audit log storage
- Implement log signing/verification
- Add regulatory compliance tags (GDPR, HIPAA)

**COMPLY-001**: Add compliance reporting
- Location: New `opt/services/compliance/`
- Generate compliance reports (GDPR, SOC2, HIPAA)
- Add compliance dashboard
- Implement policy enforcement

---
