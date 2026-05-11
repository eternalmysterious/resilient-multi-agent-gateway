import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 2, recovery_timeout_seconds: float = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.failure_count = 0
        self.state = "closed"
        self.opened_at: float | None = None

    def allow_request(self) -> bool:
        if self.state == "closed":
            return True
        if self.opened_at is None:
            return False
        if time.time() - self.opened_at >= self.recovery_timeout_seconds:
            self.state = "half-open"
            return True
        return False

    def record_success(self) -> None:
        self.failure_count = 0
        self.state = "closed"
        self.opened_at = None

    def record_failure(self) -> None:
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            self.opened_at = time.time()


class FallbackRouter:
    def __init__(self, providers: list[str]):
        self.providers = providers

    def next_provider(self, current_provider: str) -> str:
        try:
            index = self.providers.index(current_provider)
        except ValueError:
            return self.providers[0]
        next_index = min(index + 1, len(self.providers) - 1)
        return self.providers[next_index]


class RetryingCaller:
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts

    def call(self, operation: Callable[[], T]) -> T:
        last_error: Exception | None = None
        for _ in range(self.max_attempts):
            try:
                return operation()
            except Exception as exc:  # deliberately broad: gateway catches provider/tool failures
                last_error = exc
        assert last_error is not None
        raise last_error
