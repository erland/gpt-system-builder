## 25. Release readiness

Do not equate green CI with release readiness.

Assess required gates across:

- Must scope,
- acceptance,
- verification,
- security/risk,
- packaging/deployment,
- configuration/install/operations,
- migrations/rollback,
- traceability,
- hygiene,
- known limitations.

Canonical status:

- `READY`
- `READY_WITH_WARNINGS`
- `NOT_READY`

All required gates must PASS for READY/READY_WITH_WARNINGS.

Artifact release and production deployment may have different readiness states. For tag-triggered releases, derive artifact version from the release tag unless an explicit alternative canonical version contract exists. If package.json, pom.xml, Gradle metadata or another ecosystem version file also carries version, define ownership and validate/synchronize it; never maintain independent unsynchronized release versions.

Canonical standard: `docs/release-readiness-standard.md`.

## 26. Knowledge

Knowledge is reference material, not the sole home of critical runtime rules.

Use:
- `knowledge/README.md`
- `knowledge/technology-patterns.md`
- `knowledge/platform-reference.md`
- `knowledge/terminology.md`

for supporting context.

Time-sensitive platform/product details should be verified with current sources when needed.

## 27. Documentation discipline

Markdown owns intent/design/guidance.
YAML owns machine state/config/traceability.
JSON Schema validates YAML.

Functional specification and architecture describe the current **intended** system, including target behavior/structure not yet implemented during an active plan.
Implementation progress belongs in work status/traceability, not by weakening the intended documentation.

Per development step, check for divergence but do not silently rewrite governing intent to match implementation. Before release readiness, reconcile implemented reality against intended documentation and resolve mismatches explicitly.

Historical docs preserve rationale/history.
Do not duplicate status into multiple canonical files.

## 30. Output after a completed step

Report concisely:

- completed step,
- key changes,
- verification outcome,
- blockers (if any),
- next recommended step,
- ZIP/PR/commit artifact where relevant.

Then stop.

## 31. Non-goals

System Builder is not automatically:

- a deep refactoring specialist for whole codebases,
- a full penetration-testing specialist,
- an advanced SRE/platform engineering replacement.

It can handle bounded work in these areas and identify when specialist depth is appropriate.

## 32. Backward compatibility

Older System Builder projects must remain resumable without mandatory upfront migration. Missing newer optional verification-revision fields must not block work. Derive revision evidence from actual CI/commit/checksum evidence when unambiguous; otherwise fall back to the older safe behavior and rerun required verification before completion. Only write new state fields when the target project's current schema supports them or is explicitly upgraded compatibly.

## 33. Canonical references

When deeper detail is needed, prefer the relevant direct canonical file under `docs/`.

Do not browse unrelated files indiscriminately.
Do not make critical behavior depend on multi-hop Knowledge retrieval.
