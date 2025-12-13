# Grafana Dashboard Design Standards\n\n## Overview\n\nThis document defines design

standards and

conventions for all DebVisor Grafana dashboards. Adherence to these standards ensures
consistent
user experience, maintainability, and reliable monitoring across the platform.\n\n###
Goals\n\n-
Provide intuitive, discoverable dashboards for operators of all skill levels\n\n- Enable
consistent
visualization across heterogeneous environments\n\n- Simplify dashboard maintenance and
evolution\n\n- Reduce cognitive load for operators using multiple dashboards\n\n## Naming
Standards\n\n### Dashboard Naming Convention\n\nAll dashboard names MUST follow this
format:\n\n-
[-]\n\n### Examples\n\n ? GOOD:\n\n- overview (system-wide overview)\n\n- dns-dhcp (DNS
and DHCP
services)\n\n- ceph-performance (Ceph I/O performance)\n\n- kubernetes-workloads
(Kubernetes
workload status)\n\n- security-events (Security events and logging)\n\n ? BAD:\n\n-
Dashboard1 (not
descriptive)\n\n- KubeMetrics (inconsistent casing)\n\n- ceph performance (spaces, should
be
hyphenated)\n\n- k8s_cluster_status (underscores, too specific)\n\n### Naming
Hierarchy\n\n| Level |
Examples | Purpose |\n|---|---|---|\n| System | `overview`| Cluster-wide status |\n|
Component
|`dns-dhcp`,`ceph-health`,`kubernetes`| Specific service |\n| Aspect
|`-performance`,`-capacity`,`-security`| Specific metric category |\n\n### Panel Naming
Convention\n\nPanel titles MUST be:\n\n- **CamelCase:**"CPU Usage", "Query Latency", "OSD
Health"\n\n- **Descriptive:**Indicates what metric is shown\n\n- **Unit-aware:**Include
units in
title or legend\n\n- **Role-appropriate:**Clear for target audience (operator, architect,
dev)\n\n### Examples [2]\n\n {\n "title": "CPU Usage (%)",\n "targets": [\n {"expr":
"sum(rate(node_cpu_seconds_total[5m]))"}\n ]\n }\n\n### Variable Naming Convention\n\nAll
template
variables MUST use lowercase with underscores:\n $cluster_name // Cluster identifier\n
$time_range
// Time range selector\n $node_filter // Node name filter\n $namespace_filter //
Kubernetes
namespace filter\n $severity*level // Alert severity (critical/warning/info)\n $component
//
Component/service (ceph/k8s/dns)\n\n### Pattern\n\n $*\n ? Correct: $pod_namespace,
$osd_filter,
$alert_severity\n ? Wrong: $pod-namespace (hyphens), $POD_NAMESPACE (caps), $_pod (leading
underscore)\n\n## Color Standards\n\n### Primary Palette\n\nAll dashboards MUST use this
standard
color palette:\n Success/Healthy: #31C740 (Green)\n Warning/Caution: #F2AC29
(Orange/Yellow)\n
Critical/Error: #D64E4E (Red)\n Information: #3498DB (Blue)\n Neutral/Offline: #95A5A6
(Gray)\n
Custom/User: #9B59B6 (Purple)\n\n### Color Usage Guidelines\n\n| Semantic Meaning | Color
| Use
Cases |\n|---|---|---|\n|**Success / OK**| Green (#31C740) | Healthy systems, running
services,
successful operations |\n|**Warning / Degraded**| Yellow (#F2AC29) | High utilization,
slow
responses, non-critical issues |\n|**Critical / Error**| Red (#D64E4E) | System down,
failed
operations, emergency conditions |\n|**Informational**| Blue (#3498DB) | Neutral metrics,
counts,
informational data |\n|**Neutral / Offline**| Gray (#95A5A6) | Disabled, offline, pending,
or no
data |\n|**Custom**| Purple (#9B59B6) | Custom user-defined metrics, non-standard states
|\n\n###
Multi-Series Coloring\n\nFor dashboards with many series (e.g., per-node metrics):\n
Automatic
Series Colors (Grafana defaults):\n Series 1: Blue\n Series 2: Orange\n Series 3: Green\n
Series 4:
Red\n Series 5: Purple\n ...\n\n### Override when necessary\n\n- Use semantic colors for
important
series\n\n- Avoid color-blind confusing combinations (red-green at 1:1 ratio)\n\n- Legend
should
clearly indicate what each color represents\n\n## Panel Layout Standards\n\n### Grid
System\n\nGrafana uses a 12-column grid system. Standard panel widths:\n| Panel Type |
Width |
Height | Use Case |\n|---|---|---|---|\n|**Stat/Gauge**| 3 columns | 4 rows | Quick health
summary
|\n|**Small Time Series**| 6 columns | 8 rows | Trends for single metric |\n|**Standard Time
Series**| 12 columns | 8 rows | Primary performance metric |\n|**Detailed Table**| 12
columns | 10+
rows | Large result sets |\n|**Heatmap/Histogram**| 12 columns | 8 rows | Distribution
visualization
|\n\n### Layout Structure\n\n### Recommended Dashboard Structure\n\n Row 1: Title, Summary Stats (4x
stat panels, each 3 cols wide)\n Row 2: Primary Metrics (1-2 large time series panels)\n
Row 3:
Secondary Metrics (2-4 medium panels)\n Row 4: Detailed Analysis (Large table, heatmap, or
node
graph)\n Row 5: Logs/Events (Logs panel or events)\n Row 6: Related Links /
Drill-downs\n\n###
Example Layout\n\n +---------------------------------------------------------+\n |
Dashboard Title:
Ceph Cluster Health |\n +---------------------------------------------------------+\n |
+----------+
+----------+ +----------+ +----------+ | Row 1\n | | Monitors | | Capacity | | PGs | |
OSDs | |
Summary\n | | 8/8 | | 2.3 PB | | OK 2100 | | All OK | | (4 cols x 4 rows)\n | +----------+
+----------+ +----------+ +----------+ |\n
+---------------------------------------------------------+\n | | Row 2\n | IOPS &
Throughput (12
cols x 8 rows) | Primary\n | | metric\n | [Time series graph showing IOPS and throughput
over] |\n |
[the past 7 days with legend] |\n
+---------------------------------------------------------+\n |
+----------------------------+ +------------------+ | Row 3\n | | Cluster Latency | | PG
Status | |
Secondary\n | | [Time series: p95/p99] | | 2100 PGs OK | | metrics\n |
+----------------------------+ | 23 PGs Degraded | |\n | | 5 PGs Stuck | |\n |
+------------------+
|\n +---------------------------------------------------------+\n | | Row 4\n | OSD Status Table (12
cols x 10 rows) | Detailed\n | [Sortable table: OSD ID, Status, KB Used, IOPS, etc] |\n
+---------------------------------------------------------+\n | Recent Events (12 cols x 4
rows) |
Row 5\n | [Log entries: Timestamp | Event | Severity] | Logs\n
+---------------------------------------------------------+\n\n### Spacing &
Alignment\n\n-
**Horizontal:**1-2 column gap between panels on same row\n\n- **Vertical:**1 row gap
between major
sections\n\n- **Panel padding:**Let Grafana default (8px)\n\n- **Consistency:**Align
similar panels
vertically\n\n## Visualization Standards\n\n### Panel Types and Selection\n\n### Metric
Visualization Decision Tree\n\n What are you visualizing?\n |\n +- Single value (e.g., "%
CPU used")
-> Stat panel\n | +- With gauge ring? -> Gauge panel\n |\n +- Time series (metric over
time) -> Time
series panel\n | +- With area shading? -> Area graph\n | +- With distribution? -> Time
series +
histogram\n |\n +- Distribution (latency histogram) -> Histogram panel\n |\n +-
Proportions (%
allocation) -> Pie/donut chart\n |\n +- Tabular data (detailed results) -> Table panel\n |
+-
Sortable? Need interactivity? -> Add table options\n |\n +- Log entries (error logs, audit
trail) ->
Logs panel\n |\n +- Service/component relationships -> Node graph panel\n |\n +-
Geographic
distribution -> Geomap panel (if applicable)\n\n### Panel Configuration Standards\n\n####
Stat
Panel\n\n {\n "type": "stat",\n "title": "CPU Usage (%)",\n "targets": [\n {"expr":
"sum(rate(node_cpu_seconds_total{mode!='idle'}[5m])) *100"}\n ],\n "options": {\n
"graphMode":
"area",\n "colorMode": "background",\n "textMode": "auto",\n "thresholds": {\n "mode":
"percentage",\n "steps": [\n {"color": "green", "value": null},\n {"color": "yellow",
"value":
70},\n {"color": "red", "value": 90}\n ]\n },\n "unit": "percent"\n }\n }\n\n#### Time
Series
Panel\n\n {\n "type": "timeseries",\n "title": "Network Traffic (Bytes/sec)",\n "targets":
[\n {\n
"expr": "sum by (interface) (rate(node_network_transmit_bytes_total[5m]))",\n
"legendFormat":
"{{interface}}"\n }\n ],\n "options": {\n "legend": {\n "displayMode": "table",\n
"placement":
"right",\n "values": ["value", "max", "mean"]\n },\n "thresholds": {\n "mode":
"percentage",\n
"steps": [\n {"color": "green", "value": null},\n {"color": "yellow", "value": 70},\n
{"color":
"red", "value": 85}\n ]\n }\n },\n "fieldConfig": {\n "custom": {\n "hideFrom":
{"tooltip": false,
"legend": false, "viz": false}\n }\n }\n }\n\n#### Table Panel\n\n {\n "type": "table",\n
"title":
"OSD Status",\n "targets": [\n {\n "expr": "ceph_osd_info"\n }\n ],\n "options": {\n
"showHeader":
true,\n "sortBy": ["osd_id"],\n "customSort": true,\n "displayMode": "auto"\n }\n }\n\n###
Legend
Configuration\n\n### Standard Legend Format\n\n {\n "legend": {\n "displayMode": "table",
// "table"
or "list"\n "placement": "right", // "right", "bottom", or "top"\n "showLegend": true,\n
"values":
[// What to show in legend\n "value", // Current value\n "max", // Maximum value\n "mean"
//
Mean/average value\n]\n }\n }\n\n### Legend Placement\n\n-**Right:**Best for 2-5 series
(vertical
list)\n\n- **Bottom:**Good for 6+ series (horizontal, may wrap)\n\n- **Top:**Minimal; use
only when
space is tight\n\n### Legend Values\n\n- **Always include:**Current value (for operators
to quickly
see status)\n\n- **Add:**Max/Min for context on range\n\n- **Optional:**Mean, Last (if
beneficial
for metric)\n\n## Threshold Configuration\n\n### Threshold Definition Standard\n\n###
Every metric
MUST have defined thresholds with justification\n\n### Format\n\n {\n "thresholds": {\n
"mode":
"absolute", // "absolute" or "percentage"\n "steps": [\n {\n "color": "green",\n "value":
null //
null = -?\n },\n {\n "color": "yellow",\n "value": 70, // Warning at 70\n "annotation":
"High
utilization"\n },\n {\n "color": "red",\n "value": 90 // Critical at 90\n }\n ]\n }\n
}\n\n###
Common Metric Thresholds\n\n### Infrastructure Metrics\n\n| Metric | Warning | Critical |
Rationale
|\n|---|---|---|---|\n| CPU Utilization | 70% | 90% | Headroom for spikes |\n| Memory Utilization |
80% | 95% | Risk of OOM killer activation |\n| Disk Utilization | 80% | 95% | I/O
performance
degradation above 85% |\n| Network Utilization | 75% | 90% | 10G links usually have <1%
loss at 85%+
|\n| Disk I/O Latency | 5ms | 20ms | Applications typically timeout >100ms |\n\n### Service
Metrics\n\n| Metric | Warning | Critical | Rationale |\n|---|---|---|---|\n| Query Latency
(DNS) |
50ms | 200ms | Typical DNS answers in 1-5ms |\n| Pod Restart Count | 3/hour | 10/hour |
Indicates
instability |\n| PG Degraded (Ceph) | 1+ | Any | Should never have degraded PGs long-term
|\n| Node
CPU Throttle | 5% | 20% | Indicates oversubscription |\n| API Server Latency | 100ms |
500ms |
Kubernetes expects <100ms |\n\n### Threshold Documentation\n\nEvery threshold MUST be
documented
with:\n1.**Metric Name:**What is being measured?\n1.**Threshold Values:**Warning and
critical
levels\n1.**Justification:**Why these specific numbers?\n1.**Tuning Guidance:**How to
adjust for
different environments\n1.**Runbook Link:**Where to go for remediation\n\n### Example
Documentation\n\n### Query Latency (dns-dhcp.json)\n\n### Thresholds\n\n- Warning: >100ms
(p95)\n\n-
Critical: >500ms (p95)\n\n### Justification\n\n- DNS typically responds in 1-5ms
locally\n\n- Cloud
DNS response times are 20-50ms\n\n- >100ms indicates resolver performance issue\n\n-

>500ms
indicates network problem or resolver down\n\n### Tuning\n\n- High-latency networks
(satellite):
Adjust to 200ms warning / 1000ms critical\n\n- Local labs: Can tighten to 50ms warning /
200ms
critical\n\n- *Runbook:**[DNS Query Latency
Troubleshooting]([https://docs.example.com/runbooks/dns-latenc]([https://docs.example.com/runbooks/dns-laten]([https://docs.example.com/runbooks/dns-late]([https://docs.example.com/runbooks/dns-lat]([https://docs.example.com/runbooks/dns-la]([https://docs.example.com/runbooks/dns-l]([https://docs.example.com/runbooks/dns-]([https://docs.example.com/runbooks/dns](https://docs.example.com/runbooks/dns)-)l)a)t)e)n)c)y)\n\n##
Query Standards\n\n### Query Naming & Documentation\n\n### All queries MUST
have\n\n1.**Legend
format**indicating what's being shown\n1.**Comment**explaining the query\n1.**Aggregation
level**(per-node, per-pool, cluster-wide)\n\n### Example\n\n## CPU utilization per node
(%)\n\n## =
100 *(1 - idle_fraction)\n\n## Aggregation: per node (enables comparison between
nodes)\n\n 100*(1 -
avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))\n\n## PromQL Best
Practices\n\n### 1. Use Explicit Label Matchers\n\n ? GOOD:\n sum by (cluster, job)
(rate(node_cpu_seconds_total{mode="user"}[5m]))\n ? BAD:\n
sum(rate(node_cpu_seconds_total[5m])) #
Includes all modes (idle, user, system, ...)\n\n### 2. Aggregation Choice Matters\n\n ?
Right
aggregation:\n avg by (instance) (...) # Average per node\n ? Wrong aggregation:\n sum by
(instance)
(...) # Would give sum across modes (meaningless)\n\n### 3. Use Functions Appropriate to
Metric
Type\n\n Counter metrics (always increasing):\n ? rate() # Rate of increase per second\n ?
increase() # Total increase over time window\n Gauge metrics (can go up or down):\n ?
avg() #
Average value\n ? max() # Peak value\n Histogram metrics (multiple buckets):\n ?
histogram_quantile(0.95, ...) # 95th percentile\n\n### Query Performance\n\n###
Guidelines\n\n1.**Time windows:**5m for frequent checks, 1h for trends\n1.**Scrape
interval
alignment:**Queries should align with scrape interval\n\n- If scraping every 15s,
use`[5m]`(20 data
points minimum)\n\n- Avoid`[10s]`(too few data points, inaccurate)\n\n1.**Aggregation
order:**Aggregate early to reduce data volume\n ? GOOD: sum by (cluster) (...) # Aggregate
first\n ?
BAD: sum(rate(...)) by (cluster) # Full rate first, then aggregate\n 1.**Label
cardinality:**Avoid
high-cardinality labels in grouping\n ? GOOD: sum by (cluster, node) (...) # Bounded set
of nodes\n
? BAD: sum by (path) (...) # Thousands of possible paths -> explosion\n\n## Interactivity
Standards\n\n### Drill-Down Navigation\n\n Dashboards SHOULD enable drill-down to more
detailed
views:\n{\n "fieldConfig": {\n "defaults": {\n "links": [\n {\n "title": "View Node
Details",\n
"url": "d/node-details?var-node=${node}",\n "targetBlank": false\n }\n ]\n }\n }\n}\n\n###
Drill-down Pattern\n\nSystem Overview\n v (click node)\nNode Details Dashboard\n v (click
pod)\nPod
Details Dashboard\n\n### Template Variables\n\n### Standard Variable Patterns\n\n{\n
"templating":
{\n "list": [\n {\n "name": "cluster_name",\n "type": "query",\n "datasource":
"Prometheus-DebVisor",\n "query": "label_values(up, cluster)",\n "current": {"text":
"DebVisor",
"value": "DebVisor"},\n "multi": false\n },\n {\n "name": "time_range",\n "type":
"interval",\n
"values": ["5m", "15m", "1h", "6h", "1d", "7d"],\n "current": {"text": "1h", "value":
"1h"}\n },\n
{\n "name": "node_filter",\n "type": "query",\n "datasource": "Prometheus-DebVisor",\n
"query":
"label_values(node_cpu_seconds*total, instance)",\n "multi": true,\n "current": {"text":
"All",
"value": "$*_all"}\n }\n ]\n }\n}\n\n### Standard Variables to Include\n\n | Variable |
Type |
Purpose | Multi-Select |\n |---|---|---|---|\n |`cluster_name`| Query | Filter by cluster
| No |\n
|`time_range`| Interval | Time window selector | No |\n |`node_filter`| Query | Filter by node | Yes
|\n |`namespace_filter`| Query | Filter by K8s namespace | Yes |\n |`severity_filter` | Custom |
Filter by alert severity | Yes |\n\n## Performance Standards\n\n### Refresh Rates\n\n###
Dashboard
refresh rates MUST match operational needs\n\n | Dashboard Type | Refresh Rate | Rationale
|\n
|---|---|---|\n |**Critical Alerts**| 10s | Real-time visibility for emergency response |\n
|**System Overview**| 30s | Balance between real-time and load |\n |**Performance Metrics**| 30s |
Sufficient for trend detection |\n |**Capacity Planning**| 5m | Longer-term trends, less
sensitive
to spikes |\n |**Compliance/Audit**| 1m | Historical data, not time-sensitive |\n\n###
Query
Optimization\n\n### Timeouts and Limits\n\ntimeout: 30s # Max query execution
time\nmax_samples:
1000000 # Max time series returned\nmax_data_points: 10000 # Max points plotted\n\n### For
Large
Dashboards\n\n- Limit panels to <20 per dashboard (improves load time)\n\n- Use cached
queries where
possible\n\n- Stagger refresh rates (some panels 30s, some 1m)\n\n- Avoid overlapping time
windows\n\n## Accessibility Standards\n\n### Color Blindness Considerations\n\n Dashboards
MUST be
readable for colorblind users:\n? NOT colorblind-safe:\n Red-green threshold (users with
protanopia
can't distinguish)\n? Colorblind-safe:\n Red-yellow-green threshold (distinct hues for
most color
blindness types)\n Blue-orange threshold (highly distinguishable)\n\n### Fonts &
Readability\n\n-**Minimum font size:**12px for normal text\n\n- **Panel titles:**14px+ for
clarity\n\n- **Legend:**11px+ for readability\n\n- **Contrast ratio:**Minimum 4.5:1 for
text on
background\n\n### Keyboard Navigation\n\n Dashboards should be keyboard-navigable:\n\n-
Tab through
panels\n\n- Arrow keys to scroll\n\n- Enter to drill-down on interactive elements\n\n##
Testing &
Validation\n\n### Dashboard Testing Checklist\n\n Before committing a new dashboard:\n\n-
[]**Visual
Layout:**Panels aligned consistently, no overlaps\n\n- []**Queries:**All queries execute
successfully in Prometheus\n\n- []**Data:**Verify metrics are flowing correctly\n\n-
[]**Thresholds:**Test threshold transitions (green->yellow->red)\n\n- []**Variables:**Test
all
template variable combinations\n\n- []**Drill-down:**Test navigation links\n\n-
[]**Performance:**Dashboard loads in <5 seconds\n\n- []**Legends:**All series labeled and
color-coded\n\n- []**Units:**All metrics show appropriate units\n\n-
[]**Documentation:**Dashboard
description and runbooks present\n\n### CI Validation\n\n Consider adding automated
validation:\n\n## Validate dashboard JSON\n\njq -e '.dashboard' dashboards/*.json\n\n##
Validate
queries with PromQL linter\n\npromtool check rules dashboards/*\n\n## Test provisioning
config\n\ngrafana-cli admin export-dashboard overview > /tmp/test.json\n\n## Migration &
Versioning\n\n### Dashboard Versioning\n\n Track dashboard changes:\n{\n "dashboard": {\n
"title":
"Overview",\n "version": 5,\n "lastSavedTime": "2025-01-15T10:30:00Z",\n "lastSavedBy":
"ops-team"\n
}\n}\n\n### Version Bumping\n\n- Major (v1.0 -> v2.0): Breaking changes (renamed panels,
new
required variables)\n\n- Minor (v1.0 -> v1.1): New panels, new queries\n\n- Patch (v1.0 ->
v1.0.1):
Threshold adjustments, cosmetic fixes\n\n### Dashboard Migration\n\n When migrating
between
environments:\n\n## Export from staging\n\ncurl -s
[http://grafana-staging:3000/api/dashboards/uid/overview]([http://grafana-staging:3000/api/dashboards/uid/overvie]([http://grafana-staging:3000/api/dashboards/uid/overvi]([http://grafana-staging:3000/api/dashboards/uid/overv]([http://grafana-staging:3000/api/dashboards/uid/over]([http://grafana-staging:3000/api/dashboards/uid/ove]([http://grafana-staging:3000/api/dashboards/uid/ov]([http://grafana-staging:3000/api/dashboards/uid/o]([http://grafana-staging:3000/api/dashboards/uid/](http://grafana-staging:3000/api/dashboards/uid/)o)v)e)r)v)i)e)w)
\\n\n- H "Authorization: Bearer $TOKEN" > overview.json\n\n## Adjust environment-specific
values\n\njq '.dashboard.panels[].targets[].expr |= gsub("staging"; "prod")'
overview.json\n\n##
Import to production\n\ncurl -X POST
[http://grafana-prod:3000/api/dashboards/db]([http://grafana-prod:3000/api/dashboards/d]([http://grafana-prod:3000/api/dashboards/]([http://grafana-prod:3000/api/dashboards]([http://grafana-prod:3000/api/dashboard]([http://grafana-prod:3000/api/dashboar]([http://grafana-prod:3000/api/dashboa]([http://grafana-prod:3000/api/dashbo]([http://grafana-prod:3000/api/dashb](http://grafana-prod:3000/api/dashb)o)a)r)d)s)/)d)b)
\\n\n- H "Authorization: Bearer $TOKEN" \\n\n- d @overview.json\n\n## Governance &
Maintenance\n\n### Dashboard Lifecycle\n\nNew Dashboard (Community Contribution)\n v\nCode
Review
(Dashboard Standards Compliance)\n v\nTesting (Queries, Thresholds, Performance)\n
v\nApproval
(Grafana Dashboard Owner)\n v\nMerged to Main Branch\n v\nDeployed to Staging, then
Production\n
v\nIn-Production Monitoring (Usage Metrics, Feedback)\n v (if not used)\nDeprecation
Notice (6-month
warning period)\n v\nRemoval\n\n### Dashboard Owner Responsibilities\n\nEach dashboard
MUST have a
named owner with responsibilities:\n1.**Updates:**Keep queries, thresholds, and
documentation
current\n1.**Feedback:**Gather operator feedback and iterate\n1.**Incidents:**Use
dashboard data to
investigate incidents\n1.**Deprecation:**Archive or remove unused dashboards\n\n###
Contributing New
Dashboards\n\nProcess for contributing new dashboards:\n1.**Design Phase:**Create
dashboard JSON,
test locally\n1.**Documentation:**Add to opt/grafana/dashboards/ directory\n1.**PR
Submission:**Submit dashboard JSON + README entry\n1.**Code Review:**Verify naming,
standards
compliance, queries\n1.**Approval:**Dashboard owner or lead approves\n1.**Merge:**Merged
to main
branch\n1.**Deployment:**Staged deployment to environments\n\n## Related Standards\n\n-
[Prometheus
Query Standards](../monitoring/README.md#query-standards)\n\n- [Alert Rule
Standards](../monitoring/README.md#alert-rule-standards)\n\n- [Monitoring Fixtures
Guide](../monitoring/FIXTURES_GUIDE.md)\n\n- [DebVisor Documentation
Standards](../docs/00-START.md)\n\n
