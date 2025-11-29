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
