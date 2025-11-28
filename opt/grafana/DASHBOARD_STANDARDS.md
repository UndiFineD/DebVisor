# Grafana Dashboard Design Standards

## Overview

This document defines design standards and conventions for all DebVisor Grafana dashboards. Adherence to these standards ensures consistent user experience, maintainability, and reliable monitoring across the platform.

### Goals

- Provide intuitive, discoverable dashboards for operators of all skill levels
- Enable consistent visualization across heterogeneous environments
- Simplify dashboard maintenance and evolution
- Reduce cognitive load for operators using multiple dashboards

## Naming Standards

### Dashboard Naming Convention

All dashboard names MUST follow this format:

    -[-]

### Examples

    ✅ GOOD:

- overview (system-wide overview)
- dns-dhcp (DNS and DHCP services)
- ceph-performance (Ceph I/O performance)
- kubernetes-workloads (Kubernetes workload status)
- security-events (Security events and logging)

    ❌ BAD:

- Dashboard1 (not descriptive)
- KubeMetrics (inconsistent casing)
- ceph performance (spaces, should be hyphenated)
- k8s_cluster_status (underscores, too specific)

### Naming Hierarchy

| Level | Examples | Purpose |
|---|---|---|
| System | `overview` | Cluster-wide status |
| Component | `dns-dhcp`,`ceph-health`,`kubernetes` | Specific service |
| Aspect | `-performance`,`-capacity`,`-security` | Specific metric category |

### Panel Naming Convention

Panel titles MUST be:

-__CamelCase:__"CPU Usage", "Query Latency", "OSD Health"
-__Descriptive:__Indicates what metric is shown
-__Unit-aware:__Include units in title or legend
-__Role-appropriate:__Clear for target audience (operator, architect, dev)

### Examples [2]

    {
      "title": "CPU Usage (%)",
      "targets": [
        {"expr": "sum(rate(node_cpu_seconds_total[5m]))"}
      ]
    }

### Variable Naming Convention

All template variables MUST use lowercase with underscores:

    $cluster_name       // Cluster identifier
    $time_range         // Time range selector
    $node_filter        // Node name filter
    $namespace_filter   // Kubernetes namespace filter
    $severity_level     // Alert severity (critical/warning/info)
    $component          // Component/service (ceph/k8s/dns)

### Pattern

    $_

    ✅ Correct:  $pod_namespace, $osd_filter, $alert_severity
    ❌ Wrong:    $pod-namespace (hyphens), $POD_NAMESPACE (caps), $_pod (leading underscore)

## Color Standards

### Primary Palette

All dashboards MUST use this standard color palette:

    Success/Healthy:  #31C740  (Green)
    Warning/Caution:  #F2AC29  (Orange/Yellow)
    Critical/Error:   #D64E4E  (Red)
    Information:      #3498DB  (Blue)
    Neutral/Offline:  #95A5A6  (Gray)
    Custom/User:      #9B59B6  (Purple)

### Color Usage Guidelines

| Semantic Meaning | Color | Use Cases |
|---|---|---|
|__Success / OK__| Green (#31C740) | Healthy systems, running services, successful operations |
|__Warning / Degraded__| Yellow (#F2AC29) | High utilization, slow responses, non-critical issues |
|__Critical / Error__| Red (#D64E4E) | System down, failed operations, emergency conditions |
|__Informational__| Blue (#3498DB) | Neutral metrics, counts, informational data |
|__Neutral / Offline__| Gray (#95A5A6) | Disabled, offline, pending, or no data |
|__Custom__| Purple (#9B59B6) | Custom user-defined metrics, non-standard states |

### Multi-Series Coloring

For dashboards with many series (e.g., per-node metrics):

    Automatic Series Colors (Grafana defaults):
      Series 1: Blue
      Series 2: Orange
      Series 3: Green
      Series 4: Red
      Series 5: Purple
      ...

### Override when necessary

- Use semantic colors for important series
- Avoid color-blind confusing combinations (red-green at 1:1 ratio)
- Legend should clearly indicate what each color represents

## Panel Layout Standards

### Grid System

Grafana uses a 12-column grid system. Standard panel widths:

| Panel Type | Width | Height | Use Case |
|---|---|---|---|
|__Stat/Gauge__| 3 columns | 4 rows | Quick health summary |
|__Small Time Series__| 6 columns | 8 rows | Trends for single metric |
|__Standard Time Series__| 12 columns | 8 rows | Primary performance metric |
|__Detailed Table__| 12 columns | 10+ rows | Large result sets |
|__Heatmap/Histogram__| 12 columns | 8 rows | Distribution visualization |

### Layout Structure

### Recommended Dashboard Structure

    Row 1: Title, Summary Stats (4x stat panels, each 3 cols wide)
    Row 2: Primary Metrics (1-2 large time series panels)
    Row 3: Secondary Metrics (2-4 medium panels)
    Row 4: Detailed Analysis (Large table, heatmap, or node graph)
    Row 5: Logs/Events (Logs panel or events)
    Row 6: Related Links / Drill-downs

### Example Layout

    ┌─────────────────────────────────────────────────────────┐
    │ Dashboard Title: Ceph Cluster Health                    │
    ├─────────────────────────────────────────────────────────┤
    │ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │  Row 1
    │ │ Monitors │ │ Capacity │ │   PGs    │ │  OSDs    │   │  Summary
    │ │   8/8    │ │  2.3 PB  │ │ OK 2100  │ │ All OK   │   │  (4 cols x 4 rows)
    │ └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
    ├─────────────────────────────────────────────────────────┤
    │                                                         │  Row 2
    │ IOPS & Throughput (12 cols x 8 rows)                   │  Primary
    │                                                         │  metric
    │ [Time series graph showing IOPS and throughput over]   │
    │ [the past 7 days with legend]                          │
    ├─────────────────────────────────────────────────────────┤
    │ ┌────────────────────────────┐ ┌──────────────────┐   │  Row 3
    │ │ Cluster Latency            │ │ PG Status        │   │  Secondary
    │ │ [Time series: p95/p99]     │ │ 2100 PGs OK      │   │  metrics
    │ └────────────────────────────┘ │ 23 PGs Degraded  │   │
    │                                 │ 5 PGs Stuck      │   │
    │                                 └──────────────────┘   │
    ├─────────────────────────────────────────────────────────┤
    │                                                         │  Row 4
    │ OSD Status Table (12 cols x 10 rows)                   │  Detailed
    │ [Sortable table: OSD ID, Status, KB Used, IOPS, etc]   │
    ├─────────────────────────────────────────────────────────┤
    │ Recent Events (12 cols x 4 rows)                        │  Row 5
    │ [Log entries: Timestamp | Event | Severity]            │  Logs
    └─────────────────────────────────────────────────────────┘

### Spacing & Alignment

-__Horizontal:__1-2 column gap between panels on same row
-__Vertical:__1 row gap between major sections
-__Panel padding:__Let Grafana default (8px)
-__Consistency:__Align similar panels vertically

## Visualization Standards

### Panel Types and Selection

### Metric Visualization Decision Tree

    What are you visualizing?
    │
    ├─ Single value (e.g., "% CPU used") → Stat panel
    │  └─ With gauge ring? → Gauge panel
    │
    ├─ Time series (metric over time) → Time series panel
    │  ├─ With area shading? → Area graph
    │  └─ With distribution? → Time series + histogram
    │
    ├─ Distribution (latency histogram) → Histogram panel
    │
    ├─ Proportions (% allocation) → Pie/donut chart
    │
    ├─ Tabular data (detailed results) → Table panel
    │  └─ Sortable? Need interactivity? → Add table options
    │
    ├─ Log entries (error logs, audit trail) → Logs panel
    │
    ├─ Service/component relationships → Node graph panel
    │
    └─ Geographic distribution → Geomap panel (if applicable)

### Panel Configuration Standards

#### Stat Panel

    {
      "type": "stat",
      "title": "CPU Usage (%)",
      "targets": [
        {"expr": "sum(rate(node_cpu_seconds_total{mode!='idle'}[5m])) * 100"}
      ],
      "options": {
        "graphMode": "area",
        "colorMode": "background",
        "textMode": "auto",
        "thresholds": {
          "mode": "percentage",
          "steps": [
            {"color": "green", "value": null},
            {"color": "yellow", "value": 70},
            {"color": "red", "value": 90}
          ]
        },
        "unit": "percent"
      }
    }

#### Time Series Panel

    {
      "type": "timeseries",
      "title": "Network Traffic (Bytes/sec)",
      "targets": [
        {
          "expr": "sum by (interface) (rate(node_network_transmit_bytes_total[5m]))",
          "legendFormat": "{{interface}}"
        }
      ],
      "options": {
        "legend": {
          "displayMode": "table",
          "placement": "right",
          "values": ["value", "max", "mean"]
        },
        "thresholds": {
          "mode": "percentage",
          "steps": [
            {"color": "green", "value": null},
            {"color": "yellow", "value": 70},
            {"color": "red", "value": 85}
          ]
        }
      },
      "fieldConfig": {
        "custom": {
          "hideFrom": {"tooltip": false, "legend": false, "viz": false}
        }
      }
    }

#### Table Panel

    {
      "type": "table",
      "title": "OSD Status",
      "targets": [
        {
          "expr": "ceph_osd_info"
        }
      ],
      "options": {
        "showHeader": true,
        "sortBy": ["osd_id"],
        "customSort": true,
        "displayMode": "auto"
      }
    }

### Legend Configuration

### Standard Legend Format

    {
      "legend": {
        "displayMode": "table",     // "table" or "list"
        "placement": "right",        // "right", "bottom", or "top"
        "showLegend": true,
        "values": [                  // What to show in legend
          "value",                   // Current value
          "max",                     // Maximum value
          "mean"                     // Mean/average value
        ]
      }
    }

### Legend Placement

-__Right:__Best for 2-5 series (vertical list)
-__Bottom:__Good for 6+ series (horizontal, may wrap)
-__Top:__Minimal; use only when space is tight

### Legend Values

-__Always include:__Current value (for operators to quickly see status)
-__Add:__Max/Min for context on range
-__Optional:__Mean, Last (if beneficial for metric)

## Threshold Configuration

### Threshold Definition Standard

### Every metric MUST have defined thresholds with justification

### Format

    {
      "thresholds": {
        "mode": "absolute",         // "absolute" or "percentage"
        "steps": [
          {
            "color": "green",
            "value": null            // null = -∞
          },
          {
            "color": "yellow",
            "value": 70,             // Warning at 70
            "annotation": "High utilization"
          },
          {
            "color": "red",
            "value": 90              // Critical at 90
          }
        ]
      }
    }

### Common Metric Thresholds

### Infrastructure Metrics

| Metric | Warning | Critical | Rationale |
|---|---|---|---|
| CPU Utilization | 70% | 90% | Headroom for spikes |
| Memory Utilization | 80% | 95% | Risk of OOM killer activation |
| Disk Utilization | 80% | 95% | I/O performance degradation above 85% |
| Network Utilization | 75% | 90% | 10G links usually have <1% loss at 85%+ |
| Disk I/O Latency | 5ms | 20ms | Applications typically timeout >100ms |

### Service Metrics

| Metric | Warning | Critical | Rationale |
|---|---|---|---|
| Query Latency (DNS) | 50ms | 200ms | Typical DNS answers in 1-5ms |
| Pod Restart Count | 3/hour | 10/hour | Indicates instability |
| PG Degraded (Ceph) | 1+ | Any | Should never have degraded PGs long-term |
| Node CPU Throttle | 5% | 20% | Indicates oversubscription |
| API Server Latency | 100ms | 500ms | Kubernetes expects <100ms |

### Threshold Documentation

Every threshold MUST be documented with:

1.__Metric Name:__What is being measured?
1.__Threshold Values:__Warning and critical levels
1.__Justification:__Why these specific numbers?
1.__Tuning Guidance:__How to adjust for different environments
1.__Runbook Link:__Where to go for remediation

### Example Documentation

### Query Latency (dns-dhcp.json)

### Thresholds

- Warning: >100ms (p95)
- Critical: >500ms (p95)

### Justification

- DNS typically responds in 1-5ms locally
- Cloud DNS response times are 20-50ms
- >100ms indicates resolver performance issue
- >500ms indicates network problem or resolver down

### Tuning

- High-latency networks (satellite): Adjust to 200ms warning / 1000ms critical
- Local labs: Can tighten to 50ms warning / 200ms critical

    __Runbook:__[DNS Query Latency Troubleshooting](https://docs.example.com/runbooks/dns-latency)

## Query Standards

### Query Naming & Documentation

### All queries MUST have

1.__Legend format__indicating what's being shown
1.__Comment__explaining the query
1.__Aggregation level__(per-node, per-pool, cluster-wide)

### Example

## CPU utilization per node (%)

## = 100 * (1 - idle_fraction)

## Aggregation: per node (enables comparison between nodes)

    100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))

## PromQL Best Practices

### 1. Use Explicit Label Matchers

    ✅ GOOD:
    sum by (cluster, job) (rate(node_cpu_seconds_total{mode="user"}[5m]))

    ❌ BAD:
    sum(rate(node_cpu_seconds_total[5m]))  # Includes all modes (idle, user, system, ...)

### 2. Aggregation Choice Matters

    ✅ Right aggregation:
    avg by (instance) (...)  # Average per node

    ❌ Wrong aggregation:
    sum by (instance) (...)  # Would give sum across modes (meaningless)

### 3. Use Functions Appropriate to Metric Type

    Counter metrics (always increasing):
      ✅ rate()         # Rate of increase per second
      ✅ increase()     # Total increase over time window

    Gauge metrics (can go up or down):
      ✅ avg()          # Average value
      ✅ max()          # Peak value

    Histogram metrics (multiple buckets):
      ✅ histogram_quantile(0.95, ...)  # 95th percentile

### Query Performance

### Guidelines

1.__Time windows:__5m for frequent checks, 1h for trends
1.__Scrape interval alignment:__Queries should align with scrape interval

- If scraping every 15s, use `[5m]` (20 data points minimum)
- Avoid `[10s]` (too few data points, inaccurate)

1.__Aggregation order:__Aggregate early to reduce data volume

       ✅ GOOD: sum by (cluster) (...)  # Aggregate first
       ❌ BAD:  sum(rate(...)) by (cluster)  # Full rate first, then aggregate

    1.__Label cardinality:__Avoid high-cardinality labels in grouping

   ✅ GOOD: sum by (cluster, node) (...)  # Bounded set of nodes
   ❌ BAD:  sum by (path) (...)  # Thousands of possible paths → explosion

## Interactivity Standards

### Drill-Down Navigation

    Dashboards SHOULD enable drill-down to more detailed views:

{
  "fieldConfig": {
    "defaults": {
      "links": [
        {
          "title": "View Node Details",
          "url": "d/node-details?var-node=${node}",
          "targetBlank": false
        }
      ]
    }
  }
}

### Drill-down Pattern

System Overview
    ↓ (click node)
Node Details Dashboard
    ↓ (click pod)
Pod Details Dashboard

### Template Variables

### Standard Variable Patterns

{
  "templating": {
    "list": [
      {
        "name": "cluster_name",
        "type": "query",
        "datasource": "Prometheus-DebVisor",
        "query": "label_values(up, cluster)",
        "current": {"text": "DebVisor", "value": "DebVisor"},
        "multi": false
      },
      {
        "name": "time_range",
        "type": "interval",
        "values": ["5m", "15m", "1h", "6h", "1d", "7d"],
        "current": {"text": "1h", "value": "1h"}
      },
      {
        "name": "node_filter",
        "type": "query",
        "datasource": "Prometheus-DebVisor",
        "query": "label_values(node_cpu_seconds_total, instance)",
        "multi": true,
        "current": {"text": "All", "value": "$__all"}
      }
    ]
  }
}

### Standard Variables to Include

    | Variable | Type | Purpose | Multi-Select |
    |---|---|---|---|
    | `cluster_name` | Query | Filter by cluster | No |
    | `time_range` | Interval | Time window selector | No |
    | `node_filter` | Query | Filter by node | Yes |
    | `namespace_filter` | Query | Filter by K8s namespace | Yes |
    | `severity_filter` | Custom | Filter by alert severity | Yes |

## Performance Standards

### Refresh Rates

### Dashboard refresh rates MUST match operational needs

    | Dashboard Type | Refresh Rate | Rationale |
    |---|---|---|
    |__Critical Alerts__| 10s | Real-time visibility for emergency response |
    |__System Overview__| 30s | Balance between real-time and load |
    |__Performance Metrics__| 30s | Sufficient for trend detection |
    |__Capacity Planning__| 5m | Longer-term trends, less sensitive to spikes |
    |__Compliance/Audit__| 1m | Historical data, not time-sensitive |

### Query Optimization

### Timeouts and Limits

timeout: 30s              # Max query execution time
max_samples: 1000000      # Max time series returned
max_data_points: 10000    # Max points plotted

### For Large Dashboards

- Limit panels to <20 per dashboard (improves load time)
- Use cached queries where possible
- Stagger refresh rates (some panels 30s, some 1m)
- Avoid overlapping time windows

## Accessibility Standards

### Color Blindness Considerations

    Dashboards MUST be readable for colorblind users:

❌ NOT colorblind-safe:
  Red-green threshold (users with protanopia can't distinguish)

✅ Colorblind-safe:
  Red-yellow-green threshold (distinct hues for most color blindness types)
  Blue-orange threshold (highly distinguishable)

### Fonts & Readability

-__Minimum font size:__12px for normal text
-__Panel titles:__14px+ for clarity
-__Legend:__11px+ for readability
-__Contrast ratio:__Minimum 4.5:1 for text on background

### Keyboard Navigation

    Dashboards should be keyboard-navigable:

- Tab through panels
- Arrow keys to scroll
- Enter to drill-down on interactive elements

## Testing & Validation

### Dashboard Testing Checklist

    Before committing a new dashboard:

- [ ]__Visual Layout:__Panels aligned consistently, no overlaps
- [ ]__Queries:__All queries execute successfully in Prometheus
- [ ]__Data:__Verify metrics are flowing correctly
- [ ]__Thresholds:__Test threshold transitions (green→yellow→red)
- [ ]__Variables:__Test all template variable combinations
- [ ]__Drill-down:__Test navigation links
- [ ]__Performance:__Dashboard loads in <5 seconds
- [ ]__Legends:__All series labeled and color-coded
- [ ]__Units:__All metrics show appropriate units
- [ ]__Documentation:__Dashboard description and runbooks present

### CI Validation

    Consider adding automated validation:

## Validate dashboard JSON

jq -e '.dashboard' dashboards/*.json

## Validate queries with PromQL linter

promtool check rules dashboards/*

## Test provisioning config

grafana-cli admin export-dashboard overview > /tmp/test.json

## Migration & Versioning

### Dashboard Versioning

    Track dashboard changes:

{
  "dashboard": {
    "title": "Overview",
    "version": 5,
    "lastSavedTime": "2025-01-15T10:30:00Z",
    "lastSavedBy": "ops-team"
  }
}

### Version Bumping

- Major (v1.0 → v2.0): Breaking changes (renamed panels, new required variables)
- Minor (v1.0 → v1.1): New panels, new queries
- Patch (v1.0 → v1.0.1): Threshold adjustments, cosmetic fixes

### Dashboard Migration

    When migrating between environments:

## Export from staging

curl -s [http://grafana-staging:3000/api/dashboards/uid/overview](http://grafana-staging:3000/api/dashboards/uid/overview) \
  -H "Authorization: Bearer $TOKEN" > overview.json

## Adjust environment-specific values

jq '.dashboard.panels[].targets[].expr |= gsub("staging"; "prod")' overview.json

## Import to production

curl -X POST [http://grafana-prod:3000/api/dashboards/db](http://grafana-prod:3000/api/dashboards/db) \
  -H "Authorization: Bearer $TOKEN" \
  -d @overview.json

## Governance & Maintenance

### Dashboard Lifecycle

New Dashboard (Community Contribution)
    ↓
Code Review (Dashboard Standards Compliance)
    ↓
Testing (Queries, Thresholds, Performance)
    ↓
Approval (Grafana Dashboard Owner)
    ↓
Merged to Main Branch
    ↓
Deployed to Staging, then Production
    ↓
In-Production Monitoring (Usage Metrics, Feedback)
    ↓ (if not used)
Deprecation Notice (6-month warning period)
    ↓
Removal

### Dashboard Owner Responsibilities

Each dashboard MUST have a named owner with responsibilities:

1.__Updates:__Keep queries, thresholds, and documentation current
1.__Feedback:__Gather operator feedback and iterate
1.__Incidents:__Use dashboard data to investigate incidents
1.__Deprecation:__Archive or remove unused dashboards

### Contributing New Dashboards

Process for contributing new dashboards:

1.__Design Phase:__Create dashboard JSON, test locally
1.__Documentation:__Add to opt/grafana/dashboards/ directory
1.__PR Submission:__Submit dashboard JSON + README entry
1.__Code Review:__Verify naming, standards compliance, queries
1.__Approval:__Dashboard owner or lead approves
1.__Merge:__Merged to main branch
1.__Deployment:__Staged deployment to environments

## Related Standards

- [Prometheus Query Standards](../monitoring/README.md#query-standards)
- [Alert Rule Standards](../monitoring/README.md#alert-rule-standards)
- [Monitoring Fixtures Guide](../monitoring/FIXTURES_GUIDE.md)
- [DebVisor Documentation Standards](../docs/00-START.md)
