# Final Documentation Reconciliation – SB-61–SB-63

## Scope

Change series: `readme-release-version-contract`

Planned intent:

- SB-61: treat README as a current-state project entrypoint and explicitly reconcile it before release readiness.
- SB-62: use the release tag as canonical artifact version source for tag-triggered releases unless an explicit alternative version ownership contract exists.
- SB-63: add regression coverage for README reconciliation and release version consistency.

## Reconciliation method

Compared the completed series against:

- `docs/development-plan.md`,
- README current-state standard,
- release-readiness, deployment and GitHub Actions standards,
- canonical runtime instruction,
- Custom GPT runtime projection,
- System Builder's own README and README validator,
- instruction-adherence/static runtime contracts,
- deterministic README/release-version policy E2E,
- project CI integration.

## Findings

### REC-README-001 – Duplicate release-version rule in canonical runtime

Classification: **documentation/runtime projection mismatch**

The tag-derived artifact version rule had been inserted twice consecutively in the canonical runtime instruction.

Resolution:

- removed the duplicate while preserving the complete version-source/ownership rule.

Status: **resolved**

### REC-README-002 – Scope of README validator needed clarification

Classification: **documentation clarification**

`scripts/validate_readme_current_state.py` is intentionally tailored to the System Builder repository and its machine-readable state. The generic behavior requested for projects created or changed by System Builder must not depend on that repository-specific script.

Resolution:

- clarified that semantic README reconciliation in runtime behavior is the general guarantee,
- documented that project-specific automated README validators are optional/generated when stable project contracts make them useful,
- retained System Builder's validator as dogfooding evidence rather than the generic contract itself.

Status: **resolved**

### REC-README-003 – Canonical runtime omitted README reconciliation rule

Classification: **implementation/runtime mismatch**

The Custom GPT projection contained the generic README reconciliation behavior, but canonical runtime did not. This meant generated peer runtimes could miss the rule even though documentation described it.

Resolution:

- added README as a current-state entrypoint directly to canonical runtime,
- made materially stale README an explicit documentation mismatch,
- required repair before release readiness,
- retained the rule against duplicating canonical detail documentation in README.

Status: **resolved**

### REC-README-004 – Custom GPT wording was too weak for static contract

Classification: **runtime projection mismatch**

Custom GPT contained the intended README and release-version behavior, but the wording did not explicitly satisfy the static runtime contracts for `stale README = documentation mismatch` and `release tag` as the version source.

Resolution:

- made stale README → documentation mismatch explicit,
- made release-tag-derived artifact versioning explicit,
- retained the version ownership/synchronization rule,
- kept the Custom GPT instruction below the 8,000-character platform limit.

Status: **resolved**

### REC-README-005 – Duplicate versioning guidance in deployment packaging standard

Classification: **documentation mismatch**

Release-readiness review found the tag-derived versioning paragraph duplicated in `docs/deployment-packaging-patterns.md`.

Resolution:

- removed the duplicate paragraph,
- retained one canonical statement of tag-derived version source and ecosystem-version ownership/synchronization.

Status: **resolved**

### README current-state behavior

Runtime behavior now requires README, when present, to be checked during final documentation reconciliation as the project entrypoint.

A materially stale README is treated as a documentation mismatch and must be repaired before release readiness.

README is an overview and navigation surface; it does not replace detailed canonical specification, architecture, installation, configuration or operations documentation.

Status: **consistent**

### Release version source behavior

For tag-triggered releases:

- artifact version is derived from the release tag by default,
- artifact names and release metadata use the same derived release version,
- an explicit alternative canonical version contract is permitted,
- ecosystem version files such as `package.json`, `pom.xml` or Gradle metadata require explicit ownership and synchronization/validation,
- unsynchronized independent release versions are not accepted.

Status: **consistent**

### Regression coverage

Coverage includes:

- stale README blocks release progression,
- current README allows progression,
- tag-owned release version derives from `vX.Y.Z`,
- mismatch between tag and secondary ecosystem version blocks release,
- ecosystem-owned versioning is allowed only when tag consistency is validated,
- static runtime contracts protect README reconciliation and release version source behavior.

Status: **consistent**

## Reconciliation result

**PASS, subject to required full CI for the final reconciled source revision.**

No unresolved implementation, documentation or decision mismatch remains in SB-61–SB-63.

After required CI PASS for the final reconciled revision, the change series may proceed to release readiness.
