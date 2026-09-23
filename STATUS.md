# System Builder – Status

## Övergripande status
**SB-51 IN PROGRESS – small-model robustness**

## Aktuellt steg
### SB-51 – Gör work status handlingsorienterad

Första steget i small-model robustness-serien är implementerat och väntar på required CI.

Förändringen:

- lägger till optional `execution`-hints med `next_action`, `step` och `operation`,
- lägger till optional `completion`-hints med `allowed`, `waiting_for`, verifierad implementation revision och evidence status,
- behåller schema version 1 och gör alla nya fält optional,
- har en explicit legacy fixture som saknar de nya fälten och ändå måste validera,
- synkroniserar projektets egen stale `.system-builder/work-status.yaml` från SB-06/SB-07 till faktisk SB-51-state.

## Fortsättningsplan

- SB-52: deterministic execution decision table
- SB-53: kritiska invariants först i runtimeinstruktionen
- SB-54: adversarial small-model evals

## Nästa åtgärd

Kör required CI för SB-51. Vid PASS kan steget klarmarkeras och nästa rekommenderade steg blir SB-52.
