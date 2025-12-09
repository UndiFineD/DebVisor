# Database Migrations

This directory contains Alembic migration scripts managed by Flask-Migrate.

## Usage

Initialize migrations (if not already done):

```bash

flask db init -d opt/migrations

```text

Generate a migration:

```bash

flask db migrate -m "Description of change" -d opt/migrations

```text

Apply migrations:

```bash

flask db upgrade -d opt/migrations

```text

Rollback:

```bash

flask db downgrade -d opt/migrations

```text

