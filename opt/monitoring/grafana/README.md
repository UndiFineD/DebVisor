# DebVisor Grafana layout

This directory contains DebVisor's opinionated defaults for Grafana:
JSON dashboards, provisioning snippets, and alerting rules. It is
intended as a__starter pack__, not a full monitoring product.

## On-disk layout and paths

- `monitoring/grafana/dashboards/`
- Source JSON for DebVisor dashboards.
- These are typically copied or symlinked into Grafana's dashboards

    directory on the node (for example `/var/lib/grafana/dashboards/`).

- `monitoring/grafana/provisioning/dashboards/`
- Grafana dashboard provisioning files (for example `dashboards.yml`).
- Tell Grafana where to find JSON dashboards on disk and which

    folders to use.

- `monitoring/grafana/provisioning/datasources/`
- Datasource provisioning (Prometheus, Loki, etc.).
- Defines the canonical datasource names and, where supported,

    explicit UIDs.

- `monitoring/grafana/provisioning/alerting/`
- Alerting rules intended to pair with the shipped dashboards.
- Typically mounted under `/etc/grafana/provisioning/alerting/` on a

    DebVisor node.

On a DebVisor host that runs Grafana locally, the usual mapping is:

- Provisioning YAML: `/etc/grafana/provisioning/__` (mounted or copied

  from this directory).

- Dashboards JSON: `/var/lib/grafana/dashboards/` pointing back to

  `monitoring/grafana/dashboards/` via copy, sync job, or read-only
  bind mount.

In clusters where Grafana runs elsewhere, treat this directory as the
__source of truth__and sync the provisioning and dashboard JSON into
that Grafana instance.

## Datasource names and UIDs

To make dashboards portable between DebVisor deployments, we recommend
recreating datasources with the following identifiers:

- Prometheus:
- Name: `Prometheus`
- Suggested UID: `prometheus-debvisor`
- Type: `prometheus`
- URL examples:
- Single-node: [http://localhost:9090](http://localhost:9090)
- Clustered: [http://prometheus.debvisor-monitoring.svc:9090](http://prometheus.debvisor-monitoring.svc:9090)
- Loki (optional, if you deploy it):
- Name: `Loki`
- Suggested UID: `loki-debvisor`
- Type: `loki`
- URL examples:
- Single-node: [http://localhost:3100](http://localhost:3100)
- Clustered: [http://loki.debvisor-monitoring.svc:3100](http://loki.debvisor-monitoring.svc:3100)

Dashboards under `monitoring/grafana/dashboards/` should use these
names or UIDs so that operators can:

- Import them into an existing Grafana.
- Create matching datasources once per environment.

If you choose different names or UIDs, update the datasource
references in the dashboards or override them via Grafana's UI.

## Starter vs near-production content

DebVisor's Grafana content is deliberately split into two rough
categories:

-__Starter dashboards and alerts__:

- Focused on showing that metrics wiring works (node CPU/memory,

    basic DNS/VM views), not on full SRE-grade coverage.

- Safe to import into labs and small clusters as examples.
- Files are usually marked with comments noting they are

    "starter" or "example" content.

-__Near-production dashboards/alerts__(when present):

- Aim for more complete coverage of core DebVisor components (Ceph,

    ZFS, DNS HA, TSIG rotation, Kubernetes control plane) with
    thresholds that are reasonable defaults.

- Designed to be tuned rather than rewritten from scratch. Operators

    should still review scrape intervals, lookback windows, and
    severities.

As of now, most dashboards and alerts in this tree should be treated
as__starter__content. Before relying on them for production:

- Verify that all referenced metrics and label names exist in your

  Prometheus and Loki instances.

- Adjust thresholds and time ranges for your cluster size and

  performance envelope.

- Wire alert rules into your chosen Alertmanager routes and

  notification channels.

## How to use in practice

1. Ensure Prometheus (and optionally Loki) are reachable from Grafana

   and configured with the names/UIDs above.

1. Copy or mount `monitoring/grafana/provisioning/__` into your

   Grafana provisioning directory.

1. Copy or sync `monitoring/grafana/dashboards/__` into the path

   referenced by the dashboard provisioning YAML (for example
   `/var/lib/grafana/dashboards/`).

1. Restart Grafana; check that the DebVisor dashboards appear under

   the expected folders and that panels render data.

1. Enable or adjust alerting rules under

   `monitoring/grafana/provisioning/alerting/` as appropriate for your
   environment.
