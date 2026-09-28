# Final Release Readiness Report – v1.3.1

## Decision

**READY_WITH_WARNINGS**

Required gates: **23/23 PASS**

This patch release covers SB-64–SB-66 after `v1.3.0`.

## Release candidate

- Version: `1.3.1`
- Tag to publish: `v1.3.1`
- Version source for release artifacts: Git tag
- Release build: registry-driven and reproducible from the tag
- Existing `v1.3.0` is preserved
- `v1.3.1` is currently unused

## Included behavior changes

### Deferred environment verification

- actual project failures still block completion and route to repair,
- environment-limited verification performs best effort,
- deferred checks are never reported as PASS,
- a step may complete with `passed_with_deferred` when no project failure is observed and risk does not require blocking,
- deferred checks carry reason, evidence/retry condition and release-blocking status,
- security-, migration-, destructive- and deployment-critical verification may remain completion-blocking,
- release-relevant deferred checks must be retried or explicitly handled by release policy.

### Planning handoff ZIP

- after CREATE planning completes, System Builder produces a complete resumable project ZIP before DEV-001,
- the checkpoint contains planning/current-state artifacts and canonical machine state,
- `selected_step` and `in_progress` remain null,
- the first development step is stored as `next.recommended`,
- DEV-001 is not implemented or completed in the handoff run,
- ZIP integrity/resumability is verified,
- a later Chat/Work/runtime execution selects and locks DEV-001 normally.

## Reconciliation

Final reconciliation:

- `docs/changes/environment-verification-planning-handoff/reconciliation.md`

It found and resolved:

- a duplicate Planning handoff ZIP section in CREATE documentation,
- stale release-candidate metadata still pointing to v1.3.0 after that release already existed.

No unresolved implementation, documentation or decision mismatch remains for SB-64–SB-66.

## Runtime summary

| Runtime | Release state | Parity |
| --- | --- | --- |
| Chat ZIP | publish | equivalent |
| Custom GPT | publish | equivalent with platform constraints |
| Claude Projects | publish with documented limitation | reduced |
| OpenCode | publish | equivalent |
| OpenAI Plugin v1 | do not publish | reduced / not planned |

Claude Projects' reduced parity remains intentional and documented.

## Regression summary

Full project CI covers:

- canonical/schema validators,
- distribution registry synchronization,
- fresh builds and validation for all four active runtimes,
- **45 instruction-adherence cases, 37 critical**,
- static deferred-verification and planning-handoff contracts across active runtimes,
- deterministic five-case deferred-verification/planning-handoff E2E,
- runtime parity,
- CREATE/CHANGE/Docker-Coolify E2E regression,
- documentation/ZIP policy regression,
- README/release-version policy regression,
- GitHub Pages profile/workflow validation,
- repository hygiene.

Custom GPT instructions are **7,983 characters**, below the configured 8,000-character limit.

## Release assets

A `v1.3.1` release build is expected to produce:

- `system-builder-chat-1.3.1.zip`
- `system-builder-custom-gpt-1.3.1.zip`
- `system-builder-claude-projects-1.3.1.zip`
- `system-builder-opencode-1.3.1.zip`
- `SHA256SUMS.txt`
- `release-metadata.yaml`
- `distribution-build-manifest.json`

The release workflow derives `1.3.1` from tag `v1.3.1`; no separate hardcoded artifact version is used.

## Warning

Live Coolify target verification remains pending because no live Coolify environment is available. It is not reported as PASS and does not block this artifact release candidate.

## Blockers

None.
