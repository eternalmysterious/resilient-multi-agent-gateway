from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

from backend.app.state import FailureMode, STATE
from backend.app.workflow import run_demo_workflow

app = FastAPI(title="Resilient Multi-Agent Gateway")


class FailureModeRequest(BaseModel):
    mode: FailureMode


class RunDemoRequest(BaseModel):
    task: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/providers")
def providers() -> dict:
    return {
        name: {
            "status": metrics.status,
            "latency_ms": metrics.latency_ms,
            "error_count": metrics.error_count,
            "success_count": metrics.success_count,
            "last_failure_reason": metrics.last_failure_reason,
            "circuit_state": metrics.circuit_state,
        }
        for name, metrics in STATE.providers.items()
    }


@app.post("/failure-mode")
def set_failure_mode(request: FailureModeRequest) -> dict:
    STATE.failure_mode = request.mode
    STATE.trace.clear()
    for metrics in STATE.providers.values():
        metrics.status = "healthy"
        metrics.latency_ms = 0
        metrics.error_count = 0
        metrics.success_count = 0
        metrics.last_failure_reason = None
        metrics.circuit_state = "closed"
    return {"failure_mode": STATE.failure_mode.value}


@app.post("/run-demo")
def run_demo(request: RunDemoRequest) -> dict:
    if not request.task.strip():
        raise HTTPException(status_code=400, detail="task cannot be blank")
    return run_demo_workflow(request.task, STATE)


@app.get("/trace")
def trace() -> list[dict]:
    return STATE.trace
