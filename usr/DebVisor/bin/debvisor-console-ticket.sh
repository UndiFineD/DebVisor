#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

################################################################################
# debvisor-console-ticket.sh - Secure Console Access Manager
#
# This script generates and manages short-lived, signed authentication tickets
# for VNC/SPICE console access. It supports HMAC signing, JSON output,
# and automatic cleanup of expired tickets.
#
# Usage:
#   debvisor-console-ticket.sh [OPTIONS] <vm_name>
#
# Options:
#   --ttl MINUTES     Ticket validity duration (default: 5)
#   --user USERNAME   User requesting access (for audit)
#   --json            Output in JSON format
#   --verify TICKET   Verify a ticket instead of creating one
#   --help            Show this help message
#
################################################################################

set -eEuo pipefail

# Source shared library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/debvisor-lib.sh"

################################################################################
# Script Configuration
################################################################################

readonly SCRIPT_VERSION="2.0.0"
VM_NAME=""
TTL_MIN=5
REQUEST_USER="unknown"
OUTPUT_JSON=false
VERIFY_MODE=false
VERIFY_TICKET=""
TICKET_DIR="/var/lib/debvisor/console-tickets"
SECRET_FILE="/etc/debvisor/console.secret"

################################################################################
# Helper Functions
################################################################################

show_help() {
    sed -n '2,/^###/p' "$0" | grep -v '^###' | head -30
}

parse_arguments() {
    while [ $# -gt 0 ]; do
        case "$1" in
            --ttl)
                TTL_MIN="$2"
                shift 2
                ;;
            --user)
                REQUEST_USER="$2"
                shift 2
                ;;
            --json)
                OUTPUT_JSON=true
                shift
                ;;
            --verify)
                VERIFY_MODE=true
                VERIFY_TICKET="$2"
                shift 2
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            -*)
                log_error "Unknown option: $1"
                show_help
                exit 2
                ;;
            *)
                if [ -z "$VM_NAME" ]; then
                    VM_NAME="$1"
                else
                    log_error "Too many positional arguments"
                    exit 2
                fi
                shift
                ;;
        esac
    done
}

validate_arguments() {
    if [ -z "$VM_NAME" ] && [ "$VERIFY_MODE" = false ]; then
        log_error "VM name is required"
        show_help
        exit 2
    fi
}

ensure_secret() {
    if [ ! -f "$SECRET_FILE" ]; then
        log_warn "Console secret file missing, generating new one..."
        mkdir -p "$(dirname "$SECRET_FILE")"
        openssl rand -base64 32 > "$SECRET_FILE"
        chmod 600 "$SECRET_FILE"
    fi
}

cleanup_old_tickets() {
    # Remove tickets older than 1 hour (safety margin over TTL)
    find "$TICKET_DIR" -name "*.ticket" -type f -mmin +60 -delete 2>/dev/null || true
}

generate_ticket() {
    mkdir -p "$TICKET_DIR"
    chmod 700 "$TICKET_DIR"

    local expiry_ts
    expiry_ts=$(date -u +%s -d "+${TTL_MIN} minutes")

    local rand_token
    rand_token=$(openssl rand -hex 16)

    local payload="${VM_NAME}:${expiry_ts}:${rand_token}:${REQUEST_USER}"
    local secret
    # Read secret using shell input redirection to avoid spawning external processes
    secret=$(<"$SECRET_FILE")

    local signature
    # Parse openssl output reliably: "(stdin)= <hex>" -> extract the hex digest field
    signature=$(echo -n "$payload" | openssl dgst -sha256 -hmac "$secret" | cut -d ' ' -f2)

    local ticket="${payload}|${signature}"

    # Store ticket for verification (optional, but good for revocation)
    echo "$ticket" > "$TICKET_DIR/${VM_NAME}.ticket"
    chmod 600 "$TICKET_DIR/${VM_NAME}.ticket"

    if [ "$OUTPUT_JSON" = true ]; then
        printf '{"ticket": "%s", "vm": "%s", "expiry": %d, "user": "%s"}\n' \
            "$ticket" "$VM_NAME" "$expiry_ts" "$REQUEST_USER"
    else
        echo "$ticket"
    fi

    audit_log "console_ticket_create" "Created ticket for $VM_NAME (User: $REQUEST_USER)" "success"
}

verify_ticket() {
    local ticket_str="$VERIFY_TICKET"
    local payload="${ticket_str%|*}"
    local signature="${ticket_str##*|}"

    local secret
    # Read secret using shell input redirection to avoid spawning external processes
    secret=$(<"$SECRET_FILE")

    local expected_sig
    # Parse openssl output reliably: "(stdin)= <hex>" -> extract the hex digest field
    expected_sig=$(echo -n "$payload" | openssl dgst -sha256 -hmac "$secret" | cut -d ' ' -f2)

    if [ "$signature" != "$expected_sig" ]; then
        log_error "Invalid ticket signature"
        return 1
    fi

    # Parse payload: VM:EXPIRY:RAND:USER
    local vm_name expiry_ts rand_token user
    IFS=':' read -r vm_name expiry_ts rand_token user <<< "$payload"

    local current_ts
    current_ts=$(date -u +%s)

    if [ "$current_ts" -gt "$expiry_ts" ]; then
        log_error "Ticket expired"
        return 1
    fi

    log_info "Ticket valid for VM: $vm_name (User: $user)"
    return 0
}

################################################################################
# Main Execution
################################################################################

main() {
    parse_arguments "$@"
    validate_arguments
    ensure_secret
    cleanup_old_tickets

    if [ "$VERIFY_MODE" = true ]; then
        verify_ticket
    else
        generate_ticket
    fi
}

# Run main
main "$@"
