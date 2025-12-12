# Policy (Conftest / OPA)

This folder provides starter Rego policies for Kubernetes manifests validated by Conftest in CI.

Policies focus on common reliability and security checks:

- Disallow images with the `latest` tag.
- Require CPU and memory resource requests/limits on containers.

Place additional rules under `policy/k8s/` and they will be picked up by the combined validator workflow.

References:

- Conftest: <<<<<<<<<<<<<<<<<<<<<<<<<<https://www.conftest.dev/>>>>>>>>>>>>>>>>>>>>>>>>>>
- OPA/Rego: <<<<<<<<<<<<<<<<<<<<<<<<<<https://www.openpolicyagent.org/docs/latest/policy-language/>>>>>>>>>>>>>>>>>>>>>>>>>>
