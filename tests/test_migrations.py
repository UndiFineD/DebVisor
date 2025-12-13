from flask import Flask
from sqlalchemy import inspect
from unittest.mock import patch, MagicMock
import unittest
from flask_migrate import Migrate, upgrade, downgrade
from opt.web.panel.extensions import db


class TestMigrations(unittest.TestCase):

    def setUp(self) -> None:
        self.app = Flask(__name__)
        # Use in-memory SQLite for speed and isolation
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = 'test-key'

        # Initialize extensions with test app
        db.init_app(self.app)
        self.migrate = Migrate(self.app, db, directory='opt/migrations')

        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self) -> None:
        db.session.remove()
        self.app_context.pop()

    def test_migration_upgrade_downgrade(self) -> None:
        """Test that migrations can be applied and rolled back."""
        # 1. Upgrade to head
        try:
            upgrade()
        except Exception as e:
            self.fail(f"Migration upgrade failed: {e}")

        # 2. Verify tables exist
        inspector = inspect(db.engine)  # type: ignore[operator]
        tables = inspector.get_table_names()

        self.assertIn('alembic_version', tables)
        self.assertIn('user', tables)
        # Add other tables if they are in the initial migration

        # 3. Downgrade to base
        try:
            downgrade(revision='base')
        except Exception as e:
            self.fail(f"Migration downgrade failed: {e}")

        # 4. Verify tables are gone
        inspector = inspect(db.engine)  # type: ignore[operator]
        tables = inspector.get_table_names()

        self.assertNotIn('user', tables)
