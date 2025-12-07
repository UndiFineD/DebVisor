# DebVisor Troubleshooting Guide

## Overview
This guide provides step-by-step resolution procedures for common failure scenarios in the DebVisor platform.

## Table of Contents
1. [Service Startup Failures](#service-startup-failures)
2. [Database Connection Issues](#database-connection-issues)
3. [WebSocket/Real-time Updates Failing](#websocketreal-time-updates-failing)
4. [Performance Degradation](#performance-degradation)
5. [Escalation Paths](#escalation-paths)

---

## Service Startup Failures

### Symptoms
- Service fails to start via systemd
- `systemctl status debvisor` shows `failed`
- Error logs in `/var/log/debvisor/error.log`

### Diagnosis Steps
1. Check systemd logs:
   ```bash
   journalctl -u debvisor -n 50 --no-pager
   ```
2. Verify configuration validity:
   ```bash
   debvisor-cli config validate
   ```
3. Check port availability (default 8080):
   ```bash
   netstat -tulpn | grep 8080
   ```

### Resolution
- **Config Error**: Fix syntax errors in `/etc/debvisor/config.yaml`.
- **Port Conflict**: Change port in config or stop conflicting service.
- **Permission Denied**: Ensure `debvisor` user owns `/opt/debvisor` and `/var/lib/debvisor`.

---

## Database Connection Issues

### Symptoms
- "Internal Server Error" on API requests
- Logs show `OperationalError` or `FATAL: password authentication failed`

### Diagnosis Steps
1. Verify PostgreSQL status:
   ```bash
   systemctl status postgresql
   ```
2. Test connection manually:
   ```bash
   pg_isready -h localhost -p 5432
   ```
3. Check connection pool metrics (if enabled).

### Resolution
- Restart PostgreSQL: `systemctl restart postgresql`
- Verify credentials in `.env` or `config.yaml`.
- Check firewall rules allowing localhost traffic.

---

## WebSocket/Real-time Updates Failing

### Symptoms
- Dashboard metrics are stale
- "Connection lost" banner in UI
- Browser console shows WebSocket connection errors (400/1006)

### Diagnosis Steps
1. Check Nginx proxy configuration for WebSocket upgrade headers:
   ```nginx
   proxy_set_header Upgrade $http_upgrade;
   proxy_set_header Connection "upgrade";
   ```
2. Verify Socket.IO server logs.

### Resolution
- Fix Nginx config.
- Ensure client and server Socket.IO versions match.

---

## Escalation Paths

If the issue persists after following these steps:

1. **Level 1**: Create an internal ticket with logs and reproduction steps.
2. **Level 2**: Contact the DevOps Lead (devops@debvisor.internal).
3. **Level 3**: Emergency PagerDuty for production outages.
