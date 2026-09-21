# System Builder – Status

## Övergripande status
**PASS – runtime migration in progress**

## Senast slutförda steg
### SB-47 – Utöka evals och runtime parity

Instruction adherence och runtime parity omfattar nu samtliga aktiverade runtimes:

- Chat ZIP
- Custom GPT
- Claude Projects
- OpenCode

Parity bedöms explicit över fem canonical dimensioner:

- behavior
- capability
- artifact
- workspace_state
- tool

Claude Projects är fortsatt **reduced parity** och måste dokumentera de saknade exekveringsförmågorna utan att dölja dem som full equivalence.

## Verifiering

- SB-46 CI: PASS
- static instruction adherence körs för alla fyra distributioner
- samma canonical behavior-markers krävs i alla fyra runtime-entrypoints
- capability/artifact/workspace_state/tool jämförs mot canonical runtime contract
- Claude reduced parity kräver explicit dokumenterade begränsningar och bevarad no-false-PASS/state-authority
- OpenCode tool mapping måste motsvara canonical deklarerad tool-mängd och approval-policy

## Blockerare
Inga.

## Nästa steg
**SB-48 – Uppdatera CI, release och dokumentation.**
