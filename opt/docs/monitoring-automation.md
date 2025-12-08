# DebVisor Monitoring & Automation Components

This directory contains Grafana dashboards, Prometheus exporters, and automation workflows for DebVisor cluster operations.

## Grafana Dashboards

-**dns-dhcp-overview.json**: Real-time DNS/DHCP monitoring with TSIG rotation tracking
-**multi-tenant-isolation.json**: Per-tenant zone health with cross-lease leak detection
-**compliance-mfa-audit.json**: MFA enforcement status and audit trail visualization

## Kubernetes Manifests

These manifests are**test fixtures only**. They are intended to
exercise dashboards and alerting paths in a lab or staging cluster and
should not be enabled by default in production.

The synthetic metrics job is**optional**and intended primarily for
lab/staging clusters. Both the CronJob and ConfigMaps are labeled with
`debvisor.io/test-fixture: "true"` so they can be discovered and
filtered easily.

Endpoints such as DNS servers and the Prometheus Pushgateway are
parameterized via the `synthetic-metrics-config` ConfigMap. To
customize them for a given cluster, edit the values in that ConfigMap
before applying, for example:

    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: synthetic-metrics-config
      namespace: debvisor-monitoring
    data:
      PROMETHEUS_PUSHGATEWAY: "[http://prometheus-pushgateway.debvisor-monitoring.svc:9091"](http://prometheus-pushgateway.debvisor-monitoring.svc:9091")
      DNS_SERVER: "10.10.0.1"
      BIND_EXPORTER: "[http://10.10.0.1:9119"](http://10.10.0.1:9119")

To deploy the fixtures in a cluster:

    kubectl apply -f monitoring/grafana/manifests/synthetic-metrics-configmap.yaml
    kubectl apply -f monitoring/grafana/manifests/synthetic-metrics-cronjob.yaml

To remove them again:

    kubectl delete -f monitoring/grafana/manifests/synthetic-metrics-cronjob.yaml
    kubectl delete -f monitoring/grafana/manifests/synthetic-metrics-configmap.yaml

- Both resources are labeled with `debvisor.io/test-fixture: "true"` so

  that they can be discovered and filtered easily.

- The CronJob runs with conservative CPU/memory limits and a non-root

  security context.

## Ansible Playbooks

Located in `../ansible/playbooks/`:

-**enforce-mfa.yml**: Install Google Authenticator PAM module, configure SSH for MFA
-**quarantine-host.yml**: Isolate compromised node with nftables, disable VM autostart, tag in DNS/Prometheus
-**block-ips.yml**: Add malicious IPs to nftables blocklist set, log to audit trail

## ArgoCD Workflows

Located in `../argocd/`:

-**security-remediation-workflow.yaml**: Alert -> Webhook -> AWX -> Playbook -> Verification flow

## CI/CD Validation

Located in `../.github/workflows/`:

-**validate-dashboards.yml**: GitHub Actions workflow to validate JSON schema and test Grafana imports

## Usage

### Import Dashboards

    for dashboard in grafana/dashboards/*.json; do
      curl -X POST [http://admin:admin@grafana.debvisor.local/api/dashboards/db](http://admin:admin@grafana.debvisor.local/api/dashboards/db) \
        -H "Content-Type: application/json" \
        -d @"$dashboard"
    done

### Deploy Kubernetes Resources

    kubectl apply -f monitoring/grafana/manifests/synthetic-metrics-cronjob.yaml
    kubectl apply -f monitoring/grafana/manifests/synthetic-metrics-configmap.yaml

To remove the fixtures again:

    kubectl delete -f monitoring/grafana/manifests/synthetic-metrics-cronjob.yaml
    kubectl delete -f monitoring/grafana/manifests/synthetic-metrics-configmap.yaml

### Trigger Ansible Playbook

    ansible-playbook -i inventory ansible/playbooks/enforce-mfa.yml
    ansible-playbook -i inventory -e "target_host=node3" ansible/playbooks/quarantine-host.yml
    ansible-playbook -i inventory -e "blocked_ips=1.2.3.4,5.6.7.8" ansible/playbooks/block-ips.yml

## Metrics Exposed

- `bind_queries_total`: Total DNS queries by type
- `bind_updates_total`: Dynamic DNS update count
- `dnsmasq_leases_active`: Current DHCP lease count
- `tsig_rotation_last_timestamp`: Last TSIG key rotation timestamp
- `debvisor_node_mfa_enabled`: MFA enforcement status (0/1)
- `debvisor_auth_failures_total`: Failed authentication attempts
- `debvisor_blocked_ips`: Count of IPs in nftables blocklist

In addition, the `ceph-health.timer`/`ceph-health.service` pair runs a
periodic `ceph -s` check and logs the outcome with the
`ceph-health` Syslog identifier. These logs can be scraped via your
preferred log pipeline (for example journald -> Loki) and visualised or
alerted on in Grafana, for example by counting recent non-HEALTH
oK
events.

## Alerting and ownership

Alert rules under `monitoring/grafana/provisioning/alerting/` are
intended as a starting point rather than a finished SRE playbook.

- Some rules are**starter alerts**whose main goal is to prove that

  metrics wiring and notification channels work (for example basic
  node CPU/memory, simple DNS/DHCP health checks).

- Others are closer to**near-production**defaults for core DebVisor

  services (Ceph/ZFS health, DNS HA, TSIG rotation, control-plane
  reachability) but still expect site-specific tuning.

When adopting these rules in a real environment, review and adjust:

-**Scrape intervals and evaluation frequency**: higher-frequency
  scraping/evaluation yields faster detection but more load.

-**Lookback windows**: ensure ranges like `5m`or`15m` match your
  expected signal patterns and noise levels.

-**Thresholds and severities**: align warning/critical thresholds
  with your SLOs and paging policies.

Treat the shipped alerting as a baseline to copy and customize. For
production clusters, maintain your tuned rules in your own Git repo
and treat the DebVisor rules as upstream examples.
