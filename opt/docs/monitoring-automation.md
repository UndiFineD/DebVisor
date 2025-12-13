# DebVisor Monitoring & Automation Components\n\nThis directory contains Grafana

dashboards,

Prometheus exporters, and automation workflows for DebVisor cluster
operations.\n\n##
Grafana
Dashboards\n\n- **dns-dhcp-overview.json**: Real-time DNS/DHCP monitoring with
TSIG
rotation
tracking\n\n- **multi-tenant-isolation.json**: Per-tenant zone health with
cross-lease
leak
detection\n\n- **compliance-mfa-audit.json**: MFA enforcement status and audit
trail
visualization\n\n## Kubernetes Manifests\n\nThese manifests are**test fixtures
only**.
They are
intended to\nexercise dashboards and alerting paths in a lab or staging cluster
and\nshould not be
enabled by default in production.\nThe synthetic metrics job is**optional**and
intended
primarily
for\nlab/staging clusters. Both the CronJob and ConfigMaps are labeled
with\n`debvisor.io/test-fixture: "true"`so they can be discovered and\nfiltered
easily.\nEndpoints
such as DNS servers and the Prometheus Pushgateway are\nparameterized via
the`synthetic-metrics-config`ConfigMap. To\ncustomize them for a given cluster,
edit the
values in
that ConfigMap\nbefore applying, for example:\n apiVersion: v1\n kind:
ConfigMap\n
metadata:\n name:
synthetic-metrics-config\n namespace: debvisor-monitoring\n data:\n
PROMETHEUS_PUSHGATEWAY:
"[http://prometheus-pushgateway.debvisor-monitoring.svc:9091"]([http://prometheus-pushgateway.debvisor-monitoring.svc:9091]([http://prometheus-pushgateway.debvisor-monitoring.svc:909]([http://prometheus-pushgateway.debvisor-monitoring.svc:90]([http://prometheus-pushgateway.debvisor-monitoring.svc:9]([http://prometheus-pushgateway.debvisor-monitoring.svc:]([http://prometheus-pushgateway.debvisor-monitoring.svc]([http://prometheus-pushgateway.debvisor-monitoring.sv]([http://prometheus-pushgateway.debvisor-monitoring.s]([http://prometheus-pushgateway.debvisor-monitoring.]([http://prometheus-pushgateway.debvisor-monitoring]([http://prometheus-pushgateway.debvisor-monitorin]([http://prometheus-pushgateway.debvisor-monitori]([http://prometheus-pushgateway.debvisor-monitor]([http://prometheus-pushgateway.debvisor-monito]([http://prometheus-pushgateway.debvisor-monit]([http://prometheus-pushgateway.debvisor-moni]([http://prometheus-pushgateway.debvisor-mon]([http://prometheus-pushgateway.debvisor-mo]([http://prometheus-pushgateway.debvisor-m]([http://prometheus-pushgateway.debvisor-]([http://prometheus-pushgateway.debvisor]([http://prometheus-pushgateway.debviso]([http://prometheus-pushgateway.debvis]([http://prometheus-pushgateway.debvi]([http://prometheus-pushgateway.debv]([http://prometheus-pushgateway.deb]([http://prometheus-pushgateway.de]([http://prometheus-pushgateway.d]([http://prometheus-pushgateway.]([http://prometheus-pushgateway]([http://prometheus-pushgatewa]([http://prometheus-pushgatew]([http://prometheus-pushgate]([http://prometheus-pushgat]([http://prometheus-pushga]([http://prometheus-pushg]([http://prometheus-push]([http://prometheus-pus]([http://prometheus-pu]([http://prometheus-p]([http://prometheus-]([http://prometheus](http://prometheus)-)p)u)s)h)g)a)t)e)w)a)y).)d)e)b)v)i)s)o)r)-)m)o)n)i)t)o)r)i)n)g).)s)v)c):)9)0)9)1)")\n
DNS_SERVER: "10.10.0.1"\n BIND_EXPORTER:
"[http://10.10.0.1:9119"]([http://10.10.0.1:9119]([http://10.10.0.1:911]([http://10.10.0.1:91]([http://10.10.0.1:9]([http://10.10.0.1:]([http://10.10.0.1]([http://10.10.0.]([http://10.10.0]([http://10.10.]([http://10.10]([http://10.1]([http://10.]([http://10]([http://1](http://1)0).)1)0).)0).)1):)9)1)1)9)")\nTo
deploy the fixtures in a cluster:\n kubectl apply -f
monitoring/grafana/manifests/synthetic-metrics-configmap.yaml\n kubectl apply -f
monitoring/grafana/manifests/synthetic-metrics-cronjob.yaml\nTo remove them
again:\n
kubectl delete
-f monitoring/grafana/manifests/synthetic-metrics-cronjob.yaml\n kubectl delete
-f
monitoring/grafana/manifests/synthetic-metrics-configmap.yaml\n\n- Both
resources are
labeled
with`debvisor.io/test-fixture: "true"`so\n\n that they can be discovered and
filtered
easily.\n\n-
The CronJob runs with conservative CPU/memory limits and a non-root\n\n security
context.\n\n##
Ansible Playbooks\n\nLocated in`../ansible/playbooks/`:\n\n-
**enforce-mfa.yml**: Install
Google
Authenticator PAM module, configure SSH for MFA\n\n- **quarantine-host.yml**:
Isolate
compromised
node with nftables, disable VM autostart, tag in DNS/Prometheus\n\n-
**block-ips.yml**:
Add
malicious IPs to nftables blocklist set, log to audit trail\n\n## ArgoCD
Workflows\n\nLocated in
`../argocd/`:\n\n- **security-remediation-workflow.yaml**: Alert -> Webhook ->
AWX ->
Playbook ->
Verification flow\n\n## CI/CD Validation\n\nLocated in
`../.github/workflows/`:\n\n-
**validate-dashboards.yml**: GitHub Actions workflow to validate JSON schema and
test
Grafana
imports\n\n## Usage\n\n### Import Dashboards\n\n for dashboard in
grafana/dashboards/*.json; do\n
curl -X POST
[http://admin:admin@grafana.debvisor.local/api/dashboards/db]([http://admin:admin@grafana.debvisor.local/api/dashboards/d]([http://admin:admin@grafana.debvisor.local/api/dashboards/]([http://admin:admin@grafana.debvisor.local/api/dashboards]([http://admin:admin@grafana.debvisor.local/api/dashboard]([http://admin:admin@grafana.debvisor.local/api/dashboar]([http://admin:admin@grafana.debvisor.local/api/dashboa]([http://admin:admin@grafana.debvisor.local/api/dashbo]([http://admin:admin@grafana.debvisor.local/api/dashb]([http://admin:admin@grafana.debvisor.local/api/dash]([http://admin:admin@grafana.debvisor.local/api/das]([http://admin:admin@grafana.debvisor.local/api/da]([http://admin:admin@grafana.debvisor.local/api/d]([http://admin:admin@grafana.debvisor.local/api/]([http://admin:admin@grafana.debvisor.local/api]([http://admin:admin@grafana.debvisor.local/ap]([http://admin:admin@grafana.debvisor.local/a]([http://admin:admin@grafana.debvisor.local/]([http://admin:admin@grafana.debvisor.local]([http://admin:admin@grafana.debvisor.loca]([http://admin:admin@grafana.debvisor.loc]([http://admin:admin@grafana.debvisor.lo]([http://admin:admin@grafana.debvisor.l]([http://admin:admin@grafana.debvisor.]([http://admin:admin@grafana.debvisor]([http://admin:admin@grafana.debviso]([http://admin:admin@grafana.debvis]([http://admin:admin@grafana.debvi]([http://admin:admin@grafana.debv]([http://admin:admin@grafana.deb]([http://admin:admin@grafana.de]([http://admin:admin@grafana.d]([http://admin:admin@grafana.]([http://admin:admin@grafana]([http://admin:admin@grafan]([http://admin:admin@grafa]([http://admin:admin@graf]([http://admin:admin@gra]([http://admin:admin@gr]([http://admin:admin@g]([http://admin:admin@]([http://admin:admin]([http://admin:admi](http://admin:admi)n)@)g)r)a)f)a)n)a).)d)e)b)v)i)s)o)r).)l)o)c)a)l)/)a)p)i)/)d)a)s)h)b)o)a)r)d)s)/)d)b)
\\n\n - H "Content-Type: application/json" \\n\n - d @"$dashboard"\n\n
done\n\n### Deploy
Kubernetes
Resources\n\n kubectl apply -f
monitoring/grafana/manifests/synthetic-metrics-cronjob.yaml\n kubectl
apply -f monitoring/grafana/manifests/synthetic-metrics-configmap.yaml\nTo
remove the
fixtures
again:\n kubectl delete -f
monitoring/grafana/manifests/synthetic-metrics-cronjob.yaml\n
kubectl
delete -f monitoring/grafana/manifests/synthetic-metrics-configmap.yaml\n\n###
Trigger
Ansible
Playbook\n\n ansible-playbook -i inventory ansible/playbooks/enforce-mfa.yml\n
ansible-playbook -i
inventory -e "target_host=node3" ansible/playbooks/quarantine-host.yml\n
ansible-playbook
-i
inventory -e "blocked_ips=1.2.3.4,5.6.7.8" ansible/playbooks/block-ips.yml\n\n##
Metrics
Exposed\n\n- `bind_queries_total`: Total DNS queries by type\n\n-
`bind_updates_total`:
Dynamic DNS
update count\n\n- `dnsmasq_leases_active`: Current DHCP lease count\n\n-
`tsig_rotation_last_timestamp`: Last TSIG key rotation timestamp\n\n-
`debvisor_node_mfa_enabled`:
MFA enforcement status (0/1)\n\n- `debvisor_auth_failures_total`: Failed
authentication
attempts\n\n- `debvisor_blocked_ips`: Count of IPs in nftables blocklist\n\nIn
addition,
the
`ceph-health.timer`/`ceph-health.service`pair runs a\nperiodic`ceph -s`check and
logs the
outcome
with the\n`ceph-health` Syslog identifier. These logs can be scraped via
your\npreferred
log
pipeline (for example journald -> Loki) and visualised or\nalerted on in
Grafana, for
example by
counting recent non-HEALTH\noK\nevents.\n\n## Alerting and ownership\n\nAlert
rules
under`monitoring/grafana/provisioning/alerting/`are\nintended as a starting
point rather
than a
finished SRE playbook.\n\n- Some rules are**starter alerts**whose main goal is
to prove
that\n\n
metrics wiring and notification channels work (for example basic\n node
CPU/memory, simple
DNS/DHCP
health checks).\n\n- Others are closer to**near-production**defaults for core
DebVisor\n\n
services
(Ceph/ZFS health, DNS HA, TSIG rotation, control-plane\n reachability) but still
expect
site-specific tuning.\nWhen adopting these rules in a real environment, review
and
adjust:\n\n-
**Scrape intervals and evaluation frequency**: higher-frequency\n\n
scraping/evaluation
yields
faster detection but more load.\n\n- **Lookback windows**: ensure ranges
like`5m`or`15m`
match
your\n\n expected signal patterns and noise levels.\n\n- **Thresholds and
severities**:
align
warning/critical thresholds\n\n with your SLOs and paging policies.\nTreat the
shipped
alerting as a
baseline to copy and customize. For\nproduction clusters, maintain your tuned
rules in
your own Git
repo\nand treat the DebVisor rules as upstream examples.\n\n
