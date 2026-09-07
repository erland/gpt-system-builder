# Test Strategy – Example ZIP-to-GitHub Service

## Scope

Verify safe ZIP handling, GitHub repository creation, external integration failure handling and container startup.

## Quality risks

- unsafe ZIP path traversal,
- GitHub integration mismatch,
- partial repository creation,
- deployment configuration errors.

## Test levels

| Level | Purpose | Required |
|---|---|---|
| Unit | ZIP validation and domain rules | yes |
| Integration | GitHub adapter and persistence | yes |
| API | repository creation endpoint | yes |
| E2E | core happy path | selective |
| Security | unsafe ZIP rejection | yes |
| Deployment | image/startup/health | yes |

## Environments

- Local: fast unit/integration development loop.
- CI: deterministic full automated checks.
- Integration: real GitHub test target where credentials and rate limits permit.

## Test data

Use generated ZIP fixtures:
- valid small project,
- parent traversal archive,
- absolute-path archive,
- representative larger repository.

## Automated checks

### TEST-001 – Reject parent traversal ZIP

**Type:** security  
**Related:** NFR-001, AC-002

Expected: archive is rejected before extraction.

### TEST-002 – Create repository via API

**Type:** API/integration  
**Related:** FR-003, AC-001

Expected: valid request creates repository and returns URL.

### TEST-003 – Container health

**Type:** deployment

Expected: built image starts and health endpoint becomes ready.

## Manual acceptance

### Core flow

A user uploads a representative valid project ZIP, creates a repository and follows the returned GitHub link.

## Regression strategy

Every fixed ZIP security bug receives a permanent regression test. GitHub failure handling remains covered as the adapter changes.

## Traceability

- TEST-001 → NFR-001, AC-002
- TEST-002 → FR-003, AC-001
- TEST-003 → deployment readiness

## Release gates

- lint/typecheck pass,
- backend/frontend build pass,
- ZIP security tests pass,
- repository API integration passes,
- container build/startup/health passes,
- must acceptance criteria verified.

## Known gaps

Real GitHub rate-limit behavior for very large repositories requires separate feasibility evidence.
