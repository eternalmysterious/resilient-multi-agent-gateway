from backend.app.providers import MockProvider, ProviderError
from backend.app.state import AppState, FailureMode

PROVIDER_ORDER = ["primary-openai-mock", "backup-claude-mock", "local-fallback-mock"]


def _trace(state: AppState, event: str, **details) -> None:
    state.trace.append({"event": event, **details})


def _mark_success(state: AppState, provider_name: str, latency_ms: int = 42) -> None:
    metrics = state.providers[provider_name]
    metrics.status = "healthy"
    metrics.latency_ms = latency_ms
    metrics.success_count += 1
    metrics.last_failure_reason = None
    metrics.circuit_state = "closed"


def _mark_failure(state: AppState, provider_name: str, error: Exception) -> None:
    metrics = state.providers[provider_name]
    metrics.status = "down"
    metrics.error_count += 1
    metrics.last_failure_reason = str(error)
    metrics.circuit_state = "open"


def _available_provider_after(state: AppState, provider_name: str) -> str:
    current_index = PROVIDER_ORDER.index(provider_name)
    for candidate in PROVIDER_ORDER[current_index + 1:]:
        if state.providers[candidate].circuit_state != "open":
            return candidate
    return "local-fallback-mock"


def _failure_for_provider(state: AppState, provider_name: str) -> FailureMode:
    if provider_name == "primary-openai-mock":
        return state.failure_mode
    if provider_name == "backup-claude-mock" and state.providers[provider_name].circuit_state == "open":
        return FailureMode.ERROR_500
    return FailureMode.NONE


def run_demo_workflow(task: str, state: AppState) -> dict:
    _trace(state, "workflow_started", task=task)
    provider_name = "primary-openai-mock"
    degraded = False

    while True:
        if state.providers[provider_name].circuit_state == "open":
            provider_name = _available_provider_after(state, provider_name)
            degraded = True
            _trace(state, "fallback_selected", provider=provider_name)

        provider = MockProvider(provider_name)
        failure_mode = _failure_for_provider(state, provider_name)

        try:
            if provider_name == "local-fallback-mock":
                response = provider.generate(f"local fallback response for {task}", FailureMode.NONE)
            else:
                response = provider.generate(task, failure_mode)
            _mark_success(state, provider_name)
            _trace(state, "provider_success", provider=provider_name)
            return {
                "status": "completed",
                "provider": provider_name,
                "degraded": degraded,
                "output": response.output,
                "trace": state.trace,
            }
        except ProviderError as error:
            _mark_failure(state, provider_name, error)
            _trace(state, "provider_failure", provider=provider_name, error=str(error))
            degraded = True
            next_provider = _available_provider_after(state, provider_name)
            _trace(state, "fallback_selected", provider=next_provider)
            provider_name = next_provider
