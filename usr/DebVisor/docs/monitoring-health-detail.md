# Monitoring DebVisor Health with Prometheus and Grafana

DebVisor exposes a detailed health endpoint at `/health/detail` that includes build info and dependency statuses (database, Redis, SMTP).

## Prometheus Scrape (blackbox style)

If you prefer to scrape raw metrics, use `/metrics`. For dashboards that need JSON health, use the Prometheus `blackbox_exporter` HTTP probe to record status codes.

Example `blackbox_exporter` config:

```yaml

modules:
  http_2xx:
    prober: http
    timeout: 5s

```text

Prometheus job:

```yaml

scrape_configs:

- job_name: debvisor-health

    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:

      - targets:
    - <https://debvisor.example.com/health/detail>

    relabel_configs:

      - source_labels: [**address**]

        target_label: __param_target

      - source_labels: [__param_target]

        target_label: instance

      - target_label: **address**

        replacement: blackbox-exporter:9115

```text

This records probe success/failure and latency. Pair with native `/metrics` for application metrics.

## Grafana JSON Datasource (direct)

Grafana can read JSON endpoints. Add a JSON API datasource and create a panel to fetch `GET /health/detail`.

Example panel query URL: `<https://debvisor.example.com/health/detail`>

Panel transformation:

- Extract fields: `status`, `build.version`, `checks.database`, `checks.redis`, `checks.smtp`
- Map `status: ok -> 1`, `degraded -> 0` for alert thresholds.

## Grafana Alerts

- Alert if `status == degraded`
- Alert if `checks.database == error`
- Alert if `checks.redis == error` (only if Redis is expected)
- Alert if `checks.smtp == error` (only if SMTP is configured)

## Native Prometheus Metrics

For application metrics (latency, request counts), use `/metrics` which exposes Prometheus format.

Quick validation:

```bash

curl -s <https://debvisor.example.com/metrics> | head
curl -s <https://debvisor.example.com/health/detail> | jq

```text
