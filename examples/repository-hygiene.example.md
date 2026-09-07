# Repository Hygiene Assessment – Example

## Classification

### CANONICAL
- `src/`
- `docs/`
- `.system-builder/`
- `package.json`
- `pnpm-lock.yaml`

### RUNTIME
- `Dockerfile`
- `compose.yaml`

### DEVELOPMENT
- `tests/`
- `.github/workflows/`

### GENERATED
- `dist/`
- `coverage/`

### TEMPORARY
- `.DS_Store`
- `*.log`

### HISTORICAL
- `docs/architecture-decisions/`
- `docs/changes/`

## Findings

### PASS
- `node_modules/` is ignored.
- `.env` is ignored.
- lockfile is versioned.

### WARNING
- `coverage/` exists locally and can be regenerated.

### BLOCKED
- None.

## Ignore changes

- add `coverage/` to `.gitignore`
- ensure `.env` and `.env.*` are excluded from Docker build context

## Verification

- required project files remain visible to Git,
- Docker build context still contains required source.
