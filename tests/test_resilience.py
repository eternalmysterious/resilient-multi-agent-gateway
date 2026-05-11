import pytest

from backend.app.resilience import CircuitBreaker, FallbackRouter, RetryingCaller
from backend.app.providers import MockProvider, ProviderError, ProviderTimeoutError
from backend.app.state import FailureMode


def test_circuit_breaker_opens_after_threshold_failures():
    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout_seconds=30)

    assert breaker.state == "closed"
    breaker.record_failure()
    assert breaker.state == "closed"
    breaker.record_failure()
    assert breaker.state == "open"


def test_circuit_breaker_prevents_calls_while_open():
    breaker = CircuitBreaker(failure_threshold=1, recovery_timeout_seconds=30)
    breaker.record_failure()

    assert breaker.allow_request() is False


def test_fallback_router_returns_next_provider():
    router = FallbackRouter(["primary-openai-mock", "backup-claude-mock", "local-fallback-mock"])

    assert router.next_provider("primary-openai-mock") == "backup-claude-mock"
    assert router.next_provider("backup-claude-mock") == "local-fallback-mock"
    assert router.next_provider("local-fallback-mock") == "local-fallback-mock"


def test_retrying_caller_retries_then_succeeds():
    attempts = {"count": 0}

    def flaky_call():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ProviderTimeoutError("timeout")
        return "ok"

    caller = RetryingCaller(max_attempts=3)
    assert caller.call(flaky_call) == "ok"
    assert attempts["count"] == 3


def test_retrying_caller_raises_last_error_after_max_attempts():
    def always_fail():
        raise ProviderError("boom")

    caller = RetryingCaller(max_attempts=2)

    with pytest.raises(ProviderError):
        caller.call(always_fail)
