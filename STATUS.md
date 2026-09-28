# System Builder – Status

## Övergripande status
**CHANGE IN PROGRESS – SB-64 complete, SB-65 next**

## Senast slutförda steg
### SB-64 – Deferred environment verification

SB-64 är verifierad med full required CI för revision `e80d7548574f408bdf723556d8e641cfc5c8de47` och är completed.

System Builder skiljer nu mellan:

- faktisk **project failure**, som fortfarande blockerar och kräver repair,
- **environment-limited verification**, där best effort genomförs och kontrollen kan defereras med varning om riskreglerna tillåter.

Machine state stödjer `passed_with_deferred` samt strukturerade deferred checks med reason, evidence/retry condition och release-blocking-status.

Deferred checks får aldrig rapporteras som PASS. Release-relevanta kontroller ska återförsökas senare och kan fortfarande blockera release.

## Aktiv förändringsserie

Återstående:

- **SB-65** – planning handoff ZIP före DEV-001,
- **SB-66** – regression coverage.

## Nästa åtgärd

Implementera SB-65 på samma PR.
