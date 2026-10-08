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

**SB-72 – Agent Workspace integration (re-verification)**

Den live Agent Workspace-installationen är nu åtkomlig. SB-72 har reconcilerats mot faktiska capabilities: dynamisk provider/capability-probe, verify före build när artifact inte behövs, build endast för artifact-handoff och signed download links när hosten erbjuder dem. Eftersom detta ändrade runtime-kontraktet är SB-72 återöppnad tills full CI passerar igen.

## Release state

`VERSION` är fortsatt `1.3.2`, men projektet är tillbaka i aktiv CHANGE-fas. En ny release readiness-bedömning krävs efter den nya change-serien innan någon release kan deklareras redo.

## Verifiering

Tidigare SB-72-PASS är superseded av live capability reconciliation. Ny full PR-CI är pending.

## Nästa åtgärd

Kör full projekt-CI för reconcilerad SB-72. Vid PASS blir SB-73 åter nästa steg på samma PR #14.
