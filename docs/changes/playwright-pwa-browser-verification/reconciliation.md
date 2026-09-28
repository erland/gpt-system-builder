# Final Documentation Reconciliation – SB-67–SB-68

## Scope

Change series: `playwright-pwa-browser-verification`

Planned intent:

- SB-67: treat unavailable Playwright browser binaries in ZIP/Chat runtimes as environment-limited verification, run best-effort alternatives, and prefer matching Playwright CI when GitHub is available.
- SB-68: protect the behavior with instruction, static-contract and deterministic E2E regression coverage.

## Findings

### REC-BROWSER-001 – Test verification standard missed the Playwright rule

Classification: **documentation mismatch**

The ZIP, GitHub Actions, PWA profile and runtime instructions contained the intended browser fallback behavior, but `docs/test-verification-standard.md` did not.

Resolution:

- added an explicit Playwright/browser-E2E section,
- distinguished missing browser environment from actual test failure,
- documented deferred browser verification and PWA release-evidence expectations.

Status: **resolved**

### REC-BROWSER-002 – v1.3.1 already exists

Classification: **release metadata mismatch**

Tag `v1.3.1` already exists on the merged PR #10 commit while this new change series initially inherited version `1.3.1`.

Resolution:

- verified `v1.3.1` exists,
- verified `v1.3.2` is unused,
- updated `VERSION` and project candidate metadata to `1.3.2` / `v1.3.2`,
- kept the project in CHANGE phase until fresh release-readiness evidence is built.

Status: **resolved**

## Consistent behavior

The reconciled contract now consistently states:

- missing Chromium/WebKit/browser binaries in the current ZIP/Chat runtime are environment-limited when the browser environment itself is unavailable,
- all other feasible checks still run,
- browser tests remain deferred with warning and are never reported PASS without execution,
- an actual browser test that runs and fails is project failure and routes to repair,
- GitHub projects should use a Playwright CI environment matching the project Playwright version and containing required browser binaries,
- version mismatch between project Playwright and CI image/setup is a configuration error,
- PWA browser-critical checks such as service worker, offline behavior, routing/installability and browser storage normally require actual browser evidence before release readiness.

## Regression coverage

Coverage includes:

- missing browser binary → deferred environment verification,
- actual Playwright failure → project failure,
- CI Playwright version mismatch → configuration error,
- PWA release-critical browser checks still deferred → release not ready,
- static runtime contract across active distributions.

Instruction-adherence suite: 49 cases, 41 critical.

Custom GPT instructions: 7,960 characters.

## Reconciliation result

**PASS, subject to required full CI for the final reconciled source revision.**

After full CI PASS, proceed to release readiness for `v1.3.2`.
