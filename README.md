# Resilient Multi-Agent Gateway

Keep AI agents working when LLMs, MCP servers, and tools fail.

## Overview

Resilient Multi-Agent Gateway is a reliability layer for agentic AI applications. It detects provider outages, MCP/tool failures, API timeouts, rate limits, and brownouts, then automatically retries, opens circuit breakers, falls back to backup providers, resumes from checkpoints, and shows users what happened.

This project is built for the DevNetwork [AI + ML] Hackathon 2026, targeting the TrueFoundry: Resilient Agents sponsor challenge.

## Problem

AI agents increasingly rely on fragile infrastructure:

- LLM providers such as OpenAI or Claude may timeout, rate-limit, brownout, or return malformed responses.
- MCP servers and tool APIs may become slow, error out, or return invalid schemas.
- Multi-step workflows may fail halfway through, leaving users with unclear errors and no recovery path.

Most demos assume happy-path infrastructure. Real users need agents that degrade gracefully when dependencies fail.

## Solution

This gateway wraps agent workflows with resilience controls:

- Provider health checks
- Timeout and retry with jitter
- Circuit breaker state machine
- Fallback provider routing
- MCP/tool failure detection
- Checkpoint/resume for multi-step workflows
- User-visible degradation messages
- Dashboard for provider status, failure timeline, and recovery path

## Target Challenge Fit

TrueFoundry asks:

> How does your agent behave when an MCP server starts erroring out? An LLM server goes down? OpenAI or Claude errors out or browns out?

This project directly demonstrates those scenarios using controlled failure injection and a recovery-focused dashboard.

## MVP Demo Flow

1. User starts a multi-step agent task.
2. The gateway routes the task to a primary mock LLM provider.
3. A failure is injected: timeout, 500 error, rate limit, brownout, or bad tool schema.
4. The gateway retries with jitter.
5. If failures continue, the circuit breaker opens.
6. The workflow falls back to a backup provider or degraded local response.
7. The agent resumes from its last checkpoint.
8. The dashboard shows the failure, fallback route, and recovered final result.

## Planned Tech Stack

- Backend: Python + FastAPI
- Frontend: React/Vite or lightweight HTML dashboard
- Testing: pytest
- Demo providers: mock OpenAI, mock Claude, local fallback
- Resilience patterns: retry, circuit breaker, health checks, checkpoint/resume

## Repository Structure

```text
backend/                  FastAPI service and resilience engine
frontend/                 Dashboard UI
examples/                 Demo workflows
scripts/failure_injection/ Failure simulation scripts
docs/                     Architecture, submission draft, demo script
tests/                    Automated tests
```

## Safety and Ethics

The system does not hide failures from users. It explains degraded behavior, fallback decisions, and recovery status so users can decide whether to trust the result.
