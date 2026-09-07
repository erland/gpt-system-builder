# Development Plan – Example Project

## Goal and delivery scope

Deliver a small web service that accepts a validated project ZIP and creates a GitHub repository.

## Planning assumptions

- GitHub integration credentials are available.
- The first release runs as one containerized application.
- PostgreSQL is external if persistence is needed.

## Step overview

| Step | Title | Purpose |
|---|---|---|
| DEV-001 | Project skeleton | Establish buildable baseline |
| DEV-002 | Safe ZIP validation | Remove highest input-security risk |
| DEV-003 | Repository creation flow | Deliver first end-to-end capability |
| DEV-004 | Docker packaging | Make service deployable |
| DEV-005 | Release readiness | Verify first release |

## Development steps

## DEV-001 – Project skeleton

### Mål

Create a buildable backend/frontend project with baseline tests.

### Scope

**Ingår**
- project structure,
- build scripts,
- baseline CI commands.

**Ingår inte**
- GitHub integration,
- production deployment.

### Förutsättningar

- technology stack is selected.

### Implementation

- create backend/frontend skeletons,
- add basic health endpoint,
- add baseline test.

### Verifiering

- backend build,
- frontend build/typecheck,
- baseline tests.

### Klart-kriterier

- [ ] backend builds,
- [ ] frontend builds,
- [ ] health endpoint is available,
- [ ] baseline tests pass.

### Beroenden

- None.

## DEV-002 – Safe ZIP validation

### Mål

Reject unsafe ZIP files before extraction.

### Scope

**Ingår**
- absolute path rejection,
- parent traversal rejection,
- safe extraction contract.

**Ingår inte**
- GitHub upload.

### Förutsättningar

- DEV-001 completed.

### Implementation

- implement ZIP validation component,
- add focused tests.

### Verifiering

- valid archive test,
- traversal archive test,
- absolute-path archive test.

### Klart-kriterier

- [ ] safe ZIP accepted,
- [ ] unsafe ZIP rejected,
- [ ] tests pass.

### Beroenden

- DEV-001.

## DEV-003 – Repository creation flow

### Mål

Deliver the first end-to-end repository creation flow.

### Scope

**Ingår**
- upload validated ZIP,
- create repository,
- upload project contents,
- return repository link.

**Ingår inte**
- automatic deployment.

### Förutsättningar

- DEV-002 completed,
- GitHub access available.

### Implementation

- add GitHub adapter,
- add orchestration endpoint,
- add minimal UI flow.

### Verifiering

- integration/API verification,
- UI happy path,
- failure-path verification.

### Klart-kriterier

- [ ] valid project creates repository,
- [ ] result link is shown,
- [ ] common integration failures are surfaced,
- [ ] relevant tests pass.

### Beroenden

- DEV-002.

## DEV-004 – Docker packaging

### Mål

Package the service as a deployable container.

### Scope

**Ingår**
- Dockerfile,
- .dockerignore,
- runtime configuration,
- health verification.

**Ingår inte**
- Kubernetes.

### Förutsättningar

- core flow is working.

### Implementation

- add multi-stage image build,
- configure non-root runtime where practical.

### Verifiering

- image build,
- container startup,
- health endpoint.

### Klart-kriterier

- [ ] image builds,
- [ ] container starts,
- [ ] health check passes.

### Beroenden

- DEV-003.

## DEV-005 – Release readiness

### Mål

Verify first-release acceptance.

### Scope

**Ingår**
- must requirements,
- acceptance criteria,
- docs,
- known limitations.

### Förutsättningar

- DEV-004 completed.

### Implementation

- run release checklist,
- update current-state documentation.

### Verifiering

- complete relevant test/build checks,
- acceptance review.

### Klart-kriterier

- [ ] no release blockers remain,
- [ ] known limitations documented,
- [ ] installation/operations information is current.

### Beroenden

- DEV-004.

## Cross-cutting verification

Security-sensitive ZIP handling must remain covered throughout later changes.

## Plan-change rules

Future steps may be split or reprioritized if new evidence reduces risk. Completed steps are not rewritten retroactively.
