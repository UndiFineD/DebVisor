# DebVisor Grafana layout\n\nThis directory contains DebVisor's opinionated defaults for

Grafana:\nJSON dashboards, provisioning snippets, and alerting rules. It
is\nintended as
a**starter
pack**, not a full monitoring product.\n\n## On-disk layout and paths\n\n-
`monitoring/grafana/dashboards/`\n\n- Source JSON for DebVisor dashboards.\n\n-
These are
typically
copied or symlinked into Grafana's dashboards\n\n directory on the node (for
example
`/var/lib/grafana/dashboards/`).\n\n-
`monitoring/grafana/provisioning/dashboards/`\n\n-
Grafana
dashboard provisioning files (for example `dashboards.yml`).\n\n- Tell Grafana
where to
find JSON
dashboards on disk and which\n\n folders to use.\n\n-
`monitoring/grafana/provisioning/datasources/`\n\n- Datasource provisioning
(Prometheus,
Loki,
etc.).\n\n- Defines the canonical datasource names and, where supported,\n\n
explicit
UIDs.\n\n-
`monitoring/grafana/provisioning/alerting/`\n\n- Alerting rules intended to pair
with the
shipped
dashboards.\n\n- Typically mounted under `/etc/grafana/provisioning/alerting/`on
a\n\n
DebVisor
node.\nOn a DebVisor host that runs Grafana locally, the usual mapping is:\n\n-
Provisioning
YAML:`/etc/grafana/provisioning/**`(mounted or copied\n\n from this
directory).\n\n-
Dashboards
JSON:`/var/lib/grafana/dashboards/`pointing back
to\n\n`monitoring/grafana/dashboards/`via
copy,
sync job, or read-only\n bind mount.\nIn clusters where Grafana runs elsewhere,
treat this
directory
as the\n\n- *source of truth**and sync the provisioning and dashboard JSON
into\n\nthat
Grafana
instance.\n\n## Datasource names and UIDs\n\nTo make dashboards portable between
DebVisor
deployments, we recommend\nrecreating datasources with the following
identifiers:\n\n-
Prometheus:\n\n- Name:`Prometheus`\n\n- Suggested UID:
`prometheus-debvisor`\n\n- Type:
`prometheus`\n\n- URL examples:\n\n- Single-node:
[http://localhost:9090]([http://localhost:909]([http://localhost:90]([http://localhost:9]([http://localhost:]([http://localhost]([http://localhos]([http://localho]([http://localh]([http://local]([http://loca]([http://loc]([http://lo]([http://l](http://l)o)c)a)l)h)o)s)t):)9)0)9)0)\n\n-
Clustered:
[http://prometheus.debvisor-monitoring.svc:9090]([http://prometheus.debvisor-monitoring.svc:909]([http://prometheus.debvisor-monitoring.svc:90]([http://prometheus.debvisor-monitoring.svc:9]([http://prometheus.debvisor-monitoring.svc:]([http://prometheus.debvisor-monitoring.svc]([http://prometheus.debvisor-monitoring.sv]([http://prometheus.debvisor-monitoring.s]([http://prometheus.debvisor-monitoring.]([http://prometheus.debvisor-monitoring]([http://prometheus.debvisor-monitorin]([http://prometheus.debvisor-monitori]([http://prometheus.debvisor-monitor]([http://prometheus.debvisor-monito]([http://prometheus.debvisor-monit]([http://prometheus.debvisor-moni]([http://prometheus.debvisor-mon]([http://prometheus.debvisor-mo]([http://prometheus.debvisor-m]([http://prometheus.debvisor-]([http://prometheus.debvisor]([http://prometheus.debviso]([http://prometheus.debvis]([http://prometheus.debvi]([http://prometheus.debv]([http://prometheus.deb]([http://prometheus.de]([http://prometheus.d]([http://prometheus.]([http://prometheus]([http://prometheu]([http://promethe](http://promethe)u)s).)d)e)b)v)i)s)o)r)-)m)o)n)i)t)o)r)i)n)g).)s)v)c):)9)0)9)0)\n\n-
Loki (optional, if you deploy it):\n\n- Name: `Loki`\n\n- Suggested UID:
`loki-debvisor`\n\n- Type:
`loki`\n\n- URL examples:\n\n- Single-node:
[http://localhost:3100]([http://localhost:310]([http://localhost:31]([http://localhost:3]([http://localhost:]([http://localhost]([http://localhos]([http://localho]([http://localh]([http://local]([http://loca]([http://loc]([http://lo]([http://l](http://l)o)c)a)l)h)o)s)t):)3)1)0)0)\n\n-
Clustered:
[http://loki.debvisor-monitoring.svc:3100]([http://loki.debvisor-monitoring.svc:310]([http://loki.debvisor-monitoring.svc:31]([http://loki.debvisor-monitoring.svc:3]([http://loki.debvisor-monitoring.svc:]([http://loki.debvisor-monitoring.svc]([http://loki.debvisor-monitoring.sv]([http://loki.debvisor-monitoring.s]([http://loki.debvisor-monitoring.]([http://loki.debvisor-monitoring]([http://loki.debvisor-monitorin]([http://loki.debvisor-monitori]([http://loki.debvisor-monitor]([http://loki.debvisor-monito]([http://loki.debvisor-monit]([http://loki.debvisor-moni]([http://loki.debvisor-mon]([http://loki.debvisor-mo]([http://loki.debvisor-m]([http://loki.debvisor-]([http://loki.debvisor]([http://loki.debviso]([http://loki.debvis]([http://loki.debvi]([http://loki.debv]([http://loki.deb]([http://loki.de]([http://loki.d]([http://loki.]([http://loki]([http://lok]([http://lo](http://lo)k)i).)d)e)b)v)i)s)o)r)-)m)o)n)i)t)o)r)i)n)g).)s)v)c):)3)1)0)0)\n\nDashboards
under `monitoring/grafana/dashboards/`should use these\nnames or UIDs so that
operators
can:\n\n-
Import them into an existing Grafana.\n\n- Create matching datasources once per
environment.\n\nIf
you choose different names or UIDs, update the datasource\nreferences in the
dashboards or
override
them via Grafana's UI.\n\n## Starter vs near-production content\n\nDebVisor's
Grafana
content is
deliberately split into two rough\ncategories:\n\n- **Starter dashboards and
alerts**:\n\n- Focused
on showing that metrics wiring works (node CPU/memory,\n\n basic DNS/VM views),
not on
full
SRE-grade coverage.\n\n- Safe to import into labs and small clusters as
examples.\n\n-
Files are
usually marked with comments noting they are\n\n "starter" or "example"
content.\n\n-
**Near-production dashboards/alerts**(when present):\n\n- Aim for more complete
coverage
of core
DebVisor components (Ceph,\n\n ZFS, DNS HA, TSIG rotation, Kubernetes control
plane)
with\n
thresholds that are reasonable defaults.\n\n- Designed to be tuned rather than
rewritten
from
scratch. Operators\n\n should still review scrape intervals, lookback windows,
and\n
severities.\nAs
of now, most dashboards and alerts in this tree should be
treated\nas**starter**content.
Before
relying on them for production:\n\n- Verify that all referenced metrics and
label names
exist in
your\n\n Prometheus and Loki instances.\n\n- Adjust thresholds and time ranges
for your
cluster size
and\n\n performance envelope.\n\n- Wire alert rules into your chosen
Alertmanager routes
and\n\n
notification channels.\n\n## How to use in practice\n\n1. Ensure Prometheus (and
optionally Loki)
are reachable from Grafana\n\n and configured with the names/UIDs above.\n\n1.
Copy or
mount`monitoring/grafana/provisioning/**`into your\n\n Grafana provisioning
directory.\n\n1. Copy or
sync`monitoring/grafana/dashboards/__`into the path\n\n referenced by the
dashboard
provisioning
YAML (for example\n`/var/lib/grafana/dashboards/`).\n\n1. Restart Grafana; check
that the
DebVisor
dashboards appear under\n\n the expected folders and that panels render
data.\n\n1. Enable
or adjust
alerting rules under\n\n `monitoring/grafana/provisioning/alerting/` as
appropriate for
your\n
environment.\n\n
