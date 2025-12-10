"""
Tests for the standardized health check blueprint.
"""

import unittest
from flask import Flask
from opt.core.health import create_health_blueprint


class TestHealthBlueprint(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        self.client = self.app.test_client()

    def test_liveness(self) -> None:
        bp = create_health_blueprint("test-service")
        self.app.register_blueprint(bp)

        response = self.client.get("/health/live")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["service"], "test-service")

    def test_readiness_success(self) -> None:
        def check_ok() -> None:
            return {"status": "ok", "message": "All good"}  # type: ignore[return-value]

        bp = create_health_blueprint("test-service", {"db": check_ok})  # type: ignore[dict-item]
        self.app.register_blueprint(bp)

        response = self.client.get("/health/ready")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "ready")
        self.assertEqual(data["checks"]["db"]["status"], "ok")

    def test_readiness_failure(self) -> None:
        def check_fail() -> None:
            return {"status": "error", "message": "DB down"}  # type: ignore[return-value]

        bp = create_health_blueprint("test-service", {"db": check_fail})  # type: ignore[dict-item]
        self.app.register_blueprint(bp)

        response = self.client.get("/health/ready")
        self.assertEqual(response.status_code, 503)
        data = response.get_json()
        self.assertEqual(data["status"], "not_ready")
        self.assertEqual(data["checks"]["db"]["status"], "error")

    def test_readiness_exception(self) -> None:
        def check_raise() -> None:
            raise Exception("Boom")

        bp = create_health_blueprint("test-service", {"db": check_raise})  # type: ignore[dict-item]
        self.app.register_blueprint(bp)

        response = self.client.get("/health/ready")
        self.assertEqual(response.status_code, 503)
        data = response.get_json()
        self.assertEqual(data["status"], "not_ready")
        self.assertEqual(data["checks"]["db"]["status"], "error")
        self.assertIn("Boom", data["checks"]["db"]["message"])


if __name__ == '__main__':
    unittest.main()