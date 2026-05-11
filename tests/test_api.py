from fastapi.testclient import TestClient

from backend.app.main import app


def test_health_endpoint_returns_ok():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_providers_endpoint_returns_provider_statuses():
    client = TestClient(app)

    response = client.get("/providers")

    assert response.status_code == 200
    data = response.json()
    assert "primary-openai-mock" in data
    assert data["primary-openai-mock"]["status"] in {"healthy", "degraded", "down"}


def test_set_failure_mode_endpoint_updates_failure_mode():
    client = TestClient(app)

    response = client.post("/failure-mode", json={"mode": "timeout"})

    assert response.status_code == 200
    assert response.json()["failure_mode"] == "timeout"


def test_run_demo_endpoint_returns_completed_workflow_with_trace():
    client = TestClient(app)
    client.post("/failure-mode", json={"mode": "timeout"})

    response = client.post("/run-demo", json={"task": "Summarize resilience"})

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["degraded"] is True
    assert data["provider"] == "backup-claude-mock"
    assert any(event["event"] == "fallback_selected" for event in data["trace"])


def test_trace_endpoint_returns_trace_events():
    client = TestClient(app)
    client.post("/failure-mode", json={"mode": "none"})
    client.post("/run-demo", json={"task": "Summarize resilience"})

    response = client.get("/trace")

    assert response.status_code == 200
    assert any(event["event"] == "workflow_started" for event in response.json())
