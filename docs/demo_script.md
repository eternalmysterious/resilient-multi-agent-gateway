# Demo Script

Target length: 1–3 minutes.

## Scene 1: The problem

Narration:

AI agents depend on LLM providers, MCP servers, and tool APIs. When those services timeout, brownout, or return bad data, most agents fail in confusing ways.

Visual:

Dashboard shows all providers healthy.

## Scene 2: Start an agent workflow

Narration:

We start a multi-step agent workflow through the Resilient Multi-Agent Gateway.

Visual:

User submits a task. Workflow starts with the primary provider.

## Scene 3: Inject infrastructure failure

Narration:

Now we simulate infrastructure chaos: the primary LLM provider begins timing out, just like a real OpenAI or Claude brownout.

Visual:

Click or run failure injection: `timeout` or `brownout`.
Dashboard shows latency spike and failures.

## Scene 4: Resilience policy activates

Narration:

The gateway retries with jitter. When failures continue, the circuit breaker opens and blocks the unhealthy provider.

Visual:

Provider status changes from healthy to degraded to down/open circuit.
Timeline shows retry events.

## Scene 5: Fallback and resume

Narration:

Instead of losing the whole task, the workflow resumes from its last checkpoint and falls back to a backup provider.

Visual:

Fallback route changes from primary provider to backup provider.
Workflow continues.

## Scene 6: User-visible recovery

Narration:

The user receives a completed answer, along with a clear explanation of what degraded and how the system recovered.

Visual:

Final result appears. Dashboard shows full trace and reliability score.

## Closing

Narration:

Resilient Multi-Agent Gateway helps agents survive real infrastructure failures while keeping users informed and in control.
