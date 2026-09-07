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
