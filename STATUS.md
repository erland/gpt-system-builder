# System Builder – Status

## Övergripande status
**PASS – runtime migration in progress**

## Senast slutförda steg
### SB-46 – Modernisera build, lint och project hygiene

Build och hygiene är nu runtime-generiska för alla fyra aktiverade runtime-mål.

Infört:

- `runtime/distribution-registry.yaml` som gemensamt register,
- `build.targets` för Chat ZIP, Custom GPT, Claude Projects och OpenCode,
- generisk build och validation för samtliga distributioner,
- registry-validator som synkar registry, project config och runtime contract,
- CI använder registret i stället för fyra duplicerade build/validate-block,
- hygiene blockerar genererade runtime-projektioner i canonical source tree.

## Verifiering

- SB-45 CI: PASS
- aktiva targets måste matcha build.targets och planerade runtimes
- aktiva runtimes måste vara implemented i runtime contract
- artifact patterns måste vara unika och versionsparametriserade
- generated runtime adapters får inte bli canonical source
- befintlig Chat/Custom parity-körning bevaras tills SB-47 generaliserar parity-evalsen

## Blockerare
Inga.

## Nästa steg
**SB-47 – Utöka evals och runtime parity.**
