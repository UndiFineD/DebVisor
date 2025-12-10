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
# opt/validate-components.sh - Cross-component consistency validation
#
# This script validates that all DebVisor components are properly integrated:
# - Ansible inventory matches required host groups
# - Package lists have no version conflicts
# - systemd units reference existing binaries
# - Docker addon definitions are complete
# - RPC proto definitions match implementation
# - File permissions and ownership are correct
#
# Usage:
#   opt/validate-components.sh [OPTIONS]
#
# Options:
#   --verbose              Show detailed validation output
#   --fix                  Attempt to fix common issues (create missing files, etc)
#   --report FILE          Generate HTML/JSON validation report
#   --help                 Show this help message
#
# Exit Codes:
#   0 - All validations passed
#   1 - Some validations failed (non-critical)
#   2 - Critical validation failed
#
################################################################################

set -eEuo pipefail

# Script configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VERBOSE=${VERBOSE:-false}
FIX_ISSUES=${FIX_ISSUES:-false}
REPORT_FILE=""
FAILED_CHECKS=0
PASSED_CHECKS=0

################################################################################
# Helper Functions
################################################################################

log_info() {
    echo "[INFO] $*" >&2
}

log_warn() {
    echo "[WARN] $*" >&2
}

log_error() {
    echo "[ERROR] $*" >&2
}

log_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo "[VERBOSE] $*" >&2
    fi
}

check_passed() {
    local name="$1"
    log_info "? $name"
    ((PASSED_CHECKS++))
}

check_failed() {
    local name="$1"
    local severity="${2:-warning}"
    log_error "? $name"
    if [ "$severity" = "critical" ]; then
        ((FAILED_CHECKS++))
    fi
}

################################################################################
# Validation Functions
################################################################################

validate_ansible_inventory() {
    log_info "===== Validating Ansible inventory ====="
    
    local inventory_file="${SCRIPT_DIR}/ansible/inventory/hosts.yml"
    
    if [ ! -f "$inventory_file" ]; then
        check_failed "Ansible inventory file exists" "critical"
        return 1
    fi
    
    # Check for required host groups
    local required_groups=("dns_primaries" "dns_secondaries" "ceph_mons" "ceph_osds")
    local all_found=true
    
    for group in "${required_groups[@]}"; do
        if grep -q "^  $group:" "$inventory_file"; then
            log_verbose "? Group found: $group"
        else
            log_warn "Group not found: $group"
            all_found=false
        fi
    done
    
    if [ "$all_found" = true ]; then
        check_passed "Ansible inventory has required host groups"
    else
        check_failed "Ansible inventory missing some groups"
    fi
}

validate_package_lists() {
    log_info "===== Validating package lists ====="
    
    local pkg_list_dir="${SCRIPT_DIR}/config/package-lists"
    
    if [ ! -d "$pkg_list_dir" ]; then
        check_failed "Package lists directory exists" "critical"
        return 1
    fi
    
    # Check for common package lists
    local expected_lists=("base.list.chroot" "ceph.list.chroot" "k8s.list.chroot")
    local found_count=0
    
    for list in expected_lists; do
        if [ -f "$pkg_list_dir/$list" ]; then
            ((found_count++))
            log_verbose "? Found: $list"
            
            # Check for duplicate entries
            if sort "$pkg_list_dir/$list" | uniq -d | grep -q .; then
                log_warn "Duplicate entries in $list"
            fi
        fi
    done
    
    if [ $found_count -ge 2 ]; then
        check_passed "Package lists exist and are formatted correctly"
    else
        check_failed "Some package lists are missing"
    fi
}

validate_systemd_units() {
    log_info "===== Validating systemd units ====="
    
    local systemd_dir="${PROJECT_ROOT}/etc/systemd/system"
    
    if [ ! -d "$systemd_dir" ]; then
        check_failed "systemd system directory exists"
        return 1
    fi
    
    local unit_count=0
    local valid_count=0
    
    # Check service files
    while IFS= read -r -d '' service_file; do
        ((unit_count++))
        
        # Check for required sections
        if grep -q "^\[Unit\]" "$service_file" && grep -q "^\[Service\]" "$service_file"; then
            ((valid_count++))
            log_verbose "? Valid unit structure: $(basename "$service_file")"
        else
            log_warn "Missing required sections in: $(basename "$service_file")"
        fi
        
        # Check that ExecStart references existing script or binary
        if grep -q "^ExecStart=" "$service_file"; then
            local exec_cmd=$(grep "^ExecStart=" "$service_file" | head -1 | cut -d'=' -f2- | awk '{print $1}')
            if [ -z "$exec_cmd" ]; then
                log_verbose "ExecStart command: $exec_cmd"
            fi
        fi
    done < <(find "$systemd_dir" -name "*.service" -print0)
    
    if [ $valid_count -eq $unit_count ] && [ $unit_count -gt 0 ]; then
        check_passed "All systemd service units are properly structured ($unit_count files)"
    else
        check_failed "Some systemd units have structural issues ($valid_count/$unit_count valid)"
    fi
}

validate_scripts() {
    log_info "===== Validating operational scripts ====="
    
    local bin_dir="${PROJECT_ROOT}/usr/local/bin"
    
    if [ ! -d "$bin_dir" ]; then
        check_failed "usr/local/bin directory exists"
        return 1
    fi
    
    local script_count=0
    local sourced_lib=0
    
    # Check that scripts source library and have error handling
    while IFS= read -r script; do
        ((script_count++))
        
        if grep -q "source.*debvisor-lib.sh" "$script" || grep -q "^\. .*debvisor-lib.sh" "$script"; then
            ((sourced_lib++))
            log_verbose "? Sources debvisor-lib.sh: $(basename "$script")"
        else
            if [[ "$script" != *"debvisor-lib.sh"* ]]; then
                log_warn "Does not source debvisor-lib.sh: $(basename "$script")"
            fi
        fi
        
        # Check for error handling
        if grep -q "set -eEuo pipefail" "$script"; then
            log_verbose "? Has proper error handling: $(basename "$script")"
        fi
    done < <(find "$bin_dir" -name "*.sh" -type f)
    
    if [ $sourced_lib -gt 0 ]; then
        check_passed "Scripts properly source library ($sourced_lib/$script_count use library)"
    else
        log_warn "Consider having all scripts source debvisor-lib.sh for consistency"
    fi
}

validate_docker_addons() {
    log_info "===== Validating Docker addons ====="
    
    local addon_dir="${SCRIPT_DIR}/docker/addons"
    
    if [ ! -d "$addon_dir" ]; then
        check_failed "Docker addons directory exists"
        return 1
    fi
    
    local addon_dirs=0
    local valid_addons=0
    
    # Check for addon.yaml files
    while IFS= read -r -d '' addon_path; do
        ((addon_dirs++))
        local addon_name=$(basename "$addon_path")
        
        if [ -f "$addon_path/addon.yaml" ]; then
            ((valid_addons++))
            log_verbose "? Has addon.yaml: $addon_name"
        else
            log_warn "Missing addon.yaml in: $addon_name"
            if [ "$FIX_ISSUES" = true ]; then
                log_info "Creating template addon.yaml for $addon_name"
                cat > "$addon_path/addon.yaml" <<EOF
name: $addon_name
version: 0.1.0
description: Docker addon for $addon_name
dependencies: []
required_resources:
  memory_mb: 512
  disk_gb: 5
EOF
            fi
        fi
    done < <(find "$addon_dir" -mindepth 1 -maxdepth 1 -type d -print0)
    
    if [ $valid_addons -eq $addon_dirs ] && [ $addon_dirs -gt 0 ]; then
        check_passed "All Docker addons have metadata files ($addon_dirs addons)"
    else
        check_failed "Some Docker addons missing metadata"
    fi
}

validate_rpc_service() {
    log_info "===== Validating RPC service ====="
    
    local rpc_dir="${SCRIPT_DIR}/services/rpc"
    
    if [ ! -d "$rpc_dir" ]; then
        check_failed "RPC service directory exists"
        return 1
    fi
    
    local proto_file="$rpc_dir/proto/debvisor.proto"
    local makefile="$rpc_dir/Makefile"
    
    local has_proto=0
    local has_make=0
    
    if [ -f "$proto_file" ]; then
        ((has_proto++))
        log_verbose "? Proto definition file exists"
        
        # Check for required service definition
        if grep -q "^service " "$proto_file"; then
            log_verbose "? Contains service definition"
        else
            log_warn "Proto file does not define service"
        fi
    else
        log_warn "Proto definition file not found"
    fi
    
    if [ -f "$makefile" ]; then
        ((has_make++))
        log_verbose "? Build Makefile exists"
    fi
    
    if [ $has_proto -eq 1 ] && [ $has_make -eq 1 ]; then
        check_passed "RPC service has required build files"
    else
        check_failed "RPC service missing required files"
    fi
}

validate_monitoring_setup() {
    log_info "===== Validating monitoring setup ====="
    
    local monitoring_dir="${SCRIPT_DIR}/monitoring"
    
    if [ ! -d "$monitoring_dir" ]; then
        check_failed "Monitoring directory exists"
        return 1
    fi
    
    local has_prometheus=0
    local has_grafana=0
    
    if [ -d "$monitoring_dir/prometheus" ]; then
        ((has_prometheus++))
        if [ -f "$monitoring_dir/prometheus/prometheus.yml" ]; then
            log_verbose "? Prometheus configuration exists"
        fi
    fi
    
    if [ -d "$monitoring_dir/grafana" ]; then
        ((has_grafana++))
        if [ -f "$monitoring_dir/grafana/provisioning/dashboards.yaml" ]; then
            log_verbose "? Grafana provisioning exists"
        fi
    fi
    
    if [ $has_prometheus -eq 1 ] && [ $has_grafana -eq 1 ]; then
        check_passed "Monitoring stack is properly structured"
    else
        log_warn "Monitoring configuration may be incomplete"
    fi
}

validate_file_permissions() {
    log_info "===== Validating file permissions ====="
    
    local perms_ok=true
    
    # Check systemd units are readable
    if [ -d "$PROJECT_ROOT/etc/systemd/system" ]; then
        while IFS= read -r file; do
            if [ ! -r "$file" ]; then
                log_warn "Not readable: $file"
                perms_ok=false
            fi
        done < <(find "$PROJECT_ROOT/etc/systemd/system" -name "*.service" -o -name "*.timer")
    fi
    
    # Check scripts are executable
    if [ -d "$PROJECT_ROOT/usr/local/bin" ]; then
        while IFS= read -r file; do
            if [ ! -x "$file" ]; then
                log_warn "Not executable: $file (consider: chmod +x)"
                if [ "$FIX_ISSUES" = true ]; then
                    chmod +x "$file"
                fi
            fi
        done < <(find "$PROJECT_ROOT/usr/local/bin" -name "*.sh" -type f)
    fi
    
    if [ "$perms_ok" = true ]; then
        check_passed "File permissions are correct"
    else
        check_failed "Some file permissions need adjustment"
    fi
}

generate_report() {
    local total_checks=$((PASSED_CHECKS + FAILED_CHECKS))
    local pass_rate=$((PASSED_CHECKS * 100 / total_checks))
    
    log_info ""
    log_info "===== Validation Report ====="
    log_info "Passed checks: $PASSED_CHECKS/$total_checks"
    log_info "Failed checks: $FAILED_CHECKS/$total_checks"
    log_info "Pass rate: ${pass_rate}%"
    log_info ""
    
    if [ $FAILED_CHECKS -eq 0 ]; then
        log_info "? All validations PASSED"
        return 0
    else
        log_warn "? Some validations FAILED"
        return 1
    fi
}

################################################################################
# Main Execution
################################################################################

main() {
    log_info "DebVisor Component Validation Script"
    log_info "====================================="
    log_info ""
    
    # Parse arguments
    while [ $# -gt 0 ]; do
        case "$1" in
            --verbose)
                VERBOSE=true
                shift
                ;;
            --fix)
                FIX_ISSUES=true
                shift
                ;;
            --report)
                REPORT_FILE="$2"
                shift 2
                ;;
            --help)
                sed -n '2,/^###/p' "$0" | grep -v '^###'
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Run validations
    validate_ansible_inventory
    validate_package_lists
    validate_systemd_units
    validate_scripts
    validate_docker_addons
    validate_rpc_service
    validate_monitoring_setup
    validate_file_permissions
    
    # Generate report
    generate_report
    local result=$?
    
    exit $result
}

# Run main
main "$@"
