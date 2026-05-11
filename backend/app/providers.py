from backend.app.state import FailureMode, ProviderResponse


class ProviderError(Exception):
    """Base provider failure."""


class ProviderTimeoutError(ProviderError):
    """Provider timed out."""


class ProviderRateLimitError(ProviderError):
    """Provider is rate limited."""


class MockProvider:
    def __init__(self, name: str):
        self.name = name

    def generate(self, prompt: str, failure_mode: FailureMode) -> ProviderResponse:
        if failure_mode == FailureMode.TIMEOUT:
            raise ProviderTimeoutError(f"{self.name} timed out")
        if failure_mode == FailureMode.ERROR_500:
            raise ProviderError(f"{self.name} returned 500")
        if failure_mode == FailureMode.RATE_LIMIT:
            raise ProviderRateLimitError(f"{self.name} hit rate limit")
        if failure_mode == FailureMode.MALFORMED_JSON:
            raise ProviderError(f"{self.name} returned malformed JSON")
        if failure_mode == FailureMode.BROWNOUT:
            raise ProviderTimeoutError(f"{self.name} brownout: intermittent timeout")

        return ProviderResponse(
            provider=self.name,
            output=f"{self.name} completed: {prompt}",
        )
