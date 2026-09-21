# System Builder – Status

## Övergripande status
**READY_WITH_WARNINGS – runtime migration complete**

## Senast slutförda steg
### SB-49 – Full regression och ny release candidate

Migreringsplanen SB-42–SB-49 är genomförd. System Builder har nu fyra aktiverade runtime-distributioner från samma canonical kontrakt:

- Chat ZIP
- Custom GPT
- Claude Projects
- OpenCode

OpenAI Plugin v1 är fortsatt explicit bedömd som reduced / not planned.

## Release candidate

- Version: `1.0.0-rc.2`
- Tagg: `v1.0.0-rc.2`
- Release readiness: `READY_WITH_WARNINGS`
- Blockerare: 0
- Required gates: 19/19 PASS

Varningen är oförändrad: live-verifiering mot en faktisk Coolify-miljö har inte körts och rapporteras därför inte som PASS.

## Verifiering

- SB-48 CI: PASS
- fyra runtime-distributioner byggs färskt i CI
- alla fyra valideras
- instruction adherence passerar för alla fyra
- runtime parity accepterad över behavior/capability/artifact/workspace_state/tool
- CREATE/CHANGE/Docker-Coolify E2E ingår i full regression
- runtime-aware repository hygiene ingår
- release candidate-validering håller VERSION, tagg, registry, runtime compatibility och readiness synkade

## Nästa åtgärd

Efter grön SB-49 CI kan PR #2 mergas. Därefter kan taggen `v1.0.0-rc.2` användas för att publicera den nya GitHub Release-kandidaten.
