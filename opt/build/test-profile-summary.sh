#!/usr/bin/env bash
set -euo pipefail

# Smoke test for debvisor-profile-summary.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
HELPER="${ROOT_DIR}/config/includes.chroot/usr/local/sbin/debvisor-profile-summary.sh"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "${TMPDIR}"' EXIT

if [[ ! -x "${HELPER}" ]]; then
  echo "Helper not found or not executable: ${HELPER}" >&2
  exit 1
fi

profiles=(ceph zfs usb-zfs)

# Create a fake filesystem layout once
mkdir -p "${TMPDIR}/etc" "${TMPDIR}/var/log/debvisor"

for p in "${profiles[@]}"; do
  echo "Testing profile: $p"
  echo "$p" > "${TMPDIR}/etc/debvisor-profile"

  # Clean previous outputs
  rm -f "${TMPDIR}/var/log/debvisor/profile-summary.txt" "${TMPDIR}/var/log/debvisor/profile-summary.json"

  # Run helper in a chroot-like environment by overriding paths
  (
    cd "${TMPDIR}" || exit 1
    ln -sf "${TMPDIR}/etc" /etc 2>/dev/null || true
    ln -sf "${TMPDIR}/var" /var 2>/dev/null || true
    bash "${HELPER}"
  )

  TXT_OUT="${TMPDIR}/var/log/debvisor/profile-summary.txt"
  JSON_OUT="${TMPDIR}/var/log/debvisor/profile-summary.json"

  if [[ ! -s "${TXT_OUT}" ]]; then
    echo "Missing or empty ${TXT_OUT} for profile $p" >&2
    exit 1
  fi
  if [[ ! -s "${JSON_OUT}" ]]; then
    echo "Missing or empty ${JSON_OUT} for profile $p" >&2
    exit 1
  fi

  grep -qi "DebVisor storage profile: $p" "${TXT_OUT}" || {
    echo "Text summary does not contain expected profile $p" >&2
    cat "${TXT_OUT}" >&2
    exit 1
  }
  jq -e ".profile == \"$p\"" "${JSON_OUT}" >/dev/null 2>&1 || {
    echo "JSON does not report expected profile $p" >&2
    cat "${JSON_OUT}" >&2
    exit 1
  }
done

echo "debvisor-profile-summary.sh smoke test passed for profiles: ${profiles[*]}"
