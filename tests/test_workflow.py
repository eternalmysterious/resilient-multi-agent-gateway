from backend.app.state import AppState, FailureMode
from backend.app.workflow import run_demo_workflow


def test_demo_workflow_uses_primary_provider_when_no_failure():
    state = AppState(failure_mode=FailureMode.NONE)

    result = run_demo_workflow("research task", state)

    assert result["status"] == "completed"
    assert result["provider"] == "primary-openai-mock"
    assert result["degraded"] is False
    assert any(event["event"] == "workflow_started" for event in state.trace)
    assert any(event["event"] == "provider_success" for event in state.trace)


def test_demo_workflow_falls_back_to_backup_when_primary_times_out():
    state = AppState(failure_mode=FailureMode.TIMEOUT)

    result = run_demo_workflow("research task", state)

    assert result["status"] == "completed"
    assert result["provider"] == "backup-claude-mock"
    assert result["degraded"] is True
    assert state.providers["primary-openai-mock"].status == "down"
    assert state.providers["primary-openai-mock"].circuit_state == "open"
    assert any(event["event"] == "fallback_selected" for event in state.trace)


def test_demo_workflow_uses_local_fallback_if_backup_also_marked_down():
    state = AppState(failure_mode=FailureMode.RATE_LIMIT)
    state.providers["backup-claude-mock"].circuit_state = "open"
    state.providers["backup-claude-mock"].status = "down"

    result = run_demo_workflow("research task", state)

    assert result["status"] == "completed"
    assert result["provider"] == "local-fallback-mock"
    assert result["degraded"] is True
    assert "local fallback" in result["output"].lower()
