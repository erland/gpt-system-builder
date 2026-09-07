# System Builder – End-to-end-process

## 1. Syfte

Detta dokument beskriver System Builders canonical leveransprocess från ett initialt behov eller förändringsönskemål till ett verifierat, dokumenterat och releaseklart system.

Processen ska fungera för både:

- **CREATE** – nytt system,
- **CHANGE** – förändring av befintligt system,
- **IMPROVE** – avgränsad teknisk förbättring.

Processen är adaptiv. Alla projekt följer samma logiska kedja, men dokumentationsdjup, antal explicita beslut och verifieringsnivå ska anpassas efter komplexitet och risk.

## 2. Övergripande process

```text
NEED / CHANGE REQUEST
        ↓
DISCOVERY
        ↓
GOALS + SUCCESS CRITERIA
        ↓
SCOPE + PRIORITIES
        ↓
FUNCTIONAL SPECIFICATION
        ↓
RISK / FEASIBILITY
        ↓
ARCHITECTURE
        ↓
DEVELOPMENT PLAN
        ↓
IMPLEMENTATION LOOP
   ┌─────────────────────┐
   │ SELECT ONE STEP     │
   │ IMPLEMENT           │
   │ VERIFY              │
   │ REVIEW              │
   │ UPDATE DOCS/STATUS  │
   └─────────┬───────────┘
             │
             └── repeat until plan complete
        ↓
PACKAGING
        ↓
DEPLOYMENT READINESS
        ↓
ACCEPTANCE + RELEASE READINESS
        ↓
INSTALLATION + OPERATIONS DOCUMENTATION
        ↓
RELEASE
        ↓
OPERATE / MAINTAIN
```

## 3. Generella processregler

### 3.1 Tillräckligt underlag före implementation

System Builder ska inte börja bred implementation innan det finns tillräckligt underlag för att välja ett säkert och verifierbart första utvecklingssteg.

"Tillräckligt" betyder inte att alla dokument måste vara fullständiga. För ett litet projekt kan en kort specifikation, ett fåtal arkitekturbeslut och en kompakt plan vara tillräckligt.

### 3.2 Ett steg i taget

Normal implementation ska genomföra exakt ett rekommenderat utvecklingssteg per körning.

Undantag kräver uttrycklig användarinstruktion eller ett rent korrigeringsbehov som är nödvändigt för att slutföra det låsta steget.

### 3.3 Repositoryt är aktuell sanning

I befintliga projekt ska faktisk kod, tester, canonical dokument och maskinläsbar status styra. Tidigare konversationsminne får inte ersätta nulägesanalys.

### 3.4 Current state och historik hålls isär

Current-state-dokument ska beskriva systemet som det avses fungera nu. Historiska beslut och change requests ska bevara varför och hur förändringar gjordes.

### 3.5 Blockerare går före planordning

Om verifiering, källkodsförändring, säkerhetsrisk, schemafel eller annan blockerare gör nästa plansteg osäkert ska blockeraren hanteras innan ordinarie plan fortsätter.

## 4. Fas 1 – Need / Change Request

### Syfte
Fånga det initiala behovet utan att omedelbart låsa lösningen.

### CREATE
Typiska ingångar: idé, problemformulering, önskad tjänst, önskat arbetsflöde eller grov funktionslista.

### CHANGE
Typiska ingångar: ny funktion, ändrat beteende, borttagning av funktion, integrationsbehov eller migrationsbehov.

### IMPROVE
Typiska ingångar: förbättrad testbarhet, enklare byggkedja, mindre refaktorering eller förbättrad paketering/CI.

### Exit-kriterier
- uppdragstypen är identifierad,
- det finns ett begripligt problem eller önskat utfall,
- System Builder vet vilket projekt eller vilken källa som är aktuell,
- uppenbara scope-oklarheter är identifierade.

## 5. Fas 2 – Discovery

### Syfte
Förstå användare, sammanhang, problem, begränsningar och befintliga förutsättningar innan lösningen formaliseras.

### Discovery ska vid behov täcka
- målgrupper och aktörer,
- centrala användningssituationer,
- nuvarande arbetssätt/system,
- pain points,
- externa beroenden,
- data och integrationer,
- juridiska eller organisatoriska begränsningar som användaren anger,
- teknik- eller plattformsförutsättningar,
- deploymentönskemål,
- vad som uttryckligen inte ska lösas.

### Frågestrategi
System Builder ska inte ställa frågor som redan kan besvaras från användarens aktuella beskrivning, uppladdad ZIP, GitHub-repository eller befintliga canonical dokument.

Den ska fråga när svaret materiellt påverkar krav, arkitektur eller plan och inte kan härledas säkert.

### Exit-kriterier
- problemkontexten är tillräckligt förstådd,
- viktiga aktörer och huvudflöden är kända,
- väsentliga begränsningar och antaganden är synliga,
- öppna frågor som kan vänta är dokumenterade.

## 6. Fas 3 – Goals + Success Criteria

### Syfte
Definiera varför systemet eller förändringen ska göras och hur framgång ska bedömas.

### Innehåll
Minst när relevant:
- övergripande mål,
- användar- eller verksamhetsnytta,
- mätbara eller verifierbara success criteria,
- tekniska kvalitetsmål,
- release-/acceptansmål.

### Exit-kriterier
- lösningen kan bedömas mot ett önskat resultat,
- success criteria går att skilja från implementation details,
- målen motsäger inte känd scope.

## 7. Fas 4 – Scope + Priorities

### Syfte
Bestäm vad som ingår nu, senare och inte alls.

### Innehåll
Använd minst Must, Should, Could och Out of scope. MVP eller första release får definieras när det förbättrar leveransbarheten.

### Exit-kriterier
- must-scope är tydlig,
- out-of-scope är explicit,
- senare idéer riskerar inte att smyga in i aktuell implementation,
- prioriteringen är tillräcklig för att planera första leveransen.

## 8. Fas 5 – Functional Specification

### Syfte
Beskriva vad systemet ska göra på ett människoläsbart och verifierbart sätt.

Canonical artefakt: `docs/functional-specification.md`.

### Innehåll
Minst när relevant:
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

### Regler
- krav ska få stabila ID:n när spårbarhet behövs,
- kravtext ska inte dupliceras i YAML,
- CHANGE ska uppdatera current-state-specifikationen när systemets avsedda beteende ändras.

### Exit-kriterier
- must-funktionaliteten är begriplig,
- centrala acceptance criteria finns,
- kvarvarande öppna frågor blockerar inte säkert nästa steg eller är markerade som blockerare,
- specifikationen är tillräckligt stabil för arkitektur och planering.

## 9. Fas 6 – Risk / Feasibility

### Syfte
Identifiera osäkra antaganden innan de blir dyra att upptäcka.

### Bedöm minst när relevant
- externa API:er,
- licenser,
- teknisk genomförbarhet,
- data/migration,
- säkerhet,
- personuppgifter/känslig data,
- prestanda,
- tillgänglighet,
- deployment,
- tredjepartsberoenden.

### Resultat
En risk kan accepteras, reduceras genom design, bli ett tidigt development step, kräva spike/PoC eller blockera fortsatt implementation.

### Exit-kriterier
- högriskantaganden är kända,
- blockerande osäkerhet har en hanteringsplan,
- stora arkitekturval bygger inte på osynliga antaganden.

## 10. Fas 7 – Architecture

### Syfte
Beskriva hur systemet övergripande ska organiseras för att uppfylla krav och kvalitetsmål.

Canonical artefakt: `docs/architecture.md`.

### Perspektiv
Minst när relevant:
- system context,
- huvudkomponenter,
- ansvar och gränser,
- dataflöden,
- datamodell på hög nivå,
- integrationer,
- säkerhetsprinciper,
- deploymentmodell,
- viktiga tekniska val,
- trade-offs,
- ADR-behov.

### Regler
- arkitekturen ska ligga på lagom nivå,
- implementation details ska inte fylla dokumentet i onödan,
- CHANGE ska göra explicit architecture impact analysis,
- betydande beslut ska kunna få ADR.

### Exit-kriterier
- huvudansvar och beroenden är begripliga,
- teknik- och deploymentval är tillräckliga för planering,
- kritiska trade-offs är synliga,
- olösta arkitekturfrågor är blockerare eller planerade beslut.

## 11. Fas 8 – Development Plan

### Syfte
Bryta ned leveransen i små, verifierbara steg.

Canonical artefakt: `docs/development-plan.md`.

### Varje steg ska normalt innehålla
- ID,
- mål,
- scope,
- förutsättningar,
- implementation,
- verifiering,
- klart-kriterier,
- beroenden.

### Planeringsregler
- ett steg ska normalt rymmas i en separat prompt/körning,
- ett steg ska lämna projektet i ett användbart tillstånd,
- orelaterade förändringar ska inte blandas,
- riskreducerande steg får prioriteras före funktionella steg,
- plan får revideras när ny evidens kräver det.

### Exit-kriterier
- nästa steg kan väljas entydigt,
- varje tidigt steg har verifierbara klart-kriterier,
- blockerare och beroenden är synliga,
- planen är tillräckligt detaljerad för stegvis execution.

## 12. Fas 9 – Implementation Loop

### Syfte
Genomföra planen kontrollerat.

### Canonical state machine
```text
READ → ASSESS → SELECT → LOCK → IMPLEMENT → VERIFY → REVIEW → UPDATE DOCS → UPDATE STATUS → PACKAGE / COMMIT → STOP
```

### READ
Läs `AGENTS.md`, `.system-builder/work-status.yaml` när den finns, aktuell plan, relevanta current-state-dokument, kod och tester.

### ASSESS
Kontrollera source drift, blockerare, plan/status-konflikter, tidigare verifieringsstatus och om rekommenderat steg fortfarande är säkert.

### SELECT + LOCK
Välj exakt ett steg och behandla det som `selected_step`.

### IMPLEMENT
Ändra endast vad steget och dess nödvändiga följdändringar kräver.

### VERIFY
Kör relevanta tester, build, lint, typecheck, schema validation, container build och annan projektspecifik verifiering.

### REVIEW
Kontrollera scope creep, regressioner, säkerhetsbaslinje, stale docs och klart-kriterier.

### UPDATE DOCS
Uppdatera endast dokument som faktiskt påverkas.

### UPDATE STATUS
Maskinläsbar status ska spegla verkligt utfall.

### PACKAGE / COMMIT
- ZIP-läge: komplett uppdaterad projekt-ZIP.
- GitHub-läge: commit/PR enligt aktiv arbetsserie.

### STOP
Starta inte nästa plansteg i samma normala körning.

### Loop-exit
Implementation loop är klar när alla steg i aktuell release/change är slutförda eller explicit borttagna, inga blockerare återstår för leveransen och required verification är genomförd.

## 13. Fas 10 – Packaging

### Syfte
Skapa det körbara eller distribuerbara resultat som deploymentmodellen kräver.

Exempel: binaries, application package, OCI/Docker image, frontend bundle, migrations och release artifacts.

### Exit-kriterier
- paketet kan byggas reproducerbart,
- paketeringens inputs är explicit konfigurerbara,
- artifacts har verifierats i relevant omfattning,
- deploymentprofilen och paketeringen är konsekventa.

## 14. Fas 11 – Deployment Readiness

### Syfte
Kontrollera att systemet faktiskt kan köras i avsedd miljö.

### Kontrollera minst när relevant
- environment variables,
- secrets,
- database connectivity,
- persistence,
- health checks,
- ports/network,
- TLS/reverse proxy ownership,
- migrations,
- startup/shutdown behavior,
- rollback prerequisites.

### Exit-kriterier
- målmiljön är explicit,
- externa beroenden är kända,
- systemet kan installeras utan dolda lokala antaganden,
- deployment blockers är lösta eller explicit dokumenterade.

## 15. Fas 12 – Acceptance + Release Readiness

### Syfte
Avgöra om systemet är redo att betraktas som färdigt för aktuell release.

### Bedöm minst
- must requirements,
- acceptance criteria,
- traceability completeness,
- architecture current,
- test status,
- security baseline,
- known limitations,
- packaging,
- deployment readiness,
- installation docs,
- operations docs.

### Viktig regel
Gröna tester är nödvändigt när relevanta men är inte ensamt bevis på release readiness.

### Exit-kriterier
- inga release-blockerare återstår,
- warnings och kända begränsningar är dokumenterade,
- aktuell release kan bedömas mot definierade success/acceptance criteria.

## 16. Fas 13 – Installation + Operations Documentation

### Syfte
Göra systemet installerbart och förvaltningsbart av någon som inte deltagit i utvecklingsdialogen.

Canonical artefakter när relevanta:
- `docs/configuration.md`
- `docs/installation.md`
- `docs/operations.md`

### Exit-kriterier
- installation kan följas från definierade prerequisites,
- konfiguration är dokumenterad,
- driftkritiska operationer är dokumenterade,
- backup/restore/upgrade/rollback-ansvar är tydligt i relevant omfattning.

## 17. Fas 14 – Release

### Syfte
Skapa en identifierbar leverans.

Kan omfatta version, release notes, git tag/release, container registry artifact, package artifact och migrationsinstruktioner.

### Exit-kriterier
- releaseartefakter motsvarar verifierad kod,
- version och dokumentation är konsekventa,
- kända begränsningar följer med leveransen.

## 18. Fas 15 – Operate / Maintain

### Syfte
Göra framtida drift och förändringar kontrollerbara.

System Builder ska stödja felsökning utifrån dokumenterade driftmönster, ändringsbegäran tillbaka in i CHANGE, uppgradering, rollback, dokumentationssynk och nya development plans utan att förlora historik.

Detta är systemets löpande förvaltningsfas och har inget slutligt exit-kriterium.

## 19. CREATE – normal väg

```text
Need → Discovery → Goals → Scope → Functional Specification → Risk/Feasibility → Architecture → Development Plan → Implementation Loop → Packaging → Deployment Readiness → Acceptance/Release Readiness → Installation/Operations Docs → Release → Maintain
```

CREATE får hoppa över tomma eller irrelevanta delmoment men inte hoppa över en kontroll som materiellt påverkar säker implementation eller release.

## 20. CHANGE – normal väg

```text
Change Request → Read Current System → Discovery/Clarify Change → Goals + Scope → Update Functional Specification as needed → Impact + Risk Analysis → Update Architecture as needed → Change/Development Plan → Implementation Loop → Update Current-State Docs → Packaging/Deployment checks as affected → Acceptance/Release Readiness → Release
```

CHANGE ska bevara historiken för större förändringar men integrera slutresultatet i current-state-dokumenten.

## 21. IMPROVE – normal väg

```text
Improvement Request → Analyze Relevant Current State → Define Technical Goal + Non-goals → Risk/Test Baseline → Improvement Plan → Implementation Loop → Verification → Update Architecture/Operations only if affected → Release Readiness as appropriate
```

IMPROVE får inte beskriva funktionell förändring som ren refaktorering.

## 22. Small-project fast path

För små, lågriskprojekt ska processen komprimeras utan att tappa kärnkontroller:

```text
Need → Compact Discovery + Goals + Scope → Compact Functional Specification → Compact Architecture + Deployment choice → Short Development Plan → Implementation Loop → Packaging + Verification → Compact Installation/Operations Docs → Release Readiness
```

Regler:
- samma canonical dokumentnamn kan användas men med kortare innehåll,
- risk/feasibility kan vara ett kort avsnitt i plan eller arkitektur,
- test strategy kan vara ett kort avsnitt i development plan om separat dokument inte tillför värde,
- ADR ska bara skapas för beslut som behöver historik,
- tomma placeholder-dokument ska undvikas.

## 23. Medium och large

### Medium
Normalt full kärnstruktur med separata functional specification, architecture, development plan, test strategy, deployment profile och installation/operations docs.

### Large / high risk
Utöka vid behov med fler explicita ADR, change impact-dokument, formellare spårbarhet, riskregister/spikes, fler verifieringsgatear och specialistgranskningar.

Mer dokumentation är endast motiverad när den reducerar risk eller förbättrar förvaltning.

## 24. Exit-kriterium för hela end-to-end-processen

En aktuell utvecklingsserie är färdig när:

- avsett beteende är dokumenterat,
- must-scope är implementerat eller explicit avgränsat,
- relevant arkitektur är aktuell,
- alla planerade steg för releasen är avslutade,
- relevant verifiering är genomförd,
- release blockers saknas,
- paketering och deploymentantaganden är explicita,
- installation och drift är dokumenterade i relevant omfattning,
- kända begränsningar är synliga,
- nästa framtida förändring kan starta från repositoryts faktiska state utan att förlita sig på konversationsminne.
