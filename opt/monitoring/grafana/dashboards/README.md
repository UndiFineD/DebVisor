# DebVisor Grafana dashboards

This directory contains Grafana dashboards that are intended to be used with the DebVisor monitoring stack.

## Dashboards

- JSON dashboards under `grafana/dashboards/` cover areas such as security posture, MFA/compliance, DNS/DHCP, and multi-tenant isolation.

- A subset of these dashboards are**scaffolding**or early drafts and may need further tuning before use in production.

## Provisioning

In a full deployment, dashboards and alert rules are typically provisioned via:

- Kubernetes manifests in `monitoring/grafana/` (dashboards and provisioning files).

- The Grafana provisioning configuration in `monitoring/grafana/provisioning/dashboards/dashboards.yml`and`monitoring/grafana/provisioning/alerting/alerts.yml`.

If you add or rename dashboards here, ensure the provisioning configuration and any CI checks are updated to match.

## Next steps

Over time this directory should document:

- Which dashboards are considered production-ready vs experimental.

- How to contribute new panels and follow DebVisor's conventions for labels and alert names.

- How these dashboards tie into the broader security and multi-tenant monitoring story.
