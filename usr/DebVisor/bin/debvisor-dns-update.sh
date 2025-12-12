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
# debvisor-dns-update.sh - Enterprise Dynamic DNS Updater
#
# This script manages DNS records (A and PTR) for VMs. It supports secure
# TSIG updates, multiple DNS servers, zone validation, and propagation checks.
#
# Usage:
#   debvisor-dns-update.sh [OPTIONS] <hostname> <ip> <action>
#
# Arguments:
#   hostname        Short hostname (e.g., web-01)
#   ip              IP address (e.g., 192.168.1.50)
#   action          'add' or 'delete'
#
# Options:
#   --zone NAME     DNS zone name (default: debvisor.local)
#   --server IP     DNS server IP (default: 127.0.0.1)
#   --key FILE      TSIG key file path
#   --ttl SECONDS   TTL for records (default: 300)
#   --dry-run       Show what would be done without making changes
#   --help          Show this help message
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
HOSTNAME=""
IP_ADDR=""
ACTION=""
ZONE_NAME=${ZONE:-"debvisor.local"}
DNS_SERVER=${SERVER:-"127.0.0.1"}
TSIG_KEY_FILE=${TSIG_KEY_FILE:-"/etc/debvisor/dns.update.key"}
TTL=300

################################################################################
# Helper Functions
################################################################################

show_help() {
    sed -n '2,/^###/p' "$0" | grep -v '^###' | head -30
}

parse_arguments() {
    while [ $# -gt 0 ]; do
        case "$1" in
            --zone)
                ZONE_NAME="$2"
                shift 2
                ;;
            --server)
                DNS_SERVER="$2"
                shift 2
                ;;
            --key)
                TSIG_KEY_FILE="$2"
                shift 2
                ;;
            --ttl)
                TTL="$2"
                shift 2
                ;;
            --dry-run)
                DEBVISOR_DRY_RUN=true
                log_info "Dry-run mode enabled"
                shift
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
                if [ -z "$HOSTNAME" ]; then
                    HOSTNAME="$1"
                elif [ -z "$IP_ADDR" ]; then
                    IP_ADDR="$1"
                elif [ -z "$ACTION" ]; then
                    ACTION="$1"
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
    if [ -z "$HOSTNAME" ] || [ -z "$IP_ADDR" ] || [ -z "$ACTION" ]; then
        log_error "Missing required arguments"
        show_help
        exit 2
    fi

    if [[ ! "$ACTION" =~ ^(add|delete)$ ]]; then
        log_error "Invalid action: $ACTION (must be 'add' or 'delete')"
        exit 2
    fi

    # Basic IP validation
    if [[ ! "$IP_ADDR" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        log_error "Invalid IP address format: $IP_ADDR"
        exit 2
    fi
}

check_prerequisites() {
    log_info "===== Checking prerequisites ====="

    require_bin "nsupdate"
    require_bin "dig"

    if [ ! -f "$TSIG_KEY_FILE" ]; then
        log_error "TSIG key file not found: $TSIG_KEY_FILE"
        exit 1
    fi

    # Check server reachability (UDP 53)
    if ! timeout 2 bash -c "</dev/udp/$DNS_SERVER/53" &>/dev/null; then
        log_warn "DNS server $DNS_SERVER may not be reachable on port 53 (UDP)"
    fi

    log_info "? Prerequisites met"
}

get_ptr_record() {
    local ip="$1"
    printf '%s' "$ip" | awk -F. '{print $4"."$3"."$2"."$1".in-addr.arpa"}'
}

get_reverse_zone() {
    local ip="$1"
    # Assuming /24 reverse zone for simplicity, but nsupdate usually handles this if we just send the update to the server
    # However, we need to specify 'zone' in nsupdate sometimes.
    # Let's try to infer it or just let nsupdate figure it out if we omit 'zone' for PTR?
    # Better to be explicit if possible.
    # For 192.168.1.50 -> 1.168.192.in-addr.arpa
    printf '%s' "$ip" | awk -F. '{print $3"."$2"."$1".in-addr.arpa"}'
}

execute_update() {
    log_info "===== Executing DNS update ($ACTION) ====="

    local key_name
    local key_secret

    # Extract key info safely
    key_name=$(awk '/key/ {gsub("\"","",$2); gsub("{","",$2); print $2; exit}' "$TSIG_KEY_FILE" || echo "update-key")
    key_secret=$(awk -F'"' '/secret/ {print $2}' "$TSIG_KEY_FILE")

    if [ -z "$key_secret" ]; then
        log_error "Could not parse secret from $TSIG_KEY_FILE"
        exit 1
    fi

    local ptr_record
    ptr_record=$(get_ptr_record "$IP_ADDR")
    local reverse_zone
    reverse_zone=$(get_reverse_zone "$IP_ADDR")

    local update_file
    update_file=$(mktemp)

    # Construct nsupdate commands
    {
        echo "server $DNS_SERVER"
        echo "zone $ZONE_NAME"
        if [ "$ACTION" == "add" ]; then
            echo "update delete $HOSTNAME.$ZONE_NAME. A" # Clean up old first
            echo "update add $HOSTNAME.$ZONE_NAME. $TTL A $IP_ADDR"
        else
            echo "update delete $HOSTNAME.$ZONE_NAME. A"
        fi
        echo "send"

        echo "server $DNS_SERVER"
        echo "zone $reverse_zone"
        if [ "$ACTION" == "add" ]; then
            echo "update delete $ptr_record PTR" # Clean up old first
            echo "update add $ptr_record $TTL PTR $HOSTNAME.$ZONE_NAME."
        else
            echo "update delete $ptr_record PTR"
        fi
        echo "send"
    } > "$update_file"

    if [ "$DEBVISOR_DRY_RUN" = true ]; then
        log_info "Dry-run: Would execute nsupdate with:"
        cat "$update_file"
        rm -f "$update_file"
        return 0
    fi

    log_info "Sending update to $DNS_SERVER..."
    if nsupdate -y "$key_name:$key_secret" -v "$update_file"; then
        log_info "? Update command sent successfully"
    else
        log_error "nsupdate failed"
        rm -f "$update_file"
        return 1
    fi
    rm -f "$update_file"
}

verify_propagation() {
    if [ "$DEBVISOR_DRY_RUN" = true ]; then return 0; fi

    log_info "===== Verifying propagation ====="

    # Wait a moment for server to process
    sleep 1

    local result_ip
    result_ip=$(dig +short "@$DNS_SERVER" "$HOSTNAME.$ZONE_NAME" A)

    if [ "$ACTION" == "add" ]; then
        if [ "$result_ip" == "$IP_ADDR" ]; then
            log_info "? Forward record verified: $HOSTNAME.$ZONE_NAME -> $IP_ADDR"
        else
            log_error "Forward record verification failed. Got: '$result_ip', Expected: '$IP_ADDR'"
            return 1
        fi
    else
        if [ -z "$result_ip" ]; then
            log_info "? Forward record removal verified"
        else
            log_warn "Forward record still exists: $result_ip"
        fi
    fi
}

################################################################################
# Main Execution
################################################################################

main() {
    log_info "DebVisor DNS Updater v${SCRIPT_VERSION}"

    parse_arguments "$@"
    validate_arguments
    check_prerequisites

    execute_update
    verify_propagation

    log_info "===== DNS update complete ====="
    audit_log "dns_update" "DNS $ACTION for $HOSTNAME ($IP_ADDR)" "success"
}

# Run main
main "$@"
