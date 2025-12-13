# Grafana Dashboard Implementation Guide\n\n## Quick Start\n\nThis guide walks you through

creating

a new Grafana dashboard following DebVisor standards.\n\n## Step 1: Plan Your
Dashboard\n\nBefore
coding, answer these questions:\n1.**What is the dashboard for?**(e.g., "Monitor
DNS
performance")\n1.**Who uses it?**(operators, architects, security team,
developers)\n1.**What
questions does it answer?**(Is the service healthy? Why is it slow? What's
failing?)\n1.**What
metrics do I need?**(List metrics from Prometheus)\n1.**What time
range?**(Real-time, 24h
trends,
30d capacity planning?)\n1.**What thresholds?**(When should we alert?)\n\n###
Planning
Template\n\n## Dashboard Plan: [Name]\n\n## Purpose\n\n [1-2 sentence
description]\n\n##
Audience\n\n- Operators: [yes/no] - Tasks: [drill-down status, find issues,
etc]\n\n-
Architects:
[yes/no] - Tasks: [capacity planning, performance review]\n\n- Developers:
[yes/no] -
Tasks: [debug
workloads, trace requests]\n\n- Security: [yes/no] - Tasks: [audit access, find
threats]\n\n## Key
Questions Answered\n\n 1. [Question]?\n\n 1. [Question]?\n\n 1.
[Question]?\n\n## Metrics
Required\n\n- `metric_name_1`(type:
gauge/counter/histogram)\n\n-`metric_name_2`\n\n-
...\n\n##
Panels\n\n | Panel Title | Type | Metrics | Refresh |\n |---|---|---|---|\n | [Title] |
stat/graph/table | `metric`| 30s |\n\n## Thresholds\n\n | Metric | Warning | Critical |
Rationale
|\n |---|---|---|---|\n | [metric] | [value] | [value] | [reason] |\n\n## Time Ranges\n\n- Default:
1h\n\n- Optional: 24h, 7d, 30d\n\n## Success Criteria\n\n- [] All metrics
flowing from
Prometheus\n\n- [] Thresholds tuned with ops team\n\n- [] No N/A values in
production\n\n-
[]  Data Sources\n\n1. Click "Add data source"\n\n1. Select
"Prometheus"\n\n1. URL:
[http://prometheus:9090]([http://prometheus:909]([http://prometheus:90]([http://prometheus:9]([http://prometheus:]([http://prometheus]([http://prometheu]([http://promethe]([http://prometh]([http://promet]([http://prome]([http://prom]([http://pro]([http://pr]([http://p](http://p)r)o)m)e)t)h)e)u)s):)9)0)9)0)\n\n1.
Click "Save & Test"\n\n## Step 3: Create Dashboard JSON\n\n### Option A: UI
Creation
(Easier for
First-Time)\n\n1.**Create Dashboard:**Click "+" -> "Dashboard" -> "New
Panel"\n1.**Add
Panel:**Click
"Add panel"\n1.**Configure Panel:**\n\n- Title: "CPU Usage (%)"\n\n- Query:`100
*(1 -
avg(rate(node_cpu_seconds_total{mode="idle"}[5m])))`\n\n- Visualization:
"Stat"\n\n-
Legend Format:
`{{instance}}`\n\n1.**Set Thresholds:**\n\n- Green: 0-70%\n\n- Yellow:
70-90%\n\n- Red:
90%+\n\n1.**Save Dashboard:**Click "Dashboard settings" (gear icon)\n\n- Title:
"dns-dhcp"\n\n-
Folder: "DebVisor"\n\n- Save\n\n### Option B: JSON Import (For
Advanced)\n\nCreate
`dashboards/my-dashboard.json`:\n {\n "annotations": {\n "list": [\n {\n
"builtIn": 1,\n
"datasource": "-- Grafana --",\n "enable": true,\n "hide": true,\n "iconColor":
"rgba(0,
211, 255,
1)",\n "name": "Annotations & Alerts",\n "type": "dashboard"\n }\n ]\n },\n
"description":
"My
custom dashboard",\n "editable": true,\n "gnetId": null,\n "graphTooltip": 1,\n
"id":
null,\n
"links": [],\n "panels": [\n {\n "datasource": "Prometheus-DebVisor",\n
"description":
"CPU usage
across cluster",\n "fieldConfig": {\n "defaults": {\n "color": {\n "mode":
"palette-classic"\n },\n
"custom": {\n "axisLabel": "CPU Usage %",\n "axisPlacement": "auto",\n
"barAlignment":
0,\n
"drawStyle": "line",\n "fillOpacity": 10,\n "gradientMode": "none",\n
"hideFrom": {\n
"legend":
false,\n "tooltip": false,\n "viz": false\n },\n "lineInterpolation":
"linear",\n
"lineWidth": 1,\n
"pointSize": 5,\n "scaleDistribution": {\n "type": "linear"\n },\n "showPoints":
"auto",\n
"spanNulls": true,\n "stacking": {\n "group": "A",\n "mode": "none"\n },\n
"thresholdsStyle": {\n
"mode": "off"\n }\n },\n "mappings": [],\n "thresholds": {\n "mode":
"percentage",\n
"steps": [\n
{\n "color": "green",\n "value": null\n },\n {\n "color": "yellow",\n "value":
70\n },\n
{\n
"color": "red",\n "value": 90\n }\n ]\n },\n "unit": "percent"\n },\n
"overrides": []\n
},\n
"gridPos": {\n "h": 8,\n "w": 12,\n "x": 0,\n "y": 0\n },\n "id": 1,\n
"options": {\n
"legend": {\n
"displayMode": "table",\n "placement": "right",\n "values": ["value", "max",
"mean"]\n
},\n
"tooltip": {\n "mode": "single"\n }\n },\n "pluginVersion": "8.0.0",\n
"targets": [\n {\n
"expr":
"100*(1 - avg by (instance)
(rate(node_cpu_seconds_total{mode=\"idle\"}[5m])))",\n
"format":
"time_series",\n "intervalFactor": 1,\n "legendFormat": "{{instance}}",\n
"refId": "A"\n
}\n ],\n
"title": "CPU Usage (%)",\n "type": "timeseries"\n }\n ],\n "refresh": "30s",\n
"schemaVersion":
27,\n "style": "dark",\n "tags": ["debvisor", "infrastructure"],\n "templating":
{\n
"list": [\n {\n
"allValue": null,\n "current": {\n "text": "1h",\n "value": "1h"\n },\n
"datasource":
"Prometheus-DebVisor",\n "definition": "label_values(up, job)",\n "description":
null,\n
"error":
null,\n "hide": 0,\n "includeAll": false,\n "label": "Time Range",\n "multi":
false,\n
"name":
"time_range",\n "options": [],\n "query": {\n "query": "label_values(up,
job)",\n "refId":
"StandardVariableQuery"\n },\n "refresh": 1,\n "regex": "",\n "skipUrlSync":
false,\n
"sort": 0,\n
"tagValuesQuery": "",\n "tags": [],\n "tagsQuery": "",\n "type": "query",\n
"useTags":
false\n }\n
]\n },\n "time": {\n "from": "now-1h",\n "to": "now"\n },\n "timepicker": {},\n
"timezone": "",\n
"title": "My Dashboard",\n "uid": "my-dashboard",\n "version": 1\n }\n\n## Step
4: Follow
Naming
Standards\n\nApply naming conventions from DASHBOARD_STANDARDS.md:\n\n###
Dashboard
Name\n\n Format:
component-aspect[-perspective]\n ? Correct names:\n\n- dns-dhcp (DNS/DHCP
services)\n\n-
ceph-performance (Ceph I/O performance)\n\n- kubernetes-capacity (K8s resource
capacity)\n\n###
Panel Names\n\n CamelCase with units:\n ? Correct:\n\n- CPU Usage (%)\n\n- Query
Latency
(ms)\n\n-
Disk Utilization (%)\n\n ? Wrong:\n\n- cpu usage\n\n- Query_Latency_ms\n\n- Disk
util\n\n###
Variable Names\n\n Lowercase with underscores:\n ? Correct:\n $time_range\n
$cluster_name\n
$node_filter\n ? Wrong:\n $timeRange\n $cluster-name\n $NodeFilter\n\n## Step 5:
Configure
Colors\n\nUse standard colors from DASHBOARD_STANDARDS.md:\n\n### Palette\n\n
{\n
"thresholds": {\n
"steps": [\n {"color": "#31C740", "value": null}, // Green (healthy)\n {"color":
"#F2AC29", "value":
70}, // Yellow (warning)\n {"color": "#D64E4E", "value": 90} // Red (critical)\n
]\n }\n
}\n\n###
Override Panel Color\n\n1. Click panel -> "Edit"\n\n1. Go to "Field" tab\n\n1.
Select
"Thresholds"\n\n1. Set colors:\n\n- Green: #31C740\n\n- Yellow: #F2AC29\n\n-
Red:

## D64E4E\n\n## Step

6: Write Queries\n\nFollow query standards from DASHBOARD_STANDARDS.md:\n\n###
Query
Checklist\n\n-
[] Metric name is correct (verified in Prometheus)\n\n- [] Label matchers are
accurate\n\n- []
Aggregation method is appropriate (avg/sum/max)\n\n- [] Time window is
sufficient ([5m] =
20+ data
points)\n\n- [] Legend format shows dimension ({{instance}}, {{job}})\n\n- []
Query
includes comment
explaining what it measures\n\n### Example Query with Comment\n\n## CPU
utilization by
node
(%)\n\n## = 100*(1 - idle_fraction)\n\n## Aggregation: per node (enables
comparison)\n\n
100*(1 -
avg by (instance) (\n rate(node_cpu_seconds_total{mode="idle",
cluster="$cluster_name"}[5m])\n
))\n\n## Save Query Documentation\n\nAdd to dashboard description:\n\n##
Queries\n\n###
CPU
Usage\n\n- Metric: node_cpu_seconds_total\n\n- Formula: 100*(1 -
idle_fraction)\n\n- Time
Window: 5m
rate (20 data points minimum)\n\n- Aggregation: Per node\n\n## Step 7: Set
Thresholds\n\n###
Thresholds MUST be\n\n1.**Evidence-based:**Why these
values?\n1.**Documented:**Include
justification
and runbook link\n1.**Tunable:**Can operators adjust them?\n\n### Example
Threshold
Configuration\n\n {\n "thresholds": {\n "mode": "percentage",\n "steps": [\n
{"color":
"green",
"value": null, "annotation": "Healthy"},\n {"color": "yellow", "value": 70,
"annotation":
"High
utilization"},\n {"color": "red", "value": 90, "annotation": "Critical"}\n ]\n
}\n
}\n\n### Document
Thresholds in Dashboard\n\nAdd to description:\n\n## Thresholds [2]\n\n### CPU
Utilization\n\n-**Warning:**70%\n\n- **Critical:**90%\n\n-
**Rationale:**Headroom needed
for spike
absorption\n\n- **Runbook:**[CPU High
Troubleshooting]([https://docs.example.com/runbooks/cpu-hig]([https://docs.example.com/runbooks/cpu-hi]([https://docs.example.com/runbooks/cpu-h]([https://docs.example.com/runbooks/cpu-]([https://docs.example.com/runbooks/cpu]([https://docs.example.com/runbooks/cp]([https://docs.example.com/runbooks/c]([https://docs.example.com/runbooks/]([https://docs.example.com/runbooks]([https://docs.example.com/runbook]([https://docs.example.com/runboo]([https://docs.example.com/runbo]([https://docs.example.com/runb]([https://docs.example.com/run]([https://docs.example.com/ru]([https://docs.example.com/r]([https://docs.example.com/]([https://docs.example.com]([https://docs.example.co]([https://docs.example.c]([https://docs.example.]([https://docs.example]([https://docs.exampl]([https://docs.examp]([https://docs.exam]([https://docs.exa]([https://docs.ex]([https://docs.e]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)e)x)a)m)p)l)e).)c)o)m)/)r)u)n)b)o)o)k)s)/)c)p)u)-)h)i)g)h)\n\n###
Memory Utilization\n\n- **Warning:**80%\n\n- **Critical:**95%\n\n-
**Rationale:**OOM
killer
activates near 100%\n\n- **Runbook:**[Memory Pressure
Troubleshooting]([https://docs.example.com/runbooks/memory-pressur]([https://docs.example.com/runbooks/memory-pressu]([https://docs.example.com/runbooks/memory-press]([https://docs.example.com/runbooks/memory-pres]([https://docs.example.com/runbooks/memory-pre]([https://docs.example.com/runbooks/memory-pr]([https://docs.example.com/runbooks/memory-p]([https://docs.example.com/runbooks/memory-]([https://docs.example.com/runbooks/memory]([https://docs.example.com/runbooks/memor]([https://docs.example.com/runbooks/memo]([https://docs.example.com/runbooks/mem]([https://docs.example.com/runbooks/me]([https://docs.example.com/runbooks/m]([https://docs.example.com/runbooks/]([https://docs.example.com/runbooks]([https://docs.example.com/runbook]([https://docs.example.com/runboo]([https://docs.example.com/runbo]([https://docs.example.com/runb]([https://docs.example.com/run]([https://docs.example.com/ru]([https://docs.example.com/r]([https://docs.example.com/]([https://docs.example.com]([https://docs.example.co]([https://docs.example.c]([https://docs.example.]([https://docs.example]([https://docs.exampl]([https://docs.examp]([https://docs.exam]([https://docs.exa]([https://docs.ex]([https://docs.e]([https://docs.]([https://docs]([https://doc]([https://do]([https://d](https://d)o)c)s).)e)x)a)m)p)l)e).)c)o)m)/)r)u)n)b)o)o)k)s)/)m)e)m)o)r)y)-)p)r)e)s)s)u)r)e)\n\n##
Step 8: Export Dashboard\n\nAfter testing in Grafana UI:\n\n### Export from
Grafana\n\n##
Get your
dashboard\n\n curl -s
[http://localhost:3000/api/dashboards/uid/my-dashboard]([http://localhost:3000/api/dashboards/uid/my-dashboar]([http://localhost:3000/api/dashboards/uid/my-dashboa]([http://localhost:3000/api/dashboards/uid/my-dashbo]([http://localhost:3000/api/dashboards/uid/my-dashb]([http://localhost:3000/api/dashboards/uid/my-dash]([http://localhost:3000/api/dashboards/uid/my-das]([http://localhost:3000/api/dashboards/uid/my-da]([http://localhost:3000/api/dashboards/uid/my-d]([http://localhost:3000/api/dashboards/uid/my-]([http://localhost:3000/api/dashboards/uid/my]([http://localhost:3000/api/dashboards/uid/m]([http://localhost:3000/api/dashboards/uid/]([http://localhost:3000/api/dashboards/uid]([http://localhost:3000/api/dashboards/ui]([http://localhost:3000/api/dashboards/u]([http://localhost:3000/api/dashboards/]([http://localhost:3000/api/dashboards]([http://localhost:3000/api/dashboard]([http://localhost:3000/api/dashboar]([http://localhost:3000/api/dashboa]([http://localhost:3000/api/dashbo]([http://localhost:3000/api/dashb]([http://localhost:3000/api/dash]([http://localhost:3000/api/das]([http://localhost:3000/api/da]([http://localhost:3000/api/d]([http://localhost:3000/api/]([http://localhost:3000/api]([http://localhost:3000/ap]([http://localhost:3000/a]([http://localhost:3000/]([http://localhost:3000]([http://localhost:300]([http://localhost:30]([http://localhost:3]([http://localhost:]([http://localhost]([http://localhos]([http://localho]([http://localh]([http://local](http://local)h)o)s)t):)3)0)0)0)/)a)p)i)/)d)a)s)h)b)o)a)r)d)s)/)u)i)d)/)m)y)-)d)a)s)h)b)o)a)r)d)
\\n\n - H "Authorization: Bearer $GRAFANA_TOKEN" | jq '.dashboard' >
my-dashboard.json\n\n##
Validate JSON\n\n jq . my-dashboard.json > /dev/null && echo "Valid JSON"\n\n##
Add to
Repository\n\n## Copy to dashboards directory\n\n cp my-dashboard.json
opt/grafana/dashboards/\n\n##
Update dashboards.yaml if needed\n\n## vi
opt/grafana/provisioning/dashboards.yaml\n\n##
Git
commit\n\n git add opt/grafana/dashboards/my-dashboard.json\n git commit -m "Add
dashboard:
my-dashboard (CPU monitoring)"\n\n## Step 9: Create README Entry\n\nAdd
dashboard
documentation to
opt/grafana/README.md:\n\n### Your Dashboard (your-dashboard.json)\n\n-
*Purpose:**One-line
description of what this dashboard monitors.\n\n### Layout\n\n- **Row
1:**Summary stats
panels
(3-col width each)\n\n- **Row 2:**Primary metric (CPU usage over time)\n\n-
**Row
3:**Secondary
metrics (memory, disk)\n\n- **Row 4:**Detailed table (per-node breakdown)\n\n###
Template
Variables\n\n- `$cluster_name`: Cluster identifier (default: "DebVisor")\n\n-
`$time_range`:
Dashboard time range (default: last 1h)\n\n- `$node_filter`: Optional node
filter
(default: all
nodes)\n\n- *Refresh Rate:**30s (auto-refresh enabled)\n\n- *Size:**1920x1080+
(optimized
for
1080p+, responsive to smaller screens)\n\n### Alert Integration\n\n- Links to
[CPU High
Alert](../monitoring/README.md#alerts-cpu)\n\n- Drill-down to [Node Details
Dashboard](node-details.json)\n\n## Step 10: Testing Checklist\n\nBefore
submitting,
verify:\n\n###
Visual\n\n- [] Dashboard loads in yellow->red)\n\n- [] Drill-down links
work\n\n- [] Legend displays
correctly\n\n###
Standards Compliance\n\n- [] Dashboard name follows
`component-aspect`format\n\n- [] Panel
titles
are CamelCase with units\n\n- [] Colors match standard palette
(green/yellow/red)\n\n- []
Thresholds
are documented with rationale\n\n- [] All queries include comments and legend
format\n\n-
[] Time
windows are appropriate (?5 data points)\n\n### Documentation\n\n- [] Dashboard
has
description
explaining purpose\n\n- [] Queries are documented (what metric, why this
aggregation)\n\n-
[]
Thresholds documented with runbook links\n\n- [] Added to
opt/grafana/README.md\n\n- []
Tags include
"debvisor"\n\n### Performance\n\n- [] Queries optimized (no excessive label
cardinality)\n\n- []
Refresh rate appropriate (10s for alerts, 30s for normal)\n\n- [] Legends show
current,
max, mean
(not excessive)\n\n- []
Data Sources
-> Test\n\n## Solution\n\n- Verify metric name and label matchers\n\n- Check
Prometheus
scrape
config includes job\n\n- Verify datasource URL is correct\n\n### Slow Dashboard
Load\n\n-
*Problem:**Dashboard takes >5 seconds to load\n\n### Optimize\n\n 1. Reduce
number of
panels (<20
total)\n\n 1. Increase refresh rate (30s instead of 10s)\n\n 1. Simplify queries
(avoid
high-cardinality labels)\n\n 1. Add query caching where appropriate\n\n###
Threshold Not
Triggering\n\n- *Problem:**Threshold colors don't change\n\n### Debug [2]\n\n##

1. Run
query
manually\n\n curl
'[http://prometheus:9090/api/v1/query?query=YOUR_QUERY']([http://prometheus:9090/api/v1/query?query=YOUR_QUERY]([http://prometheus:9090/api/v1/query?query=YOUR_QUER]([http://prometheus:9090/api/v1/query?query=YOUR_QUE]([http://prometheus:9090/api/v1/query?query=YOUR*QU]([http://prometheus:9090/api/v1/query?query=YOUR*Q]([http://prometheus:9090/api/v1/query?query=YOUR*]([http://prometheus:9090/api/v1/query?query=YOUR]([http://prometheus:9090/api/v1/query?query=YOU]([http://prometheus:9090/api/v1/query?query=YO]([http://prometheus:9090/api/v1/query?query=Y]([http://prometheus:9090/api/v1/query?query=]([http://prometheus:9090/api/v1/query?query]([http://prometheus:9090/api/v1/query?quer]([http://prometheus:9090/api/v1/query?que]([http://prometheus:9090/api/v1/query?qu]([http://prometheus:9090/api/v1/query?q]([http://prometheus:9090/api/v1/query?]([http://prometheus:9090/api/v1/query]([http://prometheus:9090/api/v1/quer]([http://prometheus:9090/api/v1/que]([http://prometheus:9090/api/v1/qu]([http://prometheus:9090/api/v1/q]([http://prometheus:9090/api/v1/]([http://prometheus:9090/api/v1]([http://prometheus:9090/api/v]([http://prometheus:9090/api/]([http://prometheus:9090/api]([http://prometheus:9090/ap]([http://prometheus:9090/a]([http://prometheus:9090/]([http://prometheus:9090]([http://prometheus:909]([http://prometheus:90]([http://prometheus:9]([http://prometheus:]([http://prometheus]([http://prometheu]([http://promethe]([http://prometh]([http://promet]([http://prome](http://prome)t)h)e)u)s):)9)0)9)0)/)a)p)i)/)v)1)/)q)u)e)r)y)?)q)u)e)r)y)=)Y)O)U)R)*)Q)U)E)R)Y)')
| jq .\n\n## 2. Check current value vs threshold\n\n## Panel shows current value; compare to
threshold\n\n## 3. Verify threshold mode\n\n## Should be "absolute" or
"percentage" as
needed\n\n##
Solution [2]\n\n- Adjust threshold values based on actual metric range\n\n-
Verify
aggregation
produces expected value range\n\n- Test with fixtures if no real data
available\n\n## Best
Practices\n\n1.**Start Simple:**Create a single metric dashboard first\n1.**Test
Thoroughly:**Verify
all panels work before sharing\n1.**Document Well:**Future you will thank
present
you\n1.**Get
Feedback:**Share dashboard with ops team early\n1.**Iterate:**Adjust based on
real usage
patterns\n1.**Keep Current:**Review and update thresholds quarterly\n\n## Next
Steps\n\nAfter
creating your dashboard:\n1.**Share with Team:**Post in Slack or email for
feedback\n1.**Monitor
Usage:**Check if operators are actually using it\n1.**Gather Feedback:**Ask "Is
this
helpful? What's
missing?"\n1.**Refine:**Adjust panels, queries, thresholds based on
feedback\n1.**Document
Results:**Update README with lessons learned\n\n## References\n\n- [Dashboard
Standards](./DASHBOARD_STANDARDS.md)\n\n- [Prometheus Query
Documentation]([https://prometheus.io/docs/prometheus/latest/querying/basics]([https://prometheus.io/docs/prometheus/latest/querying/basic]([https://prometheus.io/docs/prometheus/latest/querying/basi]([https://prometheus.io/docs/prometheus/latest/querying/bas]([https://prometheus.io/docs/prometheus/latest/querying/ba]([https://prometheus.io/docs/prometheus/latest/querying/b]([https://prometheus.io/docs/prometheus/latest/querying/]([https://prometheus.io/docs/prometheus/latest/querying]([https://prometheus.io/docs/prometheus/latest/queryin]([https://prometheus.io/docs/prometheus/latest/queryi]([https://prometheus.io/docs/prometheus/latest/query]([https://prometheus.io/docs/prometheus/latest/quer]([https://prometheus.io/docs/prometheus/latest/que]([https://prometheus.io/docs/prometheus/latest/qu]([https://prometheus.io/docs/prometheus/latest/q]([https://prometheus.io/docs/prometheus/latest/]([https://prometheus.io/docs/prometheus/latest]([https://prometheus.io/docs/prometheus/lates]([https://prometheus.io/docs/prometheus/late]([https://prometheus.io/docs/prometheus/lat]([https://prometheus.io/docs/prometheus/la]([https://prometheus.io/docs/prometheus/l]([https://prometheus.io/docs/prometheus/]([https://prometheus.io/docs/prometheus]([https://prometheus.io/docs/prometheu]([https://prometheus.io/docs/promethe]([https://prometheus.io/docs/prometh]([https://prometheus.io/docs/promet]([https://prometheus.io/docs/prome]([https://prometheus.io/docs/prom]([https://prometheus.io/docs/pro]([https://prometheus.io/docs/pr]([https://prometheus.io/docs/p]([https://prometheus.io/docs/]([https://prometheus.io/docs]([https://prometheus.io/doc]([https://prometheus.io/do]([https://prometheus.io/d]([https://prometheus.io/]([https://prometheus.io]([https://prometheus.i](https://prometheus.i)o)/)d)o)c)s)/)p)r)o)m)e)t)h)e)u)s)/)l)a)t)e)s)t)/)q)u)e)r)y)i)n)g)/)b)a)s)i)c)s)/)\n\n-
[Grafana
Documentation]([https://grafana.com/docs/grafana/latest]([https://grafana.com/docs/grafana/lates]([https://grafana.com/docs/grafana/late]([https://grafana.com/docs/grafana/lat]([https://grafana.com/docs/grafana/la]([https://grafana.com/docs/grafana/l]([https://grafana.com/docs/grafana/]([https://grafana.com/docs/grafana]([https://grafana.com/docs/grafan]([https://grafana.com/docs/grafa]([https://grafana.com/docs/graf]([https://grafana.com/docs/gra]([https://grafana.com/docs/gr]([https://grafana.com/docs/g]([https://grafana.com/docs/]([https://grafana.com/docs]([https://grafana.com/doc]([https://grafana.com/do]([https://grafana.com/d]([https://grafana.com/]([https://grafana.com]([https://grafana.co]([https://grafana.c]([https://grafana.]([https://grafana]([https://grafan]([https://grafa]([https://graf]([https://gra]([https://gr]([https://g](https://g)r)a)f)a)n)a).)c)o)m)/)d)o)c)s)/)g)r)a)f)a)n)a)/)l)a)t)e)s)t)/)\n\n-
[DebVisor Monitoring Guide](../monitoring/README.md)\n\n- [DebVisor Fixtures
Guide](../monitoring/FIXTURES_GUIDE.md) (for testing with synthetic data)\n\n
