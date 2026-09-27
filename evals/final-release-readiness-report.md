# Final Release Readiness Report – v1.3.0

## Decision

**READY_WITH_WARNINGS**

Required gates: **22/22 PASS**

This release candidate covers the unreleased SB-55–SB-63 change series after `v1.2.1`.

## Release candidate

- Version: `1.3.0`
- Tag to publish: `v1.3.0`
- Version source for release artifacts: Git tag
- Release build: registry-driven and reproducible from the tag
- Existing `v1.2.1` is preserved; it is not moved or reused
- `v1.3.0` is currently unused

## Included behavior changes

### Documentation and ZIP verification

- functional specification and architecture remain governing intent during development,
- implementation divergence does not silently rewrite intended behavior,
- final documentation reconciliation is required before release readiness,
- ZIP mode runs technically feasible required verification automatically,
- CI orchestration is not treated as an external gate when equivalent canonical commands can run locally,
- genuinely external/manual gates remain pending when no equivalent technical verification exists.

### GitHub Pages

- `github-pages-static-pwa` is available for eligible public static browser-only apps,
- backend-dependent or sensitive/internal apps are excluded from automatic Pages selection,
- project-site repository subpath/public base is handled explicitly,
- Vite/PWA manifest/service-worker paths and routing are aligned with Pages deployment,
- Pages deployment is separate from ordinary pull-request CI,
- canonical build → upload Pages artifact → deploy Pages workflow pattern is included.

### README and release versioning

- `README.md`, when present, is treated as the current-state project entrypoint,
- a materially stale README is a documentation mismatch and blocks release readiness until resolved,
- README summarizes and links to canonical detailed documentation rather than duplicating it,
- tag-triggered release artifacts derive their version from the release tag by default,
- alternative ecosystem version sources require explicit ownership and synchronization/validation,
- unsynchronized parallel release versions are not accepted.

## Reconciliation

Three final reconciliation records cover the unreleased behavior:

- `docs/changes/documentation-reconciliation-and-zip-verification/reconciliation.md`
- `docs/changes/github-pages-static-pwa/reconciliation.md`
- `docs/changes/readme-release-version-contract/reconciliation.md`

The latest README/version reconciliation found and repaired runtime/documentation projection mismatches, including a stale omission of the README rule in canonical runtime and a duplicate versioning paragraph found during readiness review.

No unresolved implementation, documentation or decision mismatch remains for SB-55–SB-63.

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
- README current-state validator for System Builder dogfooding,
- distribution registry synchronization,
- fresh builds and validation for all four active runtimes,
- **41 instruction-adherence cases, 33 critical**,
- static README, release-version, GitHub Pages, governing-document and ZIP-verification contracts across active runtimes,
- runtime parity,
- CREATE/CHANGE/Docker-Coolify E2E regression,
- documentation/ZIP policy regression,
- README/release-version policy regression,
- GitHub Pages profile/workflow validation,
- repository hygiene.

Custom GPT instructions are **7,936 characters**, below the configured 8,000-character limit.

## Release assets

A `v1.3.0` release build is expected to produce:

- `system-builder-chat-1.3.0.zip`
- `system-builder-custom-gpt-1.3.0.zip`
- `system-builder-claude-projects-1.3.0.zip`
- `system-builder-opencode-1.3.0.zip`
- `SHA256SUMS.txt`
- `release-metadata.yaml`
- `distribution-build-manifest.json`

The release workflow derives `1.3.0` from tag `v1.3.0`; no separate hardcoded artifact version is used.

## Warning

Live Coolify target verification remains pending because no live Coolify environment is available. It is not reported as PASS and does not block the artifact release candidate.

## Blockers

None.
