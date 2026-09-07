# Release Readiness – Example

## Release candidate

- version: `1.0.0-rc.1`
- commit/tag: `abc1234`
- target: source release + Coolify deployment

## Scope

- Must: ZIP upload, safe extraction, GitHub repository creation, external PostgreSQL support
- Deferred: remember last repository visibility choice

## Gate summary

| Gate | Required | Result | Evidence |
|---|---|---|---|
| Must scope | yes | pass | FR-001, FR-002, FR-003 |
| Acceptance criteria | yes | pass | AC-001..AC-005 |
| CI | yes | pass | build/test/typecheck |
| Security baseline | yes | pass | ZIP traversal and authz tests |
| Packaging | yes | pass | Docker image build/startup |
| Migration | yes | pass | Flyway rehearsal |
| Coolify staging health | yes | pass | HTTPS + `/q/health` |
| Production DNS smoke | no | warning | production cutover not yet performed |
| Operational docs | yes | pass | configuration/install/operations |

## Acceptance

Core user flow and failure paths were accepted in the staging environment.

## Verification evidence

- unit/integration/API tests pass
- Docker image starts
- PostgreSQL connection and migration pass
- health endpoint returns HTTP 200
- unsafe ZIP fixtures are rejected

## Security / risk

No blocking security finding remains. Residual operational risk for production DNS cutover is accepted as a deployment-time check.

## Packaging / deployment

The versioned Docker image is release-ready. Coolify staging deployment is verified.

## Documentation

Configuration, installation and operations documents are current for the release candidate.

## Known limitations

Production DNS cutover has not yet been smoke-tested.

## Blockers

None for artifact release.

## Decision

READY_WITH_WARNINGS

## Decision rationale

All required gates pass. The remaining production DNS check is deployment-specific and non-blocking for publication of the release artifact.
