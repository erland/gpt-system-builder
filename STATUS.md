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

SB-74 är verifierad och completed. Browser Screenshot är nu optional visual-evidence backend med desktop som default, demand-driven extra viewports och tydlig separation från funktionell browser-verifiering. SB-75 är sista planerade steget i change-serien.

## Release state

`VERSION` är fortsatt `1.3.2`, men projektet är tillbaka i aktiv CHANGE-fas. En ny release readiness-bedömning krävs efter den nya change-serien innan någon release kan deklareras redo.

## Verifiering

SB-74 verifierades av full System Builder CI run `37725850680` på commit `807b26741881581585ca3be1d875b90c7bc50607`.

## Nästa åtgärd

Implementera SB-75 capability-aware degradation och regression coverage på samma PR #14. Efter PASS bör PR #14 vara redo för mergebedömning.
