# opt/grafana/ - Grafana Dashboards and Provisioning\n\n## Overview\n\nThe

`opt/grafana/`directory

contains Grafana dashboard templates, provisioning configurations, and
dashboarding
standards for
DebVisor cluster monitoring. Grafana serves as the visualization layer for
Prometheus
metrics,
providing operators with real-time visibility into cluster health, performance,
and
security.\n\n-
*Key Responsibility:**Provide consistent, reusable, and maintainable Grafana
dashboards
for
multi-tenant, multi-cluster DebVisor deployments.\n\n## Directory Structure\n\n
opt/grafana/\n +--
README.md # This file - Grafana overview and standards\n +-- dashboards/ #
Grafana
dashboard
definitions (JSON)\n | +-- 00-index.json # Dashboard index and navigation\n | +--
overview.json #
System overview dashboard\n | +-- dns-dhcp.json # DNS/DHCP health and performance\n | +--
security.json # Security metrics and events\n | +-- compliance.json # Compliance audit and
access
tracking\n | +-- ceph.json # Ceph cluster health\n | +-- kubernetes.json # Kubernetes
cluster
status\n | +-- networking.json # Network performance and connectivity\n | +--
storage-performance.json # Storage I/O and latency\n | +-- alerts-summary.json # Active
alerts and
history\n | +-- templates/ # Dashboard templates and examples\n | +--
DASHBOARD_TEMPLATE.json #
Blank dashboard scaffold\n | +-- MULTI_CLUSTER.json # Multi-cluster dashboard pattern\n |
+--
SINGLE_TENANT.json # Single-tenant monitoring template\n | +-- CUSTOM_METRICS.json #
Custom metric
visualization template\n +-- provisioning/ # Grafana provisioning configuration\n | +--
dashboards.yaml # Dashboard provisioning config\n | +-- datasources.yaml # Datasource
provisioning
config\n | +-- alert-notification-channels/ # Alert notification configurations\n | | +--
email.yaml

## Email notifications\n | | +-- slack.yaml # Slack integration\n | | +-- pagerduty.yaml #

PagerDuty

integration\n | | +-- webhook.yaml # Custom webhook\n | | +-- README.md # Notification
setup guide\n
| +-- alert-rules/ # Alert rule configurations\n | | +-- prometheus.yaml # Prometheus alerting
rules\n | | +-- grafana-native.yaml # Grafana native alerts\n | | +-- README.md # Alert
rules
documentation\n | +-- README.md # Provisioning overview\n +-- DASHBOARD_STANDARDS.md #
Dashboard
design and consistency guidelines\n +-- IMPLEMENTATION_GUIDE.md # How to create
new
dashboards\n +--
TROUBLESHOOTING.md # Common Grafana issues and solutions\n\n## Dashboard
Library\n\n###
System
Overview Dashboard (overview.json)\n\n- *Purpose:**Comprehensive system health
snapshot.\n\n###
Layout\n\n- **Top Row - Cluster Status:**Cluster name, node count,
online/offline nodes,
cluster
health status\n\n- **Row 2 - Resource Utilization:**CPU usage (aggregate),
memory usage,
disk usage,
network bandwidth\n\n- **Row 3 - Service Health:**Ceph health status, Kubernetes
status,
DNS status,
RPC service status\n\n- **Row 4 - Top Issues:**Top 5 most-fired alerts, critical
logs from
last 24h,
security events\n\n- **Row 5 - Performance Trends:**CPU/Memory/Disk trends
(7-day),
throughput
trends\n\n### Template Variables\n\n-`$cluster_name`: Cluster identifier
(default:
"DebVisor")\n\n-
`$time_range`: Dashboard time range (default: last 1h)\n\n- `$node_filter`:
Optional node
filter
(default: all nodes)\n\n- *Refresh Rate:**30s (auto-refresh enabled)\n\n-
*Size:**1920x1080+
(optimized for 1080p+, responsive to smaller screens)\n\n### DNS/DHCP Dashboard
(dns-dhcp.json)\n\n-
*Purpose:**DNS and DHCP service monitoring.\n\n### Layout [2]\n\n- **Top Row -
Query
Statistics:**Queries/sec, query success rate, average query time\n\n- **Row 2 -
DHCP
Leases:**Total
leases, active leases, expired leases, assignment rate\n\n- **Row 3 - Zone
Health:**Primary/secondary zone status, zone transfer success, DNSSEC validation
status\n\n- **Row 4

- Performance Metrics:**Query latency distribution, DHCP discovery time, zone
transfer
duration\n\n-
**Row 5 - Error Analysis:**Failed queries by type, DHCP errors by reason, TSIG
validation
failures\n\n- **Row 6 - Detailed Logs:**Recent DNS queries (searchable), DHCP
events,
errors\n\n###
Template Variables [2]\n\n- `$dns_primary_node`: Primary DNS server
(dropdown)\n\n-
`$dns_secondary_nodes`: Secondary DNS servers (multi-select)\n\n-
`$zone_filter`: Zone
name filter
(default: all zones)\n\n- *Refresh Rate:**15s\n\n- *Data Sources:**Prometheus
(Bind9
exporter, ISC
DHCP exporter)\n\n### Security Dashboard (security.json)\n\n-
*Purpose:**Security events,
threat
detection, and access auditing.\n\n### Layout [3]\n\n- **Top Row - Security
Summary:**Threat level,
active incidents, blocked IPs, failed auth attempts\n\n- **Row 2 - Firewall
Activity:**Blocked
packets (top 10 sources), dropped connections by port, rate-limited
connections\n\n- **Row
3 -
Authentication:**Login attempts (successful vs failed), MFA usage, privilege
escalations\n\n- **Row
4 - System Integrity:**Modified files (top 10), process anomalies detected,
capability
changes\n\n-
**Row 5 - Network Security:**SSL/TLS certificate expiry warnings, suspicious
network
activity, DDoS
indicators\n\n- **Row 6 - Compliance Events:**Policy violations, configuration
drifts
detected,
audit log entries\n\n### Template Variables [3]\n\n- `$threat_level_threshold`:
Severity
threshold
filter (default: warning+)\n\n- `$ip_blocklist`: Show specific blocked IPs
(default:
all)\n\n-
`$time_range`: Historical time range (default: 24h)\n\n- *Refresh Rate:**10s
(more
frequent for
security)\n\n- *Data Sources:**Prometheus (node exporter), Loki (system logs,
audit logs),
Wazuh
integration\n\n### Compliance Dashboard (compliance.json)\n\n-
*Purpose:**Compliance
audit, access
tracking, and regulatory evidence collection.\n\n### Layout [4]\n\n- **Top Row -
Compliance
Status:**Compliance score (%), required audits, last audit date, violations\n\n-
**Row 2 -
Access
Audit:**User logins (by role), privileged actions, failed auth, access
denials\n\n- **Row
3 -
Configuration Audit:**Configuration changes (timestamp, actor, old->new),
compliance
drift,
remediation status\n\n- **Row 4 - Data Protection:**Encryption status (data at
rest), TLS
adoption,
certificate validity\n\n- **Row 5 - Evidence Collection:**Exportable audit trail
(date
range),
detailed access logs, system state snapshots\n\n- **Row 6 - Regulatory
Reporting:**Controls matrix,
evidence availability by control, audit schedule\n\n### Template Variables
[4]\n\n-
`$regulation`:
Compliance framework (e.g., "SOC2", "HIPAA", "PCI-DSS")\n\n- `$date_range`:
Audit period
(e.g.,
"last 30 days", "month-to-date")\n\n- `$access_level`: Filter by access level
(e.g.,
"admin",
"operator", "viewer")\n\n- *Refresh Rate:**60s (compliance events are less
frequent)\n\n-
*Data
Sources:**Prometheus, Loki (audit logs), Custom compliance exporter\n\n### Ceph
Dashboard
(ceph.json)\n\n- *Purpose:**Ceph cluster health, performance, and capacity
monitoring.\n\n### Layout
[5]\n\n- **Top Row - Cluster Health:**Health status, monitors active/quorum, PGs
degraded/stuck,
pool status\n\n- **Row 2 - Capacity:**Used/total capacity, write-amplification,
pool
utilization,
OSD utilization heatmap\n\n- **Row 3 - Performance:**IOPS (read/write),
throughput,
latency
(p50/p95/p99), recovery rate\n\n- **Row 4 - OSD Status:**OSDs
online/offline/down, OSD
backfill
priority, OSD backfill rate, slow requests\n\n- **Row 5 - Pool Analytics:**Pool
IOPS/throughput by
pool, pool latency distribution, object counts\n\n- **Row 6 - Recovery &
Rebalancing:**Rebalancing
progress, recovery priority, PG rebalance rate\n\n### Template Variables
[5]\n\n-
`$cluster_name`:
Ceph cluster identifier (default: "ceph")\n\n- `$pool_filter`: Filter by pool
name
(default: all
pools)\n\n- `$osd_filter`: Filter by OSD ID (default: all OSDs)\n\n- *Refresh
Rate:**30s\n\n- *Data
Sources:**Prometheus (ceph-exporter, node exporter)\n\n### Alert
Integration\n\n- Links to
Ceph
health alerts\n\n- Click-through to OSD-specific dashboards\n\n- Drill-down to
troubleshooting
documentation\n\n### Kubernetes Dashboard (kubernetes.json)\n\n-
*Purpose:**Kubernetes
cluster
state, workload health, and resource utilization.\n\n### Layout [6]\n\n- **Top
Row -
Cluster
Health:**API server status, node status (ready/unready), etcd health, networking
status\n\n- **Row 2

- Node Status:**Node count, resource allocation (CPU/memory), node pressure
conditions,
disk
pressure\n\n- **Row 3 - Workload Status:**Pod count by phase
(running/pending/failed),
deployment
ready status, StatefulSet status\n\n- **Row 4 - Resource
Utilization:**CPU/memory by
namespace,
CPU/memory by pod, storage utilization by PVC\n\n- **Row 5 - Performance
Metrics:**API
server
latency, controller-manager latency, scheduler latency, reconciliation
duration\n\n- **Row
6 -
Events & Errors:**Recent pod errors, node conditions, kubelet errors, etcd
latency\n\n###
Template
Variables [6]\n\n- `$cluster_name`: Kubernetes cluster identifier\n\n-
`$namespace_filter`: Filter
by namespace (multi-select)\n\n- `$pod_filter`: Filter by pod label (e.g.,
"app=frontend")\n\n-
*Refresh Rate:**30s\n\n- *Data Sources:**Prometheus (kube-state-metrics,
kubelet,
kube-apiserver
metrics)\n\n### Networking Dashboard (networking.json)\n\n- *Purpose:**Network
performance,
connectivity, and traffic analysis.\n\n### Layout [7]\n\n- **Top Row - Network
Health:**Network
interface status, link status, packet errors/dropped, bandwidth utilization\n\n-
**Row 2 -
Traffic
Analysis:**Traffic by source/destination, top talkers, traffic direction
(inbound/outbound),
protocol distribution\n\n- **Row 3 - Connectivity:**Ping latency to cluster
nodes,
inter-node
latency, gateway connectivity, DNS resolution time\n\n- **Row 4 - Performance
Metrics:**Packet loss
rate, retransmission rate, out-of-order packets, TCP reset rate\n\n- **Row 5 -
VLAN
Performance:**Traffic per VLAN, VLAN errors/dropped, inter-VLAN routing
latency\n\n- **Row
6 -
Service Network:**Ingress traffic distribution, load balancer status, service
endpoint
health\n\n###
Template Variables [7]\n\n- `$interface_filter`: Network interface filter (e.g.,
"eth0",
"bond0")\n\n- `$vlan_filter`: VLAN ID filter (multi-select)\n\n- `$direction`:
Traffic
direction
(inbound/outbound/both)\n\n- *Refresh Rate:**30s\n\n- *Data Sources:**Prometheus
(node
exporter
interface metrics, network flow data)\n\n### Storage Performance Dashboard
(storage-performance.json)\n\n- *Purpose:**Storage I/O performance, latency, and
throughput
analysis.\n\n### Layout [8]\n\n- **Top Row - Performance Summary:**Aggregate
IOPS,
aggregate
throughput, p95 latency, maximum latency spike\n\n- **Row 2 - I/O by Type:**Read
IOPS/throughput,
write IOPS/throughput, mixed workload detection\n\n- **Row 3 - Latency
Distribution:**Latency
histogram (p50/p75/p95/p99), latency heatmap by time, slow I/O operations\n\n-
**Row 4 -
Queue
Depth:**I/O queue depth over time, saturation points, peak load times\n\n- **Row
5 - Disk
Health:**IOPS by disk, throughput by disk, disk utilization %, slow disk
detection\n\n-
**Row 6 -
Cache Performance:**Cache hit rate, cache write-through rate, dirty cache
pages\n\n###
Template
Variables [8]\n\n- `$disk_filter`: Storage device filter (e.g., "/dev/sda",
"ceph*rbd**")\n\n-
`$workload_type`: Workload classification (sequential/random/mixed)\n\n-
`$latency_threshold`:
Latency warning threshold (ms)\n\n- *Refresh Rate:**15s (performance metrics are
time-sensitive)\n\n- *Data Sources:**Prometheus (Ceph performance exporter, node
exporter
disk
metrics)\n\n### Alerts Summary Dashboard (alerts-summary.json)\n\n-
*Purpose:**Alert
status,
history, and remediation tracking.\n\n### Layout [9]\n\n- **Top Row - Alert
Summary:**Total alerts
(by severity), alerts fired in last 24h, MTTR (mean time to resolve), alert
trend\n\n-
**Row 2 -
Active Alerts:**Current critical/warning/info alerts, alert duration, owner
assignment\n\n- **Row 3

- Alert History:**Alert firing frequency by type, most frequent alerts, resolved
alerts,
false
positive rate\n\n- **Row 4 - Remediation Status:**Alerts with automated
remediation,
manual
remediation in progress, awaiting review\n\n- **Row 5 - Drill-Down:**Alert
detail
(condition,
threshold, current value), related logs, suggested actions\n\n- **Row 6 - Trend
Analysis:**Alert
trends by component, seasonal patterns, correlation between alert types\n\n###
Template
Variables
[9]\n\n- `$severity_filter`: Show alerts of severity
(critical/warning/info/debug)\n\n-
`$time_range`: Alert history time range (default: 7d)\n\n- `$owner_filter`:
Filter by
alert
owner/team\n\n- *Refresh Rate:**10s (alerts need real-time visibility)\n\n-
*Data
Sources:**Prometheus AlertManager, custom alerting database\n\n### Interactive
Features\n\n- Click
alert name -> drill into alert details and related logs\n\n- Click "Remediate"
-> trigger
automated
remediation action\n\n- Click severity -> filter related alerts\n\n## Dashboard
Templates\n\n###
DASHBOARD_TEMPLATE.json\n\nBlank dashboard scaffold with recommended structure
for new
dashboards.\n\n### Includes\n\n- Title and description panels\n\n- Standard
variable
declarations
($cluster, $time_range, $filter)\n\n- Example row layouts\n\n- Panel templates
for common
visualizations\n\n- Documentation links\n\n### Usage\n\n1. Copy
DASHBOARD_TEMPLATE.json to
dashboards/your-dashboard.json\n\n1. Edit title, description, queries\n\n1.
Import into
Grafana\n\n### MULTI_CLUSTER.json\n\nTemplate for dashboards supporting multiple
clusters.\n\n###
Pattern\n\n- Top variable: `$cluster`selector (dropdown of all clusters)\n\n-
All queries
prefixed
with`cluster="$cluster"`label matcher\n\n- Cluster-specific thresholds and
alerts\n\n-
Cross-cluster
comparison panels\n\n### Example Query Structure\n\n sum by (cluster, job)
(rate(node_cpu_seconds_total{cluster="$cluster"}[5m]))\n\n###
SINGLE_TENANT.json\n\nTemplate for
tenant-isolated dashboards.\n\n### Pattern [2]\n\n- Top
variable:`$tenant`selector\n\n-
All queries
filtered by tenant label\n\n- Tenant-specific SLOs and thresholds\n\n- Tenant
billing/usage
metrics\n\n### CUSTOM_METRICS.json\n\nTemplate for visualizing custom
DebVisor-specific
metrics.\n\n### Includes [2]\n\n- Remediation action tracking\n\n- VM migration
metrics\n\n- Policy
violation events\n\n- Custom service metrics\n\n## Dashboard Design
Standards\n\nAll
dashboards MUST
follow these standards for consistency and maintainability.\n\n### Naming
Conventions\n\n###
Dashboard Naming\n\n- Lowercase,
hyphen-separated:`overview`,`dns-dhcp`,`storage-performance`\n\n-
Descriptive and searchable\n\n- Format:
`[component]-[aspect]`(e.g.,`ceph-performance`)\n\n### Panel
Naming\n\n- CamelCase: "Cluster Status", "Query Latency", "OSD Utilization"\n\n-
Clear,
role-specific (what does this tell an operator?)\n\n- Include units in title
where
relevant: "CPU
Usage (%)", "Query Time (ms)"\n\n### Variable Naming\n\n- `$component`:
Cluster/service
identifier\n\n- `$time_range`: Time range selector\n\n- `$filter`: Generic
filter (e.g.,
node, pod,
pool name)\n\n- Prefix with `$`to indicate template variable\n\n### Color Scheme
&
Palette\n\n###
Standard Colors\n\n Green: #31C740 (healthy, normal, success)\n Yellow: #F2AC29
(warning,
caution,
degraded)\n Red: #D64E4E (critical, error, down)\n Blue: #3498DB (informational,
neutral)\n Purple:

## 9B59B6 (custom/user-defined)\n Orange: #FF6B35 (attention needed, pending)\n Gray:

## 95A5A6

(disabled, offline, neutral)\n\n### Usage [2]\n\n- Success metrics -> green\n\n-
Warning
thresholds
-> yellow\n\n- Errors/critical -> red\n\n- Informational/stats -> blue\n\n-
Background/neutral ->
gray\n\n### Panel Types\n\n### Standard Panel Types by Use Case\n\n| Metric Type | Panel
Type |
Example |\n|---|---|---|\n| Single metric/status | Stat | Cluster health, online nodes,
CPU % |\n|
Time series | Graph/Time series | CPU over time, throughput, latency |\n| Distribution |
Histogram |
Latency distribution, workload distribution |\n| Proportional | Gauge | Capacity
utilization %,
battery %, cache hit % |\n| Categorical | Table | Pod status list, node list, disk list
|\n|
Flow/Relationships | Node Graph | Service dependencies, traffic flow |\n| Logs/Events |
Logs panel |
Recent errors, audit trail, events |\n\n### Threshold Configuration\n\n### Define
Thresholds by
Metric\n\n {\n "metric": "cpu_usage_percent",\n "ok": 0,\n "warning": 70,\n
"critical":
90,\n
"description": "CPU utilization across all cores"\n }\n\n### Common Thresholds\n\n| Metric
| Warning
| Critical |\n|---|---|---|\n| CPU Utilization | 70% | 90% |\n| Memory Utilization | 80% | 95% |\n|
Disk Utilization | 80% | 95% |\n| Query Latency | 100ms | 500ms |\n| Network Latency |
50ms | 200ms
|\n| Pod Restart Count | 3 in 1h | 10 in 1h |\n| OSD Slow Requests | 5% | 20% |\n| PG Degraded | Any
| >5% |\n\n### Threshold Format\n\nThresholds should be:\n1.**Evidence-based:**Document why the
threshold was chosen\n1.**Tunable:**Allow operators to adjust via dashboard
variables or
environment
config\n1.**Contextual:**Different for different environments (lab, staging,
prod)\n1.**Documented:**Include link to runbook for each threshold\n\n### Query
Patterns\n\n###
Standard Query Structure\n\n## Template: by for in\n\n sum by (cluster, node)
(rate(node_cpu_seconds_total{cluster="$cluster"}[5m]))\n\n## Best
Practices\n\n1.**Use
label
matchers, not string replacement:**\n\n- ? GOOD:`cluster="$cluster"`(Prometheus
knows
$cluster is a
label)\n\n- ? BAD:`{cluster="$cluster_name"}`(quotes may be wrong, escaping
issues)\n\n1.**Aggregate
at the right level:**\n\n-`sum()`: Total across all instances\n\n- `avg()`:
Average per
instance
(useful for rates, latencies)\n\n- `max()`/`min()`: Peak/lowest
values\n\n1.**Use
functions
appropriate to metric type:**\n\n- Counter metrics: Use
`rate()`or`increase()`\n\n- Gauge
metrics:
Use directly or with `avg()`/`max()`\n\n- Histogram metrics: Use
`histogram_quantile()`\n\n1.**Document queries with comments:**\n\n- What does
this metric
represent?\n\n- Why is this aggregation method chosen?\n\n- What thresholds
trigger
alerts?\n\n###
Example - Comprehensive Query\n\n## CPU utilization per node (%)\n\n## Metric:
node_cpu_seconds_total (counter, seconds spent in each CPU mode)\n\n## Formula:
100 *(1 -
idle_fraction)\n\n## Aggregation: Per node (important for per-node
comparison)\n\n 100*(1

- avg by
(cluster, node) (\n
rate(node_cpu_seconds_total{cluster="$cluster",mode="idle"}[5m])\n
))\n\n##
Visualization Best Practices\n\n### Panel Layout\n\n-**Width:**6-unit width for
primary
metrics,
12-unit for detailed views, 3-unit for summary stats\n\n- **Height:**8-unit for
time
series, 4-unit
for stats/gauges, 6-unit for tables\n\n- **Spacing:**Consistent vertical
alignment, group
related
panels\n\n### Labels & Legends\n\n- **Legend placement:**Right side for time
series,
bottom for
multi-metric comparisons\n\n- **Legend values:**Show current, average, max for
context\n\n- **Axis
labels:**Always include units (%, ms, B/s, etc.)\n\n### Interactivity\n\n-
**Drill-down
links:**From
aggregate metrics to detailed resource panels\n\n- **Cross-dashboard
links:**From alerts
to relevant
dashboards\n\n- **Clickable series:**Enable click to filter or drill-down\n\n###
Performance\n\n-
**Query frequency:**30s for most dashboards, 10s only for critical alerts\n\n-
**Time
range
selection:**Default to 1h for ops, allow 7d/30d for trends\n\n- **Panel
caching:**Disable
caching
for live metrics, enable for historical views\n\n## Provisioning
Configuration\n\n###
dashboards.yaml\n\nGrafana dashboard provisioning configuration.\n apiVersion:
1\n
providers:\n\n-
name: 'DebVisor Dashboards'\n\n orgId: 1\n folder: 'DebVisor'\n type: file\n
disableDeletion:
false\n editable: true\n options:\n path:
/etc/grafana/provisioning/dashboards\n\n###
Configuration
Options\n\n| Option | Purpose | Value |\n|---|---|---|\n| `name`| Provisioning provider
name |
User-friendly name |\n|`orgId`| Grafana organization ID | 1 (default org) |\n|`folder`|
Dashboard
folder name | "DebVisor" |\n|`type`| Provisioning type | "file" (from filesystem) or
"cloud"
|\n|`disableDeletion`| Protect dashboards from deletion | true/false |\n|`editable`| Allow manual
editing in UI | true/false |\n|`path`| Dashboard file directory
|`/etc/grafana/provisioning/dashboards`|\n\n### datasources.yaml\n\nPrometheus datasource
provisioning.\n apiVersion: 1\n datasources:\n\n- name: Prometheus-DebVisor\n\n
type:
prometheus\n
access: proxy\n url:
[http://prometheus:9090]([http://prometheus:909]([http://prometheus:90]([http://prometheus:9]([http://prometheus:]([http://prometheus]([http://prometheu]([http://promethe]([http://prometh]([http://promet]([http://prome]([http://prom]([http://pro]([http://pr]([http://p](http://p)r)o)m)e)t)h)e)u)s):)9)0)9)0)\n
isDefault: true\n jsonData:\n timeInterval: 15s\n\n### Datasource Configuration\n\n|
Option |
Purpose | Example |\n|---|---|---|\n|`name`| Datasource identifier | "Prometheus-DebVisor"
|\n|`type`| Datasource type | "prometheus", "loki", "graphite" |\n|`url`| API endpoint
|[http://prometheus:9090]([http://prometheus:909]([http://prometheus:90]([http://prometheus:9]([http://prometheus:]([http://prometheus]([http://prometheu]([http://promethe]([http://prometh]([http://promet]([http://prome]([http://prom]([http://pro]([http://pr]([http://p](http://p)r)o)m)e)t)h)e)u)s):)9)0)9)0)
|\n| `isDefault`| Use as default data source | true/false |\n|`timeInterval`| Query scrape interval
| "15s" (must match Prometheus) |\n\n### Alert Notification Channels\n\n#### email.yaml\n\nEmail
notification configuration.\n notifiers:\n\n- name: "DebVisor Alerts Email"\n\n
type:
"email"\n uid:
"debvisor-email"\n isDefault: false\n settings:\n addresses:
"ops-team@example.com,security@example.com"\n\n### Configuration\n\n| Setting | Purpose
|\n|---|---|\n|`addresses`| Comma-separated recipient emails |\n|`singleEmail`| Send single email
with all alerts or individual emails |\n|`uploadImage`| Attach alert screenshot to email
|\n\n####
slack.yaml\n\nSlack integration.\n notifiers:\n\n- name: "DebVisor Alerts
Slack"\n\n type:
"slack"\n
uid: "debvisor-slack"\n settings:\n url:
"[https://hooks.slack.com/services/YOUR/WEBHOOK/URL"]([https://hooks.slack.com/services/YOUR/WEBHOOK/URL]([https://hooks.slack.com/services/YOUR/WEBHOOK/UR]([https://hooks.slack.com/services/YOUR/WEBHOOK/U]([https://hooks.slack.com/services/YOUR/WEBHOOK/]([https://hooks.slack.com/services/YOUR/WEBHOOK]([https://hooks.slack.com/services/YOUR/WEBHOO]([https://hooks.slack.com/services/YOUR/WEBHO]([https://hooks.slack.com/services/YOUR/WEBH]([https://hooks.slack.com/services/YOUR/WEB]([https://hooks.slack.com/services/YOUR/WE]([https://hooks.slack.com/services/YOUR/W]([https://hooks.slack.com/services/YOUR/]([https://hooks.slack.com/services/YOUR]([https://hooks.slack.com/services/YOU]([https://hooks.slack.com/services/YO]([https://hooks.slack.com/services/Y]([https://hooks.slack.com/services/]([https://hooks.slack.com/services]([https://hooks.slack.com/service]([https://hooks.slack.com/servic]([https://hooks.slack.com/servi]([https://hooks.slack.com/serv]([https://hooks.slack.com/ser]([https://hooks.slack.com/se]([https://hooks.slack.com/s]([https://hooks.slack.com/]([https://hooks.slack.com]([https://hooks.slack.co]([https://hooks.slack.c]([https://hooks.slack.]([https://hooks.slack]([https://hooks.slac]([https://hooks.sla]([https://hooks.sl]([https://hooks.s]([https://hooks.]([https://hooks]([https://hook]([https://hoo](https://hoo)k)s).)s)l)a)c)k).)c)o)m)/)s)e)r)v)i)c)e)s)/)Y)O)U)R)/)W)E)B)H)O)O)K)/)U)R)L)")\n
channel: "#alerts"\n mentionGroups: "ops-team"\n\n### Configuration [2]\n\n| Setting |
Purpose
|\n|---|---|\n|`url`| Slack webhook URL |\n|`channel`| Slack channel for alerts |\n|`mentionGroups`|
Slack user groups to mention (e.g., "@ops-team") |\n|`uploadImage`| Include alert chart in
message
|\n\n#### pagerduty.yaml\n\nPagerDuty integration for incident escalation.\n notifiers:\n\n- name:
"DebVisor PagerDuty"\n\n type: "pagerduty"\n uid: "debvisor-pagerduty"\n
settings:\n
integrationKey:
"YOUR-PAGERDUTY-KEY"\n severity: "critical"\n\n#### webhook.yaml\n\nCustom
webhook for
enterprise
integrations.\n notifiers:\n\n- name: "DebVisor Webhook"\n\n type: "webhook"\n
uid:
"debvisor-webhook"\n settings:\n url:
"[https://monitoring.example.com/alerts/receive"]([https://monitoring.example.com/alerts/receive]([https://monitoring.example.com/alerts/receiv]([https://monitoring.example.com/alerts/recei]([https://monitoring.example.com/alerts/rece]([https://monitoring.example.com/alerts/rec]([https://monitoring.example.com/alerts/re]([https://monitoring.example.com/alerts/r]([https://monitoring.example.com/alerts/]([https://monitoring.example.com/alerts]([https://monitoring.example.com/alert]([https://monitoring.example.com/aler]([https://monitoring.example.com/ale]([https://monitoring.example.com/al]([https://monitoring.example.com/a]([https://monitoring.example.com/]([https://monitoring.example.com]([https://monitoring.example.co]([https://monitoring.example.c]([https://monitoring.example.]([https://monitoring.example]([https://monitoring.exampl]([https://monitoring.examp]([https://monitoring.exam]([https://monitoring.exa]([https://monitoring.ex]([https://monitoring.e]([https://monitoring.]([https://monitoring]([https://monitorin]([https://monitori]([https://monitor]([https://monito]([https://monit]([https://moni]([https://mon]([https://mo]([https://m](https://m)o)n)i)t)o)r)i)n)g).)e)x)a)m)p)l)e).)c)o)m)/)a)l)e)r)t)s)/)r)e)c)e)i)v)e)")\n
httpMethod: "POST"\n\n### Alert Rules (Prometheus)\n\nprometheus.yaml contains alert rules for
Prometheus evaluation.\n\n### Example Rules\n\n groups:\n\n- name:
debvisor_cluster\n\n
rules:\n\n##
Cluster health\n\n- alert: CephClusterDown\n\n expr: |\n ceph_health_status != 0\n for:
5m\n
labels:\n severity: critical\n component: ceph\n annotations:\n summary: "Ceph
cluster is
down"\n
description: "Ceph cluster health status is {{ $value }}"\n\n## Node
offline\n\n- alert:
NodeOffline\n\n expr: |\n up{job="node"} == 0\n for: 5m\n labels:\n severity: warning\n
component:
cluster\n annotations:\n summary: "Node {{ $labels.node }} offline"\n runbook:
"[https://docs.example.com/runbooks/node-offline"]([https://docs.example.com/runbooks/node-offline]([https://docs.example.com/runbooks/node-offlin]([https://docs.example.com/runbooks/node-offli]([https://docs.example.com/runbooks/node-offl]([https://docs.example.com/runbooks/node-off]([https://docs.example.com/runbooks/node-of]([https://docs.example.com/runbooks/node-o]([https://docs.example.com/runbooks/node-]([https://docs.example.com/runbooks/node]([https://docs.example.com/runbooks/nod]([https://docs.example.com/runbooks/no]([https://docs.example.com/runbooks/n]([https://docs.example.com/runbooks/]([https://docs.example.com/runbooks]([https://docs.example.com/runbook]([https://docs.example.com/runboo]([https://docs.example.com/runbo]([https://docs.example.com/runb]([https://docs.example.com/run]([https://docs.example.com/ru]([https://docs.example.com/r]([https://docs.example.com/]([https://docs.example.com]([https://docs.example.co]([https://docs.example.c]([https://docs.example.]([https://docs.example]([https://docs.exampl]([https://docs.examp]([https://docs.exam]([https://docs.exa]([https://docs.ex]([https://docs.e]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)e)x)a)m)p)l)e).)c)o)m)/)r)u)n)b)o)o)k)s)/)n)o)d)e)-)o)f)f)l)i)n)e)")\n\n###
Rule Structure\n\n| Field | Purpose |\n|---|---|\n|`alert`| Alert name (used in
notifications)
|\n|`expr`| PromQL expression (must be true to fire) |\n|`for`| Duration condition must be true
before firing |\n|`labels`| Static labels applied to alert (severity, component)
|\n|`annotations`|
Dynamic fields rendered with alert (summary, description) |\n\n## Provisioning
Workflow\n\n###
Deploying Dashboard Updates\n\n1.**Edit Dashboard:**\n\n## Modify dashboard
JSON\n\n vi
opt/grafana/dashboards/overview.json\n 1.**Validate JSON:**\n\n## Ensure valid
JSON
syntax\n\n jq .
opt/grafana/dashboards/overview.json > /dev/null && echo "Valid"\n 1.**Export
from Grafana
(Optional):**\n\n## After making UI changes, export updated dashboard\n\n curl
-s
[http://grafana:3000/api/dashboards/uid/overview]([http://grafana:3000/api/dashboards/uid/overvie]([http://grafana:3000/api/dashboards/uid/overvi]([http://grafana:3000/api/dashboards/uid/overv]([http://grafana:3000/api/dashboards/uid/over]([http://grafana:3000/api/dashboards/uid/ove]([http://grafana:3000/api/dashboards/uid/ov]([http://grafana:3000/api/dashboards/uid/o]([http://grafana:3000/api/dashboards/uid/]([http://grafana:3000/api/dashboards/uid]([http://grafana:3000/api/dashboards/ui]([http://grafana:3000/api/dashboards/u]([http://grafana:3000/api/dashboards/]([http://grafana:3000/api/dashboards]([http://grafana:3000/api/dashboard]([http://grafana:3000/api/dashboar]([http://grafana:3000/api/dashboa]([http://grafana:3000/api/dashbo]([http://grafana:3000/api/dashb]([http://grafana:3000/api/dash]([http://grafana:3000/api/das]([http://grafana:3000/api/da]([http://grafana:3000/api/d]([http://grafana:3000/api/]([http://grafana:3000/api]([http://grafana:3000/ap]([http://grafana:3000/a]([http://grafana:3000/]([http://grafana:3000]([http://grafana:300]([http://grafana:30]([http://grafana:3]([http://grafana:]([http://grafana]([http://grafan]([http://grafa]([http://graf]([http://gra]([http://gr]([http://g](http://g)r)a)f)a)n)a):)3)0)0)0)/)a)p)i)/)d)a)s)h)b)o)a)r)d)s)/)u)i)d)/)o)v)e)r)v)i)e)w)
\\n\n - H "Authorization: Bearer $GRAFANA_API_TOKEN" | jq . > overview.json\n\n1.**Restart
Grafana:**\n\n## Reload provisioned dashboards\n\n systemctl restart
grafana-server\n\n##
or in
Kubernetes\n\n kubectl rollout restart deployment/grafana -n monitoring\n\n###
Multi-Environment
Provisioning\n\n### Lab Environment (single cluster)\n\n-`dashboards.yaml`:
Point
to`dashboards/lab/`\n\n- Include fixtures dashboard from
opt/monitoring/fixtures/\n\n###
Staging
Environment (multi-node)\n\n- `dashboards.yaml`: Point
to`dashboards/staging/`\n\n-
Include
multi-cluster templates\n\n### Production Environment (HA, multi-cluster)\n\n-
`dashboards.yaml`:
Point to`dashboards/prod/`\n\n- Strict query validation, performance tuning\n\n-
Backup/export
procedure\n\n## Dashboard Consistency Checklist\n\n### For Every New
Dashboard\n\n- []
Follows
naming convention (lowercase, hyphenated)\n\n- [] Has descriptive title and
description\n\n- []
Includes standard variables (`$cluster`,`$time_range`)\n\n- [] Uses standard
color scheme
(green/yellow/red/blue)\n\n- [] All panels have descriptive titles with
units\n\n- [] All
queries
are documented with comments\n\n- [] Thresholds are documented with runbook
links\n\n- []
Performance optimized (appropriate refresh rate)\n\n- [] Legend configured for
clarity\n\n- []
Drill-down links to related dashboards\n\n- [] JSON exported and committed to
git\n\n- []
README
updated with dashboard description\n\n- [] Added to dashboard.yaml provisioning
config\n\n### For
Dashboard Updates\n\n- [] Changes tested in staging first\n\n- [] Query
performance
validated\n\n-
[] Thresholds reviewed with ops team\n\n- [] Changelog entry updated\n\n- []
Dashboard
exported and
committed\n\n- [] Provisioning config updated if needed\n\n- [] Grafana
reloaded/restarted\n\n##
Troubleshooting\n\n### Dashboards Not Appearing\n\n- *Symptom:**Provisioned
dashboards not
visible
in Grafana UI.\n\n### Diagnostic Steps\n\n## 1. Check provisioning config\n\ncat
/etc/grafana/provisioning/dashboards/dashboards.yaml\n\n## 2. Verify dashboard
file
exists\n\nls -la
/etc/grafana/provisioning/dashboards/*.json\n\n## 3. Check Grafana
logs\n\njournalctl -u
grafana-server -n 100\n\n## 4. Verify JSON is valid\n\njq .
/etc/grafana/provisioning/dashboards/overview.json\n\n## 5. Check Grafana
API\n\ncurl -s
[http://grafana:3000/api/search]([http://grafana:3000/api/searc]([http://grafana:3000/api/sear]([http://grafana:3000/api/sea]([http://grafana:3000/api/se]([http://grafana:3000/api/s]([http://grafana:3000/api/]([http://grafana:3000/api]([http://grafana:3000/ap]([http://grafana:3000/a]([http://grafana:3000/]([http://grafana:3000]([http://grafana:300]([http://grafana:30]([http://grafana:3]([http://grafana:]([http://grafana]([http://grafan]([http://grafa]([http://graf]([http://gra]([http://gr]([http://g](http://g)r)a)f)a)n)a):)3)0)0)0)/)a)p)i)/)s)e)a)r)c)h)
\\n\n- H "Authorization: Bearer $GRAFANA_TOKEN" | jq '.'\n\n## Solutions\n\n- Ensure
`path` in
dashboards.yaml matches actual file location\n\n- Verify JSON has no syntax
errors\n\n-
Check file
permissions (Grafana must be able to read)\n\n- Restart Grafana after
provisioning config
changes\n\n### Queries Not Working\n\n- *Symptom:**Panels show "No data" or
error
messages.\n\n###
Diagnostic Steps [2]\n\n## 1. Verify Prometheus is accessible\n\ncurl
[http://prometheus:9090/-/healthy]([http://prometheus:9090/-/health]([http://prometheus:9090/-/healt]([http://prometheus:9090/-/heal]([http://prometheus:9090/-/hea]([http://prometheus:9090/-/he]([http://prometheus:9090/-/h]([http://prometheus:9090/-/]([http://prometheus:9090/-]([http://prometheus:9090/]([http://prometheus:9090]([http://prometheus:909]([http://prometheus:90]([http://prometheus:9]([http://prometheus:]([http://prometheus]([http://prometheu]([http://promethe]([http://prometh]([http://promet]([http://prome]([http://prom]([http://pro]([http://pr]([http://p](http://p)r)o)m)e)t)h)e)u)s):)9)0)9)0)/)-)/)h)e)a)l)t)h)y)\n\n##

- Test query in Prometheus directly\n\ncurl
'[http://prometheus:9090/api/v1/query?query=up']([http://prometheus:9090/api/v1/query?query=up]([http://prometheus:9090/api/v1/query?query=u]([http://prometheus:9090/api/v1/query?query=]([http://prometheus:9090/api/v1/query?query]([http://prometheus:9090/api/v1/query?quer]([http://prometheus:9090/api/v1/query?que]([http://prometheus:9090/api/v1/query?qu]([http://prometheus:9090/api/v1/query?q]([http://prometheus:9090/api/v1/query?]([http://prometheus:9090/api/v1/query]([http://prometheus:9090/api/v1/quer]([http://prometheus:9090/api/v1/que]([http://prometheus:9090/api/v1/qu]([http://prometheus:9090/api/v1/q]([http://prometheus:9090/api/v1/]([http://prometheus:9090/api/v1]([http://prometheus:9090/api/v]([http://prometheus:9090/api/]([http://prometheus:9090/api]([http://prometheus:9090/ap]([http://prometheus:9090/a]([http://prometheus:9090/]([http://prometheus:9090]([http://prometheus:909]([http://prometheus:90]([http://prometheus:9]([http://prometheus:]([http://prometheus]([http://prometheu]([http://promethe]([http://prometh]([http://promet]([http://prome]([http://prom]([http://pro]([http://pr]([http://p](http://p)r)o)m)e)t)h)e)u)s):)9)0)9)0)/)a)p)i)/)v)1)/)q)u)e)r)y)?)q)u)e)r)y)=)u)p)')\n\n##

- Check datasource configuration\n\ncurl
[http://grafana:3000/api/datasources]([http://grafana:3000/api/datasource]([http://grafana:3000/api/datasourc]([http://grafana:3000/api/datasour]([http://grafana:3000/api/datasou]([http://grafana:3000/api/dataso]([http://grafana:3000/api/datas]([http://grafana:3000/api/data]([http://grafana:3000/api/dat]([http://grafana:3000/api/da]([http://grafana:3000/api/d]([http://grafana:3000/api/]([http://grafana:3000/api]([http://grafana:3000/ap]([http://grafana:3000/a]([http://grafana:3000/]([http://grafana:3000]([http://grafana:300]([http://grafana:30]([http://grafana:3]([http://grafana:]([http://grafana]([http://grafan]([http://grafa]([http://graf]([http://gra]([http://gr]([http://g](http://g)r)a)f)a)n)a):)3)0)0)0)/)a)p)i)/)d)a)t)a)s)o)u)r)c)e)s)
\\n\n- H "Authorization: Bearer $GRAFANA_TOKEN" | jq '.'\n\n## 4. Look at Grafana logs for
query
errors\n\njournalctl -u grafana-server -f | grep -i error\n\n## 5. Verify metrics
exist\n\ncurl
'[http://prometheus:9090/api/v1/series?match[]=node_cpu_seconds_total'][)]([http://prometheus:9090/api/v1/series?match[]=node_cpu_seconds_total]([http://prometheus:9090/api/v1/series?match[]=node_cpu_seconds_tota]([http://prometheus:9090/api/v1/series?match[]=node_cpu_seconds_tot]([http://prometheus:9090/api/v1/series?match[]=node_cpu_seconds_to]([http://prometheus:9090/api/v1/series?match[]=node_cpu_seconds_t]([http://prometheus:9090/api/v1/series?match[]=node_cpu*seconds*]([http://prometheus:9090/api/v1/series?match[]=node_cpu*seconds]([http://prometheus:9090/api/v1/series?match[]=node_cpu*second]([http://prometheus:9090/api/v1/series?match[]=node_cpu*secon]([http://prometheus:9090/api/v1/series?match[]=node_cpu*seco]([http://prometheus:9090/api/v1/series?match[]=node_cpu*sec]([http://prometheus:9090/api/v1/series?match[]=node_cpu*se]([http://prometheus:9090/api/v1/series?match[]=node_cpu*s]([http://prometheus:9090/api/v1/series?match[]=node_cpu*]([http://prometheus:9090/api/v1/series?match[]=node_cpu]([http://prometheus:9090/api/v1/series?match[]=node*cp]([http://prometheus:9090/api/v1/series?match[]=node*c]([http://prometheus:9090/api/v1/series?match[]=node*]([http://prometheus:9090/api/v1/series?match[]=node]([http://prometheus:9090/api/v1/series?match[]=nod]([http://prometheus:9090/api/v1/series?match[]=no]([http://prometheus:9090/api/v1/series?match[]=n]([http://prometheus:9090/api/v1/series?match[]=]([http://prometheus:9090/api/v1/series?match[]]([http://prometheus:9090/api/v1/series?match[]([http://prometheus:9090/api/v1/series?match]([http://prometheus:9090/api/v1/series?matc]([http://prometheus:9090/api/v1/series?mat]([http://prometheus:9090/api/v1/series?ma]([http://prometheus:9090/api/v1/series?m]([http://prometheus:9090/api/v1/series?]([http://prometheus:9090/api/v1/series]([http://prometheus:9090/api/v1/serie]([http://prometheus:9090/api/v1/seri]([http://prometheus:9090/api/v1/ser]([http://prometheus:9090/api/v1/se]([http://prometheus:9090/api/v1/s]([http://prometheus:9090/api/v1/]([http://prometheus:9090/api/v1](http://prometheus:9090/api/v1)/)s)e)r)i)e)s)?)m)a)t)c)h))=)n)o)d)e)*)c)p)u)*)s)e)c)o)n)d)s)*)t)o)t)a)l)')\n\n##
Solutions [2]\n\n- Verify metric names are correct (check prometheus:9090 for
available
metrics)\n\n- Ensure label matchers match actual label values\n\n- Check for
typos in
variable
references\n\n- Verify Prometheus scrape config is working\n\n### Performance
Issues\n\n-
*Symptom:**Dashboards load slowly, Grafana UI sluggish.\n\n###
Optimization\n\n## Reduce
refresh
rate for non-critical panels\n\n"refresh": "1m" # Instead of "10s"\n\n## Limit
query time
range\n\n"timeshift": "1h" # Instead of "7d"\n\n## Use simpler
aggregations\n\nrate(metric[5m]) #
Instead of complex joins\n\n## Add query caching\n\n"cacheTimeout": "60s"\n\n##
Optimize
alert
queries\n\n## Use static thresholds instead of dynamic calculations\n\n## Best
Practices
[2]\n\n###
Dashboard Development\n\n 1.**Start with Dashboarding Tutorial:**Begin with
DASHBOARD_TEMPLATE.json\n 1.**Test Queries First:**Validate PromQL in Prometheus
UI before
adding to
dashboard\n 1.**Use Meaningful Names:**Dashboard and panel names should clearly
indicate
what's
being monitored\n 1.**Document Everything:**Add descriptions, runbook links,
threshold
justifications\n 1.**Version Control:**Keep dashboard JSON in git with commit
messages\n\n###
Dashboard Maintenance\n\n 1.**Regular Review:**Audit dashboards quarterly
for:\n\n- Unused
panels
(remove clutter)\n\n- Outdated thresholds (validate with ops team)\n\n- Broken
links or
queries\n\n-
Performance issues\n\n 1.**Monitor Usage:**Track which dashboards are most
viewed\n\n-
Prioritize
improvements for high-traffic dashboards\n\n- Consider deprecating unused
dashboards\n\n
1.**Gather
Feedback:**Regularly ask ops teams:\n\n- Is this dashboard helpful?\n\n- What's
missing?\n\n- What
would make monitoring easier?\n\n### Alert Tuning\n\n 1.**Avoid Alert
Fatigue:**Excessive
alerts
reduce effectiveness\n\n- Keep critical alert count manageable\n\n- Use for
truly
actionable
conditions\n\n- Avoid duplicate/related alerts\n\n 1.**False Positive
Reduction:**\n\n-
Add 5-10
minute grace periods (`for: 5m`)\n\n- Use aggregations to smooth noise\n\n-
Verify
thresholds with
real data\n\n 1.**Runbook Linkage:**\n\n- Every alert should link to a
runbook\n\n-
Runbook should
guide to resolution\n\n- Update runbooks based on incidents\n\n## Integration
with
Monitoring\n\n###
Prometheus Scrapers\n\n Ensure Prometheus scrape config
includes:\nscrape_configs:\n\n-
job_name:
'node'\n\n static_configs:\n\n- targets: ['localhost:9100']\n\n- job_name:
'ceph'\n\n
static_configs:\n\n- targets: ['ceph-mgr:9283']\n\n- job_name: 'kubernetes'\n\n
kubernetes_sd_configs:\n\n- role: endpoints\n\n### Alertmanager Integration\n\n
Grafana-generated
alerts flow to AlertManager:\nGrafana Alert Rule Fired\n v\nAlertManager
Receives Alert\n
v\nAlertManager Routes to Notification Channels\n v\nNotification Sent (Email,
Slack,
PagerDuty,
Webhook)\n\n### Loki Log Integration\n\n Dashboards can embed logs from
Loki:\n[Grafana
Dashboard
Panel]\n v\nLoki Query: {job="system-logs", level="error"}\n v\n[Logs displayed
alongside
metrics]\n\n## References\n\n- [Grafana
Documentation]([https://grafana.com/docs/grafana/latest]([https://grafana.com/docs/grafana/lates]([https://grafana.com/docs/grafana/late]([https://grafana.com/docs/grafana/lat]([https://grafana.com/docs/grafana/la]([https://grafana.com/docs/grafana/l]([https://grafana.com/docs/grafana/]([https://grafana.com/docs/grafana]([https://grafana.com/docs/grafan]([https://grafana.com/docs/grafa]([https://grafana.com/docs/graf]([https://grafana.com/docs/gra]([https://grafana.com/docs/gr]([https://grafana.com/docs/g]([https://grafana.com/docs/]([https://grafana.com/docs]([https://grafana.com/doc]([https://grafana.com/do]([https://grafana.com/d]([https://grafana.com/]([https://grafana.com]([https://grafana.co]([https://grafana.c]([https://grafana.]([https://grafana]([https://grafan]([https://grafa]([https://graf]([https://gra]([https://gr]([https://g](https://g)r)a)f)a)n)a).)c)o)m)/)d)o)c)s)/)g)r)a)f)a)n)a)/)l)a)t)e)s)t)/)\n\n-
[Prometheus
Querying]([https://prometheus.io/docs/prometheus/latest/querying/basics]([https://prometheus.io/docs/prometheus/latest/querying/basic]([https://prometheus.io/docs/prometheus/latest/querying/basi]([https://prometheus.io/docs/prometheus/latest/querying/bas]([https://prometheus.io/docs/prometheus/latest/querying/ba]([https://prometheus.io/docs/prometheus/latest/querying/b]([https://prometheus.io/docs/prometheus/latest/querying/]([https://prometheus.io/docs/prometheus/latest/querying]([https://prometheus.io/docs/prometheus/latest/queryin]([https://prometheus.io/docs/prometheus/latest/queryi]([https://prometheus.io/docs/prometheus/latest/query]([https://prometheus.io/docs/prometheus/latest/quer]([https://prometheus.io/docs/prometheus/latest/que]([https://prometheus.io/docs/prometheus/latest/qu]([https://prometheus.io/docs/prometheus/latest/q]([https://prometheus.io/docs/prometheus/latest/]([https://prometheus.io/docs/prometheus/latest]([https://prometheus.io/docs/prometheus/lates]([https://prometheus.io/docs/prometheus/late]([https://prometheus.io/docs/prometheus/lat]([https://prometheus.io/docs/prometheus/la]([https://prometheus.io/docs/prometheus/l]([https://prometheus.io/docs/prometheus/]([https://prometheus.io/docs/prometheus]([https://prometheus.io/docs/prometheu]([https://prometheus.io/docs/promethe]([https://prometheus.io/docs/prometh]([https://prometheus.io/docs/promet]([https://prometheus.io/docs/prome]([https://prometheus.io/docs/prom]([https://prometheus.io/docs/pro]([https://prometheus.io/docs/pr]([https://prometheus.io/docs/p]([https://prometheus.io/docs/]([https://prometheus.io/docs]([https://prometheus.io/doc]([https://prometheus.io/do]([https://prometheus.io/d]([https://prometheus.io/](https://prometheus.io/)d)o)c)s)/)p)r)o)m)e)t)h)e)u)s)/)l)a)t)e)s)t)/)q)u)e)r)y)i)n)g)/)b)a)s)i)c)s)/)\n\n-
[AlertManager
Configuration]([https://prometheus.io/docs/alerting/latest/configuration]([https://prometheus.io/docs/alerting/latest/configuratio]([https://prometheus.io/docs/alerting/latest/configurati]([https://prometheus.io/docs/alerting/latest/configurat]([https://prometheus.io/docs/alerting/latest/configura]([https://prometheus.io/docs/alerting/latest/configur]([https://prometheus.io/docs/alerting/latest/configu]([https://prometheus.io/docs/alerting/latest/config]([https://prometheus.io/docs/alerting/latest/confi]([https://prometheus.io/docs/alerting/latest/conf]([https://prometheus.io/docs/alerting/latest/con]([https://prometheus.io/docs/alerting/latest/co]([https://prometheus.io/docs/alerting/latest/c]([https://prometheus.io/docs/alerting/latest/]([https://prometheus.io/docs/alerting/latest]([https://prometheus.io/docs/alerting/lates]([https://prometheus.io/docs/alerting/late]([https://prometheus.io/docs/alerting/lat]([https://prometheus.io/docs/alerting/la]([https://prometheus.io/docs/alerting/l]([https://prometheus.io/docs/alerting/]([https://prometheus.io/docs/alerting]([https://prometheus.io/docs/alertin]([https://prometheus.io/docs/alerti]([https://prometheus.io/docs/alert]([https://prometheus.io/docs/aler]([https://prometheus.io/docs/ale]([https://prometheus.io/docs/al]([https://prometheus.io/docs/a]([https://prometheus.io/docs/]([https://prometheus.io/docs]([https://prometheus.io/doc]([https://prometheus.io/do]([https://prometheus.io/d]([https://prometheus.io/]([https://prometheus.io]([https://prometheus.i]([https://prometheus.]([https://prometheus](https://prometheus).)i)o)/)d)o)c)s)/)a)l)e)r)t)i)n)g)/)l)a)t)e)s)t)/)c)o)n)f)i)g)u)r)a)t)i)o)n)/)\n\n-
[DebVisor Monitoring Overview](./opt/monitoring/README.md)\n\n- [DebVisor Fixtures
Guide](./opt/monitoring/FIXTURES_GUIDE.md)\n\n## Related Documentation\n\n- See
[opt/monitoring/README.md](./opt/monitoring/README.md) for Prometheus and monitoring
infrastructure\n\n- See
[opt/monitoring/FIXTURES_GUIDE.md](./opt/monitoring/FIXTURES_GUIDE.md) for
testing dashboards with synthetic data\n\n- See
[opt/docs/GLOSSARY.md](./opt/docs/GLOSSARY.md) for
monitoring terminology\n\n## Next Steps\n\n1.**Template Library:**Create
dashboard
templates for
different cluster sizes\n1.**Multi-Cluster:**Build multi-cluster comparison
dashboards\n1.**Tenant
Isolation:**Support dashboards for multi-tenant deployments\n1.**BI
Integration:**Export
dashboard
data for business intelligence\n1.**Custom Metrics:**Add facility for custom
application
metrics
visualization\n\n
