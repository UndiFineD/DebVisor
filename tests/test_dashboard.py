import pytest
from flask import Flask
from opt.web.dashboard.app import dashboard_bp


@pytest.fixture
def app() -> None:
    app = Flask(__name__)
    app.register_blueprint(dashboard_bp)
    return app  # type: ignore[return-value]


@pytest.fixture
def client(app):
    return app.test_client()


def test_dashboard_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"DebVisor Operations Dashboard" in response.data


def test_api_stats(client):
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.get_json()
    assert "cpu_percent" in data
    assert "memory" in data
    assert "disk" in data


def test_api_alerts(client):
    response = client.get("/api/alerts")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "message" in data[0]