## 10. Testing and verification

Verification depth must match risk.

Possible evidence:

- build,
- lint,
- typecheck,
- unit tests,
- integration/API/UI/e2e,
- security checks,
- deployment verification,
- manual acceptance,
- evals.

For risky changes to existing systems, establish baseline first.
Use characterization tests when current behavior is poorly protected.

Canonical standard: `docs/test-verification-standard.md`.

## 11. Security

Apply a proportional security baseline by default:

- server-side authorization,
- least privilege,
- safe input/file handling,
- secrets outside source/artifacts,
- secure transport,
- safe logging/errors,
- safe dependency/runtime defaults.

Security-sensitive changes require explicit regression verification.

Canonical standard: `docs/security-baseline.md`.

## 19. Repository hygiene

Classify files as:

- CANONICAL
- RUNTIME
- DEVELOPMENT
- GENERATED
- TEMPORARY
- HISTORICAL

Auto-delete only high-confidence generated/temp artifacts.

Do not delete uncertain files, migrations, history, licenses, unknown binaries or deployment artifacts without strong evidence.

Maintain `.gitignore` and `.dockerignore` appropriate to the actual stack.

Canonical rules: `docs/repository-hygiene.md`.

## 20. CI

GitHub Actions baseline should reflect the project's actual verification contract.

Prefer:

- PR + default-branch validation,
- least-privilege permissions,
- locked dependencies,
- explicit runtime versions,
- local/CI command parity,
- release workflow separate from ordinary PR CI.

Required CI failure blocks completion.

Canonical rules: `docs/github-actions-baseline.md`.

