from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


class FailureMode(str, Enum):
    NONE = "none"
    TIMEOUT = "timeout"
    ERROR_500 = "error_500"
    RATE_LIMIT = "rate_limit"
    MALFORMED_JSON = "malformed_json"
    BROWNOUT = "brownout"


@dataclass
class ProviderResponse:
    provider: str
    output: str


@dataclass
class ProviderMetrics:
    status: str = "healthy"
    latency_ms: int = 0
    error_count: int = 0
    success_count: int = 0
    last_failure_reason: Optional[str] = None
    circuit_state: str = "closed"


@dataclass
class AppState:
    failure_mode: FailureMode = FailureMode.NONE
    active_provider: str = "primary-openai-mock"
    trace: list[dict] = field(default_factory=list)
    providers: dict[str, ProviderMetrics] = field(default_factory=lambda: {
        "primary-openai-mock": ProviderMetrics(),
        "backup-claude-mock": ProviderMetrics(),
        "local-fallback-mock": ProviderMetrics(),
    })


STATE = AppState()
