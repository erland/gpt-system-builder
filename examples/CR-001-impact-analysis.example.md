# CR-001 – Impact analysis

## Summary

The change affects UI input, API contract and GitHub adapter configuration but not database schema.

## Functional impact

- Requirements: FR-003 changes to include visibility selection.
- Use cases: UC-001 gains one user choice.
- Business rules: default visibility remains private.

## Architecture impact

- Components: Web UI, Backend API, GitHub adapter.
- Boundaries: unchanged.
- Data ownership: unchanged.

## Data / migration impact

No persistent schema change.

## Integration / API impact

Backend request schema adds an optional visibility field. GitHub adapter maps it to repository creation parameters.

## Security / authorization impact

Public visibility increases exposure risk; default remains private and only authenticated users may create repositories.

## UI impact

Add a private/public selector with private default.

## Test / regression impact

Add API/UI tests for explicit public and preserve regression test for default private.

## Configuration / deployment impact

None.

## Installation / operations impact

None.

## Blast radius

cross-component

## Risks / blockers

- Verify GitHub integration accepts both supported visibility values.

## Recommended plan implications

1. Update spec and API contract.
2. Implement backend/GitHub adapter.
3. Implement UI selection.
4. Run regression and acceptance.
