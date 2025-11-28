#!/bin/bash
set -euo pipefail

PROFILE_FILE="/etc/debvisor-profile"
OUT_DIR="/var/log/debvisor"
TXT_OUT="$OUT_DIR/profile-summary.txt"
JSON_OUT="$OUT_DIR/profile-summary.json"

mkdir -p "$OUT_DIR"

if [[ -f "$PROFILE_FILE" ]]; then
  profile=$(cat "$PROFILE_FILE" | tr -d '\r' | xargs)
else
  profile="unknown"
fi

echo "DebVisor storage profile: $profile" > "$TXT_OUT"
cat > "$JSON_OUT" <<EOF
{
  "profile": "${profile}",
  "source": "${PROFILE_FILE}",
  "generated_at": "$(date -Iseconds)"
}
EOF

exit 0
