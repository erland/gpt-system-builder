# System Builder – Status

## Övergripande status
**READY_WITH_WARNINGS – v1.3.2 release candidate**

## Release readiness

Release readiness är klar för SB-67–SB-68.

- Version: `1.3.2`
- Tag: `v1.3.2`
- Required gates: **24/24 PASS**
- Blockers: **0**
- Warnings: **1**
- Full kandidat-CI: PASS för `c7822cda56b47ccf05bab309bd92992784994c98`

`v1.3.1` finns och bevaras. `v1.3.2` är ännu inte använd.

## Inkluderade förändringar

- saknad Chromium/WebKit/browser binary i ZIP/Chat-runtime behandlas som environment-limited verification,
- övrig möjlig verifiering körs ändå,
- browserprov defereras med varning och rapporteras aldrig som PASS utan faktisk körning,
- faktiskt Playwright-testfel är fortsatt project failure,
- GitHub-projekt använder normalt en Playwright CI-miljö som matchar projektets Playwright-version,
- PWA-kritiska browserkontroller ska normalt ha faktisk browser-evidens före release readiness,
- regressionsskyddet omfattar **49 instruction-adherence-fall, 41 critical**.

Custom GPT-instruktionen är **7 960 tecken**.

## Warning

Live Coolify target verification är fortsatt pending eftersom ingen faktisk Coolify-miljö varit tillgänglig. Den rapporteras inte som PASS och blockerar inte artifact release.

## Nästa åtgärd

Mergea PR #11. Efter merge kan `v1.3.2` taggas och release-workflowet publicera runtime-distributionerna.
