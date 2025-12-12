# Grafana Dashboard Implementation Guide

## Quick Start

This guide walks you through creating a new Grafana dashboard following DebVisor standards.

## Step 1: Plan Your Dashboard

Before coding, answer these questions:
1.**What is the dashboard for?**(e.g., "Monitor DNS performance")
1.**Who uses it?**(operators, architects, security team, developers)
1.**What questions does it answer?**(Is the service healthy? Why is it slow? What's failing?)
1.**What metrics do I need?**(List metrics from Prometheus)
1.**What time range?**(Real-time, 24h trends, 30d capacity planning?)
1.**What thresholds?**(When should we alert?)

### Planning Template

## Dashboard Plan: [Name]

## Purpose

    [1-2 sentence description]

## Audience

- Operators: [yes/no] - Tasks: [drill-down status, find issues, etc]

- Architects: [yes/no] - Tasks: [capacity planning, performance review]

- Developers: [yes/no] - Tasks: [debug workloads, trace requests]

- Security: [yes/no] - Tasks: [audit access, find threats]

## Key Questions Answered

    1. [Question]?

    1. [Question]?

    1. [Question]?

## Metrics Required

- `metric_name_1` (type: gauge/counter/histogram)

- `metric_name_2`

- ...

## Panels

    | Panel Title | Type | Metrics | Refresh |
    |---|---|---|---|
    | [Title] | stat/graph/table | `metric` | 30s |

## Thresholds

    | Metric | Warning | Critical | Rationale |
    |---|---|---|---|
    | [metric] | [value] | [value] | [reason] |

## Time Ranges

- Default: 1h

- Optional: 24h, 7d, 30d

## Success Criteria

- [ ] All metrics flowing from Prometheus

- [ ] Thresholds tuned with ops team

- [ ] No N/A values in production

- [ ] <3 seconds load time

## Step 2: Set Up Local Development

### Verify Prometheus Metrics

Before building dashboard, confirm metrics are available:

## Verify Prometheus is running

    curl [http://localhost:9090/-/healthy](http://localhost:9090/-/healthy)

## Check for your metrics

    curl '[http://localhost:9090/api/v1/query?query=your_metric_name'](http://localhost:9090/api/v1/query?query=your_metric_name') | jq .

## List all metrics starting with your prefix

    curl '[http://localhost:9090/api/v1/series?match[]=your_prefix_*'](http://localhost:9090/api/v1/series?match[]=your_prefix_*') | jq .

## Start Grafana Locally

## Docker Compose

    docker run -d -p 3000:3000 grafana/grafana:latest

## Or systemd

    systemctl start grafana-server

## Default: [http://localhost:3000](http://localhost:3000) (admin/admin)

## Add Prometheus Datasource

1. Login to Grafana (admin/admin)

1. Navigate to Configuration -> Data Sources

1. Click "Add data source"

1. Select "Prometheus"

1. URL: [http://prometheus:9090](http://prometheus:9090)

1. Click "Save & Test"

## Step 3: Create Dashboard JSON

### Option A: UI Creation (Easier for First-Time)

1.**Create Dashboard:**Click "+" -> "Dashboard" -> "New Panel"
1.**Add Panel:**Click "Add panel"
1.**Configure Panel:**

- Title: "CPU Usage (%)"

- Query: `100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])))`

- Visualization: "Stat"

- Legend Format: `{{instance}}`

1.**Set Thresholds:**

- Green: 0-70%

- Yellow: 70-90%

- Red: 90%+

1.**Save Dashboard:**Click "Dashboard settings" (gear icon)

- Title: "dns-dhcp"

- Folder: "DebVisor"

- Save

### Option B: JSON Import (For Advanced)

Create `dashboards/my-dashboard.json`:
    {
      "annotations": {
        "list": [
          {
            "builtIn": 1,
            "datasource": "-- Grafana --",
            "enable": true,
            "hide": true,
            "iconColor": "rgba(0, 211, 255, 1)",
            "name": "Annotations & Alerts",
            "type": "dashboard"
          }
        ]
      },
      "description": "My custom dashboard",
      "editable": true,
      "gnetId": null,
      "graphTooltip": 1,
      "id": null,
      "links": [],
      "panels": [
        {
          "datasource": "Prometheus-DebVisor",
          "description": "CPU usage across cluster",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisLabel": "CPU Usage %",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 10,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": true,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "percentage",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  },
                  {
                    "color": "yellow",
                    "value": 70
                  },
                  {
                    "color": "red",
                    "value": 90
                  }
                ]
              },
              "unit": "percent"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 0,
            "y": 0
          },
          "id": 1,
          "options": {
            "legend": {
              "displayMode": "table",
              "placement": "right",
              "values": ["value", "max", "mean"]
            },
            "tooltip": {
              "mode": "single"
            }
          },
          "pluginVersion": "8.0.0",
          "targets": [
            {
              "expr": "100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])))",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "{{instance}}",
              "refId": "A"
            }
          ],
          "title": "CPU Usage (%)",
          "type": "timeseries"
        }
      ],
      "refresh": "30s",
      "schemaVersion": 27,
      "style": "dark",
      "tags": ["debvisor", "infrastructure"],
      "templating": {
        "list": [
          {
            "allValue": null,
            "current": {
              "text": "1h",
              "value": "1h"
            },
            "datasource": "Prometheus-DebVisor",
            "definition": "label_values(up, job)",
            "description": null,
            "error": null,
            "hide": 0,
            "includeAll": false,
            "label": "Time Range",
            "multi": false,
            "name": "time_range",
            "options": [],
            "query": {
              "query": "label_values(up, job)",
              "refId": "StandardVariableQuery"
            },
            "refresh": 1,
            "regex": "",
            "skipUrlSync": false,
            "sort": 0,
            "tagValuesQuery": "",
            "tags": [],
            "tagsQuery": "",
            "type": "query",
            "useTags": false
          }
        ]
      },
      "time": {
        "from": "now-1h",
        "to": "now"
      },
      "timepicker": {},
      "timezone": "",
      "title": "My Dashboard",
      "uid": "my-dashboard",
      "version": 1
    }

## Step 4: Follow Naming Standards

Apply naming conventions from DASHBOARD_STANDARDS.md:

### Dashboard Name

    Format: component-aspect[-perspective]
    ? Correct names:

- dns-dhcp (DNS/DHCP services)

- ceph-performance (Ceph I/O performance)

- kubernetes-capacity (K8s resource capacity)

### Panel Names

    CamelCase with units:
    ? Correct:

- CPU Usage (%)

- Query Latency (ms)

- Disk Utilization (%)

    ? Wrong:

- cpu usage

- Query_Latency_ms

- Disk util

### Variable Names

    Lowercase with underscores:
    ? Correct:
      $time_range
      $cluster_name
      $node_filter
    ? Wrong:
      $timeRange
      $cluster-name
      $NodeFilter

## Step 5: Configure Colors

Use standard colors from DASHBOARD_STANDARDS.md:

### Palette

    {
      "thresholds": {
        "steps": [
          {"color": "#31C740", "value": null},       // Green (healthy)
          {"color": "#F2AC29", "value": 70},          // Yellow (warning)
          {"color": "#D64E4E", "value": 90}           // Red (critical)
        ]
      }
    }

### Override Panel Color

1. Click panel -> "Edit"

1. Go to "Field" tab

1. Select "Thresholds"

1. Set colors:

- Green: #31C740

- Yellow: #F2AC29

- Red: #D64E4E

## Step 6: Write Queries

Follow query standards from DASHBOARD_STANDARDS.md:

### Query Checklist

- [ ] Metric name is correct (verified in Prometheus)

- [ ] Label matchers are accurate

- [ ] Aggregation method is appropriate (avg/sum/max)

- [ ] Time window is sufficient ([5m] = 20+ data points)

- [ ] Legend format shows dimension ({{instance}}, {{job}})

- [ ] Query includes comment explaining what it measures

### Example Query with Comment

## CPU utilization by node (%)

## = 100 * (1 - idle_fraction)

## Aggregation: per node (enables comparison)

    100 * (1 - avg by (instance) (
      rate(node_cpu_seconds_total{mode="idle", cluster="$cluster_name"}[5m])
    ))

## Save Query Documentation

Add to dashboard description:

## Queries

### CPU Usage

- Metric: node_cpu_seconds_total

- Formula: 100 * (1 - idle_fraction)

- Time Window: 5m rate (20 data points minimum)

- Aggregation: Per node

## Step 7: Set Thresholds

### Thresholds MUST be

1.**Evidence-based:**Why these values?
1.**Documented:**Include justification and runbook link
1.**Tunable:**Can operators adjust them?

### Example Threshold Configuration

    {
      "thresholds": {
        "mode": "percentage",
        "steps": [
          {"color": "green", "value": null, "annotation": "Healthy"},
          {"color": "yellow", "value": 70, "annotation": "High utilization"},
          {"color": "red", "value": 90, "annotation": "Critical"}
        ]
      }
    }

### Document Thresholds in Dashboard

Add to description:

## Thresholds [2]

### CPU Utilization

- **Warning:**70%

- **Critical:**90%

- **Rationale:**Headroom needed for spike absorption

- **Runbook:**[CPU High Troubleshooting](https://docs.example.com/runbooks/cpu-high)

### Memory Utilization

- **Warning:**80%

- **Critical:**95%

- **Rationale:**OOM killer activates near 100%

- **Runbook:**[Memory Pressure Troubleshooting](https://docs.example.com/runbooks/memory-pressure)

## Step 8: Export Dashboard

After testing in Grafana UI:

### Export from Grafana

## Get your dashboard

    curl -s [http://localhost:3000/api/dashboards/uid/my-dashboard](http://localhost:3000/api/dashboards/uid/my-dashboard) \

      - H "Authorization: Bearer $GRAFANA_TOKEN" | jq '.dashboard' > my-dashboard.json

## Validate JSON

    jq . my-dashboard.json > /dev/null && echo "Valid JSON"

## Add to Repository

## Copy to dashboards directory

    cp my-dashboard.json opt/grafana/dashboards/

## Update dashboards.yaml if needed

## vi opt/grafana/provisioning/dashboards.yaml

## Git commit

    git add opt/grafana/dashboards/my-dashboard.json
    git commit -m "Add dashboard: my-dashboard (CPU monitoring)"

## Step 9: Create README Entry

Add dashboard documentation to opt/grafana/README.md:

### Your Dashboard (your-dashboard.json)

- *Purpose:**One-line description of what this dashboard monitors.

### Layout

- **Row 1:**Summary stats panels (3-col width each)

- **Row 2:**Primary metric (CPU usage over time)

- **Row 3:**Secondary metrics (memory, disk)

- **Row 4:**Detailed table (per-node breakdown)

### Template Variables

- `$cluster_name`: Cluster identifier (default: "DebVisor")

- `$time_range`: Dashboard time range (default: last 1h)

- `$node_filter`: Optional node filter (default: all nodes)

- *Refresh Rate:**30s (auto-refresh enabled)

- *Size:**1920x1080+ (optimized for 1080p+, responsive to smaller screens)

### Alert Integration

- Links to [CPU High Alert](../monitoring/README.md#alerts-cpu)

- Drill-down to [Node Details Dashboard](node-details.json)

## Step 10: Testing Checklist

Before submitting, verify:

### Visual

- [ ] Dashboard loads in <3 seconds

- [ ] No overlapping panels

- [ ] Panels are consistently sized and aligned

- [ ] All titles are readable (font ?12px)

### Functionality

- [ ] All queries execute without errors

- [ ] All metrics show data (no "No Data" errors)

- [ ] All template variables work correctly

- [ ] Thresholds transition properly (green->yellow->red)

- [ ] Drill-down links work

- [ ] Legend displays correctly

### Standards Compliance

- [ ] Dashboard name follows `component-aspect` format

- [ ] Panel titles are CamelCase with units

- [ ] Colors match standard palette (green/yellow/red)

- [ ] Thresholds are documented with rationale

- [ ] All queries include comments and legend format

- [ ] Time windows are appropriate (?5 data points)

### Documentation

- [ ] Dashboard has description explaining purpose

- [ ] Queries are documented (what metric, why this aggregation)

- [ ] Thresholds documented with runbook links

- [ ] Added to opt/grafana/README.md

- [ ] Tags include "debvisor"

### Performance

- [ ] Queries optimized (no excessive label cardinality)

- [ ] Refresh rate appropriate (10s for alerts, 30s for normal)

- [ ] Legends show current, max, mean (not excessive)

- [ ] <20 panels per dashboard

## Common Dashboard Patterns

### Multi-Cluster Monitoring

- *Key Pattern:**Use `$cluster` selector in all queries

    {
      "targets": [
        {
          "expr": "sum by (cluster) (rate(metric_total{cluster=\"$cluster\"}[5m]))"
        }
      ]
    }

### Drill-Down Navigation

- *Pattern:**Click panel value to go to detail dashboard

    {
      "fieldConfig": {
        "defaults": {
          "links": [
            {
              "title": "View Details",
              "url": "d/node-details?var-node=${__value.raw}",
              "targetBlank": false
            }
          ]
        }
      }
    }

### Comparative Analysis

- *Pattern:**Show top 5 problematic resources

## Top 5 nodes by CPU usage

    topk(5, 100 * (1 - avg by (instance) (
      rate(node_cpu_seconds_total{mode="idle"}[5m])
    )))

## Per-Service Status Table

- *Pattern:**Table with resource names and statuses

    {
      "type": "table",
      "targets": [
        {
          "expr": "node_up",
          "format": "table",
          "instant": true
        }
      ],
      "options": {
        "showHeader": true,
        "sortBy": ["value"]
      }
    }

## Troubleshooting

### "No Data" Errors

- *Problem:**Dashboard shows "No Data" in panels

### Debug

## 1. Check metric exists in Prometheus

    curl '[http://prometheus:9090/api/v1/series?match[]=your_metric'](http://prometheus:9090/api/v1/series?match[]=your_metric') | jq .

## 2. Test query in Prometheus UI

## Go to [http://prometheus:9090](http://prometheus:9090) and paste query

## 3. Check datasource connection

## In Grafana: Configuration -> Data Sources -> Test

## Solution

- Verify metric name and label matchers

- Check Prometheus scrape config includes job

- Verify datasource URL is correct

### Slow Dashboard Load

- *Problem:**Dashboard takes >5 seconds to load

### Optimize

    1. Reduce number of panels (<20 total)

    1. Increase refresh rate (30s instead of 10s)

    1. Simplify queries (avoid high-cardinality labels)

    1. Add query caching where appropriate

### Threshold Not Triggering

- *Problem:**Threshold colors don't change

### Debug [2]

## 1. Run query manually

    curl '[http://prometheus:9090/api/v1/query?query=YOUR_QUERY'](http://prometheus:9090/api/v1/query?query=YOUR_QUERY') | jq .

## 2. Check current value vs threshold

## Panel shows current value; compare to threshold

## 3. Verify threshold mode

## Should be "absolute" or "percentage" as needed

## Solution [2]

- Adjust threshold values based on actual metric range

- Verify aggregation produces expected value range

- Test with fixtures if no real data available

## Best Practices

1.**Start Simple:**Create a single metric dashboard first
1.**Test Thoroughly:**Verify all panels work before sharing
1.**Document Well:**Future you will thank present you
1.**Get Feedback:**Share dashboard with ops team early
1.**Iterate:**Adjust based on real usage patterns
1.**Keep Current:**Review and update thresholds quarterly

## Next Steps

After creating your dashboard:
1.**Share with Team:**Post in Slack or email for feedback
1.**Monitor Usage:**Check if operators are actually using it
1.**Gather Feedback:**Ask "Is this helpful? What's missing?"
1.**Refine:**Adjust panels, queries, thresholds based on feedback
1.**Document Results:**Update README with lessons learned

## References

- [Dashboard Standards](./DASHBOARD_STANDARDS.md)

- [Prometheus Query Documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/)

- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)

- [DebVisor Monitoring Guide](../monitoring/README.md)

- [DebVisor Fixtures Guide](../monitoring/FIXTURES_GUIDE.md) (for testing with synthetic data)
