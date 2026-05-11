import pytest

from backend.app.providers import MockProvider, ProviderError, ProviderRateLimitError, ProviderTimeoutError
from backend.app.state import FailureMode


def test_mock_provider_returns_named_success_response_when_no_failure():
    provider = MockProvider("primary-openai-mock")

    response = provider.generate("Summarize agent resilience", FailureMode.NONE)

    assert response.provider == "primary-openai-mock"
    assert "primary-openai-mock completed" in response.output
    assert "Summarize agent resilience" in response.output


def test_mock_provider_timeout_mode_raises_timeout_error():
    provider = MockProvider("primary-openai-mock")

    with pytest.raises(ProviderTimeoutError) as exc:
        provider.generate("task", FailureMode.TIMEOUT)

    assert "timed out" in str(exc.value)


def test_mock_provider_error_500_mode_raises_provider_error():
    provider = MockProvider("primary-openai-mock")

    with pytest.raises(ProviderError) as exc:
        provider.generate("task", FailureMode.ERROR_500)

    assert "500" in str(exc.value)


def test_mock_provider_rate_limit_mode_raises_rate_limit_error():
    provider = MockProvider("primary-openai-mock")

    with pytest.raises(ProviderRateLimitError) as exc:
        provider.generate("task", FailureMode.RATE_LIMIT)

    assert "rate limit" in str(exc.value).lower()


def test_mock_provider_malformed_json_mode_raises_provider_error():
    provider = MockProvider("primary-openai-mock")

    with pytest.raises(ProviderError) as exc:
        provider.generate("task", FailureMode.MALFORMED_JSON)

    assert "malformed" in str(exc.value).lower()
