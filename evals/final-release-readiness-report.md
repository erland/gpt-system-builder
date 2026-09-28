# Final Release Readiness Report – v1.3.2

## Decision

**READY_WITH_WARNINGS**

Required gates: **24/24 PASS**

This patch release covers SB-67–SB-68 after `v1.3.1`.

## Release candidate

- Version: `1.3.2`
- Tag to publish: `v1.3.2`
- Version source for release artifacts: Git tag
- Existing `v1.3.1` is preserved
- `v1.3.2` is currently unused

## Included behavior changes

### Playwright/PWA browser verification

- missing Chromium/WebKit/browser binaries in the current ZIP/Chat runtime are treated as environment-limited verification when the browser environment itself is unavailable,
- all other feasible checks still run,
- browser tests remain deferred with warning and are never reported PASS without actual execution,
- an actual browser test that runs and fails is project failure and routes to repair,
- GitHub projects should use a Playwright CI environment matching the project Playwright version and containing required browser binaries,
- project/CI Playwright version mismatch is a configuration error,
- PWA browser-critical checks such as service worker, offline behavior, routing/installability and browser storage normally require actual browser evidence before release readiness.

## Reconciliation

Final reconciliation:

- `docs/changes/playwright-pwa-browser-verification/reconciliation.md`

It found and resolved:

- the Playwright/browser-E2E rule missing from the canonical test-verification standard,
- stale candidate version `1.3.1` after tag `v1.3.1` already existed.

No unresolved implementation, documentation or decision mismatch remains for SB-67–SB-68.

## Runtime summary

| Runtime | Release state | Parity |
| --- | --- | --- |
| Chat ZIP | publish | equivalent |
| Custom GPT | publish | equivalent with platform constraints |
| Claude Projects | publish with documented limitation | reduced |
| OpenCode | publish | equivalent |
| OpenAI Plugin v1 | do not publish | reduced / not planned |

## Regression summary

Full project CI covers:

- fresh builds and validation for all four active runtimes,
- **49 instruction-adherence cases, 41 critical**,
- static Playwright/PWA browser-verification contract across active runtimes,
- deterministic Playwright/PWA browser-verification E2E,
- existing deferred-verification/planning-handoff regression,
- runtime parity,
- repository hygiene.

Custom GPT instructions are **7,960 characters**, below the configured 8,000-character limit.

## Release assets

A `v1.3.2` release build is expected to produce:

- `system-builder-chat-1.3.2.zip`
- `system-builder-custom-gpt-1.3.2.zip`
- `system-builder-claude-projects-1.3.2.zip`
- `system-builder-opencode-1.3.2.zip`
- `SHA256SUMS.txt`
- `release-metadata.yaml`
- `distribution-build-manifest.json`

The release workflow derives `1.3.2` from tag `v1.3.2`.

## Warning

Live Coolify target verification remains pending because no live Coolify environment is available. It is not reported as PASS and does not block this artifact release candidate.

## Blockers

None.

Candidate validation target: `v1.3.2`.
