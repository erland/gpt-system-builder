# Functional Specification – Counter Service

## Purpose
Provide simple integer counter operations.

## Functional requirements
- FR-001: `increment(value)` returns `value + 1`.
- FR-002: `reset()` returns `0`.
- FR-003: `decrement(value)` returns `value - 1`.

## Acceptance criteria
- AC-001: increment preserves existing behavior.
- AC-002: reset preserves existing behavior.
- AC-003: decrement of `5` returns `4`.

## Out of scope
Persistence, HTTP API, authentication.
