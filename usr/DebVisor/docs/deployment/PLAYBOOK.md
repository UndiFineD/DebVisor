# Deployment Playbook

## Production Deployment Checklist

### Pre-Deployment

- [ ] **Code Review**: Ensure all PRs are approved and merged to `main`.
- [ ] **Tests**: Verify CI pipeline passed (Unit, Integration, E2E).
- [ ] **Backup**: Trigger a manual backup of the production database.

  ```bash

  debvisor-cli backup create --type full --tag pre-deploy-vX.Y.Z
```text
  debvisor-cli backup create --type full --tag pre-deploy-vX.Y.Z
```text

- [ ] **Migrations**: Check for pending database migrations.

  ```bash

- [ ] **Migrations**: Check for pending database migrations.

  ```bash

  debvisor-cli db check
```text
  debvisor-cli db check
```text

### Deployment Steps

1. **Pull Latest Image/Code**:

   ```bash
### Deployment Steps

1. **Pull Latest Image/Code**:

   ```bash

   git pull origin main
   # OR
   docker pull debvisor/debvisor:latest
```text
   git pull origin main
   # OR
   docker pull debvisor/debvisor:latest
```text

1. **Apply Migrations**:

   ```bash

1. **Apply Migrations**:

   ```bash

   debvisor-cli db upgrade
```text
   debvisor-cli db upgrade
```text

1. **Restart Services** (Rolling update if K8s, otherwise restart):

   ```bash

1. **Restart Services** (Rolling update if K8s, otherwise restart):

   ```bash

   systemctl restart debvisor
```text
   systemctl restart debvisor
```text

1. **Verify Health**:

   ```bash

1. **Verify Health**:

   ```bash

   curl -f <http://localhost:8080/health/live>
   curl -f <http://localhost:8080/health/ready>
```text
   curl -f <http://localhost:8080/health/live>
   curl -f <http://localhost:8080/health/ready>
```text

### Post-Deployment

- [ ] **Smoke Test**: Log in to the Web Panel and verify dashboard loads.
- [ ] **Monitor**: Watch error rates and latency for 15 minutes.

- --

## Rollback Procedures

If critical issues are detected:

1. **Revert Code/Image**:

   ```bash
### Post-Deployment

- [ ] **Smoke Test**: Log in to the Web Panel and verify dashboard loads.
- [ ] **Monitor**: Watch error rates and latency for 15 minutes.

- --

## Rollback Procedures

If critical issues are detected:

1. **Revert Code/Image**:

   ```bash

   # Docker
   docker tag debvisor/debvisor:previous debvisor/debvisor:latest
   docker-compose up -d
```text
   # Docker
   docker tag debvisor/debvisor:previous debvisor/debvisor:latest
   docker-compose up -d
```text

1. **Revert Database** (If migrations were applied and are destructive):

   ```bash

1. **Revert Database** (If migrations were applied and are destructive):

   ```bash

   debvisor-cli db downgrade -1
```text
   debvisor-cli db downgrade -1
```text

- Note: Only downgrade if data loss is acceptable or necessary.*

1. **Restore Backup** (Last Resort):

   ```bash

- Note: Only downgrade if data loss is acceptable or necessary.*

1. **Restore Backup** (Last Resort):

   ```bash

   debvisor-cli backup restore --tag pre-deploy-vX.Y.Z
```text
   debvisor-cli backup restore --tag pre-deploy-vX.Y.Z
```text

- --

## Health Check Validation

- **Liveness Probe**: `/health/live` - Returns 200 OK if process is running.
- **Readiness Probe**: `/health/ready` - Returns 200 OK if DB and Cache are connected.

- --

## Health Check Validation

- **Liveness Probe**: `/health/live` - Returns 200 OK if process is running.
- **Readiness Probe**: `/health/ready` - Returns 200 OK if DB and Cache are connected.
