#!/bin/sh
set -eu

if ! id debvisor-rpc >/dev/null 2>&1; then
    addgroup --system debvisor-rpc >/dev/null 2>&1 || true
    adduser \
        --system \
        --ingroup debvisor-rpc \
        --home /opt/debvisor/rpc \
        --no-create-home \
        --shell /usr/sbin/nologin \
        debvisor-rpc >/dev/null 2>&1 || true
fi

if [ -d /opt/debvisor/rpc ]; then
    chown -R debvisor-rpc:debvisor-rpc /opt/debvisor/rpc || true
fi
