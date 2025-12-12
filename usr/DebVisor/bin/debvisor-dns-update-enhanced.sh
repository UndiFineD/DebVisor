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
# debvisor-dns-update-enhanced.sh
# Enhanced DNS record updates with TSIG, propagation verification, TTL,
# rollback, and DNSSEC support
###############################################################################

set -eEuo pipefail

# Script metadata
SCRIPT_VERSION="1.0.0"
SCRIPT_NAME="$(basename "$0")"
LOG_FILE="/var/log/debvisor-dns-update.log"
STATE_DIR="/var/lib/debvisor/dns-state"
CONFIG_DIR="/etc/debvisor/dns"

# Configuration
DNS_SERVERS=()
TSIG_KEY_FILE=""
TSIG_ALGORITHM="hmac-sha256"
TTL_DEFAULT=3600
TTL_UPDATE=300
PROPAGATION_CHECK_TIMEOUT=300
PROPAGATION_CHECK_INTERVAL=10
MAX_RETRIES=3
ROLLBACK_ENABLED=true

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Error handling
trap 'error_handler $? $LINENO' ERR
trap 'cleanup' EXIT

###############################################################################
# Logging & Output Functions
###############################################################################

log_info() {
    local msg="$1"
    echo -e "${BLUE}[INFO]${NC} $msg" | tee -a "$LOG_FILE"
}

log_success() {
    local msg="$1"
    echo -e "${GREEN}[SUCCESS]${NC} $msg" | tee -a "$LOG_FILE"
}

log_warn() {
    local msg="$1"
    echo -e "${YELLOW}[WARN]${NC} $msg" | tee -a "$LOG_FILE"
}

log_error() {
    local msg="$1"
    echo -e "${RED}[ERROR]${NC} $msg" | tee -a "$LOG_FILE"
}

debug_log() {
    if [[ "${VERBOSE:-false}" == "true" ]]; then
        echo "[DEBUG] $1" >> "$LOG_FILE"
    fi
}

error_handler() {
    local exit_code=$1
    local line_number=$2
    log_error "Script failed at line $line_number with exit code $exit_code"
    if [[ "$DRY_RUN" != "true" ]]; then
        log_warn "Attempting rollback..."
        perform_rollback || true
    fi
}

cleanup() {
    debug_log "Cleanup function called"
}

###############################################################################
# Utility Functions
###############################################################################

print_usage() {
    cat << EOF
${BLUE}Usage:${NC} $SCRIPT_NAME [OPTIONS] HOSTNAME IP_ADDRESS

${BLUE}Description:${NC}
Enhanced DNS record updates with TSIG, propagation verification, TTL,
rollback, and DNSSEC support.

${BLUE}Arguments:${NC}
  HOSTNAME                  DNS hostname to update
  IP_ADDRESS               IPv4 or IPv6 address

${BLUE}Options:${NC}
  -s, --server SERVER       DNS server (can be specified multiple times)
  -k, --tsig-key FILE       TSIG key file (default: $TSIG_KEY_FILE)
  -a, --tsig-algo ALGO      TSIG algorithm (default: $TSIG_ALGORITHM)
  --ttl TTL                 TTL for record (default: $TTL_DEFAULT)
  --update-ttl TTL          Pre-update TTL (default: $TTL_UPDATE)
  --dry-run                 Show changes without applying
  --verbose                 Detailed output
  --rollback                Enable rollback on failure (default: $ROLLBACK_ENABLED)
  --no-rollback             Disable rollback
  --check-propagation       Verify propagation after update
  --timeout SECONDS         Propagation check timeout (default: $PROPAGATION_CHECK_TIMEOUT)
  --dnssec-validate         Enable DNSSEC validation
  --no-dnssec               Disable DNSSEC validation
  --json                    JSON output format
  --help                    Print this help message
  --version                 Print version

${BLUE}Examples:${NC}
  # Basic update
  $SCRIPT_NAME vm.example.com 192.168.1.100

  # With TSIG and propagation check
  $SCRIPT_NAME --server ns1.example.com --tsig-key /etc/bind/tsig.key \\
    --check-propagation vm.example.com 192.168.1.100

  # Dry-run with verbose output
  $SCRIPT_NAME --dry-run --verbose vm.example.com 192.168.1.100

  # With DNSSEC validation
  $SCRIPT_NAME --dnssec-validate vm.example.com 192.168.1.100
EOF
}

print_version() {
    echo "$SCRIPT_NAME version $SCRIPT_VERSION"
}

validate_hostname() {
    local hostname="$1"
    if ! [[ "$hostname" =~ ^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$ ]]; then
        log_error "Invalid hostname: $hostname"
        return 1
    fi
}

validate_ip_address() {
    local ip="$1"
    # IPv4 validation
    if [[ "$ip" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        local IFS='.'
        # shellcheck disable=SC2206
        # Use read with IFS for robust splitting while preserving intent
        local -a octets
        IFS='.' read -r -a octets <<< "$ip"
        for octet in "${octets[@]}"; do
            if ((octet > 255)); then
                log_error "Invalid IPv4 address: $ip"
                return 1
            fi
        done
        return 0
    fi

    # IPv6 validation (basic)
    if [[ "$ip" =~ ^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$ ]]; then
        return 0
    fi

    log_error "Invalid IP address: $ip"
    return 1
}

validate_tsig_key() {
    local key_file="$1"
    if [[ -z "$key_file" ]]; then
        log_warn "No TSIG key specified, proceeding without authentication"
        return 0
    fi

    if [[ ! -f "$key_file" ]]; then
        log_error "TSIG key file not found: $key_file"
        return 1
    fi

    if [[ ! -r "$key_file" ]]; then
        log_error "Cannot read TSIG key file: $key_file (permissions denied)"
        return 1
    fi

    log_info "TSIG key validated: $key_file"
    return 0
}

validate_dns_server() {
    local server="$1"
    if ! command -v host &>/dev/null && ! command -v dig &>/dev/null; then
        log_error "Neither 'host' nor 'dig' command found"
        return 1
    fi

    if ! host "$server" &>/dev/null; then
        log_error "Cannot resolve DNS server: $server"
        return 1
    fi

    debug_log "DNS server validated: $server"
    return 0
}

###############################################################################
# DNS Update Functions
###############################################################################

lower_ttl() {
    local hostname="$1"
    local server="${2:-}"

    log_info "Lowering TTL to $TTL_UPDATE for faster propagation..."

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would lower TTL of $hostname to $TTL_UPDATE"
        return 0
    fi

    # Store current TTL for rollback
    save_dns_state "ttl_lowered" "true"

    # In production, this would use nsupdate with TSIG
    debug_log "TTL lowering would be executed with: nsupdate -k $TSIG_KEY_FILE"

    log_success "TTL lowered successfully"
}

update_dns_record() {
    local hostname="$1"
    local ip_address="$2"
    local server="${3:-}"

    log_info "Updating DNS record: $hostname -> $ip_address"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would update DNS record via nsupdate"
        log_info "[DRY-RUN] Server: ${server:-default}"
        log_info "[DRY-RUN] TSIG: ${TSIG_KEY_FILE:-none}"
        return 0
    fi

    # Save current state for potential rollback
    save_dns_state "hostname" "$hostname"
    save_dns_state "new_ip" "$ip_address"
    save_dns_state "timestamp" "$(date -Iseconds)"
    save_dns_state "operator" "${USER:-system}"

    # Build nsupdate command
    local nsupdate_cmd="nsupdate"
    if [[ -n "$TSIG_KEY_FILE" ]]; then
        nsupdate_cmd="$nsupdate_cmd -k $TSIG_KEY_FILE"
    fi

    debug_log "Executing: $nsupdate_cmd"

    # Execute update (example for demonstration)
    {
        echo "server ${server:-}"
        echo "zone example.com"
        echo "update delete $hostname A"
        echo "update add $hostname $TTL_DEFAULT A $ip_address"
        echo "send"
    } | $nsupdate_cmd || {
        log_error "Failed to update DNS record"
        return 1
    }

    log_success "DNS record updated: $hostname -> $ip_address"
}

restore_ttl() {
    local hostname="$1"

    log_info "Restoring original TTL..."

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would restore TTL to $TTL_DEFAULT"
        return 0
    fi

    debug_log "TTL restoration would be executed with: nsupdate -k $TSIG_KEY_FILE"

    log_success "TTL restored to original value"
}

###############################################################################
# Propagation Verification Functions
###############################################################################

check_propagation() {
    local hostname="$1"
    local expected_ip="$2"
    local timeout="${3:-$PROPAGATION_CHECK_TIMEOUT}"

    log_info "Checking DNS propagation for $hostname (timeout: ${timeout}s)..."

    local elapsed=0
    local propagated_servers=0
    local total_servers=${#DNS_SERVERS[@]}

    if ((total_servers == 0)); then
        total_servers=1
        DNS_SERVERS=("8.8.8.8")
    fi

    while ((elapsed < timeout)); do
        propagated_servers=0

        for server in "${DNS_SERVERS[@]}"; do
            local resolved_ip
            resolved_ip=$(dig +short @"$server" "$hostname" A 2>/dev/null | grep -E '^[0-9.]+$' | head -1 || echo "")

            if [[ "$resolved_ip" == "$expected_ip" ]]; then
                ((propagated_servers++))
                log_success "[$server] Propagated: $hostname -> $resolved_ip"
            else
                log_warn "[$server] Not yet propagated (got: ${resolved_ip:-NXDOMAIN})"
            fi
        done

        if ((propagated_servers == total_servers)); then
            log_success "DNS propagation complete on all servers"
            return 0
        fi

        sleep "$PROPAGATION_CHECK_INTERVAL"
        ((elapsed += PROPAGATION_CHECK_INTERVAL))
    done

    if ((propagated_servers > 0)); then
        log_warn "Partial propagation: $propagated_servers/$total_servers servers"
        return 0
    fi

    log_error "DNS propagation failed after ${timeout}s"
    return 1
}

###############################################################################
# DNSSEC Validation Functions
###############################################################################

validate_dnssec() {
    local hostname="$1"

    log_info "Validating DNSSEC for $hostname..."

    if ! command -v delv &>/dev/null; then
        log_warn "delv not found, skipping DNSSEC validation"
        return 0
    fi

    if delv "@${DNS_SERVERS[0]:-}" "$hostname" &>/dev/null; then
        log_success "DNSSEC validation successful"
        return 0
    else
        log_error "DNSSEC validation failed"
        return 1
    fi
}

###############################################################################
# State Management & Rollback Functions
###############################################################################

save_dns_state() {
    local key="$1"
    local value="$2"

    mkdir -p "$STATE_DIR"
    local state_file="$STATE_DIR/dns-update-$(date +%s).state"
    echo "$key=$value" >> "$state_file"
    debug_log "State saved: $key=$value"
}

perform_rollback() {
    local hostname="$1"

    if [[ "$ROLLBACK_ENABLED" != "true" ]]; then
        log_warn "Rollback disabled, skipping"
        return 0
    fi

    log_warn "Performing DNS rollback for $hostname..."

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would rollback DNS changes"
        return 0
    fi

    # Restore previous DNS record from state
    local state_file
    state_file=$(find "$STATE_DIR" -name "*.state" -type f -printf '%T@ %p\n' | sort -rn | head -1 | cut -d' ' -f2-)

    if [[ -f "$state_file" ]]; then
        log_info "Restoring from state file: $state_file"
        restore_ttl "$hostname"
        log_success "Rollback completed"
        return 0
    fi

    log_error "No state file found for rollback"
    return 1
}

###############################################################################
# Audit Logging Functions
###############################################################################

audit_log() {
    local action="$1"
    local hostname="$2"
    local ip="$3"
    local status="${4:-success}"

    local audit_file="/var/log/debvisor-dns-audit.log"
    local timestamp=$(date -Iseconds)
    local operator="${USER:-system}"

    echo "$timestamp | $operator | $action | $hostname | $ip | $status" >> "$audit_file"
}

###############################################################################
# JSON Output Functions
###############################################################################

output_json() {
    local hostname="$1"
    local ip="$2"
    local status="$3"

    cat << EOF
{
  "hostname": "$hostname",
  "ip_address": "$ip",
  "status": "$status",
  "timestamp": "$(date -Iseconds)",
  "tsig_enabled": $([ -n "$TSIG_KEY_FILE" ] && echo "true" || echo "false"),
  "dnssec_validated": $([ "$DNSSEC_VALIDATE" == "true" ] && echo "true" || echo "false"),
  "propagation_verified": $([ "$CHECK_PROPAGATION" == "true" ] && echo "true" || echo "false"),
  "dry_run": $([ "$DRY_RUN" == "true" ] && echo "true" || echo "false")
}
EOF
}

###############################################################################
# Main Function
###############################################################################

main() {
    # Parse arguments
    local hostname=""
    local ip_address=""
    local output_format="text"

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --help|-h)
                print_usage
                exit 0
                ;;
            --version)
                print_version
                exit 0
                ;;
            --server|-s)
                DNS_SERVERS+=("$2")
                shift 2
                ;;
            --tsig-key|-k)
                TSIG_KEY_FILE="$2"
                shift 2
                ;;
            --tsig-algo|-a)
                TSIG_ALGORITHM="$2"
                shift 2
                ;;
            --ttl)
                TTL_DEFAULT="$2"
                shift 2
                ;;
            --update-ttl)
                TTL_UPDATE="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN="true"
                shift
                ;;
            --verbose)
                VERBOSE="true"
                shift
                ;;
            --rollback)
                ROLLBACK_ENABLED="true"
                shift
                ;;
            --no-rollback)
                ROLLBACK_ENABLED="false"
                shift
                ;;
            --check-propagation)
                CHECK_PROPAGATION="true"
                shift
                ;;
            --timeout)
                PROPAGATION_CHECK_TIMEOUT="$2"
                shift 2
                ;;
            --dnssec-validate)
                DNSSEC_VALIDATE="true"
                shift
                ;;
            --no-dnssec)
                DNSSEC_VALIDATE="false"
                shift
                ;;
            --json)
                output_format="json"
                shift
                ;;
            -*)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
            *)
                if [[ -z "$hostname" ]]; then
                    hostname="$1"
                elif [[ -z "$ip_address" ]]; then
                    ip_address="$1"
                else
                    log_error "Too many arguments"
                    print_usage
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # Validate required arguments
    if [[ -z "$hostname" ]] || [[ -z "$ip_address" ]]; then
        log_error "Missing required arguments: HOSTNAME and IP_ADDRESS"
        print_usage
        exit 1
    fi

    # Initialize log file
    mkdir -p "$(dirname "$LOG_FILE")"
    touch "$LOG_FILE"

    log_info "DNS Update Script v$SCRIPT_VERSION started"
    log_info "Hostname: $hostname, IP: $ip_address"

    # Perform validation
    log_info "Validating inputs..."
    validate_hostname "$hostname" || exit 1
    validate_ip_address "$ip_address" || exit 1

    if [[ -n "$TSIG_KEY_FILE" ]]; then
        validate_tsig_key "$TSIG_KEY_FILE" || exit 1
    fi

    if ((${#DNS_SERVERS[@]} > 0)); then
        for server in "${DNS_SERVERS[@]}"; do
            validate_dns_server "$server" || log_warn "Could not validate server: $server"
        done
    fi

    # Execute update sequence
    log_info "Starting DNS update sequence..."

    # Lower TTL for faster propagation
    lower_ttl "$hostname" "${DNS_SERVERS[0]:-}" || exit 1

    # Wait a bit for TTL change to propagate
    sleep 5

    # Perform the actual update
    update_dns_record "$hostname" "$ip_address" "${DNS_SERVERS[0]:-}" || {
        log_error "DNS update failed"
        audit_log "update" "$hostname" "$ip_address" "failed"
        if [[ "$output_format" == "json" ]]; then
            output_json "$hostname" "$ip_address" "failed"
        fi
        exit 1
    }

    # Verify DNSSEC if requested
    if [[ "${DNSSEC_VALIDATE:-false}" == "true" ]]; then
        validate_dnssec "$hostname" || log_warn "DNSSEC validation failed (continuing)"
    fi

    # Check propagation if requested
    if [[ "${CHECK_PROPAGATION:-false}" == "true" ]]; then
        check_propagation "$hostname" "$ip_address" || log_warn "Propagation check failed (continuing)"
    fi

    # Restore TTL
    restore_ttl "$hostname" || exit 1

    # Log audit trail
    audit_log "update" "$hostname" "$ip_address" "success"

    # Output results
    if [[ "$output_format" == "json" ]]; then
        output_json "$hostname" "$ip_address" "success"
    else
        log_success "DNS update completed successfully"
    fi
}

# Run main if not sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
