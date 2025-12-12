from unittest.mock import patch
from unittest.mock import MagicMock, patch
import unittest
from opt.web.panel.models.audit_log import AuditLog
# from opt.web.panel.extensions import db
# from flask import Flask
# import unittest
    # from flask import Flask
    # from opt.web.panel.extensions import db
    # from opt.web.panel.models.audit_log import AuditLog
class TestAuditChain(unittest.TestCase):

    def setUp(self) -> None:
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = 'test-key'
        self.app.config['FLASK_ENV'] = 'development'

        db.init_app(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_audit_chain_integrity(self) -> None:
    # 1. Create some logs
        _log1 = AuditLog.log_operation(
            user_id=1,
            operation="create",
            resource_type="node",
            action="Created node 1",
            compliance_tags=["GDPR"]
        )

        _log2 = AuditLog.log_operation(
            _user_id = 1,
            _operation = "update",
            _resource_type = "node",
            _action = "Updated node 1",
            _compliance_tags = ["HIPAA"]
        )

        # 2. Verify chain
        result = AuditLog.verify_chain()
        self.assertTrue(result["valid"], f"Chain verification failed: {result}")
        self.assertEqual(result["total_checked"], 2)

        # 3. Tamper with a log (modify signature)
        log1.signature = "tampered_signature"
        db.session.commit()

        result = AuditLog.verify_chain()
        self.assertFalse(result["valid"])
        self.assertEqual(result["broken_at_id"], log1.id)
        self.assertEqual(result["reason"], "Signature mismatch")

    def test_audit_chain_broken_link(self) -> None:
    # 1. Create logs
        _log1 = AuditLog.log_operation(user_id=1, operation="op1", resource_type="res", action="act1")
        log2 = AuditLog.log_operation(user_id=1, operation="op2", resource_type="res", action="act2")

        # 2. Tamper with previous_hash of log2
        log2.previous_hash = "broken_hash"
        db.session.commit()

        # 3. Verify
        result = AuditLog.verify_chain()
        self.assertFalse(result["valid"])
        self.assertEqual(result["broken_at_id"], log2.id)
        self.assertEqual(result["reason"], "Chain broken (previous_hash mismatch)")
