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
        log_info "? VM registration successful"
        audit_log "vm_register" "Registered VM $VM_NAME ($IP_ADDR)" "success"
    else
        log_error "VM registration failed"
        audit_log "vm_register" "Failed to register VM $VM_NAME" "error"
        exit 1
    fi
}

# Run main
main "$@"
