# ArgoCD / Automation workflows\n\nThis directory contains Argo Workflows that tie

together

DebVisor\nmonitoring, alerting, and automation systems.\n\n##
`security-remediation-workflow.yaml`\n\nThe `security-remediation-flow`workflow implements
an
end-to-end\n"alert -> AWX playbook -> verification" pipeline with comprehensive\ntimeout
constraints, retry logic, audit logging, and dead-letter queue\nhandling for failed
remediations.\n\n### Architecture Overview\n\nThe workflow follows this flow:\n Alert from
Prometheus/Alertmanager\n v\n Webhook Receiver (timeout: 5 min, retry: 3x)\n v\n Parse
Alert &
Extract Context (timeout: 1 min)\n v\n Trigger AWX Playbook (timeout: 30 min, retry: 3x)\n
v\n
Verify Remediation via Metrics (timeout: 10 min, retry: 10x)\n v\n Log Audit Success\n v\n
[OR on
failure] -> Dead-Letter Queue -> Manual Intervention Required\n\n### How alerts flow into
the
workflow\n\n1.**Alert Reception**: Prometheus Alertmanager sends HTTP webhooks
to\n`debvisor-webhook-receiver.debvisor-monitoring.svc:8080/alert`.\n\n- Timeout: 5
minutes (allows
for webhook receiver recovery).\n\n- Retry: 3 attempts with 5s initial backoff,
exponential factor
2.\n\n1.**Context Extraction**: The `extract-context`template parses the\n alert JSON
and:\n\n-
Inspects`labels.alertname`to identify the alert type.\n\n- Maps alert types to AWX
playbook names
using a built-in mapping.\n\n- Extracts`annotations`as extra variables for the
playbook.\n\n-
Returns the alert name, playbook name, extra vars, and expected\n\n success metric.\n\n-
Timeout: 60
seconds.\n\n- Logs audit events with ISO timestamps.\n\n1.**Playbook Execution**:
The`awx-job-launcher`template calls AWX:\n\n- Posts to the AWX API endpoint with
authentication.\n\n- Passes dry-run flag if enabled.\n\n- Includes audit ID and timestamp
in extra
vars.\n\n- Timeout: 30 minutes (for long-running playbooks).\n\n- Retry: 3 attempts with
10s initial
backoff, exponential factor 2.\n\n1.**Verification**: The`check-metrics`template polls
Prometheus:\n\n- Queries for the expected success metric
(e.g.,\n\n`debvisor_mfacomplianceviolation_resolved`).\n\n- Succeeds only when the metric
evaluates
to `1`.\n\n- Timeout: 10 minutes.\n\n- Retry: 10 attempts with 30s initial backoff, factor
1.5.\n\n-
Logs each verification attempt with timestamp.\n\n1.**Audit Logging**: On success, the
`log-remediation-audit`template\n writes a JSON audit entry containing:\n\n- Timestamp
(UTC ISO
format).\n\n- Workflow ID and name.\n\n- Alert name and playbook name.\n\n- Status
(success/failed).\n\n- Namespace.\n\n### Failure Handling & Dead-Letter Queue\n\nIf any
step
fails:\n1.**Immediate Termination**: The workflow stops at the failed
step.\n1.**Dead-Letter
Queue**: A dedicated`dead-letter-queue`template\n sends the failure details to an alert
sink:\n\n-
URL:`{{workflow.parameters.alert-sink}}`(configurable).\n\n- Includes workflow name, error
message,
failed node details, and\n\n timestamp.\n\n- Retry: 2 attempts with 5s backoff.\n\n-
Timeout: 60
seconds.\n\n1.**Manual Intervention Alert**: The DLQ entry
flags\n`requires_manual_intervention:
true`, signaling operators that:\n\n- The playbook failed or did not complete
remediation.\n\n-
Metrics did not confirm success within the retry window.\n\n- Manual review and possible
manual
remediation may be needed.\n\n1.**Audit Failure**: A failure audit entry is always
logged,\n
documenting:\n\n- The workflow failure timestamp.\n\n- The failed workflow name and
node.\n\n-
Status marked as "failed" for compliance/audit purposes.\n\n### Expected AWX job
templates\n\nAWX
should expose job templates matching the playbook names returned by\n`extract-context`.
Alert-to-playbook mappings:\n| Alert Name | Playbook | Purpose |\n|---|---|---|\n|
`MFAComplianceViolation`|`enforce-mfa.yml`| Enforce SSH MFA compliance across targeted
nodes.
|\n|`HostCompromised`|`quarantine-host.yml`| Isolate a compromised or suspicious node.
|\n|`MaliciousIPDetected`|`block-ips.yml`| Add IPs to the DebVisor firewall blocklist.
|\n|`UnknownAlert`|`default-remediation.yml`| Safe no-op fallback for unrecognized alerts. |\nThe
exact mapping is encoded in the Python script inside the\n`extract-context`template. To
add new
alert types:\n\n1. Add a new entry to the`playbook_map`dictionary.\n\n1. Ensure the AWX
job template
with that name exists and is properly\n\n configured.\n\n1. Update monitoring/alerting to
produce
the new`alertname`label when\n\n the condition is detected.\n\n### Prometheus /
Alertmanager
integration\n\n#### Alert Requirements\n\nEach alert that should trigger automation
must:\n\n-
**Set`alertname`label**: Must match one of the keys in the\n\n`playbook_map`(or fall back
to`UnknownAlert`).\n\n- **Provide context in`annotations`**: Should include target
hostnames,\n\n IP
addresses, tenant IDs, or other data needed by the playbook:\n annotations:\n
remediation_target:
"host-03.cluster-a"\n threat_level: "critical"\n attack_vector: "ssh_brute_force"\n\n####
Alertmanager Configuration\n\nConfigure Alertmanager to route security/remediation alerts
to
the\nworkflow webhook:\n receivers:\n\n- name: 'debvisor-automation'\n\n
webhook_configs:\n\n- url:
'[http://debvisor-webhook-receiver.debvisor-monitoring.svc:8080/alert']([http://debvisor-webhook-receiver.debvisor-monitoring.svc:8080/alert]([http://debvisor-webhook-receiver.debvisor-monitoring.svc:8080/aler]([http://debvisor-webhook-receiver.debvisor-monitoring.svc:8080/ale]([http://debvisor-webhook-receiver.debvisor-monitoring.svc:8080/al]([http://debvisor-webhook-receiver.debvisor-monitoring.svc:8080/a]([http://debvisor-webhook-receiver.debvisor-monitoring.svc:8080/]([http://debvisor-webhook-receiver.debvisor-monitoring.svc:8080](http://debvisor-webhook-receiver.debvisor-monitoring.svc:8080)/)a)l)e)r)t)')\n\n
send*resolved: false\n route:\n receiver: 'default'\n routes:\n\n- match:\n\n alertname:
'MFAComplianceViolation|HostCompromised|MaliciousIPDetected'\n receiver:
'debvisor-automation'\n\n#### Success Metric Naming Convention\n\nThe workflow constructs
the
expected success metric as:\n debvisor*{alertname_lowercase}_resolved\nFor example:\n\n-
Alert
`MFAComplianceViolation`-> Metric`debvisor_mfacomplianceviolation_resolved`\n\n- Alert
`HostCompromised`-> Metric`debvisor_hostcompromised_resolved`\n\nAWX playbooks should emit
these
metrics (via Prometheus pushgateway or\nexporter) once remediation is confirmed. The
metric should
be set to\nvalue `1`to signal success.\nExample in a playbook:\n\n- name: Emit remediation
success
metric\n\n prometheus_metric:\n name: debvisor_hostcompromised_resolved\n value: 1\n job:
'debvisor-remediation'\n\n### Timeout and Retry Strategy\n\n| Step | Timeout | Retries |
Backoff |
Purpose |\n|---|---|---|---|---|\n|`webhook-receiver`| 5 min | 3x | 5s, factor 2 |
Tolerate
transient receiver failures. |\n|`extract-context`| 1 min | None | N/A | Fast validation;
fail fast
on malformed input. |\n|`awx-job-launcher`| 30 min | 3x | 10s, factor 2 | Allow playbook
execution
time; handle transient API errors. |\n|`check-metrics`| 10 min | 10x | 30s, factor 1.5 |
Poll for
metric confirmation; account for remediation propagation delay. |\n|`dead-letter-queue`| 1
min | 2x
| 5s, factor 2 | Ensure failure is recorded even if primary sink is degraded. |\n\n###
Parameterizing endpoints and tokens\n\nThe workflow accepts the following parameters
(overridable
per invocation):\n| Parameter | Default | Usage
|\n|---|---|---|\n|`awx-base-url`|[https://awx.debvisor.local]([https://awx.debvisor.loca]([https://awx.debvisor.loc]([https://awx.debvisor.lo]([https://awx.debvisor.l]([https://awx.debvisor.]([https://awx.debvisor]([https://awx.debviso](https://awx.debviso)r).)l)o)c)a)l)
| Base URL of the AWX API. |\n|
`prometheus-base-url`|[http://prometheus.debvisor-monitoring.svc:9090]([http://prometheus.debvisor-monitoring.svc:909]([http://prometheus.debvisor-monitoring.svc:90]([http://prometheus.debvisor-monitoring.svc:9]([http://prometheus.debvisor-monitoring.svc:]([http://prometheus.debvisor-monitoring.svc]([http://prometheus.debvisor-monitoring.sv]([http://prometheus.debvisor-monitoring.s](http://prometheus.debvisor-monitoring.s)v)c):)9)0)9)0)
| Base URL of the Prometheus API. |\n| `awx-token`| (empty) | Bearer token for AWX authentication
(required). |\n|`dry-run`|`"false"`| Set to`"true"`to test playbooks without executing.
|\n|`alert-sink`|[http://alert-sink.debvisor-monitoring.svc:8080/failed]([http://alert-sink.debvisor-monitoring.svc:8080/faile]([http://alert-sink.debvisor-monitoring.svc:8080/fail]([http://alert-sink.debvisor-monitoring.svc:8080/fai]([http://alert-sink.debvisor-monitoring.svc:8080/fa]([http://alert-sink.debvisor-monitoring.svc:8080/f]([http://alert-sink.debvisor-monitoring.svc:8080/]([http://alert-sink.debvisor-monitoring.svc:8080](http://alert-sink.debvisor-monitoring.svc:8080)/)f)a)i)l)e)d)
| Endpoint for dead-letter queue (failed remediations). |\nThese can be overridden:\n\n- **Per
workflow invocation**: Pass as arguments when launching.\n\n- **Via WorkflowTemplate**:
Define
defaults in a reusable template.\n\n- **Via ConfigMap**: Reference a ConfigMap for
environment-specific values\n\n (lab, staging, production).\nExample via Argo Workflows
CLI:\n argo
submit -f security-remediation-workflow.yaml \\n\n - p
awx-base-url=[https://awx.prod.example.com]([https://awx.prod.example.co]([https://awx.prod.example.c]([https://awx.prod.example.]([https://awx.prod.example]([https://awx.prod.exampl]([https://awx.prod.examp]([https://awx.prod.exam](https://awx.prod.exam)p)l)e).)c)o)m)
\\n\n - p awx-token=$AWX_TOKEN \\n\n - p dry-run=false\n\n### Dry-run / Simulation
mode\n\nFor
safely testing new alert routes or playbook mappings:\n\n1. Set the `dry-run`parameter
to`"true"`when launching.\n\n1. The workflow will:\n\n- Parse the alert and select a
playbook +
extra vars normally.\n\n- Pass`dry*run: true`to AWX (playbook logs actions but doesn't
execute).\n\n- Still validate alert JSON and signal errors for malformed payloads.\n\n-
Still emit
audit logs (marked as dry-run in the audit context).\n\nThis allows debugging new alert
configurations without impacting live\nsystems.\n\n### ServiceAccount & RBAC\n\nThe
workflow runs as
the`debvisor-automation`ServiceAccount in the\n`argocd-debvisor`namespace. This account
should be
restricted to:\n\n- Creating and monitoring Argo Workflows in its own namespace.\n\n-
Network access
to internal AWX and Prometheus endpoints.\n\n- Reading Secrets containing AWX
tokens.\n\nExample
RBAC role:\n apiVersion: rbac.authorization.k8s.io/v1\n kind: Role\n metadata:\n name:
debvisor-automation\n namespace: argocd-debvisor\n rules:\n\n- apiGroups:
['argoproj.io']\n\n
resources: ['workflows']\n verbs: ['get', 'list', 'watch', 'create', 'update',
'patch']\n\n-
apiGroups: ['']\n\n resources: ['secrets']\n resourceNames: ['awx-token']\n verbs:
['get']\n\n###
Troubleshooting\n\n#### Alert not triggering the workflow\n\n1. Check Alertmanager
routing:\n\n-
Verify alert matches the route to`debvisor-automation`receiver.\n\n- Check Alertmanager
logs for
webhook delivery errors.\n\n1. Check webhook receiver:\n\n- Verify DNS
resolution:`nslookup
debvisor-webhook-receiver.debvisor-monitoring.svc`\n\n- Check receiver pod logs for HTTP
errors.\n\n1. Check workflow logs:\n\n-`argo logs`to see step-by-step execution.\n\n####
Playbook
fails to execute\n\n1. Check AWX configuration:\n\n- Verify job template exists with the
expected
name.\n\n- Check AWX logs for authentication or template errors.\n\n- Verify extra vars
are valid
JSON.\n\n1. Increase timeouts if playbook execution is slow:\n\n-
Update`awx-job-launcher``timeoutSeconds`value.\n\n#### Remediation not verified (metric
check
fails)\n\n1. Verify success metric is emitted:\n\n- Check Prometheus for the
metric:`debvisor**_resolved`.\n\n- Verify metric value is`1`when remediation
completes.\n\n1. Adjust
retry/backoff if metric takes time to appear:\n\n- Increase`check-metrics`retry
count.\n\n- Increase
backoff duration if propagation is slow.\n\n1. Check playbook output:\n\n- Verify AWX
playbook emits
the metric (via pushgateway or exporter).\n\n#### Manual intervention alert received\n\n1.
Review
the DLQ entry for error details.\n\n1. Check failed workflow logs:`argo logs`\n\n1.
Investigate the
root cause (network, AWX, metrics, playbook logic).\n\n1. Optionally re-run the workflow
once the
issue is resolved.\n\n### Auditing and Compliance\n\nAll remediation actions are logged to
standard
output/logs. Each audit\nentry includes:\n\n- Timestamp (UTC ISO format).\n\n- Workflow ID
and
name.\n\n- Alert name and associated playbook.\n\n- Remediation status
(success/failed).\n\n-
Namespace.\n\nOperators should integrate these logs with their centralized logging\nsystem
(e.g.,
ELK, Splunk) for compliance reporting and forensic\nanalysis.\nExample integration with
sidecar
logging agent:\n containers:\n\n- name: workflow\n\n image:
argoproj/workflow-controller:latest\n\n-
name: log-forwarder\n\n image: fluent-bit:latest\n volumeMounts:\n\n- name:
shared-logs\n\n
mountPath: /logs\nThis enables centralized aggregation of audit trails for security
and\ncompliance
audits.\n\n
