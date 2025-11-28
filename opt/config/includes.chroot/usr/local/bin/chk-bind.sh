#!/bin/bash
# Simple Bind9 health probe for DebVisor

set -euo pipefail

if ! command -v dig >/dev/null 2>&1; then
	echo "chk-bind: dig command not found, skipping check" >&2
	exit 0
fi

if dig +time=1 +tries=1 @127.0.0.1 SOA debvisor.local >/dev/null 2>&1; then
	exit 0
else
	logger "DebVisor: Bind9 health check failed for debvisor.local SOA on 127.0.0.1"
	exit 1
fi