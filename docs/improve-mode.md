# System Builder – IMPROVE-läge

## 1. Syfte

IMPROVE används när ett befintligt system ska förbättras tekniskt utan avsiktlig funktionell förändring.

Typiska mål:

- bättre struktur,
- bättre testbarhet,
- enklare byggkedja,
- förbättrad CI,
- säkrare dependencies,
- enklare deployment,
- lägre teknisk skuld,
- bättre prestanda utan ändrat funktionellt kontrakt.

IMPROVE ska bevara observerbart avsett beteende om inte användaren uttryckligen godkänner en funktionell förändring.

## 2. När IMPROVE ska väljas

Välj IMPROVE när användaren vill:

- refaktorera,
- reducera duplication,
- förbättra modulgränser,
- uppgradera bygg-/testinfrastruktur,
- förbättra lint/typecheck,
- förenkla deployment,
- förbättra observability,
- göra avgränsade dependency upgrades,
- förbättra prestanda utan ändrat funktionskontrakt.

Välj i stället CHANGE när:
- nytt beteende tillkommer,
- befintligt beteende ändras,
- affärsregel ändras,
- UI/API-kontrakt ändras funktionellt.

## 3. Huvudregel

> IMPROVE får inte smyga in funktionell förändring under etiketten refaktorering.

Om arbete upptäcker att ett funktionellt kontrakt måste ändras ska System Builder:
1. stoppa eller avgränsa IMPROVE-steget,
2. dokumentera behovet,
3. skapa eller rekommendera separat CHANGE-serie.

## 4. Canonical flöde

```text
IMPROVEMENT REQUEST
→ READ CURRENT SYSTEM
→ BASELINE
→ DEFINE TECHNICAL GOAL + NON-GOALS
→ IDENTIFY BEHAVIOR TO PRESERVE
→ RISK / CHARACTERIZATION
→ IMPROVEMENT PLAN
→ IMPLEMENTATION LOOP
→ REGRESSION / PERFORMANCE / BUILD VERIFICATION
→ UPDATE ARCHITECTURE / OPS IF ACTUALLY AFFECTED
→ RELEASE READINESS AS APPROPRIATE
```

## 5. Read current system

Läs:

- current code,
- tests,
- build/CI,
- work status,
- active plan,
- functional spec,
- architecture,
- dependency/build configuration,
- deployment profile när relevant.

IMPROVE ska utgå från faktisk source, inte enbart dokumentation.

## 6. Baseline

Etablera relevant baseline före ändring.

Kan omfatta:

- build pass/fail,
- test pass/fail,
- lint/typecheck,
- test coverage som observationsdata,
- performance metric,
- container build/startup,
- dependency scan,
- bundle size,
- startup time.

Baseline ska vara tillräcklig för att avgöra om förbättringen orsakar regression.

## 7. Technical goal

Varje IMPROVE-serie ska ha ett tydligt tekniskt mål.

Bra:
- separera GitHub-integration från application service för bättre testbarhet,
- minska frontend bundle size under en definierad nivå,
- ersätta duplicerad validation med en gemensam komponent,
- få backend och frontend build att köras reproducerbart i CI.

Svagt:
- städa kod,
- gör arkitekturen bättre.

## 8. Non-goals

Definiera explicit vad som inte ska ändras.

Exempel:
- inga nya användarfunktioner,
- inget API-kontraktsbyte,
- ingen datamigration,
- ingen UI-redesign.

Non-goals skyddar mot scope creep.

## 9. Behavior preservation

System Builder ska identifiera vilket observerbart beteende som måste förbli oförändrat.

Det kan vara:
- API responses,
- UI flows,
- persisted data,
- external integration behavior,
- CLI output,
- file formats.

## 10. Characterization tests

När befintligt beteende är svagt testat eller svårt att förstå ska characterization tests skapas före riskfylld refaktorering.

Syfte:
- fånga faktisk baseline,
- skydda mot oavsiktlig regression.

Characterization test betyder inte att beteendet är idealiskt.

## 11. Risk

Bedöm särskilt:
- blast radius,
- hidden coupling,
- legacy behavior,
- migration risk,
- dependency incompatibility,
- build/runtime changes,
- deployment assumptions.

Bred refaktorering utan baseline kan bli blockerare.

## 12. Improvement plan

Planen ska vara liten och reversibel där möjligt.

Typiskt:

```text
DEV-001 – Establish baseline
DEV-002 – Add characterization tests
DEV-003 – Refactor one boundary
DEV-004 – Verify regression/performance
DEV-005 – Update architecture/ops if needed
```

## 13. Step size

Ett IMPROVE-steg ska normalt:
- ändra ett sammanhängande tekniskt område,
- ha tydligt före/efter,
- kunna verifieras,
- inte blanda flera orelaterade refaktoreringar.

## 14. Implementation loop

```text
READ
→ ASSESS
→ SELECT
→ LOCK
→ IMPLEMENT
→ VERIFY
→ REVIEW
→ UPDATE DOCS
→ UPDATE STATUS
→ PACKAGE / COMMIT
→ STOP
```

## 15. Verification

Verifiering ska fokusera på:
- preserved behavior,
- baseline comparison,
- regression,
- build/test,
- relevant performance/quality metric.

"Refactor compiles" är inte alltid tillräckligt.

## 16. Performance improvement

När målet är prestanda:

- mät baseline,
- använd representativ input,
- definiera metric,
- mät efter förändring,
- undvik microbenchmark som inte representerar faktisk flaskhals.

## 17. Dependency upgrades

Dependency upgrade ska vara egen förbättringsserie eller tydligt steg när risken är betydande.

Undvik att:
- uppgradera många major versions samtidigt utan behov,
- blanda dependency upgrades med ny funktion,
- acceptera breaking behavior utan CHANGE.

## 18. Build/CI improvement

IMPROVE passar för:
- caching,
- parallellisering,
- snabbare testurval,
- reproducible builds,
- bättre failure diagnostics.

Men CI-förbättring får inte göra required verification svagare utan explicit beslut.

## 19. Architecture updates

Uppdatera architecture.md endast om förbättringen faktiskt ändrar:
- komponentgränser,
- ansvar,
- dependency direction,
- deployment,
- viktiga technology choices.

Lokal kodrefaktorering kräver normalt inte architecture update.

## 20. Functional specification

Functional spec ska normalt inte ändras.

Om den måste ändras för att beskriva nytt beteende har arbetet passerat gränsen till CHANGE.

## 21. Security-sensitive improve

Vid refaktorering av:
- auth,
- authorization,
- crypto,
- file handling,
- secrets,
- input validation,

krävs explicit security regression verification.

## 22. Data-sensitive improve

Vid persistence/refaktorering:
- verifiera data compatibility,
- migrations om någon,
- transaction behavior,
- rollback/restore.

Om schema eller data semantics ändras funktionellt → CHANGE.

## 23. Deployment improve

Exempel:
- bättre Dockerfile,
- mindre image,
- non-root,
- health check,
- externalized config.

Verifiera:
- image build,
- startup,
- health,
- runtime behavior,
- external dependencies.

## 24. ZIP-läge

Efter completed step:
- komplett projekt-ZIP,
- integritetskontroll,
- uppdaterad work status,
- nästa rekommenderade steg.

## 25. GitHub-läge

IMPROVE på GitHub ska normalt:
- arbeta i samma PR för samma improvement series,
- hålla scope tekniskt sammanhängande,
- inte blanda ny funktion,
- commit:a completed steps.

## 26. Relation till Kodförbättraren

System Builder kan hantera avgränsade IMPROVE-arbeten som del av full systemlivscykel.

Djup, bred eller specialiserad kodrefaktorering kan vara bättre lämpad för en specialist-GPT som Kodförbättraren.

System Builder ska behålla process- och current-state-ansvar även om specialist används.

## 27. Small IMPROVE fast path

För en liten låg-riskförbättring:

```text
Read current code
→ establish quick baseline
→ define technical goal/non-goals
→ one DEV step
→ verify preserved behavior
→ update status
→ package/commit
```

## 28. Anti-patterns

Undvik:
- "cleanup" utan mål,
- bred refaktorering utan tests,
- dependency upgrade + feature change i samma steg,
- ändrat API under förevändning refaktorering,
- mätlös performanceoptimering,
- architecture doc update för trivial filflytt,
- testborttagning för att få refaktoreringen grön.

## 29. Completion criteria

IMPROVE är klar när:
- tekniskt mål är uppnått,
- non-goals respekteras,
- relevant behavior är oförändrat,
- required regression verifiering passerar,
- nya tekniska risker saknas,
- current-state docs är uppdaterade endast där verklig struktur/drift ändrats,
- projektet kan fortsätta från repo state utan chat history.
