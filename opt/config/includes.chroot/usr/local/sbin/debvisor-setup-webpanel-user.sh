#!/bin/sh
set -eu

if ! id webpanel >/dev/null 2>&1; then
    addgroup --system webpanel >/dev/null 2>&1 || true
    adduser \
        --system \
        --ingroup webpanel \
        --home /opt/debvisor/panel \
        --no-create-home \
        --shell /usr/sbin/nologin \
        webpanel >/dev/null 2>&1 || true
fi

if [ -d /opt/debvisor/panel ]; then
    chown -R webpanel:webpanel /opt/debvisor/panel || true
fi
