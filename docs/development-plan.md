# System Builder – Development Plan

## 1. Syfte

System Builder ska bli en GPT som hjälper användaren från behov eller förändringsönskemål till ett fungerande, verifierat, dokumenterat och paketerat system.

GPT:n ska kunna:

- skapa nya system från idé eller behov,
- vidareutveckla befintliga system,
- göra avgränsade tekniska förbättringar,
- arbeta i både ZIP-läge och GitHub-läge,
- skapa och underhålla funktionell specifikation,
- skapa övergripande arkitekturbeskrivning,
- skapa en stegvis utvecklingsplan,
- implementera exakt ett rekommenderat steg åt gången,
- testa och verifiera genomförda steg,
- hantera grundläggande repository-hygien,
- skapa `.gitignore`, `.dockerignore` och relevanta GitHub Actions,
- stödja deployment- och paketeringsmönster,
- skapa installations-, konfigurations- och driftdokumentation,
- hålla maskinläsbar status och spårbarhet i YAML,
- bygga både Chat ZIP och Custom GPT från samma canonical kontrakt.

## 2. Grundläggande designbeslut

### 2.1 Runtime

Bygg båda distributionerna:

- Chat ZIP
- Custom GPT

Båda ska härledas från samma canonical beteende- och capability-kontrakt.

### 2.2 Arbetslägen

System Builder ska minst stödja:

- **CREATE** – skapa nytt system.
- **CHANGE** – ändra eller utöka befintligt system.
- **IMPROVE** – avgränsad teknisk förbättring.
- **PLAN** – skapa eller revidera plan utan implementation.
- **EXECUTE** – genomför exakt nästa rekommenderade steg.
- **REPAIR** – reparera inkonsekvent workflow/status/dokumentation.
- **RELEASE** – bedöm och förbered release readiness.

### 2.3 Dokumentformat

Princip:

> Markdown beskriver intent, design och vägledning. YAML beskriver maskinellt tillstånd, konfiguration och spårbarhet. JSON Schema validerar det maskinläsbara kontraktet.

Canonical Markdown:

- `docs/functional-specification.md`
- `docs/architecture.md`
- `docs/development-plan.md`
- `docs/test-strategy.md`
- `docs/configuration.md`
- `docs/installation.md`
- `docs/operations.md`
- `docs/product-decisions.md`
- `docs/architecture-decisions/*.md`
- `docs/changes/*/*.md`

Canonical YAML:

- `.system-builder/project.yaml`
- `.system-builder/work-status.yaml`
- `.system-builder/traceability.yaml`
- `.system-builder/deployment-profile.yaml`

Schemas:

- `schemas/project.schema.json`
- `schemas/work-status.schema.json`
- `schemas/traceability.schema.json`
- `schemas/deployment-profile.schema.json`

Undvik parallella Markdown- och YAML-versioner av samma information.

### 2.4 Source of truth

Prioritetsordning vid arbete i ett systemrepo:

1. användarens aktuella uttryckliga instruktion,
2. repositoryts `AGENTS.md`,
3. `.system-builder/work-status.yaml`,
4. aktiv utvecklingsplan och övriga canonical dokument,
5. befintlig kod, tester och projektkonventioner,
6. System Builders generiska Knowledge som fallback.

Konversationsminne får inte ersätta repository-status.

### 2.5 Exekveringsprincip

Vid `"Gör nästa steg"`:

1. READ
2. ASSESS
3. SELECT
4. LOCK
5. IMPLEMENT
6. VERIFY
7. REVIEW
8. UPDATE DOCS
9. UPDATE STATUS
10. PACKAGE/COMMIT
11. STOP

Normalt exakt ett utvecklingssteg per körning.

---

# Utvecklingssteg

## SB-01 – Skapa grundprojektet

### Mål

Skapa canonical projektstruktur för GPT-projektet System Builder.

### Leverans

Minst:

- `README.md`
- `PROJECT.md`
- `STATUS.md`
- `VERSION`
- `gpt-project.yaml`
- `project-status.yaml`
- `docs/development-plan.md`
- grundläggande katalogstruktur för `src/`, `knowledge/`, `schemas/`, `scripts/`, `evals/` och distributioner.

### Klart när

- projektstrukturen finns,
- utvecklingsplanen ingår,
- status anger SB-01 som klar,
- nästa rekommenderade steg är SB-02,
- komplett projekt-ZIP kan byggas.

---

## SB-02 – Definiera canonical identitet och scope

### Mål

Fastställ System Builders identitet, syfte, målgrupp och tydliga ansvarsgränser.

### Innehåll

Definiera:

- vad System Builder gör,
- CREATE/CHANGE/IMPROVE,
- vad som ligger utanför kärnansvaret,
- relationen till specialist-GPT:er som Kodförbättraren,
- principen om adaptiv process efter projektets komplexitet.

### Klart när

- canonical scope är dokumenterat,
- overlappar mot andra GPT:er är explicit hanterade,
- inga motstridiga huvuduppdrag finns.

---

## SB-03 – Definiera end-to-end-processen

### Mål

Beskriv processen från behov till release och vidare förvaltning.

### Process

Minst:

- Need / Change Request
- Discovery
- Goals / Success Criteria
- Scope / Priorities
- Functional Specification
- Risk / Feasibility
- Architecture
- Development Plan
- Implementation
- Test / Review
- Packaging
- Deployment Readiness
- Acceptance / Release Readiness
- Installation / Operations Documentation
- Release / Maintain

### Klart när

- varje fas har syfte och exit-kriterier,
- små projekt kan använda en lättare variant,
- processen fungerar för både CREATE och CHANGE.

---

## SB-04 – Definiera projektkomplexitet och adaptiv process

### Mål

Inför en enkel modell för att skala dokumentation och process efter projektets storlek.

### Omfattning

Minst:

- `small`
- `medium`
- `large`

Definiera vilka artefakter och kontrollnivåer som är obligatoriska respektive valfria per nivå.

### Klart när

- små projekt inte tvingas till onödig dokumentation,
- större projekt inte tappar viktiga kontrollpunkter,
- klassificeringen kan härledas utan onödiga frågor.

---

## SB-05 – Definiera dokument- och state-arkitektur

### Mål

Fastställ kontraktet mellan Markdown, YAML och JSON Schema.

### Omfattning

Definiera:

- current-state documents,
- historical decision/change documents,
- maskinläsbart state,
- regler mot dubbla sanningskällor,
- stabila ID:n för krav, steg, tester, ADR och change requests.

### Klart när

- varje informationskategori har exakt en canonical representation,
- formatreglerna är entydiga,
- spårbarhet kan byggas utan textduplicering.

---

## SB-06 – Skapa YAML-schemas för projekt och arbetsstatus

### Mål

Skapa validerbara maskinkontrakt för:

- `.system-builder/project.yaml`
- `.system-builder/work-status.yaml`

### Klart när

- JSON Schema finns,
- exempel-YAML validerar,
- invalid fixtures fångas,
- `next.recommended`, blockerare och verifieringsstatus kan representeras.

---

## SB-07 – Skapa schema för kravspårbarhet

### Mål

Definiera `.system-builder/traceability.yaml`.

### Omfattning

Stöd minst kopplingar mellan:

- funktionella krav,
- acceptance criteria,
- development steps,
- verifiering/test,
- implementation status.

### Klart när

- orphan requirements kan identifieras,
- oimplementerade must-krav kan identifieras,
- schema och exempel validerar.

---

## SB-08 – Skapa schema för deploymentprofil

### Mål

Definiera `.system-builder/deployment-profile.yaml`.

### Omfattning

Representera minst:

- packaging,
- target platform,
- runtime,
- database,
- persistence,
- networking,
- TLS/reverse proxy,
- health checks,
- registry,
- environment configuration.

### Klart när

- Docker och Coolify-scenarier kan uttryckas,
- extern PostgreSQL kan uttryckas explicit,
- schema och exempel validerar.

---

## SB-09 – Definiera funktionell specifikation

### Mål

Skapa canonical struktur och kvalitetsregler för `docs/functional-specification.md`.

### Struktur

Minst:

- syfte och mål,
- scope,
- aktörer,
- användningsfall,
- funktionella krav,
- affärsregler,
- informationsbehov,
- integrationer,
- behörighet,
- fel- och undantagsfall,
- icke-funktionella krav,
- acceptance criteria,
- out of scope,
- öppna frågor.

### Klart när

- stabila krav-ID:n stöds,
- prioritering stöds,
- spec fungerar för både nytt och befintligt system,
- GPT:n kan uppdatera current-state-spec efter genomförd change.

---

## SB-10 – Definiera arkitekturbeskrivning

### Mål

Skapa canonical struktur och kvalitetsregler för `docs/architecture.md`.

### Struktur

Minst:

- arkitekturmål,
- systemkontext,
- huvudkomponenter,
- ansvar,
- dataflöden,
- datamodell på hög nivå,
- integrationer,
- säkerhetsprinciper,
- deploymentmodell,
- tekniska huvudval,
- trade-offs,
- ADR-behov.

### Klart när

- dokumentet hålls på övergripande nivå,
- detaljdesign inte blandas in mekaniskt,
- CHANGE kan analysera arkitekturpåverkan.

---

## SB-11 – Definiera ADR- och produktbeslut

### Mål

Skapa mönster för historiska beslut.

### Leverans

- `docs/architecture-decisions/ADR-xxx-*.md`
- `docs/product-decisions.md`

### Klart när

- arkitekturbeskrivningen beskriver current state,
- ADR beskriver historiska beslut och rationale,
- produktbeslut kan följas utan att förorena functional spec.

---

## SB-12 – Definiera development plan-kontraktet

### Mål

Skapa kvalitetsregler för `docs/development-plan.md`.

### Varje steg ska minst innehålla

- ID,
- mål,
- scope,
- förutsättningar,
- implementation,
- tester/verifiering,
- klart-kriterier,
- beroenden.

### Regler

- ett steg ska vara rimligt för en separat prompt,
- ett steg ska kunna verifieras självständigt,
- framtida steg får inte implementeras i förtid,
- plan får revideras när ny evidens kräver det.

### Klart när

- planformatet stödjer robust `"Gör nästa steg"`,
- steps kan delas/slås ihop/infogas med motivering,
- status hålls utanför Markdown-planen.

---

## SB-13 – Definiera risk- och feasibility-arbete

### Mål

Skapa regler för att identifiera blockerande osäkerheter före dyr implementation.

### Omfattning

Minst:

- externa API:er,
- teknikrisk,
- licenser,
- säkerhet,
- personuppgifter/känslig data,
- prestanda,
- deployment,
- migrationsrisk,
- tredjepartsberoenden.

Stöd spike/PoC när det är det säkraste nästa steget.

### Klart när

- högriskantaganden kan flyttas tidigt i planen,
- osäkerhet inte maskeras som ett färdigt krav.

---

## SB-14 – Definiera test- och verifieringsstrategi

### Mål

Skapa `docs/test-strategy.md`-mönster och verifieringsregler.

### Omfattning

Minst:

- unit,
- integration,
- API,
- UI/e2e där relevant,
- build,
- lint/typecheck,
- security/dependency checks där relevant,
- acceptance verification.

### Klart när

- testnivån anpassas till risk,
- röda baseline-tester hanteras ärligt,
- steg inte markeras klart utan nödvändig verifiering.

---

## SB-15 – Definiera säkerhetsbaslinje

### Mål

Ge System Builder tillräcklig generell säkerhetskompetens utan att göra den till en fullständig säkerhetsgranskare.

### Omfattning

Minst:

- authentication,
- authorization,
- secrets,
- sensitive data,
- logging,
- dependency scanning,
- input validation,
- backup/restore responsibility,
- grundläggande threat awareness.

### Klart när

- säkerhet behandlas tidigt,
- högriskfrågor kan flaggas för specialistgranskning,
- säkerhetskrav kan kopplas till plan och verifiering.

---

## SB-16 – Implementera CREATE-mode

### Mål

Definiera komplett runtimebeteende för att skapa nytt system från behov eller idé.

### Klart när

GPT:n kan gå från:

- behov,
- discovery,
- spec,
- arkitektur,
- plan,

utan att börja implementera för tidigt, och kan därefter genomföra första utvecklingssteget när användaren ber om det.

---

## SB-17 – Implementera CHANGE-mode

### Mål

Definiera runtimebeteende för ändring av befintligt system.

### Process

Minst:

- förstå change request,
- analysera nuvarande kod och canonical docs,
- impact analysis,
- uppdatera spec/arkitektur där relevant,
- skapa change plan,
- implementera stegvis,
- integrera slutresultatet i current-state docs.

### Klart när

- historik och current state hålls isär,
- gamla docs inte lämnas stale efter genomförd ändring.

---

## SB-18 – Implementera IMPROVE-mode

### Mål

Definiera säkert beteende för avgränsade tekniska förbättringar.

### Gräns

System Builder ska kunna göra förbättringar som hör till den aktuella utvecklingen men hänvisa djup, bred refaktoreringsanalys till specialistflöde när det är lämpligare.

### Klart när

- refaktorering inte blandas ihop med funktionell förändring,
- scope hålls smalt,
- tester/verifiering krävs.

---

## SB-19 – Implementera next-step state machine

### Mål

Gör `"Gör nästa steg"` robust.

### State machine

READ → ASSESS → SELECT → LOCK → IMPLEMENT → VERIFY → REVIEW → UPDATE DOCS → UPDATE STATUS → PACKAGE/COMMIT → STOP

### Klart när

- exakt ett `selected_step` finns,
- blockerare prioriteras,
- plan/status-konflikter hanteras,
- framtida steg inte markeras complete,
- repository-status styr nästa steg.

---

## SB-20 – Implementera ZIP-läge

### Mål

Ge System Builder säkert och komplett ZIP-arbetsflöde.

### Regler

- validera archive paths,
- bevara wrapper/root-shape,
- bevara okända filer/binära assets,
- skapa komplett uppdaterad projekt-ZIP,
- kör inte okänd projektkod bara för inspektion,
- detektera source drift där möjligt.

### Klart när

- nytt projekt och befintligt projekt fungerar,
- returned ZIP är nästa canonical utgångsläge,
- ZIP-integritet verifieras.

---

## SB-21 – Implementera GitHub-läge

### Mål

Ge System Builder förstklassigt repository/PR-arbetsflöde.

### Regler

Minst:

- läs repo innan ändring,
- skapa branch/PR för ny serie,
- fortsätt relevant öppen PR,
- efter merge utgå från aktuell default branch,
- kontrollera drift innan nästa steg,
- commit/PR ska motsvara ett avgränsat plansteg.

### Klart när

- CREATE och CHANGE kan genomföras i GitHub-läge,
- PR-status kan användas som del av aktuell projektstatus,
- konversationsminne inte krävs.

---

## SB-22 – Repository hygiene och `.gitignore`

### Mål

Definiera hur System Builder skapar och underhåller repository-hygien.

### Omfattning

Minst:

- `.gitignore`,
- `.dockerignore`,
- stackanpassning,
- bevara användarens befintliga regler,
- undvik att committa build/cache/secrets,
- radera inte okända filer bara på namn.

### Klart när

- vanliga stackar hanteras rimligt,
- hygiene-validering finns,
- inga farliga generella delete-regler används.

---

## SB-23 – GitHub Actions-baslinje

### Mål

Ge System Builder mönster för rimlig CI.

### Omfattning

Beroende på stack:

- build,
- unit/integration tests,
- lint,
- typecheck,
- dependency/security checks när relevant,
- container build verification.

### Regler

- skapa endast workflows projektet behöver,
- ingen överdriven CI-komplexitet,
- bevara/utöka befintlig CI där det är säkrare.

### Klart när

- minst ett generellt CI-mönster finns,
- flera typiska stackar kan härledas,
- verifiering av workflow-filer finns.

---

## SB-24 – Deployment- och paketeringsmönster

### Mål

Skapa Knowledge och runtimekontrakt för vanliga deploymentmiljöer.

### Minst följande profiler

1. local development
2. Docker standalone
3. Docker + external PostgreSQL
4. Coolify + external PostgreSQL
5. generic container platform
6. basic Kubernetes

### Klart när

- System Builder frågar om deployment endast när verkligt val saknas,
- deploymentprofilen styr implementation och dokumentation,
- databas inte råkar byggas in i app-image för extern-DB-profiler.

---

## SB-25 – Docker-baslinje

### Mål

Definiera goda generella containeriseringsmönster.

### Omfattning

Minst:

- multi-stage builds där relevant,
- non-root runtime när möjligt,
- environment config,
- health checks,
- stateless design som default,
- externa secrets,
- minimal runtime image,
- `.dockerignore`.

### Klart när

- containerisering är reproducerbar,
- build/run kan verifieras,
- databas separeras från app-image.

---

## SB-26 – Coolify-profil

### Mål

Skapa explicit Coolify-stöd.

### Omfattning

Minst:

- Docker-baserad applikation,
- extern PostgreSQL,
- domän/reverse proxy hanteras av plattform,
- TLS hanteras av plattform,
- miljövariabler dokumenteras,
- health endpoint,
- persistent volumes endast när systemet faktiskt behöver dem.

### Klart när

- Coolify-profil kan väljas eller härledas,
- installation.md och operations.md kan anpassas,
- inga antaganden görs om Postgres i app-image.

---

## SB-27 – Installations-, konfigurations- och driftdokumentation

### Mål

Skapa standardmönster för:

- `docs/configuration.md`
- `docs/installation.md`
- `docs/operations.md`

### Configuration ska minst täcka

- variabel,
- required/default,
- beskrivning,
- känslighet,
- exempel där säkert.

### Installation ska minst täcka

- prerequisites,
- configuration,
- database,
- build/package,
- installation,
- first startup,
- verification,
- upgrade,
- uninstall,
- troubleshooting.

### Operations ska minst täcka

- system overview,
- start/stop/restart,
- health,
- logs,
- metrics där relevant,
- database,
- backup/restore,
- upgrades,
- rollback,
- secrets/certificates,
- troubleshooting.

### Klart när

- dokumentens omfattning anpassas till projektstorlek,
- de genereras från faktisk deploymentprofil och implementation,
- de hålls uppdaterade efter CHANGE.

---

## SB-28 – Release readiness och acceptance

### Mål

Definiera när ett system får betraktas som färdigt/releaseklart.

### Kontroll

Minst:

- must requirements,
- acceptance criteria,
- architecture current,
- tests,
- security baseline,
- packaging,
- deployment readiness,
- installation docs,
- operations docs,
- known limitations,
- traceability completeness.

### Klart när

- release kan blockeras av verkliga brister,
- warnings skiljs från blockers,
- "tests green" inte ensam likställs med färdigt system.

---

## SB-29 – Canonical Knowledge-arkitektur

### Mål

Fördela generisk kunskap i få, tydliga Knowledge-filer.

### Kandidatområden

- functional specification
- architecture
- development planning
- testing/safety
- repository/GitHub
- packaging/deployment
- operations documentation

### Regler

- kritiskt runtimebeteende ligger i canonical instruktion,
- Knowledge används för fördjupning och mönster,
- kärnflödet ska kräva få filhopp.

### Klart när

- Knowledge inte duplicerar instruktionen,
- varje fil har tydligt retrievalsyfte,
- Custom GPT-uploadmängden är rimlig.

---

## SB-30 – Bygg canonical runtimeinstruktion

### Mål

Sammanfoga de föregående kontrakten till System Builders canonical systeminstruktion.

### Klart när

- mode-routing är entydig,
- source-of-truth-regler finns,
- next-step state machine är explicit,
- ZIP/GitHub-regler finns,
- dokument/state-format är explicit,
- kritiska regler fungerar utan Knowledge-retrieval.

---

## SB-31 – Chat ZIP-runtime

### Mål

Bygg portable Chat ZIP-distribution.

### Leverans

Minst:

- `START-HERE.md`
- canonical instruktion/runtimeinstruktion,
- nödvändiga Knowledge-filer,
- schemas,
- runtime-scripts,
- manifest/version.

### Klart när

- ZIP kan användas genom att bifogas i vanlig ChatGPT-konversation,
- runtimevalidering passerar,
- inga development-only-filer läcker in onödigt.

---

## SB-32 – Custom GPT-kompilering

### Mål

Bygg Custom GPT-distribution från samma canonical kontrakt.

### Klart när

- Instructions ryms inom plattformsgränser,
- Knowledge-uploadset är definierat,
- conversation starters finns,
- rekommenderade capabilities finns,
- inga kärnregler har flyttats bort till Knowledge bara för att spara instruktionstext.

---

## SB-33 – Instruction-adherence evals

### Mål

Skapa modellneutrala kontraktstester för kritiskt beteende.

### Minst

- CREATE vs CHANGE routing,
- one-step-only,
- source of truth,
- plan/status conflict,
- YAML state updates,
- Markdown/YAML no-duplication,
- ZIP root-shape,
- GitHub PR continuation,
- verification honesty,
- documentation current-state updates,
- Coolify external PostgreSQL,
- release readiness blockers.

### Klart när

- kritiska invariantbrott fångas,
- evals fungerar för både mindre och starkare modeller.

---

## SB-34 – E2E-scenario: nytt litet system

### Mål

Testa hela CREATE-flödet från blank idé.

### Scenario

Behov → spec → architecture → plan → första implementeringssteget → verifiering → status.

### Klart när

- ingen implementation sker för tidigt,
- artefakter har korrekt format,
- state kan återupptas utan samtalsminne.

---

## SB-35 – E2E-scenario: förändring av befintligt system

### Mål

Testa CHANGE-flödet.

### Scenario

Befintligt repo + change request → impact analysis → spec/architecture update → change plan → ett implementationsteg.

### Klart när

- current-state docs uppdateras,
- change-historik bevaras,
- framtida steg inte genomförs.

---

## SB-36 – E2E-scenario: Docker/Coolify

### Mål

Testa deploymentkompetensen.

### Scenario

Containeriserad webbtjänst med extern PostgreSQL för Coolify.

### Klart när

- app-image saknar inbyggd PostgreSQL,
- deploymentprofil är korrekt,
- health/configuration/docs är konsekventa,
- CI kan verifiera image-build.

---

## SB-37 – Runtime parity och cross-runtime-validering

### Mål

Verifiera att Chat ZIP och Custom GPT representerar samma kärnbeteende.

### Klart när

- capability-skillnader är dokumenterade,
- inga oavsiktliga beteendeskillnader finns,
- båda runtimepaketen validerar.

---

## SB-38 – GitHub Actions för System Builder-projektet

### Mål

Lägg till CI för själva GPT-projektet.

### CI ska minst

- lint:a projektet,
- validera schemas,
- köra evals,
- köra E2E-fixtures där praktiskt,
- bygga distributioner,
- validera distributioner.

### Klart när

- push/PR-CI fungerar,
- fel stoppar build korrekt.

---

## SB-39 – GitHub Release-byggning

### Mål

Bygg releaseartefakter automatiskt från release-taggen.

### Leverans

Minst:

- System Builder Chat ZIP
- System Builder Custom GPT ZIP
- komplett projekt-ZIP där det är lämpligt.

### Klart när

- `vX.Y.Z` styr versionsnumret,
- assets byggs och valideras före publicering.

---

## SB-40 – Final hygiene och release readiness

### Mål

Gör fullständig slutgranskning inför första stabila release.

### Kontroll

- canonical vs generated files,
- temporary/historical files,
- stale docs,
- schemas,
- lint,
- evals,
- E2E,
- runtime parity,
- distribution validation,
- known limitations,
- release documentation.

### Klart när

- inga blockers återstår,
- warnings är dokumenterade,
- projektstatus anger release ready.

---

## SB-41 – Första stabila releasekandidat

### Mål

Förbered `v1.0.0`.

### Leverans

- versions- och releasefiler,
- release notes,
- kompletta validerade artefakter,
- slutlig status.

### Klart när

- release readiness passerar,
- distributionsartefakterna är reproducerbara,
- projektet kan återupptas efter release utan konversationshistorik.

---

# 3. Viktiga kvalitetsprinciper under hela planen

Efter varje genomfört steg ska:

1. aktuell leverans finnas,
2. relevanta valideringar köras,
3. `project-status.yaml` uppdateras,
4. `STATUS.md` synkroniseras,
5. project hygiene bedömas,
6. nästa rekommenderade steg fastställas från faktisk status,
7. en komplett projekt-ZIP byggas.

Planen får ändras när ny evidens visar att ett annat steg bör prioriteras. Blockerare, failed validation, hygieneproblem och korrigeringsbehov går före planens numeriska ordning.

# 4. Rekommenderat första genomförandesteg

**SB-01 – Skapa grundprojektet**

Det är första steget där den faktiska System Builder-projekt-ZIP:en ska skapas.
