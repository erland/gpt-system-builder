# System Builder Knowledge Bundle

Class: reference

---

## Source: `docs/risk-feasibility-standard.md`

# System Builder – Risk- och feasibility-arbete

## 1. Syfte

System Builder ska identifiera och hantera osäkerheter som kan göra implementation dyr, osäker eller felriktad.

Risk/feasibility-arbetet ska svara på:

- Finns tekniska antaganden som ännu inte är bevisade?
- Finns externa beroenden som kan blockera lösningen?
- Finns data-, säkerhets-, deployment- eller migrationsrisker?
- Behövs spike, PoC eller tidig verifiering?
- Är risken accepterad, reducerad, överförd eller blockerande?

Målet är inte att skapa ett tungt riskregister för alla projekt, utan att upptäcka viktiga osäkerheter innan de cementeras i arkitektur eller implementation.

## 2. Grundprincip

> Hög osäkerhet ska hanteras tidigt. Dokumentationsnivån ska vara proportionerlig mot sannolik konsekvens.

System Builder ska inte behandla en kritisk teknisk eller operativ osäkerhet som en fotnot i slutet av planen.

## 3. När risk/feasibility ska bedömas

Bedömningen görs särskilt när projektet innehåller:

- nytt eller okänt externt API,
- datamigration,
- autentisering/behörighet,
- känslig data eller personuppgifter,
- hög tillgänglighet,
- prestandakrav,
- filuppladdning/exekvering,
- tredjepartskod med oklar licens,
- ny deploymentplattform,
- stateful workloads,
- extern databas,
- avancerad nätverksåtkomst,
- svår rollback,
- integrationskedjor med flera system.

För små lågriskprojekt får bedömningen vara mycket kort.

## 4. Riskkategorier

System Builder ska minst kunna resonera över:

### 4.1 Technical feasibility

Exempel:

- fungerar valt bibliotek/API för behovet?
- klarar teknikstacken deploymentmiljön?
- finns begränsningar i runtime, storage eller nätverk?

### 4.2 Integration

Exempel:

- rate limits,
- auth-flöden,
- API-stabilitet,
- timeout,
- idempotency,
- tredjepartsdrift.

### 4.3 Data

Exempel:

- datakvalitet,
- schemaändring,
- migration,
- backup/restore,
- retention,
- ownership.

### 4.4 Security

Exempel:

- secrets,
- trust boundaries,
- input validation,
- access control,
- unsafe file handling,
- dependency risk.

### 4.5 Operations / deployment

Exempel:

- persistent storage,
- health checks,
- startup order,
- external database,
- reverse proxy/TLS,
- rollback.

### 4.6 Performance / scale

Exempel:

- latency,
- throughput,
- concurrency,
- memory,
- large files,
- batchvolym.

### 4.7 Legal / licensing / policy

När användaren eller projektunderlag gör det relevant:

- licensrestriktioner,
- data residency,
- policykrav,
- regulatoriska constraints.

System Builder ska inte fabricera juridiska krav.

## 5. Risk-ID

När separat riskspårning tillför värde används stabila ID:n:

- `RISK-001`
- `RISK-002`

Små projekt behöver inte ID-sätta triviala risker.

## 6. Enkel riskmodell

En risk bör normalt beskrivas med:

- ID,
- kategori,
- antagande/risk,
- trigger/evidence,
- sannolikhet,
- konsekvens,
- nivå,
- hantering,
- owner/ansvar när relevant,
- kopplade krav/plansteg,
- status.

Rekommenderade värden:

### Probability

- low
- medium
- high

### Impact

- low
- medium
- high

### Status

- open
- mitigated
- accepted
- blocked
- closed

## 7. Risknivå

System Builder får använda en enkel matris:

| Probability | Impact | Result |
|---|---|---|
| low | low | low |
| low | medium | low/medium |
| low | high | medium |
| medium | low | low/medium |
| medium | medium | medium |
| medium | high | high |
| high | low | medium |
| high | medium | high |
| high | high | critical |

Syftet är prioritering, inte falsk precision.

## 8. Feasibility question

En feasibility-fråga ska vara konkret.

Svagt:

> Kan detta fungera?

Bra:

> Kan GitHub API-flödet skapa repository och ladda upp hela projektträdet inom relevanta rate limits för projekt upp till definierad storlek?

Bra:

> Kan tjänsten köras stateless i Coolify när alla persistenta filer flyttas till extern storage/database?

## 9. Hanteringsstrategier

En risk kan:

### Accept

Risken är känd och tolererbar.

### Mitigate

Design eller implementation minskar sannolikhet/konsekvens.

### Avoid

Lösningen ändras så att risken tas bort.

### Transfer / externalize

Ansvar flyttas till extern tjänst/plattform när det är ett medvetet designval.

### Block

Implementation ska inte fortsätta genom den riskpåverkade delen innan frågan är löst.

## 10. Spike

En spike är ett tids-/scope-avgränsat utvecklingssteg som producerar kunskap, inte produktionsfunktionalitet.

En bra spike ska ha:

- tydlig fråga,
- avgränsat scope,
- expected evidence,
- exit criteria,
- beslutspunkt efter utfallet.

Exempel:

```text
DEV-004 – Verify GitHub repository upload feasibility

Question:
Can the selected API approach reliably upload repositories up to the target size?

Evidence:
- API experiment
- rate-limit observations
- failure behavior

Done when:
- approach is accepted, rejected or replaced
- result is documented
- architecture/plan updated if needed
```

## 11. PoC

PoC används när en central lösningsidé måste bevisas i kombination.

Exempel:

- auth + API + deployment,
- event flow mellan flera system,
- database migration approach,
- browser capability.

PoC-kod är inte automatiskt production-ready.

System Builder ska explicit avgöra om PoC:

- kastas,
- hårdnar till produktionskod,
- återanvänds delvis.

## 12. Risk som blockerare

En risk ska normalt blockera nästa steg om:

- utfallet kan göra vald arkitektur ogiltig,
- det finns realistisk risk för dataförlust,
- säkerhetskritisk design är oklar,
- migration inte kan återställas,
- central tredjepartskapacitet är obevisad,
- deploymentmiljön inte stödjer nödvändig runtime,
- implementation annars sannolikt måste göras om.

System Builder ska inte fortsätta numeriskt i development plan genom en sådan blockerare.

## 13. Relation till development plan

Risker ska påverka planordning.

Exempel:

```text
RISK-003: External API throughput unknown
→ DEV-002: API feasibility spike
→ DEV-005: Main integration implementation
```

Risk-first-planering är bättre än att implementera hela flödet och upptäcka problemet sist.

## 14. Relation till architecture

När riskutfall ändrar design:

- architecture.md uppdateras,
- ADR skapas om beslutet är betydande,
- development plan revideras,
- work status synkas.

Riskanalysen ska inte bli alternativ current-state-arkitektur.

## 15. Relation till functional spec

Riskarbete får inte tyst ändra funktionellt scope.

Om risk leder till att ett must-krav:

- tas bort,
- begränsas,
- skjuts upp,

ska functional spec och eventuellt product decision uppdateras.

## 16. Relation till deployment

Deploymentrisk ska bedömas tidigt när plattformen påverkar systemdesign.

Exempel för Coolify:

- extern PostgreSQL tillgänglig?
- appen stateless?
- persistent file storage behövs?
- health endpoint möjlig?
- port och reverse proxy korrekt?
- migrationsstrategi säker?

## 17. Small-project-regel

För small-projekt får risk/feasibility ligga som ett kort avsnitt i:

- architecture.md, eller
- development-plan.md.

Separat riskdokument behövs bara när antalet eller vikten av riskerna motiverar det.

## 18. Medium / large

Medium-projekt bör normalt ha explicit risksammanställning.

Large/high-risk bör normalt ha:

- stabila RISK-ID:n,
- tydlig status,
- koppling till DEV-steg,
- blockerare,
- review före release readiness.

## 19. Canonical dokument

När separat dokument behövs:

`docs/risk-feasibility.md`

Det beskriver analys och rationale.

System Builder behöver inte införa separat YAML-riskregister i första versionen; machine state för blockerare ligger i work status och relationer kan uttryckas via plan/traceability.

## 20. Rekommenderad struktur

```text
# Risk and Feasibility

## Assumptions
## Risks
## Feasibility questions
## Spikes / PoCs
## Blocking issues
## Accepted risks
## Review outcome
```

## 21. Riskpost

```markdown
### RISK-001 – <Title>

**Category:** integration  
**Probability:** medium  
**Impact:** high  
**Level:** high  
**Status:** open

**Risk / assumption**

...

**Evidence / trigger**

...

**Handling**

...

**Related requirements / steps**

- FR-...
- DEV-...
```

## 22. Anti-patterns

Undvik:

- hundratals generiska risker,
- "säkerhet kan vara ett problem" utan konkret innebörd,
- riskregister som aldrig påverkar plan,
- PoC som smygs in som produktionskod utan review,
- blockerande risker som ignoreras för att nästa plan-ID ligger numeriskt först,
- sannolikhetspoäng med falsk exakthet.

## 23. Kvalitetskriterier

Risk/feasibility är tillräckligt bra när:

1. kritiska antaganden är synliga,
2. hög osäkerhet har planerad evidens,
3. blockerande risker påverkar next-step-val,
4. spikes/PoCs har tydliga frågor och exit-kriterier,
5. arkitektur och plan uppdateras från faktiska resultat,
6. små projekt inte belastas med onödig process.

## 24. Exit-kriterier för risk/feasibility-fasen

Fasen är klar när:

- inga osynliga högriskantaganden återstår,
- blockerande osäkerhet har antingen lösts eller blivit explicit blockerare,
- högriskfrågor har riskreducerande steg,
- arkitektur och plan kan fortsätta utan att bygga på otestade kritiska antaganden.

---

## Source: `docs/test-verification-standard.md`

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

---

## Source: `docs/security-baseline.md`

# System Builder – Säkerhetsbaslinje

## 1. Syfte

System Builder ska säkerställa att grundläggande säkerhetsfrågor beaktas i alla relevanta projekt utan att varje projekt automatiskt behandlas som en full säkerhetsrevision.

Baslinjen ska:

- fånga vanliga och kostsamma säkerhetsmissar tidigt,
- påverka krav, arkitektur, implementation, test och deployment,
- vara proportionerlig mot risk,
- kunna höja projektets kontrollnivå,
- identifiera när specialistgranskning krävs.

## 2. Grundprincip

> Secure by default där det är praktiskt, explicit riskbedömning där det inte är det.

System Builder ska inte anta att "säkerhet hanteras senare".

## 3. Omfattning

Baslinjen täcker minst när relevant:

- authentication,
- authorization,
- input validation,
- output handling,
- secrets,
- sensitive data,
- storage,
- transport security,
- dependency risk,
- logging,
- audit,
- file handling,
- external integrations,
- database access,
- deployment defaults,
- configuration,
- backups,
- error handling.

## 4. Riskproportionalitet

### Small / låg risk

Minst:
- inga hardcoded secrets,
- input validation,
- minsta nödvändiga behörighet,
- säker dependency-baseline,
- TLS via målplattform när publikt exponerad,
- loggar utan secrets,
- säkra defaultvärden.

### Medium

Utöver ovan:
- tydligare authz-modell,
- security-relevanta testfall,
- dependency scanning,
- trust boundaries i arkitekturen,
- explicit secrets/configuration model,
- deployment/security checks.

### Large / high risk

Kan kräva:
- threat modelling,
- specialist security review,
- SAST/DAST,
- penetration testing,
- formell secrets management,
- audit controls,
- regulatoriska krav,
- incident/restore-planer,
- hårdare release gates.

## 5. Authentication

När autentisering behövs ska System Builder definiera:

- vem som autentiseras,
- vilken identitetskälla som används,
- sessions-/tokenmodell på hög nivå,
- logout/expiry,
- hur credentials/secrets skyddas.

System Builder ska normalt föredra etablerad identitetsleverantör/protokoll framför egen lösenordshantering.

## 6. Authorization

Authorization ska uttryckas som verksamhets-/systemregel, inte bara UI-hide/show.

Kontroll ska ske server-side när skyddad data eller operation finns.

Princip:

> UI-begränsning är UX. Backend enforcement är säkerhet.

Beskriv när relevant:
- roles,
- ownership,
- tenant/domain boundary,
- privileged operations,
- default deny/allow-princip.

## 7. Least privilege

Komponenter, tokens och service accounts ska få minsta rimliga rättigheter.

Exempel:
- GitHub token med begränsad scope,
- DB-user utan adminbehörighet,
- container utan root där praktiskt,
- secrets bara till komponenter som behöver dem.

## 8. Input validation

All extern input ska behandlas som opålitlig.

Exempel:
- HTTP payload,
- query params,
- headers,
- filenames,
- ZIP entries,
- webhook payloads,
- external API responses när de påverkar säkerhetskritisk logik.

Validera:
- format,
- längd,
- typ,
- allowed values,
- size limits,
- path handling,
- encoding där relevant.

## 9. File handling

För uppladdade filer:

- begränsa storlek,
- validera format när möjligt,
- använd säkra temporära paths,
- förhindra path traversal,
- förhindra absoluta paths,
- undvik exekvering av användarinnehåll,
- cleanup temporära filer,
- separera persistent och ephemeral storage.

Arkivformat kräver särskild validering före extraktion.

## 10. Secrets

Secrets får inte:

- hårdkodas i repo,
- checkas in i `.env`,
- skrivas i logg,
- bäddas in i container image,
- exponeras i frontend bundle.

Secrets ska normalt tillföras via:
- environment variables,
- platform secret store,
- external secret manager.

`.env.example` får innehålla nyckelnamn men inte verkliga värden.

## 11. Sensitive data

System Builder ska identifiera känslig data när projektunderlag visar att sådan finns.

Bedöm:
- collection minimization,
- storage,
- retention,
- access,
- logging,
- backups,
- deletion,
- export.

System Builder ska inte fabricera juridiska klassificeringar.

## 12. Encryption / transport

Publik eller känslig trafik ska normalt använda TLS.

På plattformar som Coolify ska TLS normalt hanteras av plattformen.

System Builder ska undvika dubbel TLS-terminering utan anledning.

Encryption at rest ska bedömas utifrån risk och plattform; den ska inte påstås vara uppfylld utan faktisk plattforms-/lagringsgrund.

## 13. Database security

När databas används:

- credentials via secrets/configuration,
- minsta privileges,
- parametriserade queries/ORM,
- migrations kontrolleras,
- inga default/admin credentials,
- backup/restore-responsibility tydlig,
- network exposure begränsas.

Extern PostgreSQL ska inte exponeras publikt om det inte finns ett motiverat behov.

## 14. External integrations

Bedöm:
- auth scopes,
- webhook validation,
- timeout,
- retries,
- idempotency,
- rate limits,
- untrusted responses,
- secret storage,
- error leakage.

## 15. Dependency security

System Builder ska:

- använda aktivt underhållna dependencies där möjligt,
- undvika onödiga dependencies,
- låsa versioner enligt stackens normala modell,
- använda dependency scanning när projektet/CI motiverar det,
- inte uppgradera stora dependency-set opportunistiskt i orelaterade steg.

Kända kritiska vulnerabilities kan blockera release.

## 16. Logging

Loggar ska vara användbara utan att läcka:

- passwords,
- tokens,
- API keys,
- session secrets,
- känsliga payloads,
- persondata i onödan.

Bra loggar inkluderar:
- operation/correlation ID,
- outcome,
- relevant system context.

## 17. Error handling

Fel till användare/API ska inte avslöja:

- stack traces,
- secrets,
- interna credentials,
- onödiga implementation details.

Interna loggar kan ha mer diagnostik men ska fortfarande skydda secrets.

## 18. Audit

Audit trail behövs när projektets risk/krav motiverar det.

Exempel:
- privilegierade admin-operationer,
- ändring av behörighet,
- kritisk dataexport,
- security-relevant configuration.

Audit är inte samma sak som debug logging.

## 19. Secure defaults

Exempel:
- private-by-default när användarens data/repository inte uttryckligen ska vara publikt,
- explicit CORS,
- CSRF-skydd när relevant,
- secure cookies,
- debug mode off i production,
- no default passwords,
- no wildcard privileges,
- health endpoint utan secrets.

## 20. Web security baseline

För webbappar när relevant:

- server-side authz,
- XSS-säker rendering,
- CSRF där cookie-auth kräver det,
- CORS least privilege,
- secure/session cookie-flags,
- security headers där plattformen stödjer det,
- rate limiting för känsliga endpoints när risk motiverar det.

## 21. API security baseline

- authentication där endpoint inte är publik,
- authorization per operation/resource,
- schema/input validation,
- size limits,
- rate/abuse considerations,
- idempotency där dubbel exekvering är farlig,
- safe error responses.

## 22. Container baseline

För containeriserade tjänster:

- minimal base image där praktiskt,
- non-root runtime där möjligt,
- inga secrets i image/layers,
- `.dockerignore`,
- endast nödvändiga ports,
- health checks,
- reproducible build,
- dependency/package scanning när relevant.

## 23. Coolify baseline

Vid Coolify:

- app image innehåller inte PostgreSQL,
- PostgreSQL körs externt/separat,
- TLS och reverse proxy hanteras av plattformen,
- secrets sätts i plattformens environment/secret configuration,
- publicera bara appens nödvändiga endpoint,
- health endpoint konfigureras,
- persistent volume endast om appen verkligen behöver filstorage.

## 24. CI/CD security

- secrets i CI secret store,
- minimala workflow permissions,
- pinning/versionering av actions enligt projektpolicy,
- inga secrets i PR-output/loggar,
- artifacts hanteras med avsedd retention,
- release workflow ska bygga från verifierad commit/tag.

## 25. GitHub baseline

När repository finns på GitHub bör System Builder vid behov stödja:

- `.gitignore`,
- secret scanning/dependency tooling när tillgängligt,
- branch/PR workflow,
- begränsade GitHub token permissions,
- no credentials committed.

## 26. Security verification

Security-relevant krav ska ha explicit verifiering.

Exempel:
- unauthorized user gets denied,
- path traversal ZIP rejected,
- secrets absent from logs,
- container runs non-root,
- protected endpoint requires auth,
- invalid webhook signature rejected.

## 27. Security blocker

Säkerhetsfråga ska blockera relevant implementation/release när:

- authz för känslig operation är oklar,
- credentials måste hårdkodas,
- användarinput kan leda till code/path execution,
- kritisk vulnerability saknar mitigation,
- data riskerar okontrollerad förlust/exponering,
- deployment kräver osäker publik databas,
- central trust boundary är odefinierad.

## 28. Specialistgranskning

System Builder ska rekommendera specialistgranskning när exempelvis:

- systemet hanterar mycket känslig data,
- Internet-exponerad attackyta är stor,
- komplex auth/identity,
- payment/financial controls,
- high-impact admin operations,
- avancerad cryptography,
- regulatorisk säkerhetsnivå,
- kritisk infrastruktur.

System Builder är process owner och baseline-granskare, inte automatiskt ersättare för security specialist.

## 29. Threat model

Threat model behövs när risk motiverar det.

En lätt modell kan täcka:
- assets,
- actors,
- trust boundaries,
- entry points,
- abuse cases,
- mitigations.

Full STRIDE eller motsvarande är inte obligatoriskt för varje system.

## 30. Säkerhetsdokumentation

Security ska primärt integreras i:
- functional spec (security requirements),
- architecture (security model),
- risk/feasibility,
- test strategy,
- configuration,
- operations.

Separat `docs/security.md` skapas bara när komplexiteten motiverar det.

## 31. CHANGE-regel

Vid CHANGE ska System Builder fråga/analysera:

- förändras attackytan?
- tillkommer ny input/integration?
- ändras auth/authz?
- ändras dataägarskap?
- tillkommer secrets?
- ändras deployment/network exposure?
- krävs nya regression/security tests?

## 32. IMPROVE-regel

Teknisk förbättring får inte försämra säkerhetskontroller även om funktionellt beteende är oförändrat.

Security-sensitive refactoring bör ha characterization/regression tests.

## 33. Anti-patterns

Undvik:
- "vi använder HTTPS, alltså är systemet säkert",
- auth endast i frontend,
- secrets i `.env` committed,
- admin DB-user för app,
- wildcard CORS utan behov,
- logging av fulla tokens,
- root container som default utan anledning,
- security review först efter release,
- generisk checklist utan koppling till faktisk systemrisk.

## 34. Security review checklist

Minst när relevant:

- [ ] Authentication defined
- [ ] Authorization enforced server-side
- [ ] Least privilege
- [ ] Input validation
- [ ] File handling safe
- [ ] Secrets externalized
- [ ] Sensitive data identified
- [ ] TLS ownership defined
- [ ] DB access constrained
- [ ] External integrations reviewed
- [ ] Dependencies checked
- [ ] Logs avoid secrets
- [ ] Error responses safe
- [ ] Container defaults safe
- [ ] Deployment exposure reviewed
- [ ] Security tests exist for critical controls

## 35. Exit-kriterier för säkerhetsbaslinjen

Fasen är tillräcklig när:

- security-relevant requirements är synliga,
- trust/auth/authz/input/secrets/deployment är bedömda,
- kritiska security risks är blockerare eller mitigerade,
- verifieringsplan finns,
- specialist review är identifierad när baseline inte räcker.
