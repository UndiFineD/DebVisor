# Security Policy

## Supported Versions

We support security updates on the `main` branch and the latest minor release.

## Reporting a Vulnerability

- Email: security@debvisor.com
- Provide steps to reproduce, impact assessment, and affected versions.
- We will acknowledge within 48 hours and provide a remediation timeline within 7 days.

## Disclosure Policy

- Responsible disclosure only.
- Do not publicly disclose until a fix is available.

## Security Practices

- SBOM generated via CycloneDX and attached to releases.
- CI runs SAST (Bandit, Semgrep) and dependency audits.
- Secrets scanning enabled; contributions must pass pre-commit hooks.
