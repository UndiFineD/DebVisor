# Monitoring DebVisor Health with Prometheus and Grafana\n\nDebVisor exposes a detailed

health

endpoint at `/health/detail`that includes build info and dependency statuses
(database,
Redis,
SMTP).\n\n## Prometheus Scrape (blackbox style)\n\nIf you prefer to scrape raw
metrics,
use`/metrics`. For dashboards that need JSON health, use the Prometheus
`blackbox_exporter`HTTP
probe to record status
codes.\nExample`blackbox_exporter`config:\n\n```yaml\nmodules:\n
http_2xx:\n
prober: http\n timeout: 5s\n```text\n\n http_2xx:\n prober: http\n timeout:
5s\n```text\nmodules:\n
http_2xx:\n prober: http\n timeout: 5s\n```text\n\n http_2xx:\n prober: http\n timeout:
5s\n```text\nmodules:\n http_2xx:\n prober: http\n timeout: 5s\n```text\n\n
http_2xx:\n
prober:
http\n timeout: 5s\n```text\n http_2xx:\n prober: http\n timeout: 5s\n```text\n\n prober: http\n
timeout: 5s\n```text\nPrometheus job:\n\n```yaml\n\n```yaml\nPrometheus
job:\n\n```yaml\n\n```yaml\nPrometheus
job:\n\n```yaml\n\n```yaml\n\n```yaml\n\n```yaml\nscrape_configs:\n\n- job_name:
debvisor-health\n
metrics_path: /probe\n params:\n module: [http_2xx]\n static_configs:\n\n -
targets:\n\n -
\n]([https://debvisor.example.com/health/detail>\]([https://debvisor.example.com/health/detail>]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)>)\)n)
relabel_configs:\n\n - source_labels: [**address**]\n target*label:
*_param_target\n\n -
source*labels: [*_param_target]\n target_label: instance\n\n - target_label:
**address**\n
replacement: blackbox-exporter:9115\n```text\n\n- job_name: debvisor-health\n\n
metrics_path:
/probe\n params:\n module: [http_2xx]\n static_configs:\n\n - targets:\n\n -

>\n\n]([https://debvisor.example.com/health/detail>>\n\]([https://debvisor.example.com/health/detail>>\n]([https://debvisor.example.com/health/detail>>\]([https://debvisor.example.com/health/detail>>]([https://debvisor.example.com/health/detail>]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)>)>)\)n)\)n)
relabel_configs:\n\n - source_labels: [**address**]\n\n target*label:
*_param_target\n\n -
source*labels: [*_param_target]\n\n target_label: instance\n\n - target_label:
**address**\n\n
replacement: blackbox-exporter:9115\n```text\nscrape_configs:\n\n- job_name:
debvisor-health\n
metrics_path: /probe\n params:\n module: [http_2xx]\n static_configs:\n\n -
targets:\n\n -
[https://debvisor.example.com/health/detail\n]([https://debvisor.example.com/health/detail\]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)\)n)
relabel_configs:\n\n - source_labels: [**address**]\n target*label:
*_param_target\n\n -
source*labels: [*_param_target]\n target_label: instance\n\n - target_label:
**address**\n
replacement: blackbox-exporter:9115\n```text\n\n- job_name: debvisor-health\n\n
metrics_path:
/probe\n params:\n module: [http_2xx]\n static_configs:\n\n - targets:\n\n -
\n\n]([https://debvisor.example.com/health/detail>\n\]([https://debvisor.example.com/health/detail>\n]([https://debvisor.example.com/health/detail>\]([https://debvisor.example.com/health/detail>]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)>)\)n)\)n)
relabel_configs:\n\n - source_labels: [**address**]\n\n target*label:
*_param_target\n\n -
source*labels: [*_param_target]\n\n target_label: instance\n\n - target_label:
**address**\n\n
replacement: blackbox-exporter:9115\n```text\nscrape_configs:\n\n- job_name:
debvisor-health\n
metrics_path: /probe\n params:\n module: [http_2xx]\n static_configs:\n\n -
targets:\n\n -
[https://debvisor.example.com/health/detail\n]([https://debvisor.example.com/health/detail\]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)\)n)
relabel_configs:\n\n - source_labels: [**address**]\n target*label:
*_param_target\n\n -
source*labels: [*_param_target]\n target_label: instance\n\n - target_label:
**address**\n
replacement: blackbox-exporter:9115\n```text\n\n- job_name: debvisor-health\n\n
metrics_path:
/probe\n params:\n module: [http_2xx]\n static_configs:\n\n - targets:\n\n -
\n\n]([https://debvisor.example.com/health/detail>\n\]([https://debvisor.example.com/health/detail>\n]([https://debvisor.example.com/health/detail>\]([https://debvisor.example.com/health/detail>]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)>)\)n)\)n)
relabel_configs:\n\n - source_labels: [**address**]\n\n target*label:
*_param_target\n\n -
source*labels: [*_param_target]\n\n target_label: instance\n\n - target_label:
**address**\n\n
replacement: blackbox-exporter:9115\n```text\n\n- job_name: debvisor-health\n
metrics_path: /probe\n
params:\n module: [http_2xx]\n static_configs:\n\n - targets:\n\n -
[https://debvisor.example.com/health/detail\n]([https://debvisor.example.com/health/detail\]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)\)n)
relabel_configs:\n\n - source_labels: [**address**]\n target*label:
*_param_target\n\n -
source*labels: [*_param_target]\n target_label: instance\n\n - target_label:
**address**\n
replacement: blackbox-exporter:9115\n```text\n\n- job_name: debvisor-health\n\n
metrics_path:
/probe\n params:\n module: [http_2xx]\n static_configs:\n\n - targets:\n\n -
\n\n]([https://debvisor.example.com/health/detail>\n\]([https://debvisor.example.com/health/detail>\n]([https://debvisor.example.com/health/detail>\]([https://debvisor.example.com/health/detail>]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)>)\)n)\)n)
relabel_configs:\n\n - source_labels: [**address**]\n\n target*label:
*_param_target\n\n -
source*labels: [*_param_target]\n\n target_label: instance\n\n - target_label:
**address**\n\n
replacement: blackbox-exporter:9115\n```text\nThis records probe success/failure
and
latency. Pair
with native`/metrics`for application metrics.\n## Grafana JSON Datasource
(direct)\nGrafana can read
JSON endpoints. Add a JSON API datasource and create a panel to fetch`GET
/health/detail`.\nExample
panel query URL:
`[https://debvisor.example.com/health/detail`\nPanel]([https://debvisor.example.com/health/detail`\nPane]([https://debvisor.example.com/health/detail`\nPan]([https://debvisor.example.com/health/detail`\nPa]([https://debvisor.example.com/health/detail`\nP]([https://debvisor.example.com/health/detail`\n]([https://debvisor.example.com/health/detail`\]([https://debvisor.example.com/health/detail`]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)`)\)n)P)a)n)e)l)
transformation:\n\n- Extract fields: `status`, `build.version`,
`checks.database`,
`checks.redis`,
`checks.smtp`\n\n- Map `status: ok -> 1`, `degraded -> 0`for alert
thresholds.\n## Grafana
Alerts\n-
Alert if`status == degraded`\n\n- Alert if `checks.database == error`\n\n- Alert
if
`checks.redis ==
error`(only if Redis is expected)\n\n- Alert if`checks.smtp == error`(only if
SMTP is
configured)\n## Native Prometheus Metrics\nFor application metrics (latency,
request
counts),
use`/metrics`which exposes Prometheus format.\nQuick
validation:\n\n```bash\n\n## Grafana
JSON
Datasource (direct) (2)\n\nGrafana can read JSON endpoints. Add a JSON API
datasource and
create a
panel to fetch`GET /health/detail`.\nExample panel query URL:
`\nPanel]([https://debvisor.example.com/health/detail`>\nPane]([https://debvisor.example.com/health/detail`>\nPan]([https://debvisor.example.com/health/detail`>\nPa]([https://debvisor.example.com/health/detail`>\nP]([https://debvisor.example.com/health/detail`>\n]([https://debvisor.example.com/health/detail`>\]([https://debvisor.example.com/health/detail`>]([https://debvisor.example.com/health/detail`]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)`)>)\)n)P)a)n)e)l)
transformation:\n\n- Extract fields: `status`, `build.version`,
`checks.database`,
`checks.redis`,
`checks.smtp`\n\n- Map `status: ok -> 1`, `degraded -> 0`for alert
thresholds.\n\n##
Grafana Alerts
(2)\n\n- Alert if`status == degraded`\n\n- Alert if `checks.database ==
error`\n\n- Alert
if
`checks.redis == error`(only if Redis is expected)\n\n- Alert if`checks.smtp ==
error`(only if SMTP
is configured)\n\n## Native Prometheus Metrics (2)\n\nFor application metrics
(latency,
request
counts), use`/metrics`which exposes Prometheus format.\nQuick
validation:\n\n```bash\nThis
records
probe success/failure and latency. Pair with native`/metrics`for application
metrics.\n\n## Grafana
JSON Datasource (direct) (3)\n\nGrafana can read JSON endpoints. Add a JSON API
datasource
and
create a panel to fetch`GET /health/detail`.\nExample panel query URL:
`[https://debvisor.example.com/health/detail`\nPanel]([https://debvisor.example.com/health/detail`\nPane]([https://debvisor.example.com/health/detail`\nPan]([https://debvisor.example.com/health/detail`\nPa]([https://debvisor.example.com/health/detail`\nP]([https://debvisor.example.com/health/detail`\n]([https://debvisor.example.com/health/detail`\]([https://debvisor.example.com/health/detail`]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)`)\)n)P)a)n)e)l)
transformation:\n\n- Extract fields: `status`, `build.version`,
`checks.database`,
`checks.redis`,
`checks.smtp`\n\n- Map `status: ok -> 1`, `degraded -> 0`for alert
thresholds.\n\n##
Grafana Alerts
(3)\n\n- Alert if`status == degraded`\n\n- Alert if `checks.database ==
error`\n\n- Alert
if
`checks.redis == error`(only if Redis is expected)\n\n- Alert if`checks.smtp ==
error`(only if SMTP
is configured)\n\n## Native Prometheus Metrics (3)\n\nFor application metrics
(latency,
request
counts), use`/metrics`which exposes Prometheus format.\nQuick
validation:\n\n```bash\n\n##
Grafana
JSON Datasource (direct) (4)\n\nGrafana can read JSON endpoints. Add a JSON API
datasource
and
create a panel to fetch`GET /health/detail`.\nExample panel query URL:
`\nPanel]([https://debvisor.example.com/health/detail`>\nPane]([https://debvisor.example.com/health/detail`>\nPan]([https://debvisor.example.com/health/detail`>\nPa]([https://debvisor.example.com/health/detail`>\nP]([https://debvisor.example.com/health/detail`>\n]([https://debvisor.example.com/health/detail`>\]([https://debvisor.example.com/health/detail`>]([https://debvisor.example.com/health/detail`]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)`)>)\)n)P)a)n)e)l)
transformation:\n\n- Extract fields: `status`, `build.version`,
`checks.database`,
`checks.redis`,
`checks.smtp`\n\n- Map `status: ok -> 1`, `degraded -> 0`for alert
thresholds.\n\n##
Grafana Alerts
(4)\n\n- Alert if`status == degraded`\n\n- Alert if `checks.database ==
error`\n\n- Alert
if
`checks.redis == error`(only if Redis is expected)\n\n- Alert if`checks.smtp ==
error`(only if SMTP
is configured)\n\n## Native Prometheus Metrics (4)\n\nFor application metrics
(latency,
request
counts), use`/metrics`which exposes Prometheus format.\nQuick
validation:\n\n```bash\nThis
records
probe success/failure and latency. Pair with native`/metrics`for application
metrics.\n##
Grafana
JSON Datasource (direct) (5)\nGrafana can read JSON endpoints. Add a JSON API
datasource
and create
a panel to fetch`GET /health/detail`.\nExample panel query URL:
`[https://debvisor.example.com/health/detail`\nPanel]([https://debvisor.example.com/health/detail`\nPane]([https://debvisor.example.com/health/detail`\nPan]([https://debvisor.example.com/health/detail`\nPa]([https://debvisor.example.com/health/detail`\nP]([https://debvisor.example.com/health/detail`\n]([https://debvisor.example.com/health/detail`\]([https://debvisor.example.com/health/detail`]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)`)\)n)P)a)n)e)l)
transformation:\n\n- Extract fields: `status`, `build.version`,
`checks.database`,
`checks.redis`,
`checks.smtp`\n\n- Map `status: ok -> 1`, `degraded -> 0`for alert
thresholds.\n## Grafana
Alerts
(5)\n- Alert if`status == degraded`\n\n- Alert if `checks.database ==
error`\n\n- Alert if
`checks.redis == error`(only if Redis is expected)\n\n- Alert if`checks.smtp ==
error`(only if SMTP
is configured)\n## Native Prometheus Metrics (5)\nFor application metrics
(latency,
request counts),
use`/metrics`which exposes Prometheus format.\nQuick
validation:\n\n```bash\n\n## Grafana
JSON
Datasource (direct) (6)\n\nGrafana can read JSON endpoints. Add a JSON API
datasource and
create a
panel to fetch`GET /health/detail`.\nExample panel query URL:
`\nPanel]([https://debvisor.example.com/health/detail`>\nPane]([https://debvisor.example.com/health/detail`>\nPan]([https://debvisor.example.com/health/detail`>\nPa]([https://debvisor.example.com/health/detail`>\nP]([https://debvisor.example.com/health/detail`>\n]([https://debvisor.example.com/health/detail`>\]([https://debvisor.example.com/health/detail`>]([https://debvisor.example.com/health/detail`]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)`)>)\)n)P)a)n)e)l)
transformation:\n\n- Extract fields: `status`, `build.version`,
`checks.database`,
`checks.redis`,
`checks.smtp`\n\n- Map `status: ok -> 1`, `degraded -> 0`for alert
thresholds.\n\n##
Grafana Alerts
(6)\n\n- Alert if`status == degraded`\n\n- Alert if `checks.database ==
error`\n\n- Alert
if
`checks.redis == error`(only if Redis is expected)\n\n- Alert if`checks.smtp ==
error`(only if SMTP
is configured)\n\n## Native Prometheus Metrics (6)\n\nFor application metrics
(latency,
request
counts), use`/metrics`which exposes Prometheus format.\nQuick
validation:\n\n```bash\n##
Grafana
JSON Datasource (direct) (7)\n\nGrafana can read JSON endpoints. Add a JSON API
datasource
and
create a panel to fetch`GET /health/detail`.\nExample panel query URL:
`[https://debvisor.example.com/health/detail`\nPanel]([https://debvisor.example.com/health/detail`\nPane]([https://debvisor.example.com/health/detail`\nPan]([https://debvisor.example.com/health/detail`\nPa]([https://debvisor.example.com/health/detail`\nP]([https://debvisor.example.com/health/detail`\n]([https://debvisor.example.com/health/detail`\]([https://debvisor.example.com/health/detail`]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)`)\)n)P)a)n)e)l)
transformation:\n\n- Extract fields: `status`, `build.version`,
`checks.database`,
`checks.redis`,
`checks.smtp`\n\n- Map `status: ok -> 1`, `degraded -> 0`for alert
thresholds.\n\n##
Grafana Alerts
(7)\n\n- Alert if`status == degraded`\n\n- Alert if `checks.database ==
error`\n\n- Alert
if
`checks.redis == error`(only if Redis is expected)\n\n- Alert if`checks.smtp ==
error`(only if SMTP
is configured)\n\n## Native Prometheus Metrics (7)\n\nFor application metrics
(latency,
request
counts), use`/metrics`which exposes Prometheus format.\nQuick
validation:\n\n```bash\n\nGrafana can
read JSON endpoints. Add a JSON API datasource and create a panel to fetch`GET
/health/detail`.\nExample panel query URL:
`\nPanel]([https://debvisor.example.com/health/detail`>\nPane]([https://debvisor.example.com/health/detail`>\nPan]([https://debvisor.example.com/health/detail`>\nPa]([https://debvisor.example.com/health/detail`>\nP]([https://debvisor.example.com/health/detail`>\n]([https://debvisor.example.com/health/detail`>\]([https://debvisor.example.com/health/detail`>]([https://debvisor.example.com/health/detail`]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)`)>)\)n)P)a)n)e)l)
transformation:\n\n- Extract fields: `status`, `build.version`,
`checks.database`,
`checks.redis`,
`checks.smtp`\n\n- Map `status: ok -> 1`, `degraded -> 0`for alert
thresholds.\n\n##
Grafana Alerts
(8)\n\n- Alert if`status == degraded`\n\n- Alert if `checks.database ==
error`\n\n- Alert
if
`checks.redis == error`(only if Redis is expected)\n\n- Alert if`checks.smtp ==
error`(only if SMTP
is configured)\n\n## Native Prometheus Metrics (8)\n\nFor application metrics
(latency,
request
counts), use`/metrics` which exposes Prometheus format.\nQuick
validation:\n\n```bash\ncurl -s
]([https://debvisor.example.com/metrics]([https://debvisor.example.com/metric]([https://debvisor.example.com/metri]([https://debvisor.example.com/metr]([https://debvisor.example.com/met]([https://debvisor.example.com/me]([https://debvisor.example.com/m]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)m)e)t)r)i)c)s)>)
| head\ncurl -s
]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)>)
| jq\n```text\n\ncurl -s
]([https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)>)
| jq\n```text\ncurl -s
[https://debvisor.example.com/metrics]([https://debvisor.example.com/metric]([https://debvisor.example.com/metri]([https://debvisor.example.com/metr]([https://debvisor.example.com/met]([https://debvisor.example.com/me]([https://debvisor.example.com/m]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)m)e)t)r)i)c)s)
| head\ncurl -s
[https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)
| jq\n```text\n\ncurl -s
[https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)
| jq\n```text\ncurl -s
[https://debvisor.example.com/metrics]([https://debvisor.example.com/metric]([https://debvisor.example.com/metri]([https://debvisor.example.com/metr]([https://debvisor.example.com/met]([https://debvisor.example.com/me]([https://debvisor.example.com/m]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)m)e)t)r)i)c)s)
| head\ncurl -s
[https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)
| jq\n```text\n\ncurl -s
[https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)
| jq\n```text\ncurl -s
[https://debvisor.example.com/health/detail]([https://debvisor.example.com/health/detai]([https://debvisor.example.com/health/deta]([https://debvisor.example.com/health/det]([https://debvisor.example.com/health/de]([https://debvisor.example.com/health/d]([https://debvisor.example.com/health/]([https://debvisor.example.com/health]([https://debvisor.example.com/healt]([https://debvisor.example.com/heal]([https://debvisor.example.com/hea]([https://debvisor.example.com/he]([https://debvisor.example.com/h]([https://debvisor.example.com/]([https://debvisor.example.com]([https://debvisor.example.co]([https://debvisor.example.c]([https://debvisor.example.]([https://debvisor.example]([https://debvisor.exampl]([https://debvisor.examp]([https://debvisor.exam]([https://debvisor.exa]([https://debvisor.ex]([https://debvisor.e]([https://debvisor.]([https://debvisor]([https://debviso]([https://debvis]([https://debvi]([https://debv]([https://deb]([https://de]([https://d](https://d)e)b)v)i)s)o)r).)e)x)a)m)p)l)e).)c)o)m)/)h)e)a)l)t)h)/)d)e)t)a)i)l)
| jq\n```text\n```text\n\n
