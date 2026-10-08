# System Builder – Status

## Övergripande status

**CHANGE IN PROGRESS – capability-aware execution**

System Builder har fem aktiva runtime-distributioner: Chat ZIP, Custom GPT, Claude Projects, OpenCode och OpenAI Plugin.

PR #11 och PR #12 är mergade. Den tidigare release-readiness-evidensen för `v1.3.2` togs fram före OpenAI Plugin-ändringen i PR #12 och är därför inte längre aktuell release-evidens för nuvarande `main`.

## Aktiv change-serie

Change request: `capability-aware-execution`

Planerade steg:

- **SB-69** – reconcile current project state
- **SB-70** – capability discovery
- **SB-71** – capability-aware tool routing/execution profiles
- **SB-72** – Agent Workspace-integration
- **SB-73** – PWA Preview-integration
- **SB-74** – Browser Screenshot-integration
- **SB-75** – capability-aware degradation och regression coverage

## Aktuellt steg

**SB-75 – capability-aware degradation och regression coverage**

SB-75 är implementerad och verifierad. Regression-suiten täcker åtta capability/degradation-scenarier och runtime parity över de fem aktiva distributionerna.

## Release state

`VERSION` är fortsatt `1.3.2`, men projektet är tillbaka i aktiv CHANGE-fas. En ny release readiness-bedömning krävs efter den nya change-serien innan någon release kan deklareras redo.

## Verifiering

SB-75 verifierades av full System Builder CI run `37726151547` på commit `b476c494499920b90ec9848bdd5458208c37b1b2`. Den nya regression-suiten rapporterade `PASS: capability-aware degradation scenarios (8 scenarios)`.

## Nästa åtgärd

Gör completion-transition för SB-75 och därefter mergebedömning för PR #14.
