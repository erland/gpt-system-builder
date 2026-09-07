# System Builder – Project Definition

## Syfte

System Builder ska hjälpa användaren att gå från behov, idé eller förändringsönskemål till ett fungerande, verifierat, dokumenterat och paketerat system genom ett sammanhållet utvecklingsflöde.

Canonical identitet, målgrupp, ansvar och avgränsningar finns i `docs/canonical-scope.md`.

## Huvudscenarier

- **CREATE** – skapa ett nytt system från behov eller idé.
- **CHANGE** – ändra eller utöka ett befintligt system.
- **IMPROVE** – genomföra avgränsade tekniska förbättringar.

## Planerade source modes

- ZIP
- GitHub

## Planerade runtimes

- Chat ZIP
- Custom GPT

## Projektprofil

Närmaste GPT Byggaren-profil: `zip_first_advanced`.

Avvikelse: GitHub-läge ska vara ett förstklassigt arbetsläge vid sidan av ZIP-läget.

## Dokumentprincip

- Markdown för människoläst intent, design och vägledning.
- YAML för maskinläsbart tillstånd, konfiguration och spårbarhet.
- JSON Schema för validering av maskinläsbara kontrakt.

## Source of truth för detta GPT-projekt

1. `gpt-project.yaml` – projektets canonical metadata och målbild.
2. `project-status.yaml` – faktisk utvecklingsstatus.
3. `docs/development-plan.md` – plan och klart-kriterier.
4. `STATUS.md` – mänskligt läsbar status.
5. Canonical implementation under `src/`, `knowledge/`, `schemas/` och `scripts/` när dessa byggs ut.

## Canonical process

Se `docs/end-to-end-process.md` för System Builders end-to-end-process och fasernas exit-kriterier.

## Adaptiv process

Se `docs/project-complexity.md` för canonical klassificering av `small`, `medium` och `large` samt artefakt- och kontrollnivåer.

## Dokument- och state-arkitektur

Se `docs/document-state-architecture.md` för canonical ansvarsfördelning mellan Markdown, YAML och JSON Schema samt regler för current-state, historik och maskinläsbar status.

## Maskinläsbart projekt- och arbetsstate

SB-06 introducerar `.system-builder/project.yaml` och `.system-builder/work-status.yaml`, validerade av `schemas/project.schema.json` respektive `schemas/work-status.schema.json`. Kör `python3 scripts/validate_state_contracts.py` för kontraktstester.

## Kravspårbarhet

Se `docs/traceability.md` för canonical regler och `.system-builder/traceability.yaml` för maskinläsbar spårbarhet.

## Deploymentprofil

Se `docs/deployment-profile.md` för canonical deploymentkontrakt och `.system-builder/deployment-profile.yaml` för maskinläsbar profil.

## Funktionell specifikation

Se `docs/functional-specification-standard.md` för canonical struktur och kvalitetsregler.

## Arkitekturbeskrivning

Se `docs/architecture-standard.md` för canonical struktur och kvalitetsregler för `docs/architecture.md`.

## ADR och produktbeslut

Se `docs/decision-records-standard.md`.

## Development plan-standard

Se `docs/development-plan-standard.md` för canonical planstruktur, stegstorlek och verifieringsregler.

## Risk och feasibility

Se `docs/risk-feasibility-standard.md` för canonical regler för risk, blockerare, spikes och PoC.

## Test och verifiering

Se `docs/test-verification-standard.md` för canonical verifieringsstrategi och release gates.

## Säkerhetsbaslinje

Se `docs/security-baseline.md` för canonical security baseline och specialistgranskningsregler.

## CREATE-läge

Se `docs/create-mode.md` för canonical nyutvecklingsflöde.

## CHANGE-läge

Se `docs/change-mode.md` för canonical förändringsflöde för befintliga system.

## IMPROVE-läge

Se `docs/improve-mode.md` för canonical beteendebevarande förbättringsflöde.

## Next-step state machine

Se `docs/next-step-state-machine.md` för canonical styrning av `Gör nästa steg`.

## ZIP-läge

Se `docs/zip-mode.md` för canonical first-class ZIP source/delivery workflow.

## GitHub-läge

Se `docs/github-mode.md` för canonical branch/PR/commit/resume-flöde.

## Repository hygiene

Se `docs/repository-hygiene.md` för canonical filklassificering, ignore-policy och release hygiene.

## GitHub Actions-baslinje

Se `docs/github-actions-baseline.md` för canonical CI-policy och verifieringsregler.

## Deployment och packaging

Se `docs/deployment-packaging-patterns.md` för canonical deploymentprofiler och packagingkontrakt.

## Docker-baslinje

Se `docs/docker-baseline.md` för canonical containerstandard och verifieringsregler.

## Coolify-profil

Se `docs/coolify-profile.md` för canonical Coolify + external PostgreSQL deploymentprofil.

## Configuration, installation och operations

Se `docs/configuration-installation-operations-standard.md` för canonical runbook-struktur och dokumentansvar.

## Release readiness och system acceptance

Se `docs/release-readiness-standard.md` för canonical releasebeslut, acceptance och gate-modell.

## Knowledge-arkitektur

Se `docs/knowledge-architecture.md` för gränsen mellan canonical runtime-regler och referensmaterial.

## Canonical runtime-instruktion

Kärninstruktionen finns i `runtime/canonical-instructions.md` och dess direkta referenser i `runtime/runtime-manifest.yaml`.

## Chat ZIP-runtime

Chat-distribution byggs med `scripts/build_chat_runtime_zip.py` och valideras med `scripts/validate_chat_runtime_zip.py`.

## Custom GPT-kompilering

Byggs med `scripts/build_custom_gpt_distribution.py` och valideras med `scripts/validate_custom_gpt_distribution.py`.

## Instruction-adherence evals

Behavioral suite: `evals/instruction-adherence.yaml`. Static parity: `scripts/run_static_instruction_evals.py`.

## SB-34 E2E small CREATE

See `evals/e2e/small-create/` and `scripts/run_e2e_small_create_eval.py`.

## SB-35 E2E existing-system CHANGE

See `evals/e2e/existing-system-change/` and `scripts/run_e2e_existing_change_eval.py`.

## SB-36 E2E Docker/Coolify

See `evals/e2e/docker-coolify/` and `scripts/run_e2e_docker_coolify_eval.py`.

## Runtime parity

Validated by `scripts/validate_runtime_parity.py`.

## System Builder project CI

Canonical CI entrypoint: `scripts/ci-project.sh`. GitHub workflow: `.github/workflows/ci.yml`.

## GitHub Release build

Release-build: `.github/workflows/release.yml` + `scripts/build_release.sh`; taggen styr versionen.

## Final release readiness

See `evals/final-release-readiness-report.md` and `evals/final-release-readiness.yaml`.
