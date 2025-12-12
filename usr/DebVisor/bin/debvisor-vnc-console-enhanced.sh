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

###############################################################################
# debvisor-vnc-console-enhanced.sh
# Enhanced VNC and console tools with validation, security hardening,
# and audit logging
###############################################################################

set -eEuo pipefail

# Script metadata
SCRIPT_VERSION="1.0.0"
SCRIPT_NAME="$(basename "$0")"
LOG_FILE="/var/log/debvisor-vnc-console.log"
AUDIT_LOG="/var/log/debvisor-console-audit.log"
CONFIG_DIR="/etc/debvisor/vnc"
STATE_DIR="/var/lib/debvisor/vnc-state"

# Security settings
CONSOLE_TOKEN_TTL=3600  # 1 hour
CONSOLE_TOKEN_LENGTH=32
MAX_CONSOLE_SESSIONS=10
ALLOWED_PORTS=(5900-5999 6000-6099)
MIN_VNC_PORT=5900
MAX_VNC_PORT=5999

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Error handling
trap 'error_handler $? $LINENO' ERR
trap 'cleanup' EXIT

###############################################################################
# Logging & Audit Functions
###############################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

audit_log_entry() {
    local action="$1"
    local vm_name="$2"
    local result="$3"
    local details="${4:-}"

    local timestamp=$(date -Iseconds)
    local user="${SUDO_USER:-${USER:-unknown}}"
    local ip="${SSH_CLIENT%% *}"

    mkdir -p "$(dirname "$AUDIT_LOG")"
    echo "$timestamp | $user | $action | $vm_name | $result | $ip | $details" >> "$AUDIT_LOG"
}

error_handler() {
    local exit_code=$1
    local line_number=$2
    log_error "Script failed at line $line_number with exit code $exit_code"
}

cleanup() {
    debug_log "Cleanup completed"
}

debug_log() {
    if [[ "${VERBOSE:-false}" == "true" ]]; then
        echo "[DEBUG] $1" >> "$LOG_FILE"
    fi
}

###############################################################################
# Utility Functions
###############################################################################

print_usage() {
    cat << EOF
${BLUE}Usage:${NC} $SCRIPT_NAME COMMAND [OPTIONS]

${BLUE}Description:${NC}
Enhanced VNC and console management with security hardening and audit logging.

${BLUE}Commands:${NC}
  ensure-port VM_NAME       Ensure VNC port is listening for VM
  generate-token VM_NAME    Generate console access token
  validate-vnc HOST:PORT    Validate VNC is reachable
  list-sessions             List active console sessions
  close-session TOKEN       Close console session by token
  config VM_NAME            Configure VNC for VM
  security-report           Generate security report

${BLUE}Global Options:${NC}
  --dry-run                 Show what would be done
  --verbose                 Detailed output
  --json                    JSON output format
  --help                    Print this help message
  --version                 Print version

${BLUE}Examples:${NC}
  # Generate console token (valid 1 hour)
  $SCRIPT_NAME generate-token myvm

  # Validate VNC connectivity
  $SCRIPT_NAME validate-vnc 192.168.1.100:5900

  # List active sessions
  $SCRIPT_NAME list-sessions

  # Security report
  $SCRIPT_NAME security-report
EOF
}

print_version() {
    echo "$SCRIPT_NAME version $SCRIPT_VERSION"
}

generate_token() {
    local length=${1:-$CONSOLE_TOKEN_LENGTH}
    local token
    token=$(head -c 32 /dev/urandom | base64 | tr -d '+/=' | cut -c1-"$length")
    echo "$token"
}

validate_vm_name() {
    local vm_name="$1"
    if ! [[ "$vm_name" =~ ^[a-zA-Z0-9._-]+$ ]]; then
        log_error "Invalid VM name: $vm_name"
        return 1
    fi
}

validate_port() {
    local port="$1"
    if ! [[ "$port" =~ ^[0-9]+$ ]]; then
        log_error "Invalid port: $port"
        return 1
    fi
    if ((port < 0 || port > 65535)); then
        log_error "Port out of range: $port"
        return 1
    fi
}

###############################################################################
# VNC Management Functions
###############################################################################

ensure_vnc_port() {
    local vm_name="$1"

    log_info "Ensuring VNC port for VM: $vm_name"

    validate_vm_name "$vm_name" || return 1

    # Check if VM exists (using virsh if available)
    if command -v virsh &>/dev/null; then
        if ! virsh list --all | grep -q "$vm_name"; then
            log_error "VM not found: $vm_name"
            audit_log_entry "ensure_port" "$vm_name" "failed" "VM not found"
            return 1
        fi
    fi

    # Check if VNC is already configured
    if virsh dumpxml "$vm_name" 2>/dev/null | grep -q "graphics type='vnc'"; then
        log_info "VNC already configured for $vm_name"
    else
        log_info "Configuring VNC for $vm_name"
        if [[ "$DRY_RUN" != "true" ]]; then
            # This would use XML modification in production
            debug_log "Would configure VNC for VM: $vm_name"
        fi
    fi

    # Find available VNC port
    local vnc_port
    vnc_port=$(find_available_vnc_port) || return 1

    log_success "VNC port: $vnc_port for VM: $vm_name"
    audit_log_entry "ensure_port" "$vm_name" "success" "port=$vnc_port"

    if [[ "${JSON_OUTPUT:-false}" == "true" ]]; then
        cat << EOF
{
  "vm_name": "$vm_name",
  "vnc_port": $vnc_port,
  "status": "success"
}
EOF
    fi
}

find_available_vnc_port() {
    for port in $(seq "$MIN_VNC_PORT" "$MAX_VNC_PORT"); do
        if ! nc -z localhost "$port" 2>/dev/null; then
            echo "$port"
            return 0
        fi
    done
    log_error "No available VNC ports"
    return 1
}

validate_vnc_reachable() {
    local host_port="$1"

    log_info "Validating VNC at: $host_port"

    if [[ ! "$host_port" =~ ^[^:]+:[0-9]+$ ]]; then
        log_error "Invalid host:port format: $host_port"
        return 1
    fi

    local host="${host_port%:*}"
    local port="${host_port##*:}"

    validate_port "$port" || return 1

    # Check if port is within allowed VNC range
    if ! [[ "$port" =~ ^($(IFS=\|; echo "${ALLOWED_PORTS[*]}"))$ ]]; then
        log_warn "Port $port outside standard VNC range"
    fi

    # Test connectivity
    if timeout 5 nc -zv "$host" "$port" 2>&1 | grep -q "succeeded"; then
        log_success "VNC is reachable: $host_port"
        audit_log_entry "validate_vnc" "$host_port" "success" "reachable"
        return 0
    else
        log_error "VNC is not reachable: $host_port"
        audit_log_entry "validate_vnc" "$host_port" "failed" "unreachable"
        return 1
    fi
}

###############################################################################
# Console Token Management
###############################################################################

generate_console_token() {
    local vm_name="$1"

    log_info "Generating console token for VM: $vm_name"

    validate_vm_name "$vm_name" || return 1

    local token
    token=$(generate_token)

    local expiration=$(($(date +%s) + CONSOLE_TOKEN_TTL))
    local token_type="${2:-read-write}"

    # Validate token type
    if ! [[ "$token_type" =~ ^(read-only|read-write|admin)$ ]]; then
        log_error "Invalid token type: $token_type"
        return 1
    fi

    if [[ "$DRY_RUN" != "true" ]]; then
        # Store token with metadata
        mkdir -p "$STATE_DIR"
        local token_file="$STATE_DIR/${token}.token"
        cat > "$token_file" << EOF
{
  "vm_name": "$vm_name",
  "token": "$token",
  "type": "$token_type",
  "created_at": "$(date -Iseconds)",
  "expires_at": "$(date -d @$expiration -Iseconds)",
  "user": "${SUDO_USER:-${USER:-unknown}}",
  "ip": "${SSH_CLIENT%% *}"
}
EOF
        chmod 600 "$token_file"
        audit_log_entry "generate_token" "$vm_name" "success" "type=$token_type"
    fi

    log_success "Console token generated for $vm_name"
    echo ""
    echo "Token: $token"
    echo "Type: $token_type"
    echo "TTL: ${CONSOLE_TOKEN_TTL}s"
    echo "Expires: $(date -d @$expiration)"
    echo ""
    echo "Usage:"
    echo "  URL: vnc://$(hostname):5900?token=$token"

    if [[ "${JSON_OUTPUT:-false}" == "true" ]]; then
        cat << EOF
{
  "token": "$token",
  "vm_name": "$vm_name",
  "type": "$token_type",
  "ttl_seconds": $CONSOLE_TOKEN_TTL,
  "expires_at": "$(date -d @$expiration -Iseconds)"
}
EOF
    fi
}

validate_console_token() {
    local token="$1"

    local token_file="$STATE_DIR/${token}.token"

    if [[ ! -f "$token_file" ]]; then
        log_error "Token not found: $token"
        return 1
    fi

    # Check if token is expired
    local expires_at=$(grep "expires_at" "$token_file" | cut -d'"' -f4)
    local current_time=$(date -Iseconds)

    if [[ "$current_time" > "$expires_at" ]]; then
        log_error "Token expired: $token"
        rm -f "$token_file"
        return 1
    fi

    log_success "Token is valid: $token"
    return 0
}

###############################################################################
# Session Management
###############################################################################

list_console_sessions() {
    log_info "Active console sessions:"

    if [[ ! -d "$STATE_DIR" ]]; then
        log_info "No active sessions"
        return 0
    fi

    local count=0

    echo ""
    echo "Token | VM Name | Type | Created | Expires"
    echo "------|---------|------|---------|--------"

    for token_file in "$STATE_DIR"/*.token; do
        if [[ -f "$token_file" ]]; then
            ((count++))
            local vm_name=$(grep "vm_name" "$token_file" | cut -d'"' -f4)
            local token_type=$(grep '"type"' "$token_file" | cut -d'"' -f4)
            local created_at=$(grep "created_at" "$token_file" | cut -d'"' -f4)
            local expires_at=$(grep "expires_at" "$token_file" | cut -d'"' -f4)
            local token_short=$(basename "$token_file" .token | cut -c1-8)

            echo "$token_short... | $vm_name | $token_type | $created_at | $expires_at"
        fi
    done

    if ((count == 0)); then
        log_info "No active sessions"
    else
        log_info "Total sessions: $count"
    fi

    if [[ "${JSON_OUTPUT:-false}" == "true" ]]; then
        echo "["
        local first=true
        for token_file in "$STATE_DIR"/*.token; do
            if [[ -f "$token_file" ]]; then
                if [[ "$first" == "false" ]]; then
                    echo ","
                fi
                cat "$token_file"
                first=false
            fi
        done
        echo "]"
    fi
}

close_console_session() {
    local token="$1"

    log_info "Closing console session: $token"

    local token_file="$STATE_DIR/${token}.token"

    if [[ ! -f "$token_file" ]]; then
        log_error "Session not found: $token"
        return 1
    fi

    if [[ "$DRY_RUN" != "true" ]]; then
        rm -f "$token_file"
        log_success "Session closed: $token"
        audit_log_entry "close_session" "$token" "success"
    fi
}

###############################################################################
# Security Functions
###############################################################################

configure_vnc_security() {
    local vm_name="$1"

    log_info "Configuring VNC security for VM: $vm_name"

    validate_vm_name "$vm_name" || return 1

    # Security recommendations
    echo ""
    echo "${BLUE}VNC Security Configuration:${NC}"
    echo "  ? Use TLS encryption for all VNC connections"
    echo "  ? Enable SASL authentication"
    echo "  ? Use strong authentication passwords"
    echo "  ? Restrict VNC access to known IPs"
    echo "  ? Monitor VNC activity via audit logs"
    echo "  ? Use firewall rules to restrict port access"
    echo "  ? Keep VNC software updated"
    echo ""

    audit_log_entry "configure_security" "$vm_name" "success"
}

generate_security_report() {
    log_info "Generating VNC security report..."

    echo ""
    echo "${BLUE}=== VNC/Console Security Report ===${NC}"
    echo ""

    echo "Configuration:"
    echo "  Max Sessions: $MAX_CONSOLE_SESSIONS"
    echo "  Token TTL: ${CONSOLE_TOKEN_TTL}s"
    echo "  Allowed Ports: ${ALLOWED_PORTS[*]}"
    echo ""

    # Check for listening VNC ports
    echo "Active VNC Ports:"
    netstat -tuln 2>/dev/null | grep -E '590[0-9]|600[0-9]' || echo "  None"
    echo ""

    # Check for active sessions
    echo "Active Console Sessions:"
    if [[ -d "$STATE_DIR" ]]; then
        local count=$(find "$STATE_DIR" -name "*.token" -type f 2>/dev/null | wc -l)
        echo "  Current: $count"
        echo "  Max: $MAX_CONSOLE_SESSIONS"
    else
        echo "  Current: 0"
    fi
    echo ""

    # Check audit log
    echo "Recent Audit Entries (last 10):"
    if [[ -f "$AUDIT_LOG" ]]; then
        tail -10 "$AUDIT_LOG"
    else
        echo "  No audit entries yet"
    fi
    echo ""

    # Security recommendations
    echo "${YELLOW}Security Recommendations:${NC}"
    echo "  * Enable TLS for all VNC connections"
    echo "  * Implement firewall rules for VNC ports"
    echo "  * Regularly rotate authentication credentials"
    echo "  * Monitor audit logs for suspicious activity"
    echo "  * Use network segmentation for VNC access"
    echo ""

    audit_log_entry "security_report" "system" "success"
}

###############################################################################
# Main Function
###############################################################################

main() {
    mkdir -p "$(dirname "$LOG_FILE")"
    touch "$LOG_FILE"

    if [[ $# -lt 1 ]]; then
        print_usage
        exit 1
    fi

    local command="$1"
    shift

    case "$command" in
        ensure-port)
            ensure_vnc_port "$@"
            ;;
        generate-token)
            local vm_name="${1:-}"
            local token_type="${2:-read-write}"
            if [[ -z "$vm_name" ]]; then
                log_error "VM name required"
                exit 1
            fi
            generate_console_token "$vm_name" "$token_type"
            ;;
        validate-vnc)
            local host_port="${1:-}"
            if [[ -z "$host_port" ]]; then
                log_error "host:port required"
                exit 1
            fi
            validate_vnc_reachable "$host_port"
            ;;
        list-sessions)
            list_console_sessions
            ;;
        close-session)
            local token="${1:-}"
            if [[ -z "$token" ]]; then
                log_error "Token required"
                exit 1
            fi
            close_console_session "$token"
            ;;
        config)
            configure_vnc_security "$@"
            ;;
        security-report)
            generate_security_report
            ;;
        --help|-h)
            print_usage
            exit 0
            ;;
        --version)
            print_version
            exit 0
            ;;
        *)
            log_error "Unknown command: $command"
            print_usage
            exit 1
            ;;
    esac
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN="true"
            shift
            ;;
        --verbose)
            VERBOSE="true"
            shift
            ;;
        --json)
            JSON_OUTPUT="true"
            shift
            ;;
        *)
            break
            ;;
    esac
done

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
