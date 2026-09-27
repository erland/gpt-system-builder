# Final Release Readiness Report – v1.3.0

## Decision

**READY_WITH_WARNINGS**

Required gates: **20/20 PASS**

This release candidate covers the reconciled SB-55–SB-57 change series.

## Release candidate

- Version: `1.3.0`
- Tag to publish: `v1.3.0`
- Version source for release artifacts: Git tag
- Release build: registry-driven and reproducible from the tag
- Existing `v1.2.1` is preserved; it is not moved or reused

## Included behavior changes

- functional specification and architecture are governing intent during development,
- implementation divergence does not silently rewrite the intended target,
- final documentation reconciliation is required before release readiness,
- ZIP mode runs every technically feasible required verification automatically,
- CI orchestration is not treated as an external gate when equivalent canonical commands can run locally,
- genuinely external/manual gates remain pending when no equivalent technical verification exists,
- regression protection covers these behaviors across active runtimes.

## Reconciliation

Final reconciliation found one implementation mismatch in the Custom GPT CREATE projection: it omitted final documentation reconciliation. The projection was repaired and the reconciled source passed full required CI.

Reconciliation evidence:
`docs/changes/documentation-reconciliation-and-zip-verification/reconciliation.md`

No unresolved implementation, documentation or decision mismatch remains for SB-55–SB-57.

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
- static instruction adherence including governing-document and ZIP-verification contracts,
- runtime parity,
- CREATE/CHANGE/Docker-Coolify E2E regression,
- documentation/ZIP policy regression,
- repository hygiene.

Custom GPT instructions are **7,947 characters**, below the configured 8,000-character limit.

## Release assets

A `v1.3.0` release build is expected to produce:

- `system-builder-chat-1.3.0.zip`
- `system-builder-custom-gpt-1.3.0.zip`
- `system-builder-claude-projects-1.3.0.zip`
- `system-builder-opencode-1.3.0.zip`
- `SHA256SUMS.txt`
- `release-metadata.yaml`
- `distribution-build-manifest.json`

## Warning

Live Coolify target verification remains pending because no live Coolify environment is available. It is not reported as PASS and does not block the artifact release candidate.

## Blockers

None.
