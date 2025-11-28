#!/bin/bash
# TSIG Key Generation Helper for DebVisor Bind9 Integration

set -euo pipefail

TSIG_CONF="/etc/bind/tsig-debvisor.conf"
NSUPDATE_KEY="/etc/debvisor/nsupdate.key"

# Generate TSIG secret using dnssec-keygen
TEMP_KEY=$(dnssec-keygen -a HMAC-SHA256 -b 256 -n HOST debvisor-update)
SECRET=$(grep "^Key:" "${TEMP_KEY}.private" | awk '{print $2}')

# Write Bind9 include file
cat > "${TSIG_CONF}" <<EOF
# DebVisor Bind9 TSIG Key Configuration
# Auto-generated: $(date -Iseconds)

key "debvisor-update" {
    algorithm hmac-sha256;
    secret "${SECRET}";
};
EOF

chmod 640 "${TSIG_CONF}"
chown root:bind "${TSIG_CONF}"

# Write client nsupdate key file
mkdir -p /etc/debvisor
cat > "${NSUPDATE_KEY}" <<EOF
key debvisor-update {
    algorithm hmac-sha256;
    secret "${SECRET}";
};
EOF

chmod 600 "${NSUPDATE_KEY}"

# Cleanup temporary files
rm -f "${TEMP_KEY}.key" "${TEMP_KEY}.private"

echo "TSIG key generated successfully:"
echo "  Bind9 config: ${TSIG_CONF}"
echo "  Client key: ${NSUPDATE_KEY}"
echo "Restart bind9 to apply: systemctl restart bind9"
