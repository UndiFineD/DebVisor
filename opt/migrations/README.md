# Database Migrations

This directory contains Alembic migration scripts managed by Flask-Migrate.

## Usage

Initialize migrations (if not already done):
```bash
flask db init -d opt/migrations
```text
```text
flask db init -d opt/migrations
```text
```text
flask db init -d opt/migrations
```text
```text
```text
```text
Generate a migration:
```bash
```bash
Generate a migration:
```bash
```bash
Generate a migration:
```bash
```bash
```bash
```bash
flask db migrate -m "Description of change" -d opt/migrations
```text
```text
flask db migrate -m "Description of change" -d opt/migrations
```text
```text
flask db migrate -m "Description of change" -d opt/migrations
```text
```text
```text
```text
Apply migrations:
```bash
```bash
Apply migrations:
```bash
```bash
Apply migrations:
```bash
```bash
```bash
```bash
flask db upgrade -d opt/migrations
```text
```text
flask db upgrade -d opt/migrations
```text
```text
flask db upgrade -d opt/migrations
```text
```text
```text
```text
Rollback:
```bash
```bash
Rollback:
```bash
```bash
Rollback:
```bash
```bash
```bash
```bash
flask db downgrade -d opt/migrations
```text
```text
flask db downgrade -d opt/migrations
```text
```text
flask db downgrade -d opt/migrations
```text
```text
```text
```text
