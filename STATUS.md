# System Builder – Status

## Övergripande status
**READY_WITH_WARNINGS – v1.3.1 release candidate**

## Release readiness

Release readiness är klar för patchserien SB-64–SB-66.

- Version: `1.3.1`
- Tag: `v1.3.1`
- Required gates: **23/23 PASS**
- Blockers: **0**
- Warnings: **1**
- Full kandidat-CI: PASS för `743194c50028ea4ac954796fdb20dfe7e51356a4`

`v1.3.0` finns och bevaras. `v1.3.1` är ännu inte använd.

## Inkluderade förändringar

- environment-limited verification kan defereras med best effort och utan falskt PASS,
- faktiska projektfel blockerar fortfarande och kräver repair,
- riskkritiska verifieringar kan fortsatt vara completion-blocking,
- planning handoff ZIP skapas efter planering men före DEV-001,
- handoff-state är resumable mellan Chat, Work och andra runtimes,
- DEV-001 implementeras inte i handoff-körningen,
- regressionsskyddet omfattar 45 instruction-adherence-fall, varav 37 critical.

Custom GPT-instruktionen är **7 983 tecken**.

## Warning

Live Coolify target verification är fortsatt pending eftersom ingen faktisk Coolify-miljö varit tillgänglig. Den rapporteras inte som PASS och blockerar inte artifact release.

## Releaseversionering

Release-workflowet använder Git-taggen som canonical versionskälla.

När `v1.3.1` skapas härleds artifactversionen `1.3.1` och används för de fyra runtime-ZIP-filerna och release metadata.

## Nästa åtgärd

Mergea PR #10. Efter merge kan `v1.3.1` taggas och release-workflowet publicera runtime-distributionerna.
