# System Builder – Test- och verifieringsstrategi

## 1. Syfte

System Builder ska använda verifiering som evidens för att ett steg, krav eller en release faktiskt är korrekt.

Strategin ska:

- vara proportionerlig mot risk,
- kombinera automatiska och manuella kontroller när det behövs,
- skilja deterministic tests från evals och human acceptance,
- göra regressioner synliga,
- stödja stegvis utveckling,
- koppla must-krav till verifierbar evidens.

## 2. Grundprincip

> Verifiera på den lägsta kostnadsnivå som ger tillräcklig evidens, men aldrig lägre än risknivån kräver.

System Builder ska inte automatiskt välja e2e för allt, och inte heller nöja sig med unit tests när integrations- eller deploymentrisk är central.

## 3. Verifieringstyper

### 3.1 Build

Kontrollerar att projektet kan byggas.

Exempel:
- `mvn test/package`
- `pnpm build`
- container image build

### 3.2 Lint / static checks

Kontrollerar kodkvalitet och strukturella regler.

Exempel:
- lint
- formatting check
- schema validation
- dependency policy

### 3.3 Typecheck / compile

Kontrollerar typ- och kompileringsfel.

### 3.4 Unit tests

Verifierar isolerad logik.

Passar:
- affärsregler,
- parsning,
- transformationer,
- pure functions.

### 3.5 Integration tests

Verifierar samspel mellan komponenter eller externa beroenden.

Passar:
- database,
- repository layer,
- GitHub adapter,
- auth provider,
- filesystem/storage.

### 3.6 API tests

Verifierar kontrakt på HTTP/API-nivå.

### 3.7 UI/component tests

Verifierar UI-beteende där det ger värde.

### 3.8 End-to-end

Verifierar kritiska användarflöden över flera lager.

Ska användas selektivt för:
- kritiska happy paths,
- viktiga regressionsflöden,
- release acceptance.

### 3.9 Security verification

Exempel:
- input validation,
- authz,
- path traversal,
- secret leakage,
- dependency scanning,
- insecure defaults.

### 3.10 Deployment verification

Exempel:
- image build,
- container startup,
- health check,
- migration,
- config validation,
- external DB connectivity.

### 3.11 Manual acceptance

Används när mänsklig bedömning är relevant:
- usability,
- visuellt beteende,
- affärsmässig acceptans,
- komplexa operator flows.

### 3.12 Evals

Evals används för modeller, prompts eller andra icke-deterministiska beteenden.

Evals ska skiljas från deterministic software tests.

## 4. Deterministic tests vs evals

Deterministic tests:
- samma input ska ge samma förväntade outcome,
- används som hårda gates när relevanta.

Evals:
- mäter kvalitet, beteende eller adherence över flera cases,
- kan använda scoring/toleranser,
- bör ha regression set,
- ska inte beskrivas som vanliga unit tests.

För System Builder-projektet självt kommer båda typerna användas senare.

## 5. Testpyramid som riktlinje

En rimlig default är:

- många snabba unit/static checks,
- färre integration/API tests,
- få välvalda e2e.

Detta är en riktlinje, inte en dogm.

Om systemets risk huvudsakligen ligger i integration kan fler integration tests vara mer värdefulla än många unit tests.

## 6. Riskbaserad verifiering

Verifieringsdjup ska styras av:

- konsekvens vid fel,
- sannolikhet för regression,
- komplexitet,
- förändringens blast radius,
- integrationsberoenden,
- säkerhet,
- data/migration,
- deployment.

### Låg risk

Typiskt:
- build,
- lint,
- relevanta unit tests.

### Medium risk

Typiskt:
- build,
- lint/typecheck,
- unit + integration,
- relevant API/UI verification,
- focused regression.

### Hög risk

Typiskt:
- full relevant automated suite,
- targeted integration/e2e,
- migration/deployment verification,
- security checks,
- explicit acceptance evidence.

## 7. Verification per development step

Varje `DEV-xxx` ska ha en verifieringssektion.

System Builder ska efter implementation:

1. köra stegets definierade verifiering,
2. lägga till nödvändiga regression checks om ändringen påverkar befintligt beteende,
3. inte markera steget completed om required verification misslyckas,
4. uppdatera work status med faktiskt resultat.

## 8. Verification baseline

För befintliga system ska System Builder före riskfylld CHANGE/IMPROVE etablera baseline.

Baseline kan innehålla:

- aktuell teststatus,
- buildstatus,
- lint/typecheck,
- kända failing tests,
- versions-/dependency state.

Poängen är att skilja nya regressioner från redan existerande problem.

## 9. Characterization tests

Vid refaktorering eller ändring av svårförstådd legacy-kod kan characterization tests behövas först.

De dokumenterar befintligt observerat beteende.

De betyder inte att beteendet är önskvärt.

## 10. Regression tests

När en bug fixas ska System Builder normalt lägga till ett test som hade fångat buggen innan fixen.

När en CHANGE påverkar befintlig funktion ska relevanta regressionsfall uppdateras eller läggas till.

## 11. Traceability

När `.system-builder/traceability.yaml` används ska verifiering kunna kopplas:

```text
FR/NFR
→ AC
→ DEV
→ TEST
```

`TEST-xxx` används när stabila verifieringsreferenser behövs.

Full testkod ska inte dupliceras i traceability YAML.

## 12. TEST-ID

Stabila ID:n:

- `TEST-001`
- `TEST-002`

Används när:
- kravspårbarhet kräver det,
- acceptance ska följas över tid,
- verifieringskontrakt behöver refereras från flera artefakter.

Små projekt behöver inte ID-sätta varje unit test.

## 13. Test strategy-dokument

Canonical fil när separat dokument behövs:

`docs/test-strategy.md`

För small-projekt får strategin ligga i development plan.

Separat dokument är värdefullt när:
- flera testnivåer används,
- release gates är viktiga,
- testmiljö/data kräver förklaring,
- många krav behöver traceability,
- CI-strategin är central.

## 14. Rekommenderad struktur

```text
# Test Strategy

## Scope
## Quality risks
## Test levels
## Environments
## Test data
## Automated checks
## Manual acceptance
## Regression strategy
## Traceability
## Release gates
## Known gaps
```

## 15. Testmiljö

Beskriv när relevant:

- local,
- CI,
- integration environment,
- staging,
- production smoke checks.

Testmiljön ska vara tillräckligt lik målet där deployment/integration är riskbärande.

## 16. Testdata

System Builder ska tänka på:

- reproducerbarhet,
- sekretess,
- isolation,
- cleanup,
- edge cases,
- representativa storlekar.

Produktionsdata ska inte användas slentrianmässigt i test.

## 17. External integrations

För externa API:er ska strategin balansera:

- mocks/stubs för snabb deterministic test,
- contract/integration test mot verklig tjänst där möjligt,
- failure cases,
- rate limits,
- timeout,
- auth.

Enbart mock-testning är inte tillräcklig om den största risken är verklig integration.

## 18. Database verification

När databas används:

- migrationer ska testas,
- constraints/queries ska verifieras,
- integration tests bör använda realistisk databas när risk kräver det.

För PostgreSQL bör viktiga PostgreSQL-specifika beteenden inte enbart testas mot SQLite.

## 19. Deployment verification

För containeriserade tjänster bör relevant verifiering omfatta:

- image build,
- startup,
- health,
- environment configuration,
- external dependencies,
- migrations.

För Coolify ska minst container-/health- och extern DB-konfiguration kunna verifieras före release.

## 20. Security verification

Säkerhetskritiska krav ska ha explicit evidens.

Exempel:
- path traversal rejection,
- unauthorized access denied,
- secrets absent from logs,
- input size limits,
- safe defaults.

## 21. Acceptance criteria

Acceptance criteria är inte samma sak som testfall men ska kunna verifieras.

Ett AC kan verifieras av:
- automated test,
- manual acceptance,
- kombination.

Release readiness ska kunna visa vilka must-AC som är verifierade.

## 22. Failed verification

Om required verification misslyckas:

- steget blir inte completed,
- failure dokumenteras,
- work status blir warning/blocked/failed beroende på konsekvens,
- fixen har företräde framför nästa numeriska steg.

## 23. Flaky tests

Flaky tests ska inte ignoreras.

System Builder ska:
- försöka skilja flakiness från faktisk regression,
- dokumentera known flaky state,
- inte behandla slumpmässig omkörning som fullgod lösning,
- prioritera stabilisering om testet är release-kritiskt.

## 24. Release gates

En release gate kan kräva:

- lint pass,
- build pass,
- unit/integration pass,
- critical e2e pass,
- schema validation,
- container build,
- security baseline,
- must acceptance verified,
- no blockers.

Exakta gates ska anpassas till projektet.

## 25. Green build räcker inte

Ett grönt CI-jobb betyder inte automatiskt:
- att alla must-krav är implementerade,
- att deployment fungerar,
- att docs är aktuella,
- att acceptance criteria är verifierade,
- att risker är lösta.

Release readiness använder en bredare evidensmodell.

## 26. Small-project-regel

För small-projekt kan en kompakt strategi vara:

```text
- lint/typecheck
- unit tests
- one integration/API happy path
- container build/health if deployable
- manual acceptance of core flow
```

Skapa inte onödiga testlager.

## 27. Medium / large

Medium:
- explicit test strategy,
- regression plan,
- integration coverage,
- release gates.

Large/high-risk:
- stable TEST-ID,
- full traceability,
- environment strategy,
- security/deployment gates,
- explicit known gaps,
- possibly specialist review.

## 28. Anti-patterns

Undvik:
- 100 % coverage som mål utan riskkoppling,
- e2e för allt,
- mocks för all extern integration,
- gröna tests utan acceptance,
- manuella tester utan dokumenterad outcome,
- flaky tests som permanent ignoreras,
- tester som endast verifierar implementation details.

## 29. Kvalitetskriterier

Strategin är tillräckligt bra när:
1. kritiska risker har motsvarande verifiering,
2. varje development step kan verifieras,
3. regression baseline är tydlig,
4. must-krav kan kopplas till evidens där traceability används,
5. deployment och integration testas på rätt nivå,
6. release gates är explicit definierade,
7. små projekt inte övertestas.

## 30. Exit-kriterier för teststrategifasen

Fasen är klar när:
- relevanta testnivåer är valda,
- risker har verifieringsplan,
- baseline/gates är definierade där relevant,
- acceptance kan verifieras,
- development plan kan referera till konkret verifiering.
