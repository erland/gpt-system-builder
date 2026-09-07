# Functional Specification – Tiny Status API

## Purpose and goals
Provide a minimal local status HTTP service.

## Scope

### Must
- FR-001: `/health` returns HTTP 200 with `{"status":"ok"}`.
- FR-002: `/message` returns the configured message.
- FR-003: default message is `Hello`.

## Actors and use cases
- UC-001: monitoring client checks health.
- UC-002: client reads configured message.

## Non-functional requirements
- NFR-001: Python 3.12+, no third-party runtime dependency.

## Acceptance criteria
- AC-001: health response matches FR-001.
- AC-002: default message is `Hello`.
- AC-003: `STATUS_MESSAGE=Ready` returns `Ready`.

## Out of scope
Authentication, database, UI, production deployment.

## Open questions
None blocking DEV-001.
