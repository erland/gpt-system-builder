## 12. CREATE

CREATE flow:

```text
NEED
→ DISCOVERY
→ GOALS + SUCCESS
→ SCOPE
→ FUNCTIONAL SPEC
→ RISK / FEASIBILITY
→ ARCHITECTURE
→ DEVELOPMENT PLAN
→ PLANNING HANDOFF ZIP
→ IMPLEMENTATION LOOP
→ FINAL DOCUMENTATION RECONCILIATION
→ PACKAGING
→ DEPLOYMENT READINESS
→ ACCEPTANCE / RELEASE READINESS
→ INSTALL / OPS DOCS
→ RELEASE
```

Adapt depth to project complexity.

When CREATE planning is complete and the next action would otherwise be DEV-001, first create a planning handoff ZIP. Include the planning/current-state artifacts and canonical machine state, set the first development step as `next.recommended`, keep `selected_step` and `in_progress` null, do not implement DEV-001 in that run, verify ZIP integrity/resumability, deliver the checkpoint, and stop. A later Chat/Work/runtime execution selects and locks DEV-001 normally.

