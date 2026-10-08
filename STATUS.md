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

**SB-73 – PWA Preview integration**

SB-72 är verifierad och completed. GitHub Actions är nu explicit förstahandsval i GitHub source mode när CI räcker; Agent Workspace används endast när det tillför en required capability eller ett explicit workflowbehov motiverar extra execution-kostnad. SB-73 är nästa planerade steg.

## Release state

`VERSION` är fortsatt `1.3.2`, men projektet är tillbaka i aktiv CHANGE-fas. En ny release readiness-bedömning krävs efter den nya change-serien innan någon release kan deklareras redo.

## Verifiering

SB-72 verifierades av full System Builder CI run `37724643707` på commit `b36faa2863915eb0c3bf884fd50b13f2330f2913`.

## Nästa åtgärd

Implementera SB-73 PWA Preview-integration på samma PR #14.
