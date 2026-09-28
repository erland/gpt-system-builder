# System Builder – Completion och verifierad source revision

## 1. Syfte

Detta dokument definierar hur ett utvecklingssteg går från `in_progress` till `completed` utan att förväxla implementation med completion-state eller köra om dyr verifiering i onödan.

Grundprincip:

> Ett steg får normalt markeras `completed` först när required verification för den source revision som steget avser har PASS.

Undantag: en kontroll som inte kan köras färdigt enbart på grund av aktuell runtime/miljö får klassificeras som **deferred environment verification** när reglerna nedan är uppfyllda. Då kan steget markeras completed med `passed_with_deferred`, utan att kontrollen rapporteras som PASS.

Completion är därefter en state transition. Om completion endast ändrar tillåtet machine state behöver den inte utlösa samma fulla verifiering en gång till.

## 2. Verifierad source revision

Verification evidence ska, när runtime/source mode medger det, bindas till en identifierbar source revision.

Exempel:

- GitHub: commit SHA.
- ZIP: SHA-256 för verifierad project source/package eller annan stabil source fingerprint.
- Annat workspace: runtime-specifik immutable revision/fingerprint.

En PASS gäller den revision som faktiskt verifierades. Om executable source, buildkonfiguration eller annan verifieringsrelevant input ändras efter PASS är evidensen stale och full required verification ska köras igen.

## 3. Completion transition

Normal modell:

```text
IMPLEMENT SOURCE
→ FULL REQUIRED VERIFICATION
→ PASS FOR IDENTIFIED SOURCE REVISION
→ COMPLETION TRANSITION
→ LIGHTWEIGHT STATE/CONSISTENCY VALIDATION
→ DELIVER / STOP
```

Completion transition får endast ändra state och metadata som direkt följer av verifieringsresultatet, exempelvis:

- selected/in-progress → completed,
- completion evidence,
- next recommended,
- blocker/failure resolution som direkt följer av PASS,
- traceability-status som endast uttrycker completion.

Den får inte smyga in implementation, dependency-, workflow-, deployment- eller annan verifieringsrelevant förändring.

## 4. Lightweight completion validation

Efter en ren completion transition ska System Builder verifiera proportionellt:

- schema-validitet för ändrat machine state,
- state transition consistency,
- att recorded evidence refererar till den verifierade revisionen,
- att inga otillåtna filer eller sourceändringar ingår,
- att next recommended kan härledas från aktuell plan/state.

Detta är inte samma sak som att påstå att full build/test/e2e körts mot completion-state-revisionen.

## 5. GitHub mode

I GitHub-läge är normal sekvens:

```text
implementation commit
→ push
→ required full CI
→ PASS for implementation commit SHA
→ completion-only commit
→ lightweight completion check
→ STOP
```

Completion-only commit får endast innehålla tillåtna state/traceability-filer som projektets policy uttryckligen klassificerar som completion metadata.

Om committen innehåller någon verifieringsrelevant förändring ska snabbspåret inte användas; full CI krävs.

### Required checks

Använd inte ett upplägg där required workflow helt uteblir på completion-committen och därmed riskerar pending/missing required checks.

Föredra i stället ett stabilt required check/workflow som alltid körs och internt väljer:

- full verification för vanliga source changes,
- lightweight completion validation för en strikt verifierad completion-only change.

## 6. ZIP mode

ZIP-runtime ska först försöka köra all required verification som tekniskt kan utföras med tillgängliga verktyg och miljö. En CI-gate är inte automatiskt extern om dess canonical verifieringskommandon kan köras lokalt med likvärdig evidens.

När System Builder själv kan köra all required verification:

```text
ZIP source
→ implementation
→ full required verification
→ PASS
→ completion transition
→ lightweight state validation
→ build and verify complete output ZIP
```

Ingen extra full verifiering krävs efter att endast completion-state ändrats.

Endast om en required gate efter best-effort-bedömning genuint kräver en otillgänglig extern miljö, credential, fysisk resurs eller mänsklig acceptance får steget lämnas pending och inte markeras completed. Leverera i stället ett resumable checkpoint med steget fortsatt incomplete/pending verification. När giltig extern evidence senare kan knytas till oförändrad source får completion transition genomföras utan att full verifiering körs om enbart för statusändringen.

## 7. Backward compatibility

Äldre System Builder-projekt ska fungera utan förhandsmigrering.

Regler:

1. Om äldre `.system-builder/work-status.yaml` saknar explicit verified-source-fält ska filen fortfarande accepteras enligt projektets befintliga schema.
2. System Builder får härleda verifierad revision från faktisk GitHub CI/commit-evidens, ZIP-checksum eller befintliga verification notes när sambandet är entydigt.
3. Om sambandet inte kan bevisas säkert används den äldre säkra modellen: full required verification före completion.
4. Nya optional state-fält får endast skrivas om projektets aktuella schema stödjer dem, eller om schema/state uppgraderas explicit och bakåtkompatibelt som del av samma arbete.
5. Avsaknad av nya fält är aldrig ensam anledning att blockera resume.

## 8. Stale evidence

Full verification måste köras igen om exempelvis något av följande ändras efter den verifierade revisionen:

- executable source,
- tests som ingår i required contract,
- dependency/lock files,
- build configuration,
- Docker/deployment artifacts som verifieringen omfattar,
- CI/workflow-logik som definierar required verification,
- schema/contract som påverkar verifieringsutfallet.

Ren completion metadata gör inte tidigare evidence stale.

## 8A. Deferred environment verification

Skilj på faktisk projektfailure och miljöbegränsning.

### Project failure

Om en verifiering faktiskt körs och visar exempelvis:

- compile/build error,
- lint/typecheck error,
- failing test,
- schema/contract violation,
- runtime crash som kan härledas till projektet,

är utfallet FAIL och steget ska repareras innan senare beroende steg.

### Environment-limited verification

En kontroll kan defereras om:

1. System Builder försökte köra kontrollen eller en tekniskt likvärdig kontroll.
2. Evidensen pekar på miljön, exempelvis registry/network timeout, saknad package cache, otillgänglig extern toolchain eller liknande runtimebegränsning.
3. Ingen körd kontroll visar ett projektfel.
4. Kontrollens riskklass kräver inte completion-blocking verifiering.
5. Den defererade kontrollen registreras i machine state med check, reason, evidence/retry condition och om den blockerar release.

Typiskt exempel: `npm install` kan inte nå npm-registret och lokal cache saknas. Statisk granskning och andra möjliga kontroller genomförs, steget kan completed med varning, och lint/test/build läggs i deferred-listan.

### Får inte defereras för att fortsätta

Verifiering ska fortsatt blockera completion när den behövs för att säkert gå vidare, exempelvis vid:

- verifierad eller misstänkt data-/migrationsrisk,
- säkerhetskritisk kontroll,
- destruktiv/irreversibel operation,
- deployment/production gate som uttryckligen är required före nästa steg,
- en planregel som explicit markerar kontrollen completion-blocking.

### Senare hantering

Deferred checks ska återförsökas opportunistiskt när miljön senare medger det. Release readiness får inte kalla dem PASS. En release-relevant deferred check måste antingen lösas eller uttryckligen hanteras av releasepolicyn som warning/non-blocking.

## 9. Failure

Om required verification visar faktisk project FAIL:

- steget förblir incomplete,
- completion transition får inte göras,
- failure/blocker registreras,
- nästa säkra åtgärd är repair/unblock.

Om kontrollen endast är environment-limited ska 8A användas i stället för att mekaniskt blockera planen.

## 10. Anti-patterns

Undvik:

- markera completed före required remote CI PASS,
- köra full CI igen endast för en ren statusändring när lightweight validation kan bevisa att source är oförändrad,
- använda osäkra `paths-ignore` så required check saknas på senaste committen,
- blanda implementation i completion-only commit,
- återanvända PASS från en revision efter verifieringsrelevant source drift,
- kräva migrering av äldre project state bara för att kunna återuppta arbetet.
