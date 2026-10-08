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

**SB-71 – Capability-aware tool routing / execution profiles**

SB-70 är verifierad av full PR-CI. SB-71 är implementerad och använder discovery-resultatet för att välja den enklaste deterministiska execution profile som uppfyller operationens required capabilities. GitHub behåller repository authority även vid extern execution.

## Release state

`VERSION` är fortsatt `1.3.2`, men projektet är tillbaka i aktiv CHANGE-fas. En ny release readiness-bedömning krävs efter den nya change-serien innan någon release kan deklareras redo.

## Verifiering

SB-70 verifierades av System Builder CI run `37723538840`. SB-71 full PR-CI är pending.

## Nästa åtgärd

Kör full projekt-CI för SB-71. Vid PASS kan SB-71 completed och SB-72 Agent Workspace-integration blir nästa steg på samma PR #14.
