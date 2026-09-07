# Runtime behavior walkthrough – Example

User: "Gör nästa steg"

Expected System Builder behavior:

1. Read current source and work status.
2. Assess blockers, failed verification and source drift.
3. Continue active incomplete step if one exists.
4. Otherwise select the first safe incomplete planned step.
5. Lock the step.
6. Implement only that step.
7. Run required verification.
8. If verification fails, keep the step incomplete and recommend REPAIR.
9. If verification passes, update current-state docs and machine state.
10. Build complete ZIP or commit/push to active GitHub work series.
11. Report the result and next recommended action.
12. Stop.

The runtime must not automatically begin another development step.
