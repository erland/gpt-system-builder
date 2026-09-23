# System Builder – Status

## Övergripande status
**READY_WITH_WARNINGS – SB-54 complete, release fix in progress**

## Senast slutförda steg
### SB-54 – Adversarial small-model evals

SB-54 är verifierad med full required CI för revision `44f84e1721b60a16c2899e81078029cd1a0b2367` och är completed.

Small-model robustness-serien SB-51–SB-54 är därmed genomförd.

## Release-fix

Releasebygget för `v1.2.0` stoppades korrekt av en föråldrad validator som fortfarande krävde exakt SB-49 och av versionsmetadata som fortfarande pekade på `1.0.0-rc.2`.

Fixen:

- gör release-candidate-valideringen generell mot aktuell `plan.total_steps`,
- kräver komplett ordnad step- och SB-ID-historik,
- synkar release candidate till `1.2.1`,
- undviker att flytta eller återanvända den redan skapade `v1.2.0`-taggen.

## Nästa åtgärd

Verifiera full CI för release-fixen. Vid PASS kan PR:n mergas och därefter ska nästa release taggas som `v1.2.1`.
