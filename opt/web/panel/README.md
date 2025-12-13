# DebVisor web panel (prototype)\n\nThis directory contains a small Flask-based web application that

serves as a**placeholder panel**for DebVisor.\n\n## Purpose\n\n- Demonstrate how a web UI could
interact with the DebVisor RPC service.\n\n- Experiment with basic workflows such as listing nodes,
tenants, or workloads.\n\n- Provide a place to iterate on UX before committing to a production-ready
panel.\n\nThe current app is**not production-ready**:\n\n- Authentication, authorization, and
multi-tenant isolation are incomplete.\n\n- Error handling, logging, and auditability are
minimal.\n\n- Hardening (TLS, headers, CSRF, session management) has not been completed.\n\n##
Relation to the RPC service\n\nIn the long term, this panel is intended to proxy and visualize data
from the `debvisor.v1`RPC API:\n\n- The panel should not shell out directly to hypervisor
tools.\n\n- All state-changing operations should flow through the RPC service.\n\n## Deployment
notes\n\n- The app is intended to run close to the DebVisor RPC service,\n\n typically on the
hypervisor itself as a systemd service that talks\n to`debvisor-rpcd`on`127.0.0.1:7443`.\n\n-
`requirements.txt`describes the Python dependencies; a common\n\n pattern is to create a dedicated
virtual environment (for example\n under`/var/lib/debvisor-panel/venv`) and install the
requirements\n there.\n\n- Packagers and image build scripts can use the\n\n
`systemd/debvisor-panel.service.example` unit as a starting point\n for wiring the panel into the
base image.\nDo not expose this prototype directly on the Internet without additional hardening.\n\n
