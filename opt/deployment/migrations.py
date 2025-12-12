# !/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
Database Migration Support for DebVisor Phase 4

Provides database migration framework for schema versioning and upgrades.
Supports multiple databases (SQLite, PostgreSQL, MySQL).

Features:
- Migration versioning
- Rollback support
- Schema versioning
- Backward compatibility
- Migration validation
- Dry-run capability

Author: DebVisor Team
Date: 2025-11-26
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class MigrationType(Enum):
    """Types of database migrations"""

    CREATE_TABLE = "create_table"
    ADD_COLUMN = "add_column"
    DROP_COLUMN = "drop_column"
    MODIFY_COLUMN = "modify_column"
    CREATE_INDEX = "create_index"
    DROP_INDEX = "drop_index"
    ADD_CONSTRAINT = "add_constraint"
    DROP_CONSTRAINT = "drop_constraint"
    CUSTOM = "custom"


class MigrationStatus(Enum):
    """Migration execution status"""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class MigrationStep:
    """Single migration step"""

    step_id: int
    description: str
    migration_type: MigrationType
    up_sql: str    # SQL to apply migration
    down_sql: str    # SQL to rollback

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class Migration:
    """Database migration definition"""

    version: str    # e.g., "001_initial_schema"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    description: str = ""
    steps: List[MigrationStep] = field(default_factory=list)
    status: MigrationStatus = MigrationStatus.PENDING
    applied_at: Optional[datetime] = None
    rolled_back_at: Optional[datetime] = None
    error_message: Optional[str] = None

    def add_step(
        self,
        description: str,
        migration_type: MigrationType,
        up_sql: str,
        down_sql: str,
    ) -> MigrationStep:
        """Add migration step"""
        step_id = len(self.steps) + 1
        step = MigrationStep(
            step_id=step_id,
            description=description,
            migration_type=migration_type,
            up_sql=up_sql,
            down_sql=down_sql,
        )
        self.steps.append(step)
        return step

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        d["applied_at"] = self.applied_at.isoformat() if self.applied_at else None
        d["rolled_back_at"] = (
            self.rolled_back_at.isoformat() if self.rolled_back_at else None
        )
        d["status"] = self.status.value
        d["steps"] = [s.to_dict() for s in self.steps]
        return d


class MigrationExecutor(ABC):
    """Abstract migration executor"""

    @abstractmethod
    async def execute_migration(
        self, migration: Migration, dry_run: bool = False
    ) -> tuple[Any, ...]:
        """Execute migration and return (success, message)"""
        pass

    @abstractmethod
    async def rollback_migration(
        self, migration: Migration, dry_run: bool = False
    ) -> tuple[Any, ...]:
        """Rollback migration and return (success, message)"""
        pass

    @abstractmethod
    async def get_current_version(self) -> Optional[str]:
        """Get current schema version"""
        pass


class SQLiteMigrationExecutor(MigrationExecutor):
    """SQLite migration executor"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    async def connect(self) -> None:
        """Connect to database"""
        try:
            import sqlite3

            self.connection = sqlite3.connect(self.db_path)  # type: ignore[assignment]
            self.connection.row_factory = sqlite3.Row  # type: ignore[attr-defined]
            logger.info(f"Connected to SQLite: {self.db_path}")
        except Exception as e:
            logger.error(f"SQLite connection failed: {e}")
            raise

    async def disconnect(self) -> None:
        """Disconnect from database"""
        if self.connection:
            self.connection.close()
            self.connection = None

    async def execute_migration(
        self, migration: Migration, dry_run: bool = False
    ) -> tuple[Any, ...]:
        """Execute migration"""
        try:
            if not self.connection:
                await self.connect()

            cursor = self.connection.cursor()  # type: ignore[attr-defined]

            for step in migration.steps:
                logger.info(f"Executing: {step.description}")

                if not dry_run:
                    cursor.execute(step.up_sql)

            if not dry_run:
            # Record migration
                cursor.execute(
                    """
                    INSERT INTO debvisor_migrations
                    (version, description, applied_at, status)
                    VALUES (?, ?, ?, ?)
                """,
                    (
                        migration.version,
                        migration.description,
                        datetime.now(timezone.utc).isoformat(),
                        MigrationStatus.SUCCESS.value,
                    ),
                )
                self.connection.commit()  # type: ignore[attr-defined]
                migration.status = MigrationStatus.SUCCESS
                migration.applied_at = datetime.now(timezone.utc)

            return True, f"Migration {migration.version} executed successfully"

        except Exception as e:
            if self.connection:
                self.connection.rollback()
            migration.status = MigrationStatus.FAILED
            migration.error_message = str(e)
            logger.error(f"Migration failed: {e}")
            return False, f"Migration failed: {str(e)}"

    async def rollback_migration(
        self, migration: Migration, dry_run: bool = False
    ) -> tuple[Any, ...]:
        """Rollback migration"""
        try:
            if not self.connection:
                await self.connect()

            cursor = self.connection.cursor()  # type: ignore[attr-defined]

            # Execute rollback steps in reverse order
            for step in reversed(migration.steps):
                logger.info(f"Rolling back: {step.description}")

                if not dry_run:
                    cursor.execute(step.down_sql)

            if not dry_run:
            # Record rollback
                cursor.execute(
                    """
                    UPDATE debvisor_migrations
                    SET rolled_back_at = ?, status = ?
                    WHERE version = ?
                """,
                    (
                        datetime.now(timezone.utc).isoformat(),
                        MigrationStatus.ROLLED_BACK.value,
                        migration.version,
                    ),
                )
                self.connection.commit()  # type: ignore[attr-defined]
                migration.status = MigrationStatus.ROLLED_BACK
                migration.rolled_back_at = datetime.now(timezone.utc)

            return True, f"Migration {migration.version} rolled back successfully"

        except Exception as e:
            if self.connection:
                self.connection.rollback()
            logger.error(f"Rollback failed: {e}")
            return False, f"Rollback failed: {str(e)}"

    async def get_current_version(self) -> Optional[str]:
        """Get current schema version"""
        try:
            if not self.connection:
                await self.connect()

            cursor = self.connection.cursor()  # type: ignore[attr-defined]
            cursor.execute(
                """
                SELECT version FROM debvisor_migrations
                WHERE status = ?
                ORDER BY applied_at DESC
                LIMIT 1
            """,
                (MigrationStatus.SUCCESS.value,),
            )

            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting current version: {e}")
            return None


class MigrationManager:
    """Manage database migrations"""

    def __init__(self, executor: MigrationExecutor):
        self.executor = executor
        self.migrations: Dict[str, Migration] = {}

    def register_migration(self, migration: Migration) -> None:
        """Register migration"""
        self.migrations[migration.version] = migration

    async def apply_migrations(self, dry_run: bool = False) -> List[tuple[Any, ...]]:
        """Apply all pending migrations"""
        results = []
        current = await self.executor.get_current_version()

        for version in sorted(self.migrations.keys()):
            if current and version <= current:
                continue    # Already applied

            migration = self.migrations[version]
            logger.info(f"Applying migration: {version}")
            success, message = await self.executor.execute_migration(
                migration, dry_run=dry_run
            )
            results.append((version, success, message))

        return results

    async def rollback_migration(self, version: str, dry_run: bool = False) -> tuple[Any, ...]:
        """Rollback specific migration"""
        if version not in self.migrations:
            return False, f"Migration {version} not found"

        migration = self.migrations[version]
        return await self.executor.rollback_migration(migration, dry_run=dry_run)

    async def get_migration_history(self) -> List[Dict[str, Any]]:
        """Get migration history"""
        history = []
        for version in sorted(self.migrations.keys()):
            migration = self.migrations[version]
            history.append(migration.to_dict())
        return history

    async def get_status(self) -> Dict[str, Any]:
        """Get migration status"""
        current = await self.executor.get_current_version()

        pending = []
        applied = []

        for version in sorted(self.migrations.keys()):
            if current and version <= current:
                applied.append(version)
            else:
                pending.append(version)

        return {
            "current_version": current,
            "applied": applied,
            "pending": pending,
            "total": len(self.migrations),
        }


# Pre-defined migrations for Phase 4


def create_phase4_migrations() -> MigrationManager:
    """Create Phase 4 database migrations"""

    # SQLite executor
    executor = SQLiteMigrationExecutor(
        ":memory:"
    )    # Use :memory: for test or configure path
    manager = MigrationManager(executor)

    # Migration 001: Initial Schema
    m001 = Migration(
        version="001_initial_schema",
        description="Create initial database schema for Phase 4",
    )

    m001.add_step(
        description="Create User2FA table",
        migration_type=MigrationType.CREATE_TABLE,
        up_sql="""
            CREATE TABLE IF NOT EXISTS user_2fa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                totp_secret TEXT,
                totp_enabled BOOLEAN DEFAULT FALSE,
                totp_verified BOOLEAN DEFAULT FALSE,
                webauthn_enabled BOOLEAN DEFAULT FALSE,
                webauthn_verified BOOLEAN DEFAULT FALSE,
                backup_codes_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        down_sql="DROP TABLE IF EXISTS user_2fa",
    )

    m001.add_step(
        description="Create BackupCode table",
        migration_type=MigrationType.CREATE_TABLE,
        up_sql="""
            CREATE TABLE IF NOT EXISTS backup_code (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_2fa_id INTEGER NOT NULL,
                code_hash TEXT UNIQUE NOT NULL,
                sequence_number INTEGER NOT NULL,
                used BOOLEAN DEFAULT FALSE,
                used_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_2fa_id) REFERENCES user_2fa(id) ON DELETE CASCADE
            )
        """,
        down_sql="DROP TABLE IF EXISTS backup_code",
    )

    m001.add_step(
        description="Create ThemePreference table",
        migration_type=MigrationType.CREATE_TABLE,
        up_sql="""
            CREATE TABLE IF NOT EXISTS theme_preference (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                theme_mode TEXT DEFAULT 'light',
                custom_colors TEXT,
                accessibility_enabled BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        down_sql="DROP TABLE IF EXISTS theme_preference",
    )

    m001.add_step(
        description="Create BatchOperation table",
        migration_type=MigrationType.CREATE_TABLE,
        up_sql="""
            CREATE TABLE IF NOT EXISTS batch_operation (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                operation_type TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                total_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                parameters TEXT,
                results TEXT
            )
        """,
        down_sql="DROP TABLE IF EXISTS batch_operation",
    )

    m001.add_step(
        description="Create AuditLog table",
        migration_type=MigrationType.CREATE_TABLE,
        up_sql="""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                actor_id TEXT NOT NULL,
                action TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                resource_id TEXT NOT NULL,
                result TEXT,
                error_message TEXT,
                duration_ms FLOAT,
                ip_address TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        down_sql="DROP TABLE IF EXISTS audit_log",
    )

    m001.add_step(
        description="Create migration tracking table",
        migration_type=MigrationType.CREATE_TABLE,
        up_sql="""
            CREATE TABLE IF NOT EXISTS debvisor_migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version TEXT UNIQUE NOT NULL,
                description TEXT,
                applied_at TIMESTAMP,
                rolled_back_at TIMESTAMP,
                status TEXT DEFAULT 'pending',
                error_message TEXT
            )
        """,
        down_sql="DROP TABLE IF EXISTS debvisor_migrations",
    )

    manager.register_migration(m001)

    # Migration 002: Add indexes
    m002 = Migration(version="002_add_indexes", description="Add performance indexes")

    m002.add_step(
        description="Create indexes for audit logs",
        migration_type=MigrationType.CREATE_INDEX,
        up_sql="""
            CREATE INDEX IF NOT EXISTS idx_audit_log_actor
            ON audit_log(actor_id)
        """,
        down_sql="DROP INDEX IF EXISTS idx_audit_log_actor",
    )

    m002.add_step(
        description="Create indexes for batch operations",
        migration_type=MigrationType.CREATE_INDEX,
        up_sql="""
            CREATE INDEX IF NOT EXISTS idx_batch_operation_user
            ON batch_operation(user_id)
        """,
        down_sql="DROP INDEX IF EXISTS idx_batch_operation_user",
    )

    manager.register_migration(m002)

    return manager


class MigrationValidator:
    """Validate migrations"""

    @staticmethod
    def validate_migration(migration: Migration) -> tuple[Any, ...]:
        """Validate migration"""
        errors = []
        warnings = []

        # Check version format
        if not migration.version:
            errors.append("Migration version is required")

        # Check steps
        if not migration.steps:
            warnings.append("Migration has no steps")

        # Check SQL
        for step in migration.steps:
            if not step.up_sql:
                errors.append(f"Step {step.step_id} has no up SQL")
            if not step.down_sql:
                errors.append(f"Step {step.step_id} has no down SQL")

        return len(errors) == 0, errors, warnings
