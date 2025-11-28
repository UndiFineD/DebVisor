# opt/grafana/ - Grafana Dashboards and Provisioning

## Overview

The `opt/grafana/` directory contains Grafana dashboard templates, provisioning configurations, and dashboarding standards for DebVisor cluster monitoring. Grafana serves as the visualization layer for Prometheus metrics, providing operators with real-time visibility into cluster health, performance, and security.

__Key Responsibility:__Provide consistent, reusable, and maintainable Grafana dashboards for multi-tenant, multi-cluster DebVisor deployments.

## Directory Structure

    opt/grafana/
    ├── README.md                          # This file - Grafana overview and standards
    ├── dashboards/                        # Grafana dashboard definitions (JSON)
    │   ├── 00-index.json                  # Dashboard index and navigation
    │   ├── overview.json                  # System overview dashboard
    │   ├── dns-dhcp.json                  # DNS/DHCP health and performance
    │   ├── security.json                  # Security metrics and events
    │   ├── compliance.json                # Compliance audit and access tracking
    │   ├── ceph.json                      # Ceph cluster health
    │   ├── kubernetes.json                # Kubernetes cluster status
    │   ├── networking.json                # Network performance and connectivity
    │   ├── storage-performance.json        # Storage I/O and latency
    │   ├── alerts-summary.json            # Active alerts and history
    │   └── templates/                     # Dashboard templates and examples
    │       ├── DASHBOARD_TEMPLATE.json    # Blank dashboard scaffold
    │       ├── MULTI_CLUSTER.json         # Multi-cluster dashboard pattern
    │       ├── SINGLE_TENANT.json         # Single-tenant monitoring template
    │       └── CUSTOM_METRICS.json        # Custom metric visualization template
    ├── provisioning/                      # Grafana provisioning configuration
    │   ├── dashboards.yaml                # Dashboard provisioning config
    │   ├── datasources.yaml               # Datasource provisioning config
    │   ├── alert-notification-channels/   # Alert notification configurations
    │   │   ├── email.yaml                 # Email notifications
    │   │   ├── slack.yaml                 # Slack integration
    │   │   ├── pagerduty.yaml             # PagerDuty integration
    │   │   ├── webhook.yaml               # Custom webhook
    │   │   └── README.md                  # Notification setup guide
    │   ├── alert-rules/                   # Alert rule configurations
    │   │   ├── prometheus.yaml            # Prometheus alerting rules
    │   │   ├── grafana-native.yaml        # Grafana native alerts
    │   │   └── README.md                  # Alert rules documentation
    │   └── README.md                      # Provisioning overview
    ├── DASHBOARD_STANDARDS.md             # Dashboard design and consistency guidelines
    ├── IMPLEMENTATION_GUIDE.md            # How to create new dashboards
    └── TROUBLESHOOTING.md                 # Common Grafana issues and solutions

## Dashboard Library

### System Overview Dashboard (overview.json)

__Purpose:__Comprehensive system health snapshot.

### Layout

-__Top Row - Cluster Status:__Cluster name, node count, online/offline nodes, cluster health status
-__Row 2 - Resource Utilization:__CPU usage (aggregate), memory usage, disk usage, network bandwidth
-__Row 3 - Service Health:__Ceph health status, Kubernetes status, DNS status, RPC service status
-__Row 4 - Top Issues:__Top 5 most-fired alerts, critical logs from last 24h, security events
-__Row 5 - Performance Trends:__CPU/Memory/Disk trends (7-day), throughput trends

### Template Variables

- `$cluster_name`: Cluster identifier (default: "DebVisor")
- `$time_range`: Dashboard time range (default: last 1h)
- `$node_filter`: Optional node filter (default: all nodes)

__Refresh Rate:__30s (auto-refresh enabled)

__Size:__1920x1080+ (optimized for 1080p+, responsive to smaller screens)

### DNS/DHCP Dashboard (dns-dhcp.json)

__Purpose:__DNS and DHCP service monitoring.

### Layout [2]

-__Top Row - Query Statistics:__Queries/sec, query success rate, average query time
-__Row 2 - DHCP Leases:__Total leases, active leases, expired leases, assignment rate
-__Row 3 - Zone Health:__Primary/secondary zone status, zone transfer success, DNSSEC validation status
-__Row 4 - Performance Metrics:__Query latency distribution, DHCP discovery time, zone transfer duration
-__Row 5 - Error Analysis:__Failed queries by type, DHCP errors by reason, TSIG validation failures
-__Row 6 - Detailed Logs:__Recent DNS queries (searchable), DHCP events, errors

### Template Variables [2]

- `$dns_primary_node`: Primary DNS server (dropdown)
- `$dns_secondary_nodes`: Secondary DNS servers (multi-select)
- `$zone_filter`: Zone name filter (default: all zones)

__Refresh Rate:__15s

__Data Sources:__Prometheus (Bind9 exporter, ISC DHCP exporter)

### Security Dashboard (security.json)

__Purpose:__Security events, threat detection, and access auditing.

### Layout [3]

-__Top Row - Security Summary:__Threat level, active incidents, blocked IPs, failed auth attempts
-__Row 2 - Firewall Activity:__Blocked packets (top 10 sources), dropped connections by port, rate-limited connections
-__Row 3 - Authentication:__Login attempts (successful vs failed), MFA usage, privilege escalations
-__Row 4 - System Integrity:__Modified files (top 10), process anomalies detected, capability changes
-__Row 5 - Network Security:__SSL/TLS certificate expiry warnings, suspicious network activity, DDoS indicators
-__Row 6 - Compliance Events:__Policy violations, configuration drifts detected, audit log entries

### Template Variables [3]

- `$threat_level_threshold`: Severity threshold filter (default: warning+)
- `$ip_blocklist`: Show specific blocked IPs (default: all)
- `$time_range`: Historical time range (default: 24h)

__Refresh Rate:__10s (more frequent for security)

__Data Sources:__Prometheus (node exporter), Loki (system logs, audit logs), Wazuh integration

### Compliance Dashboard (compliance.json)

__Purpose:__Compliance audit, access tracking, and regulatory evidence collection.

### Layout [4]

-__Top Row - Compliance Status:__Compliance score (%), required audits, last audit date, violations
-__Row 2 - Access Audit:__User logins (by role), privileged actions, failed auth, access denials
-__Row 3 - Configuration Audit:__Configuration changes (timestamp, actor, old→new), compliance drift, remediation status
-__Row 4 - Data Protection:__Encryption status (data at rest), TLS adoption, certificate validity
-__Row 5 - Evidence Collection:__Exportable audit trail (date range), detailed access logs, system state snapshots
-__Row 6 - Regulatory Reporting:__Controls matrix, evidence availability by control, audit schedule

### Template Variables [4]

- `$regulation`: Compliance framework (e.g., "SOC2", "HIPAA", "PCI-DSS")
- `$date_range`: Audit period (e.g., "last 30 days", "month-to-date")
- `$access_level`: Filter by access level (e.g., "admin", "operator", "viewer")

__Refresh Rate:__60s (compliance events are less frequent)

__Data Sources:__Prometheus, Loki (audit logs), Custom compliance exporter

### Ceph Dashboard (ceph.json)

__Purpose:__Ceph cluster health, performance, and capacity monitoring.

### Layout [5]

-__Top Row - Cluster Health:__Health status, monitors active/quorum, PGs degraded/stuck, pool status
-__Row 2 - Capacity:__Used/total capacity, write-amplification, pool utilization, OSD utilization heatmap
-__Row 3 - Performance:__IOPS (read/write), throughput, latency (p50/p95/p99), recovery rate
-__Row 4 - OSD Status:__OSDs online/offline/down, OSD backfill priority, OSD backfill rate, slow requests
-__Row 5 - Pool Analytics:__Pool IOPS/throughput by pool, pool latency distribution, object counts
-__Row 6 - Recovery & Rebalancing:__Rebalancing progress, recovery priority, PG rebalance rate

### Template Variables [5]

- `$cluster_name`: Ceph cluster identifier (default: "ceph")
- `$pool_filter`: Filter by pool name (default: all pools)
- `$osd_filter`: Filter by OSD ID (default: all OSDs)

__Refresh Rate:__30s

__Data Sources:__Prometheus (ceph-exporter, node exporter)

### Alert Integration

- Links to Ceph health alerts
- Click-through to OSD-specific dashboards
- Drill-down to troubleshooting documentation

### Kubernetes Dashboard (kubernetes.json)

__Purpose:__Kubernetes cluster state, workload health, and resource utilization.

### Layout [6]

-__Top Row - Cluster Health:__API server status, node status (ready/unready), etcd health, networking status
-__Row 2 - Node Status:__Node count, resource allocation (CPU/memory), node pressure conditions, disk pressure
-__Row 3 - Workload Status:__Pod count by phase (running/pending/failed), deployment ready status, StatefulSet status
-__Row 4 - Resource Utilization:__CPU/memory by namespace, CPU/memory by pod, storage utilization by PVC
-__Row 5 - Performance Metrics:__API server latency, controller-manager latency, scheduler latency, reconciliation duration
-__Row 6 - Events & Errors:__Recent pod errors, node conditions, kubelet errors, etcd latency

### Template Variables [6]

- `$cluster_name`: Kubernetes cluster identifier
- `$namespace_filter`: Filter by namespace (multi-select)
- `$pod_filter`: Filter by pod label (e.g., "app=frontend")

__Refresh Rate:__30s

__Data Sources:__Prometheus (kube-state-metrics, kubelet, kube-apiserver metrics)

### Networking Dashboard (networking.json)

__Purpose:__Network performance, connectivity, and traffic analysis.

### Layout [7]

-__Top Row - Network Health:__Network interface status, link status, packet errors/dropped, bandwidth utilization
-__Row 2 - Traffic Analysis:__Traffic by source/destination, top talkers, traffic direction (inbound/outbound), protocol distribution
-__Row 3 - Connectivity:__Ping latency to cluster nodes, inter-node latency, gateway connectivity, DNS resolution time
-__Row 4 - Performance Metrics:__Packet loss rate, retransmission rate, out-of-order packets, TCP reset rate
-__Row 5 - VLAN Performance:__Traffic per VLAN, VLAN errors/dropped, inter-VLAN routing latency
-__Row 6 - Service Network:__Ingress traffic distribution, load balancer status, service endpoint health

### Template Variables [7]

- `$interface_filter`: Network interface filter (e.g., "eth0", "bond0")
- `$vlan_filter`: VLAN ID filter (multi-select)
- `$direction`: Traffic direction (inbound/outbound/both)

__Refresh Rate:__30s

__Data Sources:__Prometheus (node exporter interface metrics, network flow data)

### Storage Performance Dashboard (storage-performance.json)

__Purpose:__Storage I/O performance, latency, and throughput analysis.

### Layout [8]

-__Top Row - Performance Summary:__Aggregate IOPS, aggregate throughput, p95 latency, maximum latency spike
-__Row 2 - I/O by Type:__Read IOPS/throughput, write IOPS/throughput, mixed workload detection
-__Row 3 - Latency Distribution:__Latency histogram (p50/p75/p95/p99), latency heatmap by time, slow I/O operations
-__Row 4 - Queue Depth:__I/O queue depth over time, saturation points, peak load times
-__Row 5 - Disk Health:__IOPS by disk, throughput by disk, disk utilization %, slow disk detection
-__Row 6 - Cache Performance:__Cache hit rate, cache write-through rate, dirty cache pages

### Template Variables [8]

- `$disk_filter`: Storage device filter (e.g., "/dev/sda", "ceph_rbd_*")
- `$workload_type`: Workload classification (sequential/random/mixed)
- `$latency_threshold`: Latency warning threshold (ms)

__Refresh Rate:__15s (performance metrics are time-sensitive)

__Data Sources:__Prometheus (Ceph performance exporter, node exporter disk metrics)

### Alerts Summary Dashboard (alerts-summary.json)

__Purpose:__Alert status, history, and remediation tracking.

### Layout [9]

-__Top Row - Alert Summary:__Total alerts (by severity), alerts fired in last 24h, MTTR (mean time to resolve), alert trend
-__Row 2 - Active Alerts:__Current critical/warning/info alerts, alert duration, owner assignment
-__Row 3 - Alert History:__Alert firing frequency by type, most frequent alerts, resolved alerts, false positive rate
-__Row 4 - Remediation Status:__Alerts with automated remediation, manual remediation in progress, awaiting review
-__Row 5 - Drill-Down:__Alert detail (condition, threshold, current value), related logs, suggested actions
-__Row 6 - Trend Analysis:__Alert trends by component, seasonal patterns, correlation between alert types

### Template Variables [9]

- `$severity_filter`: Show alerts of severity (critical/warning/info/debug)
- `$time_range`: Alert history time range (default: 7d)
- `$owner_filter`: Filter by alert owner/team

__Refresh Rate:__10s (alerts need real-time visibility)

__Data Sources:__Prometheus AlertManager, custom alerting database

### Interactive Features

- Click alert name → drill into alert details and related logs
- Click "Remediate" → trigger automated remediation action
- Click severity → filter related alerts

## Dashboard Templates

### DASHBOARD_TEMPLATE.json

Blank dashboard scaffold with recommended structure for new dashboards.

### Includes

- Title and description panels
- Standard variable declarations ($cluster, $time_range, $filter)
- Example row layouts
- Panel templates for common visualizations
- Documentation links

### Usage

1. Copy DASHBOARD_TEMPLATE.json to dashboards/your-dashboard.json
1. Edit title, description, queries
1. Import into Grafana

### MULTI_CLUSTER.json

Template for dashboards supporting multiple clusters.

### Pattern

- Top variable: `$cluster` selector (dropdown of all clusters)
- All queries prefixed with `cluster="$cluster"` label matcher
- Cluster-specific thresholds and alerts
- Cross-cluster comparison panels

### Example Query Structure

    sum by (cluster, job) (rate(node_cpu_seconds_total{cluster="$cluster"}[5m]))

### SINGLE_TENANT.json

Template for tenant-isolated dashboards.

### Pattern [2]

- Top variable: `$tenant` selector
- All queries filtered by tenant label
- Tenant-specific SLOs and thresholds
- Tenant billing/usage metrics

### CUSTOM_METRICS.json

Template for visualizing custom DebVisor-specific metrics.

### Includes [2]

- Remediation action tracking
- VM migration metrics
- Policy violation events
- Custom service metrics

## Dashboard Design Standards

All dashboards MUST follow these standards for consistency and maintainability.

### Naming Conventions

### Dashboard Naming

- Lowercase, hyphen-separated: `overview`,`dns-dhcp`,`storage-performance`
- Descriptive and searchable
- Format: `[component]-[aspect]`(e.g.,`ceph-performance`)

### Panel Naming

- CamelCase: "Cluster Status", "Query Latency", "OSD Utilization"
- Clear, role-specific (what does this tell an operator?)
- Include units in title where relevant: "CPU Usage (%)", "Query Time (ms)"

### Variable Naming

- `$component`: Cluster/service identifier
- `$time_range`: Time range selector
- `$filter`: Generic filter (e.g., node, pod, pool name)
- Prefix with `$` to indicate template variable

### Color Scheme & Palette

### Standard Colors

    Green:    #31C740   (healthy, normal, success)
    Yellow:   #F2AC29   (warning, caution, degraded)
    Red:      #D64E4E   (critical, error, down)
    Blue:     #3498DB   (informational, neutral)
    Purple:   #9B59B6   (custom/user-defined)
    Orange:   #FF6B35   (attention needed, pending)
    Gray:     #95A5A6   (disabled, offline, neutral)

### Usage [2]

- Success metrics → green
- Warning thresholds → yellow
- Errors/critical → red
- Informational/stats → blue
- Background/neutral → gray

### Panel Types

### Standard Panel Types by Use Case

| Metric Type | Panel Type | Example |
|---|---|---|
| Single metric/status | Stat | Cluster health, online nodes, CPU % |
| Time series | Graph/Time series | CPU over time, throughput, latency |
| Distribution | Histogram | Latency distribution, workload distribution |
| Proportional | Gauge | Capacity utilization %, battery %, cache hit % |
| Categorical | Table | Pod status list, node list, disk list |
| Flow/Relationships | Node Graph | Service dependencies, traffic flow |
| Logs/Events | Logs panel | Recent errors, audit trail, events |

### Threshold Configuration

### Define Thresholds by Metric

    {
      "metric": "cpu_usage_percent",
      "ok": 0,
      "warning": 70,
      "critical": 90,
      "description": "CPU utilization across all cores"
    }

### Common Thresholds

| Metric | Warning | Critical |
|---|---|---|
| CPU Utilization | 70% | 90% |
| Memory Utilization | 80% | 95% |
| Disk Utilization | 80% | 95% |
| Query Latency | 100ms | 500ms |
| Network Latency | 50ms | 200ms |
| Pod Restart Count | 3 in 1h | 10 in 1h |
| OSD Slow Requests | 5% | 20% |
| PG Degraded | Any | >5% |

### Threshold Format

Thresholds should be:

1.__Evidence-based:__Document why the threshold was chosen
1.__Tunable:__Allow operators to adjust via dashboard variables or environment config
1.__Contextual:__Different for different environments (lab, staging, prod)
1.__Documented:__Include link to runbook for each threshold

### Query Patterns

### Standard Query Structure

## Template:  by  for  in

    sum by (cluster, node) (rate(node_cpu_seconds_total{cluster="$cluster"}[5m]))

## Best Practices

1.__Use label matchers, not string replacement:__

- ✅ GOOD: `cluster="$cluster"` (Prometheus knows $cluster is a label)
- ❌ BAD: `{cluster="$cluster_name"}` (quotes may be wrong, escaping issues)

1.__Aggregate at the right level:__

- `sum()`: Total across all instances
- `avg()`: Average per instance (useful for rates, latencies)
- `max()`/`min()`: Peak/lowest values

1.__Use functions appropriate to metric type:__

- Counter metrics: Use `rate()`or`increase()`
- Gauge metrics: Use directly or with `avg()`/`max()`
- Histogram metrics: Use `histogram_quantile()`

1.__Document queries with comments:__

- What does this metric represent?
- Why is this aggregation method chosen?
- What thresholds trigger alerts?

### Example - Comprehensive Query

## CPU utilization per node (%)

## Metric: node_cpu_seconds_total (counter, seconds spent in each CPU mode)

## Formula: 100 * (1 - idle_fraction)

## Aggregation: Per node (important for per-node comparison)

    100 * (1 - avg by (cluster, node) (
      rate(node_cpu_seconds_total{cluster="$cluster",mode="idle"}[5m])
    ))

## Visualization Best Practices

### Panel Layout

-__Width:__6-unit width for primary metrics, 12-unit for detailed views, 3-unit for summary stats
-__Height:__8-unit for time series, 4-unit for stats/gauges, 6-unit for tables
-__Spacing:__Consistent vertical alignment, group related panels

### Labels & Legends

-__Legend placement:__Right side for time series, bottom for multi-metric comparisons
-__Legend values:__Show current, average, max for context
-__Axis labels:__Always include units (%, ms, B/s, etc.)

### Interactivity

-__Drill-down links:__From aggregate metrics to detailed resource panels
-__Cross-dashboard links:__From alerts to relevant dashboards
-__Clickable series:__Enable click to filter or drill-down

### Performance

-__Query frequency:__30s for most dashboards, 10s only for critical alerts
-__Time range selection:__Default to 1h for ops, allow 7d/30d for trends
-__Panel caching:__Disable caching for live metrics, enable for historical views

## Provisioning Configuration

### dashboards.yaml

Grafana dashboard provisioning configuration.

    apiVersion: 1

    providers:

- name: 'DebVisor Dashboards'

        orgId: 1
        folder: 'DebVisor'
        type: file
        disableDeletion: false
        editable: true
        options:
          path: /etc/grafana/provisioning/dashboards

### Configuration Options

| Option | Purpose | Value |
|---|---|---|
| `name` | Provisioning provider name | User-friendly name |
| `orgId` | Grafana organization ID | 1 (default org) |
| `folder` | Dashboard folder name | "DebVisor" |
| `type` | Provisioning type | "file" (from filesystem) or "cloud" |
| `disableDeletion` | Protect dashboards from deletion | true/false |
| `editable` | Allow manual editing in UI | true/false |
| `path`| Dashboard file directory |`/etc/grafana/provisioning/dashboards` |

### datasources.yaml

Prometheus datasource provisioning.

    apiVersion: 1

    datasources:

- name: Prometheus-DebVisor

        type: prometheus
        access: proxy
        url: [http://prometheus:9090](http://prometheus:9090)
        isDefault: true
        jsonData:
          timeInterval: 15s

### Datasource Configuration

| Option | Purpose | Example |
|---|---|---|
| `name` | Datasource identifier | "Prometheus-DebVisor" |
| `type` | Datasource type | "prometheus", "loki", "graphite" |
| `url`| API endpoint |[http://prometheus:9090](http://prometheus:9090) |
| `isDefault` | Use as default data source | true/false |
| `timeInterval` | Query scrape interval | "15s" (must match Prometheus) |

### Alert Notification Channels

#### email.yaml

Email notification configuration.

    notifiers:

- name: "DebVisor Alerts Email"

        type: "email"
        uid: "debvisor-email"
        isDefault: false
        settings:
          addresses: "ops-team@example.com,security@example.com"

### Configuration

| Setting | Purpose |
|---|---|
| `addresses` | Comma-separated recipient emails |
| `singleEmail` | Send single email with all alerts or individual emails |
| `uploadImage` | Attach alert screenshot to email |

#### slack.yaml

Slack integration.

    notifiers:

- name: "DebVisor Alerts Slack"

        type: "slack"
        uid: "debvisor-slack"
        settings:
          url: "[https://hooks.slack.com/services/YOUR/WEBHOOK/URL"](https://hooks.slack.com/services/YOUR/WEBHOOK/URL")
          channel: "#alerts"
          mentionGroups: "ops-team"

### Configuration [2]

| Setting | Purpose |
|---|---|
| `url` | Slack webhook URL |
| `channel` | Slack channel for alerts |
| `mentionGroups` | Slack user groups to mention (e.g., "@ops-team") |
| `uploadImage` | Include alert chart in message |

#### pagerduty.yaml

PagerDuty integration for incident escalation.

    notifiers:

- name: "DebVisor PagerDuty"

        type: "pagerduty"
        uid: "debvisor-pagerduty"
        settings:
          integrationKey: "YOUR-PAGERDUTY-KEY"
          severity: "critical"

#### webhook.yaml

Custom webhook for enterprise integrations.

    notifiers:

- name: "DebVisor Webhook"

        type: "webhook"
        uid: "debvisor-webhook"
        settings:
          url: "[https://monitoring.example.com/alerts/receive"](https://monitoring.example.com/alerts/receive")
          httpMethod: "POST"

### Alert Rules (Prometheus)

prometheus.yaml contains alert rules for Prometheus evaluation.

### Example Rules

    groups:

- name: debvisor_cluster

        rules:

## Cluster health

- alert: CephClusterDown

            expr: |
              ceph_health_status != 0
            for: 5m
            labels:
              severity: critical
              component: ceph
            annotations:
              summary: "Ceph cluster is down"
              description: "Ceph cluster health status is {{ $value }}"

## Node offline

- alert: NodeOffline

            expr: |
              up{job="node"} == 0
            for: 5m
            labels:
              severity: warning
              component: cluster
            annotations:
              summary: "Node {{ $labels.node }} offline"
              runbook: "[https://docs.example.com/runbooks/node-offline"](https://docs.example.com/runbooks/node-offline")

### Rule Structure

| Field | Purpose |
|---|---|
| `alert` | Alert name (used in notifications) |
| `expr` | PromQL expression (must be true to fire) |
| `for` | Duration condition must be true before firing |
| `labels` | Static labels applied to alert (severity, component) |
| `annotations` | Dynamic fields rendered with alert (summary, description) |

## Provisioning Workflow

### Deploying Dashboard Updates

1.__Edit Dashboard:__

## Modify dashboard JSON

       vi opt/grafana/dashboards/overview.json

    1.__Validate JSON:__

## Ensure valid JSON syntax

   jq . opt/grafana/dashboards/overview.json > /dev/null && echo "Valid"

    1.__Export from Grafana (Optional):__

## After making UI changes, export updated dashboard

       curl -s [http://grafana:3000/api/dashboards/uid/overview](http://grafana:3000/api/dashboards/uid/overview) \
         -H "Authorization: Bearer $GRAFANA_API_TOKEN" | jq . > overview.json

1.__Restart Grafana:__

## Reload provisioned dashboards

   systemctl restart grafana-server

## or in Kubernetes

   kubectl rollout restart deployment/grafana -n monitoring

### Multi-Environment Provisioning

### Lab Environment (single cluster)

- `dashboards.yaml`: Point to`dashboards/lab/`
- Include fixtures dashboard from opt/monitoring/fixtures/

### Staging Environment (multi-node)

- `dashboards.yaml`: Point to`dashboards/staging/`
- Include multi-cluster templates

### Production Environment (HA, multi-cluster)

- `dashboards.yaml`: Point to`dashboards/prod/`
- Strict query validation, performance tuning
- Backup/export procedure

## Dashboard Consistency Checklist

### For Every New Dashboard

- [ ] Follows naming convention (lowercase, hyphenated)
- [ ] Has descriptive title and description
- [ ] Includes standard variables (`$cluster`,`$time_range`)
- [ ] Uses standard color scheme (green/yellow/red/blue)
- [ ] All panels have descriptive titles with units
- [ ] All queries are documented with comments
- [ ] Thresholds are documented with runbook links
- [ ] Performance optimized (appropriate refresh rate)
- [ ] Legend configured for clarity
- [ ] Drill-down links to related dashboards
- [ ] JSON exported and committed to git
- [ ] README updated with dashboard description
- [ ] Added to dashboard.yaml provisioning config

### For Dashboard Updates

- [ ] Changes tested in staging first
- [ ] Query performance validated
- [ ] Thresholds reviewed with ops team
- [ ] Changelog entry updated
- [ ] Dashboard exported and committed
- [ ] Provisioning config updated if needed
- [ ] Grafana reloaded/restarted

## Troubleshooting

### Dashboards Not Appearing

    __Symptom:__Provisioned dashboards not visible in Grafana UI.

### Diagnostic Steps

## 1. Check provisioning config

cat /etc/grafana/provisioning/dashboards/dashboards.yaml

## 2. Verify dashboard file exists

ls -la /etc/grafana/provisioning/dashboards/*.json

## 3. Check Grafana logs

journalctl -u grafana-server -n 100

## 4. Verify JSON is valid

jq . /etc/grafana/provisioning/dashboards/overview.json

## 5. Check Grafana API

curl -s [http://grafana:3000/api/search](http://grafana:3000/api/search) \
  -H "Authorization: Bearer $GRAFANA_TOKEN" | jq '.'

## Solutions

- Ensure `path` in dashboards.yaml matches actual file location
- Verify JSON has no syntax errors
- Check file permissions (Grafana must be able to read)
- Restart Grafana after provisioning config changes

### Queries Not Working

    __Symptom:__Panels show "No data" or error messages.

### Diagnostic Steps [2]

## 1. Verify Prometheus is accessible

curl [http://prometheus:9090/-/healthy](http://prometheus:9090/-/healthy)

## 2. Test query in Prometheus directly

curl '[http://prometheus:9090/api/v1/query?query=up'](http://prometheus:9090/api/v1/query?query=up')

## 3. Check datasource configuration

curl [http://grafana:3000/api/datasources](http://grafana:3000/api/datasources) \
  -H "Authorization: Bearer $GRAFANA_TOKEN" | jq '.'

## 4. Look at Grafana logs for query errors

journalctl -u grafana-server -f | grep -i error

## 5. Verify metrics exist

curl '[http://prometheus:9090/api/v1/series?match[]=node_cpu_seconds_total'](http://prometheus:9090/api/v1/series?match[]=node_cpu_seconds_total')

## Solutions [2]

- Verify metric names are correct (check prometheus:9090 for available metrics)
- Ensure label matchers match actual label values
- Check for typos in variable references
- Verify Prometheus scrape config is working

### Performance Issues

    __Symptom:__Dashboards load slowly, Grafana UI sluggish.

### Optimization

## Reduce refresh rate for non-critical panels

"refresh": "1m"  # Instead of "10s"

## Limit query time range

"timeshift": "1h"  # Instead of "7d"

## Use simpler aggregations

rate(metric[5m])  # Instead of complex joins

## Add query caching

"cacheTimeout": "60s"

## Optimize alert queries

## Use static thresholds instead of dynamic calculations

## Best Practices [2]

### Dashboard Development

    1.__Start with Dashboarding Tutorial:__Begin with DASHBOARD_TEMPLATE.json
    1.__Test Queries First:__Validate PromQL in Prometheus UI before adding to dashboard
    1.__Use Meaningful Names:__Dashboard and panel names should clearly indicate what's being monitored
    1.__Document Everything:__Add descriptions, runbook links, threshold justifications
    1.__Version Control:__Keep dashboard JSON in git with commit messages

### Dashboard Maintenance

    1.__Regular Review:__Audit dashboards quarterly for:

- Unused panels (remove clutter)
- Outdated thresholds (validate with ops team)
- Broken links or queries
- Performance issues

    1.__Monitor Usage:__Track which dashboards are most viewed

- Prioritize improvements for high-traffic dashboards
- Consider deprecating unused dashboards

    1.__Gather Feedback:__Regularly ask ops teams:

- Is this dashboard helpful?
- What's missing?
- What would make monitoring easier?

### Alert Tuning

    1.__Avoid Alert Fatigue:__Excessive alerts reduce effectiveness

- Keep critical alert count manageable
- Use for truly actionable conditions
- Avoid duplicate/related alerts

    1.__False Positive Reduction:__

- Add 5-10 minute grace periods (`for: 5m`)
- Use aggregations to smooth noise
- Verify thresholds with real data

    1.__Runbook Linkage:__

- Every alert should link to a runbook
- Runbook should guide to resolution
- Update runbooks based on incidents

## Integration with Monitoring

### Prometheus Scrapers

    Ensure Prometheus scrape config includes:

scrape_configs:

- job_name: 'node'

    static_configs:

- targets: ['localhost:9100']

- job_name: 'ceph'

    static_configs:

- targets: ['ceph-mgr:9283']

- job_name: 'kubernetes'

    kubernetes_sd_configs:

- role: endpoints

### Alertmanager Integration

    Grafana-generated alerts flow to AlertManager:

Grafana Alert Rule Fired
    ↓
AlertManager Receives Alert
    ↓
AlertManager Routes to Notification Channels
    ↓
Notification Sent (Email, Slack, PagerDuty, Webhook)

### Loki Log Integration

    Dashboards can embed logs from Loki:

[Grafana Dashboard Panel]
    ↓
Loki Query: {job="system-logs", level="error"}
    ↓
[Logs displayed alongside metrics]

## References

- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [Prometheus Querying](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [AlertManager Configuration](https://prometheus.io/docs/alerting/latest/configuration/)
- [DebVisor Monitoring Overview](./opt/monitoring/README.md)
- [DebVisor Fixtures Guide](./opt/monitoring/FIXTURES_GUIDE.md)

## Related Documentation

- See [opt/monitoring/README.md](./opt/monitoring/README.md) for Prometheus and monitoring infrastructure
- See [opt/monitoring/FIXTURES_GUIDE.md](./opt/monitoring/FIXTURES_GUIDE.md) for testing dashboards with synthetic data
- See [opt/docs/GLOSSARY.md](./opt/docs/GLOSSARY.md) for monitoring terminology

## Next Steps

1.__Template Library:__Create dashboard templates for different cluster sizes
1.__Multi-Cluster:__Build multi-cluster comparison dashboards
1.__Tenant Isolation:__Support dashboards for multi-tenant deployments
1.__BI Integration:__Export dashboard data for business intelligence
1.__Custom Metrics:__Add facility for custom application metrics visualization
