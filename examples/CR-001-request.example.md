# CR-001 – Add repository visibility selection

**Status:** Accepted  
**Date:** 2026-09-07

## Current problem

The current flow always creates private repositories.

## Desired outcome

Allow the user to choose private or public repository visibility during repository creation.

## Scope

### Must
- user can select private/public,
- backend validates allowed visibility,
- selected visibility is sent to GitHub.

### Should
- default remains private.

### Could
- remember last choice.

### Out of scope
- organization policy management.

## Affected users / actors

- authenticated user,
- GitHub integration.

## Compatibility expectations

Existing users who make no explicit choice should continue to create private repositories.

## Data / migration expectations

No database migration required for first implementation.

## Acceptance

A user selecting public gets a public repository; omitting the choice keeps private behavior.

## Open questions

### Blocking
- None.

### Non-blocking
- Whether to remember previous selection.
