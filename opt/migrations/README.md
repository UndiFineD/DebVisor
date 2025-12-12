# Database Migrations

This directory contains Alembic migration scripts managed by Flask-Migrate.

## Usage

Initialize migrations (if not already done):
```bash

flask db init -d opt/migrations
```text

flask db init -d opt/migrations
```text
flask db init -d opt/migrations
```text
```text

Generate a migration:
```bash

Generate a migration:
```bash
Generate a migration:
```bash
```bash

flask db migrate -m "Description of change" -d opt/migrations
```text

flask db migrate -m "Description of change" -d opt/migrations
```text
flask db migrate -m "Description of change" -d opt/migrations
```text
```text

Apply migrations:
```bash

Apply migrations:
```bash
Apply migrations:
```bash
```bash

flask db upgrade -d opt/migrations
```text

flask db upgrade -d opt/migrations
```text
flask db upgrade -d opt/migrations
```text
```text

Rollback:
```bash

Rollback:
```bash
Rollback:
```bash
```bash

flask db downgrade -d opt/migrations
```text

flask db downgrade -d opt/migrations
```text
flask db downgrade -d opt/migrations
```text
```text
