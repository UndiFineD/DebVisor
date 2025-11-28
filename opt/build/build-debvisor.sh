#!/usr/bin/env bash
# Build script for DebVisor ISO
set -euo pipefail

usage() {
    cat <<EOF
Usage: $(basename "$0") [options]

Environment variables:
    DEBVISOR_DIST                 Target Debian distribution (default: trixie)
    DEBVISOR_FAST                 0 = clean+config (default), 1 = skip clean, 2 = skip clean+config
    DEBVISOR_ARCH                 Target architecture (default: amd64)
    DEBVISOR_VERSION              Optional version tag used in ISO filename
    DEBVISOR_MIRROR_BOOTSTRAP     Override live-build bootstrap mirror URL
    DEBVISOR_MIRROR_BINARY        Override live-build binary mirror URL
    DEBVISOR_FIRMWARE_CHROOT      Include firmware in chroot (boolean, default: true)
    DEBVISOR_FIRMWARE_BINARY      Include firmware in binary (boolean, default: true)
    DEBVISOR_DRYRUN               1 = validate and configure only, no lb build
    DEBVISOR_SIGN_ISO             1 = create sha256 and optional GPG signature
    DEBVISOR_GPG_KEY              GPG key ID to use when signing (optional)

Options:
    -h, --help      Show this help message and exit
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
    -h|--help)
        usage
        exit 0
        ;;
    *)
        echo "[DebVisor] Unknown argument: $1" >&2
        usage >&2
        exit 1
        ;;
    esac
done

DEBVISOR_DIST="${DEBVISOR_DIST:-trixie}"
DEBVISOR_FAST="${DEBVISOR_FAST:-0}"
DEBVISOR_ARCH="${DEBVISOR_ARCH:-amd64}"
DEBVISOR_VERSION="${DEBVISOR_VERSION:-}"
DEBVISOR_MIRROR_BOOTSTRAP="${DEBVISOR_MIRROR_BOOTSTRAP:-http://deb.debian.org/debian/}"
DEBVISOR_MIRROR_BINARY="${DEBVISOR_MIRROR_BINARY:-http://deb.debian.org/debian/}"
DEBVISOR_FIRMWARE_CHROOT="${DEBVISOR_FIRMWARE_CHROOT:-true}"
DEBVISOR_FIRMWARE_BINARY="${DEBVISOR_FIRMWARE_BINARY:-true}"

normalize_bool() {
    case "${1,,}" in
        1|true|yes|on)
            echo "true"
            ;;
        0|false|no|off)
            echo "false"
            ;;
        *)
            echo "[DebVisor] ERROR: Invalid boolean value: $1" >&2
            exit 1
            ;;
    esac
}

DEBVISOR_FIRMWARE_CHROOT="$(normalize_bool "${DEBVISOR_FIRMWARE_CHROOT}")"
DEBVISOR_FIRMWARE_BINARY="$(normalize_bool "${DEBVISOR_FIRMWARE_BINARY}")"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "${script_dir}/.." && pwd)"

cd "${project_root}"

if ! command -v lb >/dev/null; then
    echo "live-build not installed. Install prerequisites first." >&2
    exit 1
fi

if [ ! -f /etc/debian_version ]; then
    echo "[DebVisor] WARNING: This script is intended to run on Debian-based hosts." >&2
else
    host_debian="$(cut -d. -f1 < /etc/debian_version 2>/dev/null || echo "")"
    case "${host_debian}" in
        '' )
            echo "[DebVisor] WARNING: Unable to parse /etc/debian_version; continuing without version check." >&2 ;;
        * )
            # For now we only warn if running on releases older than bookworm (12).
            if [ "${host_debian}" -lt 12 ] 2>/dev/null; then
                echo "[DebVisor] WARNING: Host Debian release (${host_debian}) is older than recommended (bookworm/12+)." >&2
            fi
            ;;
    esac
fi

for bin in debootstrap xorriso; do
    if ! command -v "$bin" >/dev/null 2>&1; then
        echo "[DebVisor] ERROR: Required tool missing: $bin" >&2
        exit 1
    fi
done

if ! command -v shellcheck >/dev/null 2>&1; then
    echo "[DebVisor] WARNING: shellcheck not found; build scripts will not be linted. Install it with 'apt install shellcheck' on Debian-based hosts." >&2
fi

if [ "${DEBVISOR_SIGN_ISO:-0}" = "1" ] && ! command -v gpg >/dev/null 2>&1; then
    echo "[DebVisor] ERROR: DEBVISOR_SIGN_ISO=1 but gpg is not installed." >&2
    exit 1
fi

trap 'echo "[DebVisor] ERROR: build failed" >&2' ERR

echo "[DebVisor] Project root: ${project_root}"
echo "[DebVisor] Target distribution: ${DEBVISOR_DIST}"
echo "[DebVisor] FAST mode: ${DEBVISOR_FAST} (0=clean,1=no-clean)"
echo "[DebVisor] Architecture: ${DEBVISOR_ARCH}"
if [ -n "${DEBVISOR_VERSION}" ]; then
    echo "[DebVisor] Version tag: ${DEBVISOR_VERSION}"
fi
echo "[DebVisor] Mirror (bootstrap): ${DEBVISOR_MIRROR_BOOTSTRAP}"
echo "[DebVisor] Mirror (binary):    ${DEBVISOR_MIRROR_BINARY}"
echo "[DebVisor] Firmware flags:     chroot=${DEBVISOR_FIRMWARE_CHROOT}, binary=${DEBVISOR_FIRMWARE_BINARY}"

case "${DEBVISOR_ARCH}" in
    amd64|arm64)
        ;;
    *)
        echo "[DebVisor] ERROR: Unsupported DEBVISOR_ARCH: ${DEBVISOR_ARCH} (allowed: amd64, arm64)" >&2
        exit 1
        ;;
esac

if [ ! -f config/preseed.cfg ]; then
    echo "[DebVisor] WARNING: config/preseed.cfg not found in project root" >&2
fi

required_paths=(
    "config/package-lists"
    "config/includes.chroot"
)

for path in "${required_paths[@]}"; do
    if [ ! -e "${path}" ]; then
        echo "[DebVisor] ERROR: required path missing: ${path}" >&2
        exit 1
    fi
done

SKIP_CONFIG=0
case "${DEBVISOR_FAST}" in
    0)
        echo "[DebVisor] FAST=0: full clean & re-configure"
        lb clean || true
        ;;
    1)
        echo "[DebVisor] FAST=1: skipping clean, will re-configure"
        ;;
    2)
        echo "[DebVisor] FAST=2: skipping clean and config"
        SKIP_CONFIG=1
        ;;
    *)
        echo "[DebVisor] ERROR: Invalid DEBVISOR_FAST: ${DEBVISOR_FAST} (use 0,1,2)" >&2
        exit 1
        ;;
esac

if [ "${SKIP_CONFIG}" -ne 1 ]; then
    echo "[DebVisor] Configuring live-build"
    lb config \
    --mode debian \
    --distribution "${DEBVISOR_DIST}" \
    --binary-images iso-hybrid \
    --architectures "${DEBVISOR_ARCH}" \
    --linux-flavours "${DEBVISOR_ARCH}" \
    --apt-recommends true \
    --archive-areas "main contrib non-free non-free-firmware" \
    --debian-installer live \
    --debian-installer-gui false \
    --debian-installer-preseed config/preseed.cfg \
    --bootloaders grub-efi \
    --system live \
    --firmware-chroot "${DEBVISOR_FIRMWARE_CHROOT}" \
    --firmware-binary "${DEBVISOR_FIRMWARE_BINARY}" \
    --updates true \
    --security true \
    --backports true \
    --iso-application "DebVisor" \
    --iso-volume "DebVisor" \
    --mirror-bootstrap "${DEBVISOR_MIRROR_BOOTSTRAP}" \
    --mirror-binary "${DEBVISOR_MIRROR_BINARY}" \
    --grub-splash none
fi

echo "[DebVisor] Syncing addons playbook (if script present)"
if [ -x build/sync-addons-playbook.sh ]; then
    build/sync-addons-playbook.sh
else
    echo "[DebVisor] Skipping addons sync (build/sync-addons-playbook.sh not executable)"
fi

if [ "${DEBVISOR_SELFTEST:-0}" = "1" ]; then
    echo "[DebVisor] SELFTEST mode enabled: running lb config only (no build)"
    exit 0
fi

if [ "${DEBVISOR_DRYRUN:-0}" = "1" ]; then
    echo "[DebVisor] DRYRUN enabled: configuration validated, skipping lb build"
    exit 0
fi

echo "[DebVisor] Building ISO (this can take a while)"
lb build
iso_name() {
    if [ -n "${DEBVISOR_VERSION}" ]; then
        printf 'debvisor-%s-%s.hybrid.iso\n' "${DEBVISOR_VERSION}" "${DEBVISOR_ARCH}"
    else
        printf 'live-image-%s.hybrid.iso\n' "${DEBVISOR_ARCH}"
    fi
}

ISO="$(iso_name)"
if [ -f "${ISO}" ]; then
    if command -v readlink >/dev/null 2>&1; then
        ISO_PATH="$(readlink -f "${ISO}" 2>/dev/null || echo "${ISO}")"
    else
        ISO_PATH="${ISO}"
    fi
    echo "[DebVisor] Build complete: ${ISO_PATH}"
else
    echo "[DebVisor] Build finished but ISO not found" >&2
    exit 1
fi

if [ "${DEBVISOR_SIGN_ISO:-0}" = "1" ]; then
    echo "[DebVisor] Generating SHA256 checksum for ISO"
    sha256sum "${ISO}" > "${ISO}.sha256"

    if command -v gpg >/dev/null 2>&1; then
        if [ -n "${DEBVISOR_GPG_KEY:-}" ]; then
            echo "[DebVisor] Creating detached GPG signature with key: ${DEBVISOR_GPG_KEY}"
            gpg --local-user "${DEBVISOR_GPG_KEY}" --detach-sign --armor "${ISO}"
        else
            echo "[DebVisor] Creating detached GPG signature with default key"
            gpg --detach-sign --armor "${ISO}"
        fi
    else
        echo "[DebVisor] WARNING: gpg not found; skipping ISO signature" >&2
    fi
fi

if [ -x build/test-firstboot.sh ]; then
    echo "[DebVisor] You can run post-build tests with: build/test-firstboot.sh"
fi
