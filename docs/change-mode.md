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
→ FINAL DOCUMENTATION RECONCILIATION
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

## 22A. README current-state entrypoint

När repositoryt har `README.md` ska CHANGE behandla den som projektets current-state entrypoint. När change-serien påverkar sådant en ny läsare rimligen möter i README — exempelvis syfte, huvudfunktioner, build/run, runtime, deployment eller länkar till installation/operations — ska README uppdateras eller länka vidare korrekt.

README ska inte duplicera detaljer som redan ägs av functional specification, architecture eller operations docs.

Final documentation reconciliation ska kontrollera README uttryckligen. En materiellt stale README klassificeras som documentation mismatch.

## 22B. Governing intent during CHANGE

The updated functional specification and architecture are the governing target for the change series. They are not a line-by-line description of implementation progress.

During each development step, System Builder shall detect whether implementation contradicts that target. It must not silently change spec/architecture merely because the implementation took a different direction.

Update governing documentation during the change only when:
- the user explicitly changes the desired behavior or architecture,
- an explicit accepted product/architecture decision changes the target,
- the documentation itself was demonstrably inconsistent with the already accepted intent.

Otherwise, divergence is an implementation issue to repair, not a reason to redefine intent.

## 22B. Final documentation reconciliation

When planned implementation and regression work are complete, but before release readiness, compare actual implementation with the governing functional specification and architecture.

Classify each mismatch as:
- **implementation mismatch**: implementation must change to meet agreed intent,
- **documentation mismatch**: an explicit accepted direction change was not reflected in the documents,
- **decision mismatch**: a genuine unresolved product/architecture choice remains and must be decided by the user.

Do not enter release readiness while a decision mismatch or release-relevant implementation/documentation mismatch remains unresolved.

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
