## 13. CHANGE

CHANGE is for new or changed intended behavior.

Flow:

```text
CHANGE REQUEST
→ READ CURRENT SYSTEM
→ BASELINE
→ CLARIFY CHANGE
→ GOALS + SCOPE
→ IMPACT ANALYSIS
→ UPDATE FUNCTIONAL SPEC
→ RISK / FEASIBILITY
→ UPDATE ARCHITECTURE
→ CHANGE PLAN
→ IMPLEMENTATION LOOP
→ REGRESSION / ACCEPTANCE
→ FINAL DOCUMENTATION RECONCILIATION
→ PACKAGING / DEPLOYMENT CHECKS
→ RELEASE READINESS
```

Functional specification and architecture are governing current-intent documents during CHANGE. Do not change their direction merely because implementation diverges. Update them when the user or another explicit accepted decision changes intended behavior/architecture.

During each development step, detect divergence between implementation and governing intent. Do not silently reconcile by rewriting intent to match code.

Before release readiness, perform final documentation reconciliation between actual implementation and governing functional specification/architecture. Classify any mismatch as:
- implementation does not meet intended documentation → change implementation,
- documentation is stale after an explicit accepted decision → update documentation,
- genuine product/architecture decision is unresolved → ask the user before proceeding.

If `README.md` exists, treat it as the project's current-state entrypoint and verify it still represents the current implemented system. A materially stale README is a documentation mismatch and must be fixed before release readiness. Correct stale purpose/capability/build/run/runtime/deployment/version/link claims without duplicating canonical docs.

Historical change records explain why/how the change happened.

