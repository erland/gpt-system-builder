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

SB-75 är verifierad och completed. Custom GPT behåller sin befintliga instruktionstext och deklarerar explicit reducerat capability-aware stöd i metadata; övriga runtimes behåller sin starkare capability-aware funktionalitet enligt parity-kontraktet.

## Release state

`VERSION` är fortsatt `1.3.2`, men projektet är tillbaka i aktiv CHANGE-fas. En ny release readiness-bedömning krävs efter den nya change-serien innan någon release kan deklareras redo.

## Verifiering

SB-75 verifierades av full System Builder CI run `37727138092` på implementation revision `12feba26fc113d4199d1adb3ef541a8a1bd8ded2`. Full gate inkluderade project-ZIP build/integritetskontroll, fem distributionsbyggen/-valideringar och capability-aware runtime parity.

## Nästa åtgärd

PR #14 är redo för slutlig merge review.
