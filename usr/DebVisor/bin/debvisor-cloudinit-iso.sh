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

# DebVisor cloud-init ISO helper

set -euo pipefail

usage() {
  cat <<EOF
Usage: debvisor-cloudinit-iso.sh --name VMNAME --out PATH [options]

Creates a minimal cloud-init "cidata" ISO with user-data and meta-data
for use with cloud-style images under libvirt.

Required arguments:
  --name VMNAME       Logical VM name (used in meta-data and default hostname)
  --out PATH          Output ISO path (will be created; parent dir auto-created)

Optional arguments:
  --user-data FILE    Path to cloud-init user-data YAML to embed
  --meta-data FILE    Path to cloud-init meta-data YAML to embed
  --network-config FILE Path to network-config YAML
  --template          Enable variable substitution in input files
  --validate          Validate YAML syntax before building
  --dry-run           Show what would be done without making changes
  --help              Show this help message

If user-data or meta-data are not provided, conservative defaults are used.

Examples:
  debvisor-cloudinit-iso.sh --name vm1 --out /var/lib/libvirt/images/vm1-seed.iso
EOF
}

# Source shared library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/debvisor-lib.sh"

################################################################################
# Script Configuration
################################################################################

readonly SCRIPT_VERSION="2.0.0"
VMNAME=""
OUT_PATH=""
USER_DATA_SRC=""
META_DATA_SRC=""
NETWORK_CONFIG_SRC=""
ENABLE_TEMPLATING=false
ENABLE_VALIDATION=false

################################################################################
# Helper Functions
################################################################################

show_help() {
    sed -n '2,/^###/p' "$0" | grep -v '^###' | head -30
}

parse_arguments() {
    while [ $# -gt 0 ]; do
        case "$1" in
            --name)
                VMNAME="$2"
                shift 2
                ;;
            --out)
                OUT_PATH="$2"
                shift 2
                ;;
            --user-data)
                USER_DATA_SRC="$2"
                shift 2
                ;;
            --meta-data)
                META_DATA_SRC="$2"
                shift 2
                ;;
            --network-config)
                NETWORK_CONFIG_SRC="$2"
                shift 2
                ;;
            --template)
                ENABLE_TEMPLATING=true
                shift
                ;;
            --validate)
                ENABLE_VALIDATION=true
                shift
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
            *)
                log_error "Unknown argument: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

validate_arguments() {
    if [ -z "$VMNAME" ] || [ -z "$OUT_PATH" ]; then
        log_error "--name and --out are required."
        show_help
        exit 1
    fi
}

check_prerequisites() {
    log_info "===== Checking prerequisites ====="

    if command -v genisoimage >/dev/null 2>&1; then
        ISO_CMD="genisoimage"
    elif command -v mkisofs >/dev/null 2>&1; then
        ISO_CMD="mkisofs"
    else
        log_error "genisoimage or mkisofs is required."
        exit 1
    fi

    if [ "$ENABLE_VALIDATION" = true ]; then
        require_bin "cloud-init" "cloud-init (for schema validation)"
    fi

    log_info "Using ISO builder: $ISO_CMD"
}

process_file() {
    local src="$1"
    local dst="$2"
    local type="$3"

    if [ -n "$src" ]; then
        if [ ! -f "$src" ]; then
            log_error "$type file not found: $src"
            exit 1
        fi

        if [ "$ENABLE_TEMPLATING" = true ]; then
            log_info "Processing template for $type..."
            # Simple envsubst-like replacement for specific variables
            # We use sed to avoid replacing everything in the environment
            sed "s|{{VMNAME}}|$VMNAME|g" "$src" > "$dst"
        else
            cp "$src" "$dst"
        fi

        if [ "$ENABLE_VALIDATION" = true ]; then
            log_info "Validating $type..."
            if ! cloud-init schema --config-file "$dst" &>/dev/null; then
                log_warn "$type validation failed (schema check). Proceeding anyway, but check your YAML."
                # We don't exit here because cloud-init schema check can be finicky
            else
                log_info "? $type valid"
            fi
        fi
    else
        # Generate defaults
        log_info "Generating default $type..."
        case "$type" in
            "user-data")
                cat >"$dst" <<EOF
#cloud-config
users:
  - default
hostname: $VMNAME
ssh_pwauth: false
EOF
                ;;
            "meta-data")
                cat >"$dst" <<EOF
instance-id: $VMNAME
local-hostname: $VMNAME
EOF
                ;;
            "network-config")
                # Optional, don't create if not requested
                ;;
        esac
    fi
}

build_iso() {
    local workdir
    workdir=$(mktemp -d)
    trap 'rm -rf "$workdir"' EXIT

    log_info "===== Preparing ISO content ====="

    process_file "$USER_DATA_SRC" "$workdir/user-data" "user-data"
    process_file "$META_DATA_SRC" "$workdir/meta-data" "meta-data"

    if [ -n "$NETWORK_CONFIG_SRC" ]; then
        process_file "$NETWORK_CONFIG_SRC" "$workdir/network-config" "network-config"
    fi

    mkdir -p "$(dirname "$OUT_PATH")"

    if [ "$DEBVISOR_DRY_RUN" = true ]; then
        log_info "Dry-run: Would build ISO at $OUT_PATH with content from $workdir"
        ls -l "$workdir"
        return 0
    fi

    log_info "Building ISO image..."
    if "$ISO_CMD" -output "$OUT_PATH" -volid cidata -joliet -rock "$workdir"/* &>/dev/null; then
        log_info "? ISO created successfully: $OUT_PATH"
    else
        log_error "Failed to create ISO image"
        return 1
    fi
}

verify_iso() {
    if [ "$DEBVISOR_DRY_RUN" = true ]; then return 0; fi

    if [ ! -f "$OUT_PATH" ]; then
        log_error "ISO file was not created"
        return 1
    fi

    local size
    size=$(du -h "$OUT_PATH" | cut -f1)
    log_info "ISO Size: $size"
}

################################################################################
# Main Execution
################################################################################

main() {
    log_info "DebVisor Cloud-Init ISO Generator v${SCRIPT_VERSION}"

    parse_arguments "$@"
    validate_arguments
    check_prerequisites

    build_iso
    verify_iso

    audit_log "iso_create" "Created cloud-init ISO for $VMNAME" "success"
}

# Run main
main "$@"

VMNAME=""
OUT=""
USER_DATA_SRC=""
META_DATA_SRC=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      VMNAME="$2"; shift 2;;
    --out)
      OUT="$2"; shift 2;;
    --user-data)
      USER_DATA_SRC="$2"; shift 2;;
    --meta-data)
      META_DATA_SRC="$2"; shift 2;;
    -h|--help)
      usage; exit 0;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1;;
  esac
done

if [[ -z "$VMNAME" || -z "$OUT" ]]; then
  echo "--name and --out are required." >&2
  usage
  exit 1
fi

if ! command -v genisoimage >/dev/null 2>&1 && ! command -v mkisofs >/dev/null 2>&1; then
  echo "genisoimage or mkisofs is required to build the cloud-init ISO." >&2
  exit 1
fi

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

mkdir -p "$WORKDIR"

# user-data
if [[ -n "$USER_DATA_SRC" ]]; then
  if [[ ! -f "$USER_DATA_SRC" ]]; then
    echo "user-data file not found: $USER_DATA_SRC" >&2
    exit 1
  fi
  cp "$USER_DATA_SRC" "$WORKDIR/user-data"
else
  cat >"$WORKDIR/user-data" <<EOF
#cloud-config
users:
  - default
hostname: $VMNAME
ssh_pwauth: false
EOF
fi

# meta-data
if [[ -n "$META_DATA_SRC" ]]; then
  if [[ ! -f "$META_DATA_SRC" ]]; then
    echo "meta-data file not found: $META_DATA_SRC" >&2
    exit 1
  fi
  cp "$META_DATA_SRC" "$WORKDIR/meta-data"
else
  cat >"$WORKDIR/meta-data" <<EOF
instance-id: $VMNAME
local-hostname: $VMNAME
EOF
fi

mkdir -p "$(dirname "$OUT")"

ISO_CMD=""
if command -v genisoimage >/dev/null 2>&1; then
  ISO_CMD="genisoimage"
else
  ISO_CMD="mkisofs"
fi

echo "Building cloud-init ISO at $OUT"
$ISO_CMD -output "$OUT" -volid cidata -joliet -rock "$WORKDIR/user-data" "$WORKDIR/meta-data"

echo "Cloud-init ISO created: $OUT"
