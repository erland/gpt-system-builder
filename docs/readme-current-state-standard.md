# System Builder – README current-state standard

## Syfte

`README.md` är repositoryts current-state entrypoint. Den ska hjälpa en ny läsare att förstå vad systemet är, hur man kommer igång och var den canonical detaljdokumentationen finns.

README är inte ersättning för functional specification, architecture, installation, configuration eller operations documentation. Kontrollen gäller projekt som System Builder skapar eller ändrar, inte bara System Builder-repot självt.

## Minimikrav när relevanta

README ska vara konsekvent med faktisk implementation och övrig canonical dokumentation för:

- systemets syfte och huvudfunktioner,
- huvudsakliga runtime-/komponentmodell,
- hur projektet byggs, verifieras och körs,
- viktiga prerequisites,
- deploymentmodell på översiktsnivå,
- länkar till relevant installation/configuration/operations-dokumentation,
- aktivt stödda distributions-/leveransformer,
- release/version-information om README väljer att visa den.

## Final documentation reconciliation

När `README.md` finns ska System Builder alltid inkludera den i final documentation reconciliation före release readiness.

Kontrollen ska minst fråga:

1. Beskriver README fortfarande det system som faktiskt finns?
2. Har capabilities/runtime/deployment som tillkommit eller tagits bort hanterats?
3. Fungerar build/run-instruktionerna fortfarande?
4. Pekar länkar till nuvarande canonical dokument?
5. Innehåller README versions-/statuspåståenden som blivit stale?
6. Duplicerar README detaljinformation som bättre ägs av canonical docs?

En materiellt stale README är en **documentation mismatch**. Den ska repareras innan release readiness.

Denna semantiska reconciliation är den generella garantin för alla projekt. Projektspecifik automatisk README-validering bör läggas till när den kan kontrollera stabila maskinläsbara kontrakt utan att skapa falska antaganden om projektets struktur. System Builders egen `scripts/validate_readme_current_state.py` är ett sådant dogfooding-test och är inte i sig det generella projektkontraktet.

## CHANGE

När en change påverkar README-relevant current state ska README uppdateras som del av change-serien eller senast under final reconciliation.

## CREATE

CREATE ska normalt skapa en README som entrypoint när projektet är repository-baserat.

## Version och status

README bör undvika snabbt åldrande statusdetaljer när canonical machine state redan finns. Länka hellre till statusfil än att duplicera stegnummer eller releasekandidat.

Om README visar version ska den komma från projektets canonical versionskälla eller tydligt vara en hänvisning till senaste release.

## Anti-patterns

Undvik:

- gamla steg/status i README,
- hårdkodad gammal releasekandidat,
- buildkommandon som inte längre finns,
- listor över runtimes/deployment targets som inte matchar projektet,
- README som enda plats för viktig arkitektur eller driftinformation,
- kopierade detaljer som driver isär från canonical docs.
