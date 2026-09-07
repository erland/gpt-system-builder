# IMPROVE Work Initiation – Example

## Technical goal

Separate GitHub HTTP details from repository creation orchestration so the core flow can be tested without live HTTP calls.

## Motivation

Current backend mixes orchestration and GitHub-specific request construction, making tests slow and error handling difficult to isolate.

## Behavior to preserve

- repository creation API contract,
- default repository visibility,
- returned repository URL,
- existing error mapping.

## Non-goals

- no new GitHub features,
- no API schema change,
- no UI redesign,
- no database migration.

## Baseline

- Build: pass
- Tests: pass
- Lint/typecheck: pass
- Performance/other: not relevant

## Risk areas

- hidden coupling between orchestration and GitHub error types,
- regression in partial failure handling.

## Characterization tests needed

yes

## Proposed improvement steps

- DEV-001: capture current orchestration behavior,
- DEV-002: introduce GitHub adapter boundary,
- DEV-003: move HTTP-specific logic,
- DEV-004: run regression and cleanup obsolete coupling.

## Verification

- all existing API tests pass,
- characterization tests pass,
- no contract/schema changes,
- build/lint remain green.

## Blocking issues

- None.
