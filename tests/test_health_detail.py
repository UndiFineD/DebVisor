import os
import pytest


@pytest.fixture
def app_client() -> None:
    os.environ.setdefault("FLASK_ENV", "testing")
    os.environ["RATELIMIT_STORAGE_URI"] = "memory://"
    try:
        import sys

        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        from opt.web.panel.app import create_app
    except SystemExit:
        pytest.skip(
            "Flask app dependencies not installed; skipping health_detail tests"
        )
    except ImportError:
        pytest.skip("Import error for Flask app; skipping health_detail tests")

    import warnings

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="Using the in-memory storage for tracking rate limits",
        )
        app = create_app("production")

    app.testing = True

    # Mock user for RBAC
    from opt.web.panel.app import login_manager

    class MockUser:
        is_authenticated = True
        is_active = True
        is_anonymous = False
        role = "admin"
        email = "test@example.com"

        def get_id(self) -> None:
            return "1"

    @login_manager.user_loader
    def load_user(user_id):
        return MockUser()

    client = app.test_client()
    with client.session_transaction() as sess:
        sess["_user_id"] = "1"
        sess["_fresh"] = True

    return client


def test_health_detail_ok(app_client):
    resp = app_client.get("/health/detail", base_url="https://localhost")
    if resp.status_code == 301:
        print(f"Redirecting to: {resp.headers.get('Location')}")
    assert resp.status_code in (200, 503)
    data = resp.get_json()
    assert "build" in data
    assert "checks" in data
    assert "database" in data["checks"]
    assert "redis" in data["checks"]
    assert "smtp" in data["checks"]
    assert data["status"] in ("ok", "degraded")


def test_health_detail_with_envs(app_client, monkeypatch):
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_STARTTLS", "true")

    resp = app_client.get("/health/detail", base_url="https://localhost")
    assert resp.status_code in (200, 503)
    data = resp.get_json()
    assert "checks" in data
    assert "redis" in data["checks"]
    assert "smtp" in data["checks"]
