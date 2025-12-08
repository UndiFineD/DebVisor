# DebVisor Monitoring - Complete Reference

This directory contains DebVisor's monitoring, observability, and synthetic testing infrastructure.

## Directory Structure

    monitoring/
    +-- README.md                          # This file
    +-- FIXTURES_GUIDE.md                 # Synthetic metrics fixtures guide
    +-- fixtures/                         # Optional synthetic metrics (labs only)
    |   +-- README.md
    |   +-- FIXTURES_GUIDE.md
    |   +-- edge-lab.yaml                # Lab environment fixture
    |   +-- edge-lab-deployment.yaml     # Lab environment generator
    |   +-- generator/                   # Synthetic metrics generator source
    |   +-- kustomize/                   # Environment-specific customization
    +-- grafana/                         # Grafana dashboards and provisioning
        +-- README.md
        +-- dashboards/                  # Dashboard JSON files
        +-- provisioning/
        |   +-- dashboards/              # Dashboard provisioning config
        |   +-- alerting/                # Alert rules (provisional)
        +-- manifests/                   # Kubernetes manifests (optional)

## Core Components

### 1. Prometheus

**Purpose:**Time-series metrics collection, storage, and querying

### DebVisor Integration

- Scrapes metrics from all cluster nodes (Node Exporter)
- Scrapes Kubernetes metrics (kube-state-metrics)
- Scrapes container metrics (cAdvisor)
- Scrapes Ceph cluster metrics (Ceph Exporter)
- Scrapes custom DebVisor metrics (RPC service, web panel)

### Default Configuration

- URL: [http://prometheus.debvisor-monitoring.svc:9090](http://prometheus.debvisor-monitoring.svc:9090)
- Retention: 30 days (configurable)
- Global scrape interval: 30 seconds
- Evaluation interval: 1 minute for alert rules

### Key Queries

## Node CPU usage

    100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])))

## Pod memory usage

    sum(container_memory_usage_bytes) by (pod_name)

## Ceph cluster usage

    ceph_cluster_used_bytes / ceph_cluster_capacity_bytes

## API latency (p95)

    histogram_quantile(0.95, rate(apiserver_request_duration_seconds_bucket[5m]))

## 2. Grafana

**Purpose:**Visualization and dashboarding for Prometheus data

### DebVisor Dashboards

| Dashboard | Purpose | Key Metrics |
|-----------|---------|-------------|
| `compliance-mfa-audit` | MFA compliance tracking | MFA status, audit events |
| `debvisor-dns-dashboard` | DNS service health | Query rates, resolution time |
| `debvisor-multitenant-dashboard` | Multi-tenant isolation | Resource usage per tenant |
| `dns-dhcp-overview` | DNS/DHCP operations | Zone transfers, DHCP leases |
| `multi-tenant-isolation` | Tenant network isolation | Traffic patterns, boundaries |
| `security-overview` | Security events and alerts | Alert firing, remediation status |

### Default Configuration [2]

- URL: [http://grafana.debvisor-monitoring.svc:3000](http://grafana.debvisor-monitoring.svc:3000)
- Datasource: Prometheus (UID: `prometheus-debvisor`)
- Default admin: `admin`/`admin` (change in production)

### Dashboard Provisioning

- Dashboards auto-loaded from `provisioning/dashboards/` on startup
- No manual import needed
- Compatible with dashboard-as-code workflows

### 3. Alertmanager

**Purpose:**Alert routing, grouping, and notification

### DebVisor Alert Receivers

| Receiver | Notification | Use Case |
|----------|--------------|----------|
| `email-ops` | Email to ops team | Critical infrastructure alerts |
| `slack-security` | Slack to security channel | Security events, remediations |
| `webhook-remediation` | HTTP webhook to Argo Workflows | Trigger automated remediation |
| `pagerduty` | PagerDuty incident | On-call escalation for critical issues |

### Alert Routing

    default receiver: email-ops
    +-- route: security-alerts
    |   +-- receiver: slack-security
    |       +-- match: alertname ~= "Security.*"
    +-- route: remediation-alerts
    |   +-- receiver: webhook-remediation
    |       +-- match: alertname ~= ".*Remediation.*"
    +-- route: critical
        +-- receiver: pagerduty
            +-- match: severity="critical"

### 4. Prometheus Alerting Rules

**Location:**`grafana/provisioning/alerting/`

### Rule Categories

| Category | Examples | Severity |
|----------|----------|----------|
| Infrastructure | Node down, disk full, memory pressure | Critical/Warning |
| Storage | Ceph health, ZFS pool degradation | Critical/Warning |
| Kubernetes | Pod crash loop, deployment not ready | Warning/Info |
| Network | DNS resolution failures, connectivity issues | Warning/Info |
| Security | MFA violations, unauthorized access attempts | Critical |
| Performance | API latency high, request rate high | Warning |

### Alert Propagation

    Metric Value Exceeds Threshold
        v
    Prometheus Evaluates Rule
        v
    Alert Fires (active for duration threshold)
        v
    Alertmanager Receives Alert
        v
    Alertmanager Routes to Receiver(s)
        v
    Notification Sent (email, Slack, webhook, etc.)
        v
    Optional: Auto-Remediation Triggered (via webhook to Argo Workflows)

## Monitoring Setup Paths

### Path 1: DebVisor-Provided Stack (Recommended for Labs)

Use DebVisor's Prometheus + Grafana + Alertmanager:

## Apply DebVisor monitoring stack

    kubectl apply -f opt/monitoring/manifests/prometheus.yaml
    kubectl apply -f opt/monitoring/manifests/grafana.yaml
    kubectl apply -f opt/monitoring/manifests/alertmanager.yaml

## Access Grafana

    kubectl port-forward svc/grafana 3000:3000 -n monitoring

## Open [http://localhost:3000,](http://localhost:3000,) login as admin/admin

## Pros

- Integrated with DebVisor dashboards out-of-box
- Minimal configuration needed
- Pre-configured alert rules

### Cons

- Single-node deployment (OK for labs)
- Limited to Prometheus (no multi-metrics backends)
- Requires Kubernetes cluster

### Path 2: External Prometheus/Grafana

Integrate with existing monitoring infrastructure:

## Configure Prometheus to scrape DebVisor targets

## Add scrape job

- job_name: 'debvisor-cluster'

        static_configs:

- targets:
- 'debvisor-prometheus:9090'
- 'debvisor-grafana:3000'

## Import DebVisor dashboards into your Grafana

## 1. Download JSON from opt/monitoring/grafana/dashboards/*.json

## 2. Import via Grafana UI: Home -> Import -> Paste JSON

## 3. Select datasource (your existing Prometheus)

## Pros [2]

- Centralized monitoring
- Integrates with existing tools
- Scalable to multiple clusters

### Cons [2]

- Manual setup and configuration
- Must sync dashboards manually
- Requires coordination with existing monitoring

### Path 3: Hybrid (DebVisor + External)

Run DebVisor monitoring, but integrate into central stack:

## Deploy DebVisor monitoring

    kubectl apply -f opt/monitoring/manifests/

## Configure central Prometheus to scrape DebVisor Prometheus

## Central Alertmanager routes to same channels

## Central Grafana queries DebVisor Prometheus

## Synthetic Testing (Labs Only)

For dashboard and alert testing without real workloads:

## Deploy synthetic metrics generator

    kubectl apply -f opt/monitoring/fixtures/edge-lab-deployment.yaml

## Generate high CPU scenario for 5 minutes

    kubectl set env deployment/synthetic-metrics \
      ALERT_SCENARIO=high_cpu -n monitoring
    sleep 300
    kubectl set env deployment/synthetic-metrics \
      ALERT_SCENARIO=none -n monitoring

## Cleanup

    kubectl delete -f opt/monitoring/fixtures/edge-lab-deployment.yaml

See [FIXTURES_GUIDE.md](FIXTURES_GUIDE.md) for detailed scenarios.

## Metrics Reference

### Standard Prometheus Metrics

### Node Exporter (Host Metrics)

    node_cpu_seconds_total
    node_memory_MemTotal_bytes
    node_memory_MemAvailable_bytes
    node_disk_io_time_seconds_total
    node_network_receive_bytes_total
    node_filesystem_avail_bytes

### cAdvisor (Container Metrics)

    container_cpu_usage_seconds_total
    container_memory_usage_bytes
    container_network_receive_bytes_total
    container_last_seen

### Kubernetes (kube-state-metrics)

    kube_node_status_ready
    kube_pod_status_phase
    kube_deployment_status_replicas_ready
    kube_statefulset_status_ready_replicas

### DebVisor-Specific Metrics

### RPC Service

    debvisor_rpc_requests_total
    debvisor_rpc_request_duration_seconds
    debvisor_rpc_errors_total
    debvisor_rpc_auth_failures_total

### Remediation (from Argo Workflows)

    debvisor_remediation_total
    debvisor_remediation_duration_seconds
    debvisor_remediation_failed_total
    debvisor_remediation_alerts_received_total

### Cluster Health

    debvisor_cluster_health_score
    debvisor_cluster_nodes_ready
    debvisor_cluster_storage_available_bytes

### Security

    debvisor_security_violations_total
    debvisor_audit_events_total
    debvisor_rbac_denials_total

## Best Practices

### Configuration

1.**Retention:**Set appropriate retention for your use case

- Labs: 7 days (minimize disk usage)
- Production: 30-90 days (regulatory requirements)

1.**Scrape Intervals:**Balance between granularity and load

- Default: 30 seconds (good for most cases)
- High-frequency: 10-15 seconds (more granular, higher load)
- Low-frequency: 1-2 minutes (minimum load, less granular)

1.**Alert Thresholds:**Tune based on your environment

- Don't copy thresholds from other clusters
- Start with defaults, adjust based on baselines
- Document why each threshold is set

### Alerting

1.**Alert Severity:**Use consistent severity levels

- Critical: Immediate action required
- Warning: Action needed within hours
- Info: Informational, no immediate action

1.**Alert Routing:**Send to appropriate receivers

- Critical -> On-call PagerDuty
- Security -> Security team Slack
- Infrastructure -> Ops team email

1.**Avoid Alert Fatigue:**

- Adjust thresholds to reduce false positives
- Group related alerts
- Use silence rules for known maintenance windows

### Dashboard Design

1.**Clarity:**Each panel should be self-explanatory

- Use descriptive titles
- Include units (e.g., "%", "MB/s")
- Document non-obvious panels in comments

1.**Hierarchy:**Organize panels logically

- Top: Overall cluster health
- Middle: Component status
- Bottom: Detailed metrics

1.**Updates:**Keep dashboards current

- Review quarterly for stale or missing metrics
- Update when new services added
- Archive outdated dashboards

## Troubleshooting

### No Data in Grafana

1.**Check Prometheus targets:**[http://prometheus:9090/targets](http://prometheus:9090/targets)
1.**Check scrape errors:**[http://prometheus:9090/graph](http://prometheus:9090/graph) -> query`up`
1.**Verify datasource:**Grafana -> Configuration -> Datasources
1.**Check dashboard JSON:**Ensure metric names are correct

### High Prometheus Memory Usage

1.**Check cardinality:**High-cardinality metrics use more memory

- Use `promtool analyze cardinality` to identify culprits
- Consider dropping labels or rewriting queries

1.**Reduce retention:**Lower `--storage.tsdb.retention.time`

1.**Disable unused scrape jobs:**Comment out unused targets

### Alert Not Firing

1.**Check rule evaluation:**[http://prometheus:9090/rules](http://prometheus:9090/rules)
1.**Verify metric exists:**[http://prometheus:9090/graph](http://prometheus:9090/graph) -> query metric name
1.**Check threshold:**Ensure current value exceeds alert threshold
1.**Check duration:**Alert must exceed `for:` duration before firing

### Alertmanager Not Sending Notifications

1.**Check Alertmanager status:**[http://alertmanager:9093](http://alertmanager:9093)
1.**Verify receiver config:**Check `alertmanager.yml` syntax
1.**Test webhook:**Use `curl` to post test alert to webhook receiver
1.**Check logs:**`kubectl logs deployment/alertmanager -n monitoring`

## Related Documentation

- [Grafana README](grafana/README.md) - Dashboard setup and datasources
- [Fixtures Guide](FIXTURES_GUIDE.md) - Synthetic metrics for testing
- [Prometheus Docs](https://prometheus.io/docs/) - Official Prometheus documentation
- [Grafana Docs](https://grafana.com/docs/grafana/latest/) - Official Grafana documentation
- [Alerting Best Practices](https://prometheus.io/docs/alerting/latest/best_practices/) - Alert design guidance

## Support

-**Issue:**File in main DebVisor repository
-**Documentation:**Check this README and linked guides
-**Dashboards:**See Grafana folder structure under `dashboards/`
-**Fixtures:**See `FIXTURES_GUIDE.md` for synthetic metrics testing

---

**Last Updated:**2025-11-26

**Status:**Monitoring infrastructure documented and ready for deployment

### Next Steps

1. Deploy monitoring stack to your cluster
1. Verify all targets are scraping successfully
1. Test Grafana dashboards with real or synthetic data
1. Configure alert notification channels
1. Test alert firing and remediation workflows
