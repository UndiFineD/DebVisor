

file_path = 'improvements.md'

blocks_to_remove = [
    """### Documentation

**DOC-002**: Create troubleshooting runbooks

- Location: New `docs/runbooks/`
- Common failure scenarios
- Step-by-step resolution procedures
- Escalation paths

**DOC-003**: Add architecture decision records (ADRs)

- Location: New `docs/adr/`
- Document key technical decisions
- Rationale and tradeoffs
- Alternative approaches considered

**DOC-004**: Create deployment playbooks

- Location: `docs/deployment/`
- Production deployment checklist
- Rollback procedures
- Health check validation""",

    """**DOC-002**: Create troubleshooting runbooks

- Location: New `docs/runbooks/`
- Common failure scenarios
- Step-by-step resolution procedures
- Escalation paths""",

    """**DOC-003**: Add architecture decision records (ADRs)

- Location: New `docs/adr/`
- Document key technical decisions
- Rationale and tradeoffs
- Alternative approaches considered""",

    """**DOC-004**: Create deployment playbooks

- Location: `docs/deployment/`
- Production deployment checklist
- Rollback procedures
- Health check validation""",

    """**FEAT-001**: Implement WebSocket real-time updates

- Location: `opt/web/panel/socketio_server.py` (enhance NotImplementedError)
- Real-time VM status updates
- Live metrics streaming
- Chat/notification system"""
]

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

for block in blocks_to_remove:
    content = content.replace(block, "")

# Clean up double empty lines
while "\n\n\n" in content:
    content = content.replace("\n\n\n", "\n\n")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleanup complete.")
