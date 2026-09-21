# System Builder – Status

## Övergripande status
**PASS – runtime migration in progress**

## Senast slutförda steg
### SB-44 – Implementera Claude Projects-runtime

Claude Projects är nu en byggbar runtime-distribution härledd från System Builders
canonical instruktion och plattformsneutrala runtime-kontrakt.

Distributionen innehåller:

- `project-instructions.md` från canonical runtime-instruktion,
- relevant Knowledge,
- `runtime-contract.json` som snapshot,
- `compatibility.md` med explicit **reduced parity**,
- README med installations-/användningsinstruktioner.

## Verifiering

- SB-43 CI: PASS
- builder för Claude Projects införd
- validator för Claude Projects införd
- ordinarie CI bygger och validerar Claude Projects-ZIP
- validatorn kräver canonical behavior-markers
- validatorn förbjuder development-only state/scripts i distributionen
- validatorn kräver att reduced parity och begränsningar för exekvering/GitHub/state är explicita

## Blockerare
Inga.

## Nästa steg
**SB-45 – Implementera OpenCode-runtime.**
