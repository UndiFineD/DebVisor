# MFA Role (Stub)

This role is a non-operational stub kept in sync with DebVisor's real control paths for MFA enforcement. Use `ansible/playbooks/enforce-mfa.yml` and eventual RPC/web-panel workflows or AWX job templates for actual enforcement.

- Purpose: Document intended integration points without performing system changes.
- Future integration: System policy tasks, RPC/web workflows, AWX templates.
- Note: This role intentionally does not modify PAM/sshd or fetch packages.
