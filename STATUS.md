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

SB-75 är implementerad och genomgår slutlig re-verifiering efter parity-reparationen. Custom GPT deklarerar nu explicit reducerat capability-aware stöd i metadata, utan ändring av instruktionstexten.

## Release state

`VERSION` är fortsatt `1.3.2`, men projektet är tillbaka i aktiv CHANGE-fas. En ny release readiness-bedömning krävs efter den nya change-serien innan någon release kan deklareras redo.

## Verifiering

Tidigare SB-75 PASS är superseded av slutlig parity-reparation. Ny full PR-CI är pending.

## Nästa åtgärd

Kör full projekt-CI efter parity-reparationen. Vid PASS görs completion-transition och slutlig mergebedömning för PR #14.
