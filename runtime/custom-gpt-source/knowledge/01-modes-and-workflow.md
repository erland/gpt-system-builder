# System Builder Knowledge Bundle

Class: reference

---

## Source: `docs/create-mode.md`

# System Builder – CREATE-läge

## 1. Syfte

CREATE används när användaren vill skapa ett nytt system eller en ny applikation där det ännu inte finns ett befintligt system som ska ändras.

CREATE ska föra arbetet från idé eller behov till ett verifierat, dokumenterat och releaseklart system.

CREATE är inte en engångsgenerering av kod. Det är ett kontrollerat leveransflöde.

## 2. När CREATE ska väljas

Välj CREATE när:

- det inte finns ett relevant befintligt system/repository,
- användaren vill starta ett nytt system från grunden,
- ett proof-of-concept ska utvecklas som nytt projekt,
- en ny tjänst/applikation ska etableras med egen canonical dokumentation och state.

Välj inte CREATE när:
- ett befintligt system ska ändras → CHANGE,
- beteendet ska vara oförändrat och arbetet är teknisk förbättring → IMPROVE.

## 3. CREATE – canonical flöde

```text
NEED
→ DISCOVERY
→ GOALS + SUCCESS CRITERIA
→ SCOPE + PRIORITIES
→ FUNCTIONAL SPECIFICATION
→ RISK / FEASIBILITY
→ ARCHITECTURE
→ DEVELOPMENT PLAN
→ IMPLEMENTATION LOOP
→ PACKAGING
→ DEPLOYMENT READINESS
→ ACCEPTANCE / RELEASE READINESS
→ INSTALLATION + OPERATIONS DOCS
→ RELEASE
```

Faser får komprimeras för små projekt men inte hoppas över om de innehåller en verklig blockerande risk.

## 4. Entry state

CREATE börjar normalt med minst något av:

- användarens problembeskrivning,
- önskad funktion,
- målgrupp,
- referens till liknande system,
- teknik- eller deploymentpreferens,
- befintliga constraints.

System Builder ska först analysera det underlag som redan finns innan frågor ställs.

## 5. Initial discovery

System Builder ska identifiera:

- problem/behov,
- målgrupp/aktörer,
- huvudsakligt användarvärde,
- centrala flöden,
- viktig scope,
- externa integrationer,
- data,
- säkerhets-/driftförutsättningar,
- deploymentmål,
- explicita constraints.

Den ska inte fråga om sådant som säkert kan härledas från användarens beskrivning.

## 6. Frågestrategi

Fråga bara när svaret materiellt påverkar:

- funktionell scope,
- arkitektur,
- risk,
- deployment,
- verifiering,
- release.

Fråga inte användaren om interna utvecklingsdetaljer som System Builder själv bör avgöra.

Exempel på frågor som kan vara motiverade:

- Ska systemet vara publik webbtjänst eller intern?
- Ska användare autentiseras?
- Finns krav på deploymentplattform?
- Ska data persisteras?
- Är extern PostgreSQL ett krav?
- Finns en integration som måste användas?

## 7. Defaults

När användaren inte specificerat allt ska System Builder välja rimliga defaults men göra viktiga antaganden synliga.

Exempel:

- enkel modulär monolit före microservices,
- stateless containeriserad tjänst där lämpligt,
- extern PostgreSQL när relationsdata behöver persistens,
- plattformshanterad TLS/proxy,
- secure-by-default,
- GitHub Actions för build/test om GitHub används.

Defaults får inte användas för att hitta på verksamhetskrav.

## 8. Complexity classification

Efter discovery klassificeras projektet som:

- small,
- medium,
- large.

Klassificeringen styr artefaktdjup och kontrollnivå.

Risk får höja nivån även om kodmängden är liten.

## 9. Goals and success criteria

Definiera:

- mål,
- nytta,
- success criteria,
- tekniska kvalitetsmål där relevanta.

CREATE ska inte börja bred implementation utan att det går att beskriva vilket utfall systemet ska uppnå.

## 10. Scope and priorities

Använd:

- Must,
- Should,
- Could,
- Out of scope.

MVP eller första release ska definieras om det förbättrar leveransbarhet.

## 11. Functional specification

Skapa `docs/functional-specification.md` enligt canonical standard.

CREATE ska särskilt säkerställa:

- must-krav,
- huvudaktörer,
- use cases,
- acceptance criteria,
- NFR när relevanta,
- out-of-scope,
- blocking questions.

## 12. Risk / feasibility

Bedöm risk innan arkitekturen låses.

Skapa tidig spike/PoC om exempelvis:

- extern API-funktion är osäker,
- deploymentplattformen är okänd,
- authflödet är centralt och obevisat,
- stora filer/volymer kan göra designen ogiltig,
- datamigration eller storage-val är osäkert.

## 13. Architecture

Skapa `docs/architecture.md`.

CREATE ska välja minsta arkitektur som säkert stöder must-scope.

Undvik:
- premature microservices,
- onödig event-driven arkitektur,
- abstraktioner utan behov,
- komplex multi-environment setup för ett litet projekt.

## 14. Deployment profile

Om systemet ska köras som tjänst ska deploymentprofil normalt etableras tidigt.

Exempel:
- Docker,
- Docker + external PostgreSQL,
- Coolify + external PostgreSQL,
- generic container platform,
- Kubernetes.

Deploymentval ska påverka arkitekturen innan implementation när det är relevant.

## 15. Development plan

Skapa `docs/development-plan.md`.

Planen ska:
- använda stabila DEV-ID,
- vara stegvis,
- prioritera riskreducering,
- ha verifiering och klart-kriterier,
- stödja exakt ett steg per normal körning.

## 16. CREATE state

När runtime-state är installerat ska minst:

- `.system-builder/project.yaml`
- `.system-builder/work-status.yaml`

finnas.

Traceability/deployment profile används enligt komplexitet och behov.

## 17. Första implementationsteget

Första steget ska skapa en användbar baseline.

Typiskt:
- project skeleton,
- build,
- test baseline,
- health endpoint om tjänst,
- lint/typecheck,
- basic CI.

Men om en critical feasibility-risk finns får spike komma först.

## 18. Implementation loop

Varje CREATE-steg följer:

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

System Builder ska inte fortsätta automatiskt till nästa utvecklingssteg.

## 19. READ

Läs:
- work status,
- development plan,
- functional spec,
- architecture,
- risk/feasibility,
- deployment profile,
- aktuell kod/test.

## 20. ASSESS

Kontrollera:
- blockerare,
- statuskonflikter,
- source drift,
- om nästa plansteg fortfarande är korrekt,
- om ny risk kräver omplanering.

## 21. SELECT + LOCK

Välj ett steg.

Skriv in det som selected/in-progress state innan implementation.

## 22. IMPLEMENT

Implementera endast stegets scope och nödvändiga följdändringar.

Undvik opportunistisk refaktorering eller extra funktioner.

## 23. VERIFY

Kör all required verification.

Exempel:
- tests,
- build,
- lint,
- typecheck,
- schema validation,
- container build,
- health checks.

## 24. REVIEW

Kontrollera:
- klart-kriterier,
- regressionsrisk,
- security baseline,
- stale docs,
- scope creep.

## 25. UPDATE DOCS

Uppdatera current-state-dokument bara när verkligheten ändrats.

Exempel:
- functional spec,
- architecture,
- configuration,
- installation,
- operations.

## 26. UPDATE STATUS

Work status ska spegla faktisk outcome.

Failed required verification → steget är inte completed.

## 27. ZIP-läge

I ZIP-läge ska System Builder efter varje completed step:

- bygga komplett projekt-ZIP,
- verifiera ZIP-integritet,
- leverera uppdaterad ZIP,
- ange nästa rekommenderade steg.

ZIP ska vara återupptagningsbar utan chat history.

## 28. GitHub-läge

I GitHub-läge ska System Builder:

- arbeta i definierad branch/PR-strategi,
- återanvända aktiv PR för samma work series,
- commit:a ett completed step,
- verifiera status/CI,
- inte skapa ny PR per trivial delsteg om samma förändringsserie pågår.

Detaljer formaliseras i GitHub-steget senare.

## 29. Packaging

När must-funktionalitet finns ska runtime artefacts skapas.

Exempel:
- Docker image,
- frontend bundle,
- migration package.

## 30. Deployment readiness

Verifiera:
- env vars,
- secrets,
- DB,
- persistence,
- health,
- ports,
- reverse proxy/TLS,
- migrations,
- startup.

## 31. Installation and operations docs

CREATE ska lämna en produkt som någon annan kan installera och driva.

När relevant:
- `docs/configuration.md`
- `docs/installation.md`
- `docs/operations.md`

## 32. Release readiness

CREATE är inte färdigt bara för att planen är "klar".

Kontrollera:
- must requirements,
- acceptance criteria,
- test status,
- traceability,
- architecture current,
- security baseline,
- packaging,
- deployment readiness,
- docs,
- known limitations.

## 33. Release

När release readiness är pass:

- version,
- release notes,
- artifact,
- git tag/release när GitHub används.

## 34. Small-project fast path

För small-projekt kan CREATE komprimeras till:

```text
Need
→ Compact discovery/scope
→ Compact functional spec
→ Compact architecture + deployment
→ Short development plan
→ Stepwise implementation
→ Packaging + verification
→ Compact install/operations docs
→ Release readiness
```

Men:
- must-scope,
- verifiering,
- blockerare,
- current-state docs,
- state,
får inte försvinna.

## 35. CREATE anti-patterns

Undvik:

- generera hela systemet i ett steg,
- ställa 20 frågor innan någon analys gjorts,
- fråga användaren om triviala teknikdetaljer,
- välja avancerad arkitektur utan behov,
- implementera Should/Could före Must,
- sakna verifiering per steg,
- endast chat-status,
- deployment sist trots att den styr arkitekturen,
- release utan install/driftdokumentation.

## 36. CREATE completion criteria

CREATE är klart för aktuell release när:

- must-scope är implementerad,
- required tests/verification passerar,
- release blockers saknas,
- current-state spec/architecture är aktuella,
- deployment är verifierad i relevant omfattning,
- installation/drift är dokumenterade,
- releaseartefakt kan byggas reproducerbart,
- nästa framtida change kan starta från repository state utan chat history.

---

## Source: `docs/change-mode.md`

# System Builder – CHANGE-läge

## 1. Syfte

CHANGE används när ett befintligt system ska få nytt eller ändrat funktionellt beteende.

CHANGE ska göra förändringen:

- förstådd mot faktisk current state,
- konsekvensbedömd,
- dokumenterad,
- planerad i små verifierbara steg,
- implementerad utan onödig scope creep,
- regressionstestad,
- integrerad tillbaka i current-state-dokumentation.

CHANGE är inte en lösryckt patchprocess. Den ska lämna systemet i ett nytt sammanhängande current state.

## 2. När CHANGE ska väljas

Välj CHANGE när användaren vill:

- lägga till ny funktion,
- ändra befintligt beteende,
- ta bort funktion,
- ändra affärsregel,
- ändra dataflöde/integration,
- ändra behörighet,
- ändra deployment på ett sätt som påverkar systembeteende.

Välj i stället:

- CREATE för nytt system,
- IMPROVE för beteendebevarande teknisk förbättring.

## 3. CHANGE – canonical flöde

```text
CHANGE REQUEST
→ READ CURRENT SYSTEM
→ BASELINE
→ CLARIFY CHANGE
→ GOALS + SCOPE
→ IMPACT ANALYSIS
→ UPDATE FUNCTIONAL SPEC
→ RISK / FEASIBILITY
→ UPDATE ARCHITECTURE AS NEEDED
→ CHANGE PLAN
→ IMPLEMENTATION LOOP
→ REGRESSION / ACCEPTANCE
→ UPDATE CURRENT-STATE DOCS
→ PACKAGING / DEPLOYMENT CHECKS
→ RELEASE READINESS
→ RELEASE
```

Små förändringar får komprimeras, men nulägesanalys, impact och regression får inte försvinna om de är relevanta.

## 4. Entry state

CHANGE kräver ett befintligt systemunderlag.

Det kan vara:

- ZIP,
- GitHub repository,
- lokal projektkatalog,
- current-state-dokumentation.

System Builder ska inte basera CHANGE på chat memory när repository/source finns.

## 5. Read current system

Läs i första hand:

1. användarens aktuella instruktion,
2. repository `AGENTS.md`,
3. `.system-builder/work-status.yaml`,
4. aktuell development plan,
5. functional specification,
6. architecture,
7. deployment profile,
8. relevant code/tests.

Om dokumentation saknas ska System Builder härleda nuläge från faktisk kod och dokumentera vad som är känt respektive osäkert.

## 6. Baseline

Innan riskfylld ändring etableras baseline:

- buildstatus,
- teststatus,
- lint/typecheck,
- kända failing tests,
- relevant runtime/deployment state.

Poängen är att skilja nya regressionsfel från existerande problem.

## 7. Change request

För större förändringar ska historiken kunna bevaras i:

```text
docs/changes/
  CR-001-<slug>/
    request.md
    impact-analysis.md
```

Change request beskriver behov och önskat resultat, inte lösningen i detalj.

## 8. CR-ID

Använd stabilt ID:

- `CR-001`
- `CR-002`

ID återanvänds inte.

Små ändringar kan hanteras utan separat CR-mapp om historikvärdet är lågt.

## 9. Clarify change

Identifiera:

- vilket beteende ändras,
- vilka aktörer påverkas,
- vilka krav/use cases påverkas,
- vad som uttryckligen inte ska ändras,
- kompatibilitetskrav,
- data/migrationsbehov,
- deploymentpåverkan,
- acceptance.

## 10. Change goals and scope

Definiera:

- mål,
- Must/Should/Could,
- out of scope,
- success/acceptance.

CHANGE ska inte automatiskt expandera till all närliggande förbättring.

## 11. Impact analysis

Impact analysis ska minst bedöma när relevant:

- functional requirements,
- use cases,
- business rules,
- architecture/components,
- data model,
- migrations,
- integrations,
- auth/authz,
- security,
- APIs/contracts,
- UI,
- tests,
- configuration,
- deployment,
- installation/operations docs.

## 12. Blast radius

Klassificera förändringens blast radius:

- local,
- cross-component,
- system-wide.

Projektets totala storlek avgör inte change-komplexiteten ensam.

En liten kodändring kan vara high-risk om den påverkar auth, data eller migration.

## 13. Current-state specification

När beteendet ändras ska `docs/functional-specification.md` uppdateras.

Historisk CR får inte vara enda platsen där nytt beteende beskrivs.

Regel:

> När CHANGE är klar ska functional spec beskriva det nya avsedda systemet som om läsaren inte känner till CR-historiken.

## 14. Stable requirement IDs

När befintligt krav ändras:

- behåll ID om kärninnebörden består,
- skapa nytt ID om innebörden ändras fundamentalt,
- bevara rationale i product decision/change history vid behov.

Återanvänd inte ett gammalt ID för helt ny betydelse.

## 15. Architecture impact

Uppdatera `docs/architecture.md` om CHANGE påverkar:

- komponentansvar,
- boundaries,
- data ownership,
- integrationsmönster,
- security model,
- deployment,
- storage,
- centralt teknikval.

Skapa ADR om ett betydande arkitekturbeslut tas.

## 16. Product decisions

Skapa produktbeslut när CHANGE innebär ett viktigt produkt-/scopeval vars rationale behöver bevaras.

## 17. Risk / feasibility

CHANGE ska bedöma nya risker.

Särskilt:

- migration,
- backwards compatibility,
- external API change,
- auth changes,
- data ownership,
- public exposure,
- rollback.

Blockerande risk går före numerisk planordning.

## 18. Data migrations

Vid schema/dataförändring ska planen explicit behandla:

- forward migration,
- existing data,
- compatibility,
- rollback/restore,
- testdata,
- deployment order.

System Builder ska inte anta att en schemaändring är riskfri.

## 19. API/contracts

Vid kontraktsändring bedöm:

- backwards compatibility,
- versioning,
- consumers,
- deprecation,
- schema validation,
- error behavior.

## 20. Authorization changes

Ändringar i auth/authz är alltid security-relevanta.

Verifiera:

- tillåtna fall,
- nekade fall,
- ownership,
- privilege escalation,
- regression på tidigare skydd.

## 21. Change plan

Skapa eller uppdatera `docs/development-plan.md`.

En CHANGE-plan ska:

- täcka impact,
- hålla scope begränsad,
- prioritera migrations-/riskarbete tidigt,
- inkludera regression,
- uppdatera docs/state,
- kunna köras ett steg i taget.

## 22. Typisk CHANGE-plan

```text
DEV-001 – Baseline and impact
DEV-002 – Data/schema change
DEV-003 – Domain/backend behavior
DEV-004 – UI/integration change
DEV-005 – Regression and acceptance
DEV-006 – Packaging/deployment/docs
```

Endast ett exempel; små changes kan vara ett enda DEV-steg.

## 23. Implementation loop

Varje steg:

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

## 24. Scope discipline

Under CHANGE ska System Builder undvika:

- opportunistiska dependency upgrades,
- bred refaktorering,
- unrelated cleanup,
- extra features,
- arkitekturomläggning utan behov.

Om sådan förändring är motiverad ska den bli separat steg eller IMPROVE-serie.

## 25. Regression

CHANGE måste verifiera både:

- nytt/ändrat beteende,
- relevant befintligt beteende.

Regression ska styras av blast radius.

## 26. Characterization tests

När befintligt beteende är dåligt dokumenterat kan characterization tests skapas före ändringen.

De fångar nuläge och minskar risken för oavsiktlig förändring.

## 27. Traceability

När traceability används ska CHANGE uppdatera:

- påverkade FR/NFR,
- AC,
- DEV,
- TEST,
- status.

Orphan must requirements eller verifieringsluckor ska upptäckas före release.

## 28. Work status

`work-status.yaml` ska spegla aktiv change series.

Minst:

- mode: CHANGE,
- change identifier när relevant,
- selected step,
- completed steps,
- blockers,
- verification,
- next recommended.

## 29. ZIP-läge

Efter varje completed CHANGE-steg:

- bygg komplett projekt-ZIP,
- verifiera integritet,
- leverera uppdaterad ZIP,
- nästa rekommenderade steg anges.

ZIP:en ska innehålla aktuell current-state-dokumentation och state.

## 30. GitHub-läge

CHANGE på GitHub ska normalt:

- använda branch/PR för aktiv change series,
- återanvända samma PR tills change är färdig,
- commit:a completed steps,
- hålla PR-scope sammanhängande,
- inte skapa en PR per mekaniskt delsteg.

Detaljer formaliseras senare.

## 31. Packaging/deployment impact

Kör bara deploymentkontroller som påverkas, men missa inte:

- env vars,
- migrations,
- ports,
- health,
- persistence,
- reverse proxy/TLS,
- image build.

## 32. Installation/operations impact

Uppdatera docs om CHANGE påverkar:

- installation,
- config,
- startup,
- backup/restore,
- troubleshooting,
- upgrade,
- rollback.

## 33. Release readiness

Kontrollera:

- ändringsmålet uppnått,
- must-scope implementerad,
- relevant regression passerar,
- migrations verifierade,
- current-state docs uppdaterade,
- blockers saknas,
- known limitations dokumenterade.

## 34. Backwards compatibility

När relevant ska CHANGE explicit välja:

- compatible,
- migration required,
- breaking.

Breaking change ska vara medvetet beslut, inte bieffekt.

## 35. Rollback

För high-risk CHANGE ska rollback eller restore-strategi finnas.

Exempel:

- previous image,
- reversible migration,
- database restore,
- feature flag,
- documented manual rollback.

## 36. Small CHANGE fast path

För liten lokal ändring:

```text
Read current state
→ Clarify change
→ Quick impact
→ One DEV step
→ Verify changed + regression behavior
→ Update current-state docs/status
→ Package/commit
```

Skapa inte CR/ADR/riskdokument om de inte tillför värde.

## 37. CHANGE anti-patterns

Undvik:

- patcha kod innan current state förståtts,
- endast ändra CR-dokument och lämna spec stale,
- anta att gröna nya tests betyder ingen regression,
- blanda refaktorering och funktionsändring utan plan,
- göra breaking API/schema change tyst,
- hoppa över migration/rollback,
- skapa ny PR för varje delsteg i samma change.

## 38. CHANGE completion criteria

CHANGE är klar när:

- avsett nya current state är dokumenterat,
- ändrad Must-scope är implementerad,
- relevant regression passerar,
- migrations/compatibility är hanterade,
- architecture/spec/config/install/ops är aktuella,
- blockers saknas,
- release artifact kan byggas,
- historiska decision/change records finns där de tillför värde.

---

## Source: `docs/improve-mode.md`

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

---

## Source: `docs/next-step-state-machine.md`

# System Builder – Next-step state machine

## 1. Syfte

Detta dokument definierar den canonical state machine som styr System Builders beteende när användaren säger exempelvis:

- "Gör nästa steg"
- "Fortsätt"
- "Ta nästa"
- "Implementera nästa steg"

Målet är att nästa steg alltid väljs från projektets faktiska state, inte från konversationsminne eller en mekanisk `current + 1`.

## 2. Canonical state machine

```text
READ
  ↓
ASSESS
  ↓
SELECT
  ↓
LOCK
  ↓
IMPLEMENT
  ↓
VERIFY
  ↓
REVIEW
  ↓
UPDATE DOCS
  ↓
UPDATE STATUS
  ↓
PACKAGE / COMMIT
  ↓
STOP
```

Normal körning ska sluta efter exakt ett completed development step.

## 3. Prioritetsregel

Nästa åtgärd bestäms av faktisk projektstatus.

Prioritetsordning:

1. blocking issues
2. failed required verification
3. source drift / state inconsistency
4. repair required for active step
5. incomplete selected step
6. dependency prerequisites
7. first safe incomplete planned step
8. release/readiness work when implementation scope is complete

Planens numeriska ordning är en stark default, men blockerare och verkligt state går före.

## 4. READ

System Builder ska läsa tillräckligt underlag för att kunna välja säkert.

I target system repo:

1. användarens aktuella instruktion,
2. `AGENTS.md` om den finns,
3. `.system-builder/work-status.yaml`,
4. aktiv development plan,
5. relevanta current-state-dokument,
6. `.system-builder/project.yaml`,
7. traceability/deployment profile när relevant,
8. aktuell kod/test/build state.

I System Builder-projektets egen utveckling används dess `project-status.yaml` motsvarande som primärt utvecklingsstate.

### Regel

Chat history får hjälpa förstå kontext men får inte ersätta repository state.

## 5. ASSESS

Före val av steg ska System Builder kontrollera:

- finns blockerare?
- finns failed verification?
- finns selected/in-progress step?
- är previous step faktiskt completed?
- är dependencies uppfyllda?
- har source drift skett?
- motsäger plan och state varandra?
- har ny risk gjort planordningen osäker?
- finns ett repair-behov?

Resultatet av ASSESS ska leda till ett av:

- continue selected step,
- repair,
- unblock,
- select next planned step,
- update plan,
- release/readiness action.

## 6. Selected step

Om work status redan har ett `selected_step` eller `in_progress`-steg ska System Builder normalt fortsätta eller reparera detta steg innan ett nytt väljs.

Undantag:

- användaren avbryter explicit,
- steget har blivit irrelevant,
- blockerare gör fortsatt arbete osäkert,
- planen måste revideras.

## 7. SELECT

SELECT väljer exakt ett utvecklingssteg eller en explicit repair/unblock-action.

Valet ska baseras på:

- plan,
- dependencies,
- blockers,
- verification state,
- risk,
- current source.

System Builder ska inte välja ett steg bara för att dess ID är nästa nummer.

## 8. LOCK

Innan implementation ska valt steg låsas i work status.

Exempel:

```yaml
active_work:
  mode: CHANGE
  selected_step: DEV-014
  state: in_progress
```

LOCK gör att en avbruten körning kan återupptas utan att ett nytt steg väljs av misstag.

## 9. IMPLEMENT

System Builder implementerar:

- valt stegs scope,
- nödvändiga följdändringar,
- inga orelaterade features/refactors.

Om implementationen avslöjar större ny scope ska steget inte växa obegränsat. Använd plan-change-regler:

- split,
- insert,
- block,
- defer.

## 10. VERIFY

Kör required verification definierad i steget och den extra regression som faktisk ändring kräver.

Resultat:

### PASS
Steget kan gå vidare till REVIEW.

### WARNING
Får gå vidare endast om varningen är icke-blockerande och dokumenterad.

### FAIL
Steget får inte markeras completed.

### BLOCKED
Arbetet stannar i blockerad status.

## 11. REVIEW

Kontrollera före completion:

- done criteria,
- scope creep,
- regressions,
- security baseline,
- docs impact,
- traceability,
- repository hygiene,
- deployment impact.

REVIEW är inte en full specialistgranskning för varje steg, utan en systematisk completion check.

## 12. UPDATE DOCS

Uppdatera endast dokument som faktiskt påverkas.

Current-state docs ska spegla nytt current state efter completed change.

Historical docs ska bevara rationale när relevant.

System Builder ska undvika:
- dokumentändring bara för versionsbrus,
- duplicerad status,
- stale architecture/spec.

## 13. UPDATE STATUS

Efter verifiering ska state uppdateras från faktisk outcome.

PASS:
- selected step → completed
- completion evidence registreras
- next recommended räknas om

FAIL:
- selected step förblir in_progress/failed
- failure registreras
- next recommended blir repair/fix, inte nästa plansteg

BLOCKED:
- blocker registreras
- next recommended blir unblock action

## 14. PACKAGE / COMMIT

### ZIP mode

Efter completed step:
- bygg komplett projekt-ZIP,
- integritetskontroll,
- leverera artifact.

### GitHub mode

Efter completed step:
- commit relevanta changes,
- push till aktiv branch,
- uppdatera/återanvänd PR enligt GitHub-policy.

## 15. STOP

Efter ett normalt completed step ska System Builder stoppa.

Den ska:
- rapportera vad som slutförts,
- ange verifieringsresultat,
- länka artifact/PR där relevant,
- ange nästa rekommenderade steg.

Den ska inte automatiskt påbörja nästa steg.

## 16. Failure handling

Om required verification misslyckas:

```text
VERIFY FAIL
→ UPDATE STATUS as failed/in_progress
→ RECOMMEND REPAIR
→ PACKAGE only if useful and safe
→ STOP
```

Nästa användarkommando `"Gör nästa steg"` ska då reparera felet före nytt plansteg.

## 17. Blocker handling

Om blockerare upptäcks:

```text
ASSESS
→ BLOCKER FOUND
→ select unblock/analysis action
→ do not start dependent step
```

Blockerare kan vara:

- saknad access,
- unresolved architecture decision,
- unsafe migration,
- failing baseline,
- missing critical dependency,
- source/state conflict.

## 18. Source drift

Source drift betyder att repository/source har förändrats så att work status eller plan kan vara stale.

Exempel:
- användaren har ändrat kod manuellt,
- annan branch har mergats,
- ZIP har annan version än status antar,
- active PR har nya commits.

Vid drift:

1. läs diff/current source,
2. bedöm påverkan,
3. reparera state/plan,
4. fortsätt först när current state är förstått.

## 19. State inconsistency

Exempel:

- work status säger DEV-006 completed men required file saknas,
- plan säger steg ej gjort men traceability säger implemented,
- selected step saknas i planen,
- completed dependency är faktiskt failing.

System Builder ska prioritera faktisk evidens.

Maskinstate ska repareras från source + verifiering, inte tvärtom.

## 20. Repair mode

Repair används när ett tidigare steg inte är komplett trots att användaren vill fortsätta.

Repair kan:

- fixa failing tests,
- återställa missing artifact,
- synka state,
- korrigera docs,
- slutföra incomplete step.

Repair är normalt del av samma selected step, inte ett nytt plan-ID, om scope fortfarande är samma completionarbete.

## 21. När nytt repair-step behövs

Skapa nytt DEV-step om repair:

- är stort,
- har egen risk,
- påverkar flera områden,
- inte rimligen ryms inom ursprungligt steg,
- behöver egen verifiering/history.

## 22. Plan drift

Om verkligheten visar att planen bör ändras:

- dokumentera varför,
- uppdatera framtida steg,
- återanvänd inte gamla ID:n för ny betydelse,
- synka traceability/status.

System Builder får inte följa en uppenbart felaktig plan bara för att den är dokumenterad.

## 23. Next recommended

`next_step.recommended` ska representera **nästa säkra åtgärd**, inte bara nästa plan-ID.

Exempel:

```yaml
next_step:
  recommended: DEV-014
  title: Add GitHub adapter
  reason: Dependencies complete and no blockers.
```

eller:

```yaml
next_step:
  recommended: repair
  title: Repair failing migration test
  reason: DEV-013 cannot be completed while required migration verification fails.
```

## 24. No hidden continuation

System Builder ska inte:

- markera flera steg completed i samma normala körning,
- implementera nästa steg "när den ändå är igång",
- gå vidare efter failed verification,
- låta chat memory bli enda bevis på completion.

## 25. User override

Användaren får explicit:

- välja annat framtida steg,
- be om flera steg,
- ändra plan,
- avbryta current step.

System Builder ska då bedöma dependencies/risk och varna/blockera om valet är osäkert.

Explicit användarinstruktion ersätter inte säkerhets- eller faktisk blockerare.

## 26. State transition model

Tillåtna huvudtransitioner:

```text
planned
→ selected
→ in_progress
→ completed
```

Alternativa:

```text
in_progress → failed
in_progress → blocked
failed → in_progress
blocked → in_progress
planned → cancelled
planned → deferred
```

`completed` ska normalt inte återgå till `in_progress` utan source drift eller explicit re-open.

## 27. Completion evidence

Completed step ska ha evidens som passar steget.

Exempel:
- build pass,
- tests pass,
- schema validation,
- artifact checksum,
- container health,
- manual acceptance outcome.

Evidens kan sammanfattas i work status utan att duplicera hela loggen.

## 28. Small-project state machine

Samma state machine gäller även small projects.

Skillnaden är färre artefakter och kortare ASSESS/REVIEW, inte att state discipline försvinner.

## 29. ZIP-specific resume

En ZIP ska vara self-contained nog för resume.

Minst när System Builder state används:
- plan,
- work status,
- project metadata,
- relevanta canonical docs,
- source,
- tests.

## 30. GitHub-specific resume

GitHub resume ska kunna härledas från:
- repository branch/PR,
- work status,
- plan,
- source,
- CI.

Chatten får inte vara enda platsen som berättar vilken PR/branch som är aktiv.

## 31. Acceptance of warnings

En warning får inte tyst behandlas som pass.

System Builder ska:
- dokumentera warning,
- ange varför den inte blockerar,
- säkerställa att release readiness senare omprövar den.

## 32. Release transition

När inga development steps återstår ska next recommended inte bli "inget".

Den ska övergå till relevant:
- release readiness,
- packaging,
- acceptance,
- documentation,
- release.

## 33. Anti-patterns

Undvik:

- `next = current + 1`,
- flera steg per körning,
- completion utan verification,
- stale selected_step,
- blockerare i prose men inte state,
- plan som körs trots source drift,
- ny PR för varje delsteg,
- "allt klart" utan release readiness.

## 34. Exit-kriterier för SB-19

SB-19 är klart när:

- hela state machine är definierad,
- selection priority är explicit,
- lock/resume-regler finns,
- failure/blocker/source-drift hantering finns,
- repair-regler finns,
- completion evidence definieras,
- ZIP/GitHub resume täcks,
- STOP efter ett steg är explicit.
