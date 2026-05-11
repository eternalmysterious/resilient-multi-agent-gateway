# Architecture

## Goal

Build a resilience gateway for AI agent workflows. The gateway should keep a workflow moving when LLM providers, MCP servers, or external tools fail, while clearly showing users what happened.

## Components

### 1. Agent Workflow Runner

Responsible for executing a multi-step task. Each step can call an LLM provider or a tool server.

Initial demo workflow:

1. Interpret user request.
2. Query a mock research tool.
3. Generate a structured summary.
4. Produce a final action plan.

### 2. Provider Adapter Layer

Normalizes calls to multiple providers:

- `primary-openai-mock`
- `backup-claude-mock`
- `local-fallback-mock`

Each provider exposes:

- `generate(prompt)`
- `health_check()`
- latency metrics
- error count
- last failure reason

### 3. Failure Injection Layer

Simulates infrastructure chaos:

- timeout
- HTTP 500
- rate limit
- brownout / intermittent failures
- malformed JSON
- bad tool schema
- slow response

### 4. Resilience Policy Engine

Implements:

- timeout boundary
- retry with jitter
- circuit breaker
- fallback routing
- graceful degradation
- checkpoint/resume

### 5. Health Store / Trace Store

Keeps in-memory state for MVP:

- provider status
- circuit breaker state
- workflow checkpoints
- failure timeline
- fallback events
- final recovered result

### 6. Dashboard

Shows:

- provider health table
- current workflow status
- injected failure mode
- active fallback route
- trace timeline
- final result
- reliability score

## Data Flow

```text
User Task
  -> Agent Workflow Runner
  -> Resilience Policy Engine
  -> Provider Adapter
  -> Failure Injection / Mock Provider
  -> Trace Store
  -> Dashboard
```

## Circuit Breaker States

- Closed: provider is considered healthy.
- Open: provider is blocked after repeated failures.
- Half-open: gateway sends a limited test request to see if provider recovered.

## MVP Constraints

- Do not depend on real OpenAI or Claude API keys for the main demo.
- Mock providers must be enough to demonstrate the full failure and recovery story.
- Real providers can be added later as optional integrations.
