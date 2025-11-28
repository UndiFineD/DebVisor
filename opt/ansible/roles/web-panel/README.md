# `web-panel` role

Purpose:

- Placeholder role for the future DebVisor web UI ("web panel").
- Creates a marker directory on nodes where the web panel addon is

  conceptually enabled.

Status:

- Stub / non-operational.
- Does__not__deploy Flask, gunicorn, nginx, or any systemd units.

  The real web panel implementation will live under `services/web-panel`
  and be integrated later.

Key variables:

- None at present. Future versions of this role are expected to

  consume variables for bind addresses, TLS certificates, and
  authentication settings.

Control paths:

- Until the web panel is implemented, management of DebVisor nodes

  is done via Cockpit, CLI tools, and Ansible playbooks documented
  under `docs/`.
