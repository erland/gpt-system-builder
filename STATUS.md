# System Builder – Status

## Övergripande status
**CHANGE IN PROGRESS – SB-61**

## Ny förändringsserie

README reconciliation och releaseversionering:

- **SB-61** – README som current-state entrypoint och final reconciliation gate,
- **SB-62** – release tag som canonical versionskälla,
- **SB-63** – regression coverage.

## Aktivt steg

SB-61 gör README-kontrollen generell för projekt som System Builder skapar eller ändrar.

En materiellt stale README ska räknas som documentation mismatch före release readiness. README ska vara en current-state entrypoint och länka vidare till canonical detaljdokumentation i stället för att duplicera den.

System Builders egen README har samtidigt reconcilerats mot aktuell state och en validator har lagts till i full project CI.

## Nästa åtgärd

Verifiera SB-61 med full required CI. Därefter är SB-62 nästa steg.
