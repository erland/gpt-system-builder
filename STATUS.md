# System Builder – Status

## Övergripande status
**CHANGE IN PROGRESS – SB-64**

## Ny förändringsserie

- **SB-64** – deferred environment verification,
- **SB-65** – planning handoff ZIP före DEV-001,
- **SB-66** – regression coverage.

## Aktivt steg

SB-64 skiljer faktiska projektfel från verifiering som endast blockeras av aktuell runtime/miljö.

När exempelvis ett package registry inte kan nås får System Builder göra best effort, registrera uteblivna kontroller som deferred och fortsätta planen om:

- ingen faktisk project failure observerats,
- kontrollen inte är completion-blocking av risk/säkerhet/data/deployment-skäl,
- deferred checks sparas och inte rapporteras som PASS.

Machine state stödjer nu `passed_with_deferred` och strukturerade deferred checks.

## Nästa åtgärd

Verifiera SB-64 med full required CI.
