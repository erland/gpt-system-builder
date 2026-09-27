# System Builder – Status

## Övergripande status
**CHANGE IN PROGRESS – SB-61 complete, SB-62 next**

## Senast slutförda steg
### SB-61 – README som current-state entrypoint

SB-61 är verifierad med full required CI för revision `f6292a7a955aa83966ed11d181c3261256bca372` och är completed.

System Builder behandlar nu `README.md` som projektets current-state entrypoint när filen finns.

Final documentation reconciliation ska uttryckligen kontrollera README mot faktisk implementation och canonical dokumentation. En materiellt stale README är en documentation mismatch som måste lösas före release readiness.

README ska vara en översikt och länka vidare till functional specification, architecture, installation/configuration/operations och annan canonical detaljdokumentation i stället för att duplicera den.

System Builders egen stale README har reconcilerats och full CI innehåller nu `scripts/validate_readme_current_state.py`.

## Aktiv förändringsserie

Återstående:

- **SB-62** – release tag som canonical versionskälla,
- **SB-63** – regression coverage.

## Nästa åtgärd

Implementera SB-62 på samma PR.
