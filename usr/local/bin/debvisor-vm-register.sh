#!/bin/bash
################################################################################
# debvisor-vm-register.sh - VM Registration Helper
#
# This script registers a VM's DNS record upon creation/boot.
# It is a wrapper around debvisor-dns-update.sh, designed to be called
# by libvirt hooks or Ansible.
#
# Usage:
#   debvisor-vm-register.sh <vm_name> <ip_address>
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
IP_ADDR=""
TSIG_CONF="/etc/bind/tsig-vm.conf"

################################################################################
# Main Execution
################################################################################

main() {
    if [ $# -lt 2 ]; then
        log_error "Usage: $0 <vm_name> <ip_address>"
        exit 1
    fi
    
    VM_NAME="$1"
    IP_ADDR="$2"
    
    log_info "DebVisor VM Register v${SCRIPT_VERSION}"
    log_info "Registering VM: $VM_NAME -> $IP_ADDR"
    
    # Check if TSIG config exists (legacy check)
    if [ -f "$TSIG_CONF" ]; then
        # If using legacy TSIG conf, we might need to extract key or pass it
        # For now, we assume debvisor-dns-update.sh is configured correctly
        # or we pass the key file if it differs.
        :
    fi
    
    # Call the robust DNS updater
    if "${SCRIPT_DIR}/debvisor-dns-update.sh" --action add "$VM_NAME" "$IP_ADDR"; then
        log_info "✓ VM registration successful"
        audit_log "vm_register" "Registered VM $VM_NAME ($IP_ADDR)" "success"
    else
        log_error "VM registration failed"
        audit_log "vm_register" "Failed to register VM $VM_NAME" "error"
        exit 1
    fi
}

# Run main
main "$@"
