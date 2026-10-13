## 3. One-step rule

When the user says:

- "Gör nästa steg"
- "Fortsätt"
- "Ta nästa"
- "Implementera nästa steg"

perform **one safe development step** by default, then stop.

Do not automatically continue to another development step.

Canonical loop:

```text
READ
→ ASSESS
→ SELECT
→ LOCK
→ IMPLEMENT
→ VERIFY
→ REVIEW
→ UPDATE DOCS
→ UPDATE STATUS
→ PACKAGE / COMMIT
→ STOP
```

First-hop decision procedure: `runtime/execution-rules.md`.
Detailed rules: `docs/next-step-state-machine.md`.

Completion after verification follows `docs/completion-verification.md`: bind PASS to the source revision actually verified, then allow a state-only completion transition with lightweight consistency validation when source is unchanged.

## 4. Selection priority

Choose the next safe action from actual state. Prefer a valid `execution.next_action` hint when present, but never over actual blockers, verification evidence or source drift.

Use `runtime/execution-rules.md` as the deterministic IF/ELSE decision table.

Priority:

1. blockers
2. failed required verification
3. source drift / state inconsistency
4. repair of active/incomplete step
5. unmet dependencies
6. first safe incomplete planned step
7. release/readiness work when implementation is complete

Never use a blind `next = current + 1` rule.

## 5. Step completion

A step is complete only when:

- its scoped deliverable exists,
- required verification passes,
- done criteria are met,
- relevant docs/state are updated,
- repository hygiene is acceptable,
- delivery artifact/commit is produced when required.

If required verification fails:
- do **not** mark the step completed,
- record failure/blocker,
- make REPAIR the next action,
- stop.

Never report an unrun check as PASS. Environment-only limitations may be recorded as `passed_with_deferred` after best-effort verification when no project failure is observed and the missing check is not completion-blocking; retry deferred release-relevant checks later. For Playwright/browser tests, missing Chromium/WebKit/browser binaries in the current ZIP/runtime is environment-limited when the test environment itself is unavailable: run all other feasible checks, defer browser tests with a warning, and continue when risk allows. If GitHub is available, prefer browser verification in CI using a Playwright environment matching the project Playwright version. A browser test that actually runs and fails is project failure, not deferred verification. For PWA, release-relevant checks such as service worker, offline behavior, routing/installability or browser storage should normally have actual browser PASS evidence before release readiness.

When remote CI is required and is genuinely completion-blocking, do not mark the step completed before that CI passes for the implementation revision. After PASS, a completion-only state change does not require repeating full verification if no verification-relevant source changed; run lightweight state/consistency validation instead.

## 16. State and traceability

Machine-readable state belongs under `.system-builder/`.

Use:

- `.system-builder/project.yaml`
- `.system-builder/work-status.yaml`
- `.system-builder/traceability.yaml`
- `.system-builder/deployment-profile.yaml`

when applicable.

Human intent/design belongs in Markdown.
Schemas validate YAML.
Do not duplicate the same truth across both.

## 17. ZIP mode

ZIP is a first-class source/delivery mode.

When working from ZIP:

```text
RECEIVE ZIP
→ SAFE EXTRACT
→ READ STATE
→ ASSESS
→ SELECT ONE STEP
→ IMPLEMENT
→ VERIFY
→ UPDATE STATE/DOCS
→ BUILD COMPLETE PROJECT ZIP
→ VERIFY ZIP
→ DELIVER
→ STOP
```

Default output is a **complete project ZIP**, not only changed files.

For ZIP completion, proactively run every required verification gate that is technically possible with available tools/runtime. CI is not inherently an external gate when equivalent canonical build/test/validation commands can run locally. Require external/manual verification only when no technically equivalent check is possible because of unavailable environment, credentials/service, physical resource, live deployment, or genuinely human acceptance. Keep incomplete only for such remaining required gates, and distinguish verified PASS/FAIL from external pending.

Protect against:
- path traversal,
- self-inclusion,
- transient/generated junk,
- secrets.

Canonical rules: `docs/zip-mode.md`.

## 18. GitHub mode

GitHub is a first-class source mode.

Repository, branch, PR, commits, CI and work status are execution state.

Default:

- one work branch/PR per coherent CREATE/CHANGE/IMPROVE series,
- reuse the active PR for the same series,
- one completed `DEV` step per commit when practical,
- required verification before completed commit,
- CI/review feedback can block or repair the active step,
- do not force-push by default.

If GitHub write access is unavailable, do not pretend to have pushed/created a PR; fall back to ZIP/patch delivery.

For GitHub completion, prefer: implementation commit → full required CI PASS → completion-only commit → lightweight completion check. The completion-only commit must not contain implementation or other verification-relevant changes. Required checks should still resolve on the latest commit; do not rely on a skipped required workflow.

Canonical rules: `docs/github-mode.md`.

