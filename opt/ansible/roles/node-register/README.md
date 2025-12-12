# Node Register Role (Stub)

This role is a non-operational stub kept in sync with DebVisor's real control paths for node registration. Hostname/DNS registration is handled by built-in services on the DebVisor image (e.g., `hostname-register.service`). Future RPC/web-panel workflows or AWX job templates may coordinate registration.

- Purpose: Document intended integration points without performing system changes.

- Current behavior: No changes are applied; built-in services manage registration.

- Future integration: RPC/web workflows, AWX templates.
