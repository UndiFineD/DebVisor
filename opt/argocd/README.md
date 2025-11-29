# ArgoCD / Automation workflows

This directory contains Argo Workflows that tie together DebVisor
monitoring, alerting, and automation systems.

## `security-remediation-workflow.yaml`

The `security-remediation-flow` workflow implements an end-to-end
"alert -> AWX playbook -> verification" pipeline with comprehensive
timeout constraints, retry logic, audit logging, and dead-letter queue
handling for failed remediations.

### Architecture Overview

The workflow follows this flow:

    Alert from Prometheus/Alertmanager
        v
    Webhook Receiver (timeout: 5 min, retry: 3x)
        v
    Parse Alert & Extract Context (timeout: 1 min)
        v
    Trigger AWX Playbook (timeout: 30 min, retry: 3x)
        v
    Verify Remediation via Metrics (timeout: 10 min, retry: 10x)
        v
    Log Audit Success
        v
    [OR on failure] -> Dead-Letter Queue -> Manual Intervention Required

### How alerts flow into the workflow

1.__Alert Reception__: Prometheus Alertmanager sends HTTP webhooks to
   `debvisor-webhook-receiver.debvisor-monitoring.svc:8080/alert`.

- Timeout: 5 minutes (allows for webhook receiver recovery).
- Retry: 3 attempts with 5s initial backoff, exponential factor 2.

1.__Context Extraction__: The `extract-context` template parses the
   alert JSON and:

- Inspects `labels.alertname` to identify the alert type.
- Maps alert types to AWX playbook names using a built-in mapping.
- Extracts `annotations` as extra variables for the playbook.
- Returns the alert name, playbook name, extra vars, and expected

     success metric.

- Timeout: 60 seconds.
- Logs audit events with ISO timestamps.

1.__Playbook Execution__: The `awx-job-launcher` template calls AWX:

- Posts to the AWX API endpoint with authentication.
- Passes dry-run flag if enabled.
- Includes audit ID and timestamp in extra vars.
- Timeout: 30 minutes (for long-running playbooks).
- Retry: 3 attempts with 10s initial backoff, exponential factor 2.

1.__Verification__: The `check-metrics` template polls Prometheus:

- Queries for the expected success metric (e.g.,

     `debvisor_mfacomplianceviolation_resolved`).

- Succeeds only when the metric evaluates to `1`.
- Timeout: 10 minutes.
- Retry: 10 attempts with 30s initial backoff, factor 1.5.
- Logs each verification attempt with timestamp.

1.__Audit Logging__: On success, the `log-remediation-audit` template
   writes a JSON audit entry containing:

- Timestamp (UTC ISO format).
- Workflow ID and name.
- Alert name and playbook name.
- Status (success/failed).
- Namespace.

### Failure Handling & Dead-Letter Queue

If any step fails:

1.__Immediate Termination__: The workflow stops at the failed step.

1.__Dead-Letter Queue__: A dedicated `dead-letter-queue` template
   sends the failure details to an alert sink:

- URL: `{{workflow.parameters.alert-sink}}` (configurable).
- Includes workflow name, error message, failed node details, and

     timestamp.

- Retry: 2 attempts with 5s backoff.
- Timeout: 60 seconds.

1.__Manual Intervention Alert__: The DLQ entry flags
   `requires_manual_intervention: true`, signaling operators that:

- The playbook failed or did not complete remediation.
- Metrics did not confirm success within the retry window.
- Manual review and possible manual remediation may be needed.

1.__Audit Failure__: A failure audit entry is always logged,
   documenting:

- The workflow failure timestamp.
- The failed workflow name and node.
- Status marked as "failed" for compliance/audit purposes.

### Expected AWX job templates

AWX should expose job templates matching the playbook names returned by
`extract-context`. Alert-to-playbook mappings:

| Alert Name | Playbook | Purpose |
|---|---|---|
| `MFAComplianceViolation`|`enforce-mfa.yml` | Enforce SSH MFA compliance across targeted nodes. |
| `HostCompromised`|`quarantine-host.yml` | Isolate a compromised or suspicious node. |
| `MaliciousIPDetected`|`block-ips.yml` | Add IPs to the DebVisor firewall blocklist. |
| `UnknownAlert`|`default-remediation.yml` | Safe no-op fallback for unrecognized alerts. |

The exact mapping is encoded in the Python script inside the
`extract-context` template. To add new alert types:

1. Add a new entry to the `playbook_map` dictionary.
1. Ensure the AWX job template with that name exists and is properly

   configured.

1. Update monitoring/alerting to produce the new `alertname` label when

   the condition is detected.

### Prometheus / Alertmanager integration

#### Alert Requirements

Each alert that should trigger automation must:

-__Set `alertname` label__: Must match one of the keys in the
  `playbook_map`(or fall back to`UnknownAlert`).

-__Provide context in `annotations`__: Should include target hostnames,
  IP addresses, tenant IDs, or other data needed by the playbook:

    annotations:
      remediation_target: "host-03.cluster-a"
      threat_level: "critical"
      attack_vector: "ssh_brute_force"

#### Alertmanager Configuration

Configure Alertmanager to route security/remediation alerts to the
workflow webhook:

    receivers:

- name: 'debvisor-automation'

      webhook_configs:

- url: '[http://debvisor-webhook-receiver.debvisor-monitoring.svc:8080/alert'](http://debvisor-webhook-receiver.debvisor-monitoring.svc:8080/alert')

        send_resolved: false

    route:
      receiver: 'default'
      routes:

- match:

          alertname: 'MFAComplianceViolation|HostCompromised|MaliciousIPDetected'
        receiver: 'debvisor-automation'

#### Success Metric Naming Convention

The workflow constructs the expected success metric as:

    debvisor_{alertname_lowercase}_resolved

For example:

- Alert `MFAComplianceViolation`-> Metric`debvisor_mfacomplianceviolation_resolved`
- Alert `HostCompromised`-> Metric`debvisor_hostcompromised_resolved`

AWX playbooks should emit these metrics (via Prometheus pushgateway or
exporter) once remediation is confirmed. The metric should be set to
value `1` to signal success.

Example in a playbook:

- name: Emit remediation success metric

      prometheus_metric:
        name: debvisor_hostcompromised_resolved
        value: 1
        job: 'debvisor-remediation'

### Timeout and Retry Strategy

| Step | Timeout | Retries | Backoff | Purpose |
|---|---|---|---|---|
| `webhook-receiver` | 5 min | 3x | 5s, factor 2 | Tolerate transient receiver failures. |
| `extract-context` | 1 min | None | N/A | Fast validation; fail fast on malformed input. |
| `awx-job-launcher` | 30 min | 3x | 10s, factor 2 | Allow playbook execution time; handle transient API errors. |
| `check-metrics` | 10 min | 10x | 30s, factor 1.5 | Poll for metric confirmation; account for remediation propagation delay. |
| `dead-letter-queue` | 1 min | 2x | 5s, factor 2 | Ensure failure is recorded even if primary sink is degraded. |

### Parameterizing endpoints and tokens

The workflow accepts the following parameters (overridable per invocation):

| Parameter | Default | Usage |
|---|---|---|
| `awx-base-url`|[https://awx.debvisor.local](https://awx.debvisor.local) | Base URL of the AWX API. |
| `prometheus-base-url`|[http://prometheus.debvisor-monitoring.svc:9090](http://prometheus.debvisor-monitoring.svc:9090) | Base URL of the Prometheus API. |
| `awx-token` | (empty) | Bearer token for AWX authentication (required). |
| `dry-run`|`"false"`| Set to`"true"` to test playbooks without executing. |
| `alert-sink`|[http://alert-sink.debvisor-monitoring.svc:8080/failed](http://alert-sink.debvisor-monitoring.svc:8080/failed) | Endpoint for dead-letter queue (failed remediations). |

These can be overridden:

-__Per workflow invocation__: Pass as arguments when launching.
-__Via WorkflowTemplate__: Define defaults in a reusable template.
-__Via ConfigMap__: Reference a ConfigMap for environment-specific values
  (lab, staging, production).

Example via Argo Workflows CLI:

    argo submit -f security-remediation-workflow.yaml \
      -p awx-base-url=[https://awx.prod.example.com](https://awx.prod.example.com) \
      -p awx-token=$AWX_TOKEN \
      -p dry-run=false

### Dry-run / Simulation mode

For safely testing new alert routes or playbook mappings:

1. Set the `dry-run`parameter to`"true"` when launching.
1. The workflow will:

- Parse the alert and select a playbook + extra vars normally.
- Pass `dry_run: true` to AWX (playbook logs actions but doesn't execute).
- Still validate alert JSON and signal errors for malformed payloads.
- Still emit audit logs (marked as dry-run in the audit context).

This allows debugging new alert configurations without impacting live
systems.

### ServiceAccount & RBAC

The workflow runs as the `debvisor-automation` ServiceAccount in the
`argocd-debvisor` namespace. This account should be restricted to:

- Creating and monitoring Argo Workflows in its own namespace.
- Network access to internal AWX and Prometheus endpoints.
- Reading Secrets containing AWX tokens.

Example RBAC role:

    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: debvisor-automation
      namespace: argocd-debvisor
    rules:

- apiGroups: ['argoproj.io']

      resources: ['workflows']
      verbs: ['get', 'list', 'watch', 'create', 'update', 'patch']

- apiGroups: ['']

      resources: ['secrets']
      resourceNames: ['awx-token']
      verbs: ['get']

### Troubleshooting

#### Alert not triggering the workflow

1. Check Alertmanager routing:

- Verify alert matches the route to `debvisor-automation` receiver.
- Check Alertmanager logs for webhook delivery errors.

1. Check webhook receiver:

- Verify DNS resolution: `nslookup debvisor-webhook-receiver.debvisor-monitoring.svc`
- Check receiver pod logs for HTTP errors.

1. Check workflow logs:

- `argo logs` to see step-by-step execution.

#### Playbook fails to execute

1. Check AWX configuration:

- Verify job template exists with the expected name.
- Check AWX logs for authentication or template errors.
- Verify extra vars are valid JSON.

1. Increase timeouts if playbook execution is slow:

- Update `awx-job-launcher` `timeoutSeconds` value.

#### Remediation not verified (metric check fails)

1. Verify success metric is emitted:

- Check Prometheus for the metric: `debvisor_*_resolved`.
- Verify metric value is `1` when remediation completes.

1. Adjust retry/backoff if metric takes time to appear:

- Increase `check-metrics` retry count.
- Increase backoff duration if propagation is slow.

1. Check playbook output:

- Verify AWX playbook emits the metric (via pushgateway or exporter).

#### Manual intervention alert received

1. Review the DLQ entry for error details.
1. Check failed workflow logs: `argo logs`
1. Investigate the root cause (network, AWX, metrics, playbook logic).
1. Optionally re-run the workflow once the issue is resolved.

### Auditing and Compliance

All remediation actions are logged to standard output/logs. Each audit
entry includes:

- Timestamp (UTC ISO format).
- Workflow ID and name.
- Alert name and associated playbook.
- Remediation status (success/failed).
- Namespace.

Operators should integrate these logs with their centralized logging
system (e.g., ELK, Splunk) for compliance reporting and forensic
analysis.

Example integration with sidecar logging agent:

    containers:

- name: workflow

      image: argoproj/workflow-controller:latest

- name: log-forwarder

      image: fluent-bit:latest
      volumeMounts:

- name: shared-logs

        mountPath: /logs

This enables centralized aggregation of audit trails for security and
compliance audits.
