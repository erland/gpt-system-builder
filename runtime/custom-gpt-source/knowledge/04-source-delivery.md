# System Builder Knowledge Bundle

Class: reference

---

## Source: `docs/zip-mode.md`

# System Builder – ZIP-läge

## 1. Syfte

ZIP-läge används när användaren levererar ett helt eller delvis utvecklat system som ZIP och vill att System Builder ska analysera, planera, ändra eller fortsätta arbetet stegvis.

ZIP ska behandlas som ett first-class source mode, inte som ett tillfälligt filformat.

Målet är att varje levererad ZIP ska vara tillräckligt komplett för att arbetet ska kunna återupptas utan konversationsminne.

## 2. Grundprincip

> ZIP in → analysera faktisk source → genomför exakt ett säkert steg → verifiera → bygg komplett ny ZIP → stoppa.

System Builder ska inte arbeta från gamla extraherade filer om användaren har laddat upp en nyare ZIP.

## 3. ZIP som source of truth

När en aktuell ZIP är användarens källa gäller:

1. användarens aktuella instruktion,
2. innehållet i den aktuella ZIP:en,
3. `AGENTS.md`,
4. `.system-builder/work-status.yaml`,
5. aktiv plan/current-state-dokument,
6. kod/test,
7. generell System Builder Knowledge.

Chat history är sekundär.

## 4. Import

Vid import ska System Builder:

1. identifiera ZIP-filen,
2. verifiera att den går att läsa,
3. inspektera root shape,
4. extrahera säkert,
5. identifiera projektrot,
6. läsa canonical state om det finns,
7. bedöma om ZIP:en representerar CREATE, CHANGE, IMPROVE eller annan fas.

## 5. Säker extraktion

ZIP-extraktion ska skydda mot:

- `../` path traversal,
- absoluta paths,
- paths som lämnar projektroten,
- symlink-problem när runtime kan representera dem,
- orimligt stora eller uppenbart skadliga archives när relevant.

System Builder ska inte skriva filer utanför vald workspace-root.

## 6. Root-shape detection

ZIP kan exempelvis innehålla:

### Direkt projektrot

```text
README.md
src/
docs/
```

### Wrapper directory

```text
my-project/
  README.md
  src/
  docs/
```

System Builder ska identifiera projektroten utan att skapa dubbla wrappers i output.

Output-ZIP ska normalt representera projektets root direkt om projektets build/packaging-regler inte säger annat.

## 7. Repository state discovery

Efter extraktion ska System Builder söka efter:

- `AGENTS.md`
- `.system-builder/project.yaml`
- `.system-builder/work-status.yaml`
- `.system-builder/traceability.yaml`
- `.system-builder/deployment-profile.yaml`
- `docs/development-plan.md`
- `docs/functional-specification.md`
- `docs/architecture.md`
- build/test files
- `.gitignore`
- `.dockerignore`
- CI workflows.

Saknade state-filer är inte automatiskt fel; behovet styrs av projektets mognad och komplexitet.

## 8. Existing System Builder state

Om ZIP:en redan har `.system-builder/` ska den användas som machine state efter validering.

System Builder ska kontrollera:

- schema validity,
- selected step,
- blockers,
- verification,
- source drift,
- plan/state consistency.

Felaktigt state repareras från faktisk source och evidens.

## 9. ZIP utan System Builder state

Om ett befintligt system saknar state ska System Builder:

1. analysera faktisk source,
2. identifiera mode,
3. skapa minsta nödvändiga `.system-builder/` state,
4. inte fabricera completed history,
5. dokumentera vad som härletts.

För ett nytt projekt kan CREATE-state initieras.

## 10. Source drift mellan ZIP-versioner

Om användaren laddar upp en ny ZIP mellan körningar ska System Builder inte anta att den är identisk med föregående output.

Kontrollera när praktiskt:

- version,
- checksum,
- filskillnader,
- work status,
- selected step.

Om source har ändrats externt ska ASSESS avgöra om state/plan behöver repareras innan nästa steg.

## 11. Checksum

System Builder bör beräkna SHA-256 för levererad output-ZIP.

Checksum används som:

- artifact identity,
- felsökningshjälp,
- enkel driftindikator.

Checksum ersätter inte Git-history.

## 12. ZIP development loop

Normal ZIP-körning:

```text
RECEIVE ZIP
→ SAFE EXTRACT
→ READ STATE
→ ASSESS
→ SELECT ONE STEP
→ LOCK
→ IMPLEMENT
→ VERIFY
→ REVIEW
→ UPDATE DOCS/STATE
→ HYGIENE
→ BUILD COMPLETE ZIP
→ VERIFY ZIP
→ DELIVER
→ STOP
```

## 13. Ett steg per ZIP

Normalregel:

- en input-ZIP,
- ett completed development step,
- en output-ZIP.

Användaren kan uttryckligen be om flera steg, men System Builder ska då fortfarande hålla state och verifiering per steg.

## 14. Output completeness

Output-ZIP ska vara komplett för projektet.

Den får inte bara innehålla ändrade filer.

Den ska normalt innehålla:

- hela source tree,
- current-state docs,
- machine state,
- tests,
- scripts,
- configuration,
- build files,
- relevanta CI/deployment files.

## 15. Generated artifacts

Projektets egna genererade artefakter ska bara ligga i ZIP om projektets packaging-regler kräver det.

Typiskt ska följande exkluderas från source ZIP:

- `node_modules/`
- build cache,
- `.venv/`
- `target/`
- `dist/` när det endast är transient build output,
- OS/editor files,
- temporära testartefakter.

Repositoryts `.gitignore` och hygiene-policy ska styra.

## 16. ZIP filename

Output bör ha begripligt namn.

Exempel:

```text
my-system-project-v0.3.0-dev.zip
my-system-project-sb17.zip
```

System Builder ska inte förlita sig på filnamnet som enda versionskälla.

## 17. Version

Om projektet har canonical versionfil ska den respekteras.

Utvecklingssteg behöver inte automatiskt bumpa releaseversion.

För non-release artifacts får:

- dev,
- rc,
- step suffix

användas för tydlighet.

Releaseversion ska styras av projektets releasepolicy.

## 18. ZIP integrity verification

Innan leverans ska System Builder minst:

- öppna ZIP:en,
- testa CRC/integritet,
- kontrollera required files,
- säkerställa att projektroten är korrekt,
- kontrollera att output inte råkat packa sig själv.

## 19. Self-inclusion

Buildscript får inte inkludera output-ZIP inuti output-ZIP.

Exkludera:

- output path,
- generated distribution directory,
- temporära workspacefiler.

## 20. Project hygiene

Före ZIP-build:

- identifiera generated/temp files,
- ta bort endast hög-säkerhetsklassade skräpfiler,
- respektera canonical/history files,
- använd Git som historik när Git finns,
- dokumentera tveksamma findings hellre än att radera osäkert.

## 21. Required resume content

En System Builder-styrd ZIP ska normalt kunna återupptas med:

- project metadata,
- work status,
- development plan,
- relevant current-state docs,
- source,
- tests,
- build/validation scripts.

För small projects kan vissa artefakter saknas om de inte behövs.

## 22. Resume

När användaren återkommer med en output-ZIP och säger `"Gör nästa steg"`:

1. läs ZIP:ens state,
2. validera selected/completed/next,
3. kontrollera blockerare/drift,
4. följ next-step state machine,
5. genomför ett steg,
6. leverera ny ZIP.

System Builder ska inte kräva att användaren återberättar tidigare steg om ZIP-state är komplett.

## 23. ZIP + CHANGE

Vid CHANGE:

- läs current source,
- skapa/uppdatera CR/impact vid behov,
- uppdatera current-state docs,
- implementera ett change step,
- kör regression,
- leverera komplett ZIP.

## 24. ZIP + IMPROVE

Vid IMPROVE:

- etablera baseline,
- bevara behavior,
- implementera ett tekniskt step,
- regression,
- komplett ZIP.

## 25. ZIP + CREATE

Vid CREATE kan första implementationsteget skapa hela projektstrukturen från canonical plan.

Efter första implementationsteget ska projektet levereras som komplett ZIP och därefter fortsätta som normalt ZIP-resume.

## 26. Validation scripts

När projektet innehåller scripts för:

- schema validation,
- build,
- lint,
- tests,
- packaging,

ska System Builder använda dem före egna ad-hoc-alternativ när de är relevanta och säkra.

## 27. Unknown tooling

Om ZIP innehåller okänd stack:

- läs README/build files,
- identifiera package manager/build system,
- använd projektets egna kommandon,
- undvik att introducera ny tooling utan behov.

## 28. Binary files

System Builder ska bevara binära projektfiler som inte behöver ändras.

Den ska inte konvertera eller regenerera binärer utan skäl.

## 29. Secrets

ZIP-output får inte inkludera:

- credentials,
- riktiga `.env` secrets,
- private keys,
- tokens,

om de inte redan är explicit avsedda som test fixtures och säkert identifierade.

Om secrets upptäcks ska de behandlas som security issue.

## 30. Large archives

För stora projekt ska System Builder:

- analysera selektivt,
- undvika att läsa alla filer om det inte behövs,
- fokusera på state, plan, relevanta källfiler och tests,
- fortfarande leverera komplett ZIP.

## 31. ZIP diff summary

Efter completed step bör leveransen sammanfatta:

- completed step,
- huvudsakliga ändringar,
- verification,
- artifact checksum,
- next recommended step.

Full diff behöver inte återges i chatten.

## 32. Failure outcome

Om steget inte kan completed:

- state ska visa failure/blocker,
- ZIP får ändå levereras om den behövs för resume,
- den får inte beskrivas som completed artifact,
- nästa recommended ska vara repair/unblock.

## 33. Partial output

System Builder ska inte leverera en partial source ZIP som ser ut som fullständig projektleverans.

Om endast patch/diff efterfrågas explicit kan det göras, men default är komplett project ZIP.

## 34. Artifact naming vs project naming

Outputfilens namn får förändras utan att projektets interna namn ändras.

Interna canonical identifiers ska inte automatiskt härledas från artifact filename.

## 35. ZIP mode anti-patterns

Undvik:

- endast skicka ändrade filer,
- förlita sig på chat history,
- packa `node_modules`,
- packa tidigare ZIP i ny ZIP,
- glömma work status,
- skriva utanför workspace,
- markera step completed utan verification,
- börja nästa steg före leverans.

## 36. Exit-kriterier för SB-20

SB-20 är klart när:

- ZIP import/safe extraction definierats,
- root detection definierats,
- state discovery/resume definierats,
- source drift mellan ZIP-versioner definierats,
- one-step loop definierats,
- complete output ZIP definierats,
- hygiene/exclusions definierats,
- integrity/checksum definierats,
- failure/repair artifact-regler definierats.

---

## Source: `docs/github-mode.md`

# System Builder – GitHub-läge

## 1. Syfte

GitHub-läge används när användaren vill att System Builder ska arbeta direkt mot ett GitHub-repository i stället för att leverera ZIP efter varje steg.

GitHub ska behandlas som ett first-class source mode med:

- repository som source of truth,
- branch/PR som aktiv work series,
- commits som verifierade steg,
- CI som viktig evidens,
- machine state i repositoryt,
- resume utan beroende av chat history.

## 2. Grundprincip

> Läs aktuell repository state → återanvänd rätt branch/PR → genomför exakt ett säkert steg → verifiera → commit/push → uppdatera PR/state → stoppa.

System Builder ska inte skapa ny branch eller PR slentrianmässigt om en aktiv work series redan finns.

## 3. Source of truth

I GitHub-läge gäller normalt:

1. användarens aktuella uttryckliga instruktion,
2. aktuell branch/PR i repositoryt,
3. `AGENTS.md`,
4. `.system-builder/work-status.yaml`,
5. aktiv development plan,
6. current-state docs,
7. code/tests,
8. CI-status,
9. generell System Builder Knowledge.

Chat history är sekundär.

## 4. Repository discovery

Vid första kontakt med ett repository ska System Builder identifiera:

- default branch,
- aktiv branch om användaren anger en,
- öppna PRs som kan tillhöra samma work series,
- `AGENTS.md`,
- `.system-builder/`,
- development plan,
- functional specification,
- architecture,
- CI workflows,
- build/test tooling,
- release conventions.

## 5. Repository cleanliness

Före mutation ska System Builder bedöma:

- finns osynkade work-state-filer?
- finns en aktiv selected step?
- finns conflicting PR?
- har default branch förändrats?
- finns failing CI på baseline?
- finns source drift sedan senaste state?

Repositoryt får inte behandlas som statiskt mellan körningar.

## 6. Work series

En work series är ett sammanhängande CREATE-, CHANGE- eller IMPROVE-arbete.

Exempel:

```text
CHANGE CR-014
branch: system-builder/cr-014-repository-visibility
PR: #42
```

Alla plansteg för samma change bör normalt ligga i samma branch/PR tills serien är klar.

## 7. Branch strategy

Default:

```text
system-builder/<mode-or-id>-<short-slug>
```

Exempel:

- `system-builder/create-initial`
- `system-builder/cr-014-repository-visibility`
- `system-builder/improve-github-adapter`

Använd repositoryts befintliga branch policy om den finns.

System Builder ska inte skapa ny branch om:

- aktiv work series redan har branch,
- användaren uttryckligen anger branch,
- repository workflow kräver annan strategi.

## 8. PR strategy

Normalregel:

> En PR per sammanhängande work series, inte en PR per DEV-step.

Skapa ny PR när:

- ingen relevant aktiv PR finns,
- användaren vill separera arbetet,
- tidigare PR är merged/closed,
- ny work series har annan scope.

Återanvänd befintlig PR när:

- samma change/improve/create series fortsätter,
- branch och scope fortfarande är giltiga.

## 9. Commit strategy

Normalregel:

- ett completed DEV-step → en tydlig commit,
- commit efter required verification,
- commit message refererar step-ID när relevant.

Exempel:

```text
DEV-014: add repository visibility support
```

Små mekaniska följdändringar inom samma steg hör i samma commit om repository policy inte säger annat.

## 10. Commit completion rule

Ett steg ska normalt inte commit:as som completed om required verification misslyckas.

Undantag:

- explicit checkpoint/WIP om användaren ber om det,
- blockerande state behöver bevaras för samarbete.

Då ska commit/PR inte beskriva steget som completed.

## 11. PR description

PR-beskrivningen ska kunna sammanfatta:

- work series,
- mål/scope,
- completed steps,
- aktuellt selected/next step,
- verification,
- blockers,
- known limitations.

PR-beskrivningen får inte ersätta repositoryts canonical work status.

## 12. Machine state

GitHub-läge ska hålla `.system-builder/work-status.yaml` i repositoryt när System Builder state används.

Den bör kunna representera:

- source mode: github,
- repository,
- base branch,
- work branch,
- PR number/URL när relevant,
- mode,
- active work series,
- selected step,
- completed steps,
- blockers,
- verification,
- next recommended.

Detaljer i schema kan utökas senare utan att ändra principen.

## 13. Resume

När användaren senare säger `"Gör nästa steg"` ska System Builder kunna:

1. läsa repository,
2. hitta aktiv branch/PR från state,
3. kontrollera att PR fortfarande är open och branch finns,
4. kontrollera drift/CI,
5. fortsätta selected step eller välja nästa säkra steg,
6. commit/push,
7. uppdatera state/PR,
8. stoppa.

Chatten ska inte vara enda platsen som berättar vilken PR som är aktiv.

## 14. Pull before work

Före implementation ska aktuell remote state läsas.

Om branch ligger efter base eller har nya commits från annan aktör ska System Builder bedöma påverkan innan ändring.

## 15. Source drift

GitHub source drift kan vara:

- nya commits på work branch,
- base branch har mergats framåt,
- PR har ändrats,
- CI-resultat har förändrats,
- användaren har manuellt ändrat state/docs.

Vid drift:

1. läs förändringarna,
2. bedöm plan/state impact,
3. reparera vid behov,
4. fortsätt först när current state är förstådd.

## 16. Base branch drift

System Builder ska inte automatiskt rebase/merge base branch i work branch om repository policy eller change risk gör detta osäkert.

När base drift påverkar aktuell change:

- bedöm konflikter,
- följ repositoryts normala merge/rebase-policy,
- verifiera igen efter integration.

## 17. Merge conflicts

Vid konflikt:

- identifiera semantic conflict, inte bara text conflict,
- bevara current intended behavior,
- uppdatera docs/state,
- kör relevant regression.

Konfliktlösning är del av aktiv work series om den krävs för completion.

## 18. CI as evidence

CI är viktig verifiering men inte enda release evidence.

System Builder ska skilja:

- local/tool verification,
- pushed commit verification,
- CI status.

Ett steg kan behöva CI pass innan det betraktas som completed om repositoryts policy kräver det.

## 19. Failing baseline CI

Om default branch redan har failing CI:

- dokumentera baseline,
- avgör om felet är relevant för aktuellt steg,
- undvik att tillskriva gammalt fel nya changes,
- blockera om failure gör säker verifiering omöjlig.

## 20. New CI failure

Om aktuell commit introducerar failing required CI:

- steget är inte completed,
- repair prioriteras,
- nästa numeriska DEV-step ska inte starta.

## 21. Review feedback

När PR-review tillkommer ska System Builder behandla relevant feedback som del av work series.

Feedback kan:

- kräva repair av current step,
- skapa nytt DEV-step,
- justera plan,
- identifiera blockerare.

System Builder ska inte ignorera review bara för att local tests är gröna.

## 22. One-step GitHub loop

Normal körning:

```text
READ REPO/PR
→ ASSESS
→ SELECT ONE STEP
→ LOCK IN STATE
→ IMPLEMENT
→ VERIFY
→ REVIEW
→ UPDATE DOCS/STATE
→ COMMIT
→ PUSH
→ CHECK/RECORD CI
→ UPDATE PR
→ STOP
```

## 23. CREATE on GitHub

För nytt system kan System Builder:

1. skapa initial branch/repository structure när repository redan finns,
2. etablera state/docs,
3. skapa första PR/work series,
4. fortsätta stegvis i samma PR tills initial release scope är klar.

Om användaren vill skapa ett helt nytt GitHub-repository krävs att tillgänglig GitHub-integration stödjer den åtgärden.

## 24. CHANGE on GitHub

CHANGE ska normalt:

- använda CR/change-ID i branch eller state,
- samla samma change i en PR,
- uppdatera current-state docs,
- inkludera regression evidence,
- behålla historical change records när relevant.

## 25. IMPROVE on GitHub

IMPROVE ska normalt:

- ha tekniskt sammanhängande PR-scope,
- inte blanda ny funktion,
- bevara behavior,
- hålla baseline/verification synligt.

## 26. PR reuse rules

Återanvänd PR om alla är sanna:

- PR är open,
- work branch finns,
- samma work series,
- scope är fortfarande sammanhängande,
- ingen repository policy kräver ny PR.

Skapa ny PR om:

- tidigare PR merged,
- tidigare PR closed/abandoned,
- work series byter scope,
- användaren begär separation.

## 27. Merged PR

När PR är merged ska work series normalt:

- markeras completed/released beroende på fas,
- active PR tas bort från state,
- nästa nya change få ny branch/PR.

Fortsätt inte pusha till merged PR-branch som om den fortfarande var aktiv.

## 28. Closed unmerged PR

Closed/unmerged PR ska behandlas som explicit avbruten eller pausad tills annat beslutas.

System Builder ska inte automatiskt återöppna eller skapa ny PR utan att bedöma användarens intention och repository state.

## 29. Direct-to-default-branch

Default är PR-baserat arbete för icke-triviala changes.

Direkt commit till default branch får användas när:

- användaren uttryckligen begär det,
- repository policy tillåter det,
- risken är låg,
- ingen PR-review krävs.

## 30. Branch protection

Om branch protection kräver PR/review/checks ska System Builder följa den.

Den ska inte försöka kringgå repository controls.

## 31. GitHub permissions

Använd minsta nödvändiga GitHub-behörighet.

System Builder ska inte:

- ändra repository settings utan behov,
- bredda token permissions,
- force-pusha utan uttrycklig och säker anledning,
- skriva secrets i commits/PR.

## 32. Force push

Undvik force push som default.

Tillåt endast när:

- repository workflow kräver rebase/rewritten history,
- work branch är kontrollerad,
- ingen annans arbete riskerar att förloras,
- användaren/policy stödjer det.

## 33. Commit message quality

Commit ska vara:

- kort,
- handlingsorienterad,
- kopplad till steg/scope.

Exempel:

```text
DEV-021: add GitHub mode contract
```

Undvik generiska:

```text
updates
fix stuff
changes
```

## 34. PR title

PR-titel ska beskriva work series, inte senaste mekaniska delsteget.

Exempel:

```text
CR-014: Add repository visibility selection
```

snarare än:

```text
DEV-004 update UI selector
```

## 35. PR status summary

Efter varje steg kan PR-beskrivningen uppdateras med:

```text
Completed:
- DEV-003
- DEV-004

Current:
- none

Next:
- DEV-005

Verification:
- API tests pass
- frontend build pass
```

Repository work status är fortfarande canonical machine state.

## 36. Issues

GitHub issue kan användas som input/context om användaren anger det eller repository workflow använder issues.

Issue ska inte automatiskt bli source of truth framför canonical spec/state.

## 37. Releases

GitHub Release hör till RELEASE-läge.

Work PR ska inte betraktas som release bara för att den är merge-ready.

## 38. Tags

Release tag ska representera verifierad release, inte varje development step.

## 39. Repository hygiene

GitHub-läge ska också kontrollera:

- `.gitignore`,
- generated files,
- committed secrets,
- stale artifacts,
- CI workflow health.

Detaljer formaliseras i nästa hygiene-/CI-steg.

## 40. No GitHub access fallback

Om GitHub-verktyg inte är tillgängliga ska System Builder inte låtsas ha pushat/öppnat PR.

Den får:

- arbeta i ZIP-läge,
- producera patch/project ZIP,
- dokumentera avsedd branch/PR-plan.

## 41. User-supplied PR

Om användaren anger en specifik PR ska System Builder använda den som primär kandidat för aktiv work series, efter att ha verifierat att den matchar repository och scope.

## 42. Multiple candidate PRs

Om flera öppna PRs verkar matcha samma work series:

- analysera branch, title, state och commits,
- välj inte godtyckligt,
- om det inte går att avgöra säkert kan detta bli en genuin blockerande fråga.

## 43. GitHub mode anti-patterns

Undvik:

- ny PR per DEV-step,
- ny branch trots aktiv work series,
- commit före required verification,
- push utan att läsa senaste remote,
- ignorera review/CI,
- force push som default,
- merge utan release/readiness när sådan krävs,
- hålla aktiv PR endast i chat memory.

## 44. Exit-kriterier för SB-21

SB-21 är klart när:

- repository discovery definierats,
- branch/PR/work-series-regler definierats,
- commit strategy definierats,
- state/resume definierats,
- CI/review/drift definierats,
- PR reuse/merge/close-regler definierats,
- permissions/force-push-regler definierats,
- one-step GitHub loop definierats,
- fallback utan GitHub access definierats.

---

## Source: `docs/repository-hygiene.md`

# System Builder – Repository hygiene och ignore-policy

## 1. Syfte

System Builder ska hålla repositoryn rena, reproducerbara och begripliga utan att radera filer på osäker grund.

Repository hygiene ska:

- skilja canonical source från generated artifacts,
- förhindra att temporära filer commit:as,
- minska risk för secrets och lokala miljöfiler i Git,
- stödja reproducerbara builds,
- bevara legitim historik,
- göra ZIP- och GitHub-leveranser konsekventa.

## 2. Grundprincip

> Radera automatiskt bara när klassificeringen är säker. Vid tveksamhet: dokumentera fyndet, inte filen.

Git är historik. Repositoryt ska inte behålla kopior av gamla filer bara för att "vara säker" om Git redan bevarar historiken.

## 3. Filklasser

Varje relevant fil/folder ska kunna klassificeras som:

### CANONICAL

Källa till current state eller projektkontrakt.

Exempel:
- source code,
- `docs/functional-specification.md`,
- `docs/architecture.md`,
- `docs/development-plan.md`,
- `.system-builder/*.yaml`,
- schemas,
- build scripts.

Ska normalt behållas och versioneras.

### RUNTIME

Filer som krävs för att projektet ska kunna köras eller distribueras.

Exempel:
- Dockerfile,
- compose files,
- manifests,
- runtime config templates,
- migrations.

Ska normalt versioneras.

### DEVELOPMENT

Utvecklingsstöd som behövs för build/test/quality.

Exempel:
- tests,
- lint config,
- CI workflows,
- dev scripts,
- fixtures.

Ska normalt versioneras.

### GENERATED

Kan återskapas från canonical source.

Exempel:
- `dist/`,
- `build/`,
- `target/`,
- generated reports,
- compiled bundles.

Ska normalt inte versioneras om projektet inte uttryckligen kräver checked-in artifacts.

### TEMPORARY

Lokala/intermediära filer utan långsiktigt värde.

Exempel:
- cache,
- temp folders,
- editor swap files,
- OS metadata,
- test leftovers.

Ska ignoreras/rensas.

### HISTORICAL

Legitim besluts-/förändringshistorik.

Exempel:
- ADR,
- change requests,
- product decisions,
- migration history när den är canonical.

Ska inte raderas som "stale docs" bara för att de är gamla.

## 4. High-confidence auto-delete

System Builder får automatiskt ta bort typiska temporära/genererade filer när det är hög säkerhet att de kan återskapas.

Exempel:

- `.DS_Store`
- `Thumbs.db`
- `*.swp`
- `*.tmp`
- Python `__pycache__/`
- `.pytest_cache/`
- Node cache
- transient `coverage/`
- lokala build outputs som tydligt är generated
- tidigare output-ZIP i source tree

Förutsättning:
- filen är inte canonical enligt projektets policy,
- build/release kräver inte checked-in output.

## 5. Low-confidence findings

Radera inte automatiskt när det är oklart om filen:

- är handredigerad,
- krävs av deployment,
- används av externa system,
- är generated men avsiktligt versionerad,
- är historisk dokumentation,
- innehåller migrations-/seed-data.

Markera i hygiene report.

## 6. `.gitignore`

Alla nya Git-baserade projekt ska normalt ha `.gitignore`.

Den ska anpassas till faktisk stack och bara ignorera det som verkligen är lokalt/generated.

Gemensam baseline kan inkludera:

```gitignore
# OS
.DS_Store
Thumbs.db

# Editors
.idea/
.vscode/*
!.vscode/extensions.json
!.vscode/settings.json

# Environment / secrets
.env
.env.*
!.env.example

# Logs / temp
*.log
*.tmp
*.swp

# Python
__pycache__/
*.py[cod]
.pytest_cache/
.venv/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
pnpm-debug.log*

# Java
target/
*.class

# Build outputs
dist/
build/
coverage/

# System Builder delivery
*.zip
```

Baseline ska reduceras/anpassas om den skulle ignorera canonical filer.

## 7. `.env`-regel

Verkliga `.env`-filer ska normalt ignoreras.

Tillåtet:

- `.env.example`
- `.env.template`

Dessa får innehålla variabelnamn och säkra exempelvärden, men inga riktiga secrets.

## 8. `.dockerignore`

Containerprojekt ska normalt ha `.dockerignore`.

Syfte:

- mindre build context,
- inga secrets i build context,
- inga lokala caches,
- inga onödiga artifacts.

Baseline:

```dockerignore
.git
.gitignore
node_modules
target
dist
build
coverage
.env
.env.*
*.log
*.tmp
*.zip
```

Men:
- exkludera inte filer som Docker-build faktiskt behöver,
- `.env.example` kan behöva vara kvar om dokumentation/build kräver den.

## 9. Docker build context

System Builder ska bedöma Docker context mot Dockerfile.

En aggressiv `.dockerignore` som gör image build omöjlig är ett fel.

Efter ändring av `.dockerignore` ska container build verifieras när Docker finns i projektets required verification.

## 10. Secrets hygiene

Repository hygiene ska flagga:

- `.env` med verkliga värden,
- private keys,
- tokens,
- credential JSON,
- cloud service account files,
- hardcoded passwords.

System Builder ska inte skriva ut secretvärden i rapporten.

Om secret har commit:ats kan borttagning från working tree vara otillräcklig; historikrotation/revoke kan behövas och ska behandlas som security issue.

## 11. Generated reports

Generated documentation/report output ska normalt ligga under tydlig generated directory, exempel:

```text
dist/
reports/generated/
artifacts/
```

Om output är en releaseartefakt ska den byggas i releaseflödet, inte nödvändigtvis commit:as.

## 12. Build artifacts

Exempel:

- Java `target/`
- React/Vite `dist/`
- Python wheel/build
- compiled binaries

ska normalt:
- ignoreras,
- byggas i CI/release,
- inte ligga i project ZIP source delivery om de inte uttryckligen behövs.

## 13. Dependency directories

Versionera normalt inte:

- `node_modules/`
- `.venv/`
- Maven/Gradle caches
- package manager caches.

Versionera lockfiles när stackens normala praxis använder dem.

## 14. Lockfiles

Lockfiles är normalt DEVELOPMENT/CANONICAL dependency state, inte generated trash.

Exempel:
- `package-lock.json`
- `pnpm-lock.yaml`
- `yarn.lock`
- `poetry.lock`

De ska normalt behållas när projektet använder dem.

## 15. IDE configuration

IDE-filer bedöms selektivt.

Ignorera normalt personliga:
- workspace metadata,
- local history,
- caches.

Versionera vid behov gemensamma:
- formatting settings,
- recommended extensions,
- code style.

## 16. Test artifacts

Ignorera normalt:
- screenshots från failed local test,
- temp databases,
- coverage output,
- browser cache.

Behåll canonical fixtures/snapshots som tester faktiskt behöver.

## 17. Database files

Lokala SQLite/testdatabaser ska normalt ignoreras om de är runtime artifacts.

Canonical migrations/seed scripts ska versioneras.

## 18. Logs

Applikationsloggar ska inte commit:as.

Om exempel-logg behövs för dokumentation ska den vara explicit fixture/sample och sanerad.

## 19. Archive files

Input/output-ZIP och tarballs ska normalt ignoreras från source repository om de är generated delivery artifacts.

Undantag:
- canonical test fixture,
- distribution source som projektet explicit versionerar.

## 20. Historical files

System Builder ska inte skapa:
- `old/`
- `backup/`
- `previous-version/`
- `final-final/`

för att bevara tidigare source.

Git används som historik.

Legitim historik som ADR/CR ska däremot bevaras.

## 21. Stale duplicate docs

Om två dokument verkar beskriva samma current state:

1. identifiera canonical källa,
2. verifiera om den andra är historical/reference,
3. merge/flytta/radera bara vid hög säkerhet,
4. uppdatera länkar.

## 22. Naming hygiene

Undvik:
- `final.md`
- `final2.md`
- `new-version.md`
- `copy.md`

Använd stabila canonical namn och Git history.

## 23. Root hygiene

Projektroten bör innehålla bara tydliga top-level artifacts.

Exempel:

```text
README.md
AGENTS.md
docs/
src/
tests/
scripts/
schemas/
.github/
.system-builder/
Dockerfile
compose.yaml
```

Undvik oklassificerade tempfiler i root.

## 24. Hygiene pass

Ett hygiene pass ska minst kontrollera:

- ignored/generated content,
- temp files,
- duplicate archives,
- secrets candidates,
- stale output,
- unexpected root files,
- missing `.gitignore`,
- missing `.dockerignore` för containerprojekt,
- checked-in dependency folders.

## 25. Hygiene severity

### PASS

Inga relevanta findings.

### WARNING

Fynd finns men blockerar inte step/release.

Exempel:
- gammal generated report,
- onödig IDE-fil.

### BLOCKED

Hygiene-fynd innebär säkerhets- eller leveransrisk.

Exempel:
- committed secret,
- output ZIP packas in i sig själv,
- Docker context inkluderar secret,
- required source ignoreras.

## 26. Pre-step hygiene

Före implementation behövs inte full cleanup varje gång.

Men System Builder ska upptäcka hygiene-problem som påverkar steget.

## 27. Post-step hygiene

Efter completed step:

- kontrollera nya generated/temp files,
- säkerställ att artifacts inte råkat hamna i source tree,
- uppdatera ignore-regler om nya verktyg introducerats.

## 28. Release hygiene

Före release ska full hygiene gate köras.

Kontrollera särskilt:

- secrets,
- temp/generated files,
- stale distributions,
- version consistency,
- docs state,
- reproducibility,
- artifact exclusions.

## 29. ZIP-mode hygiene

Före project ZIP:

- exkludera generated/temp enligt policy,
- inkludera canonical/history/runtime/development,
- inkludera inte tidigare project ZIP,
- verifiera required files.

## 30. GitHub-mode hygiene

Före commit:

- `git status`/diff-review,
- inga secrets,
- inga generated artifacts utan policy,
- endast relevant scope,
- ignore files uppdaterade vid behov.

## 31. Project-specific policy

Om repository redan har dokumenterad policy för generated files/IDE/config ska den gälla före generisk baseline.

System Builder ska inte ersätta etablerad praxis utan skäl.

## 32. Ignore-file generation

När `.gitignore` saknas får System Builder skapa en baserat på upptäckt stack.

När den finns:
- mergea försiktigt,
- bevara projektunika entries,
- undvik att skriva över hela filen mekaniskt.

Samma gäller `.dockerignore`.

## 33. Verification after ignore changes

Efter `.gitignore`-ändring:
- säkerställ att required canonical files inte ignoreras.

Efter `.dockerignore`-ändring:
- bygg container om det är relevant.

## 34. Hygiene report

När explicit rapport behövs kan den innehålla:

```text
PASS:
- node_modules ignored

WARNING:
- old generated coverage report tracked

BLOCKED:
- .env.production contains credentials
```

Rapportera path och kategori, inte secretvärde.

## 35. Auto-clean rules

Auto-clean får ske när alla är sanna:

- filen är tydligt TEMPORARY/GENERATED,
- den är reproducerbar eller meningslös,
- den är inte required runtime/development/history,
- ingen repository policy säger annat.

## 36. Never auto-delete

Radera aldrig automatiskt vid osäkerhet:

- migrations,
- user data,
- keys/certs,
- unknown binary,
- historical decision records,
- legal/license files,
- deployment manifests.

## 37. License files

`LICENSE`, notices och tredjepartslicensfiler är inte hygiene clutter.

De ska bevaras.

## 38. README och docs

README ska vara aktuell men behöver inte duplicera all dokumentation.

Hygiene betyder inte att allt ska pressas in i en fil.

## 39. `.gitignore` och project ZIP

`.gitignore` styr Git men är också en viktig signal för ZIP packaging.

ZIP build script får ha explicit policy som avviker från `.gitignore` när det finns skäl, men skillnaden ska vara medveten.

## 40. `.dockerignore` och secrets

En secret som är ignorerad av Git kan fortfarande skickas till Docker daemon om `.dockerignore` saknar den.

Därför ska `.env`/secret candidates hanteras i båda när Docker används.

## 41. Monorepo

I monorepo kan ignore-policy vara:
- root-level,
- package-level.

System Builder ska följa befintlig struktur och inte duplicera ignore-filer utan behov.

## 42. Generated source code

Generated source kan vara specialfall.

Om build kräver generated source checked-in ska projektpolicy dokumentera det.

System Builder ska inte anta att all generated code kan raderas.

## 43. Hygiene anti-patterns

Undvik:

- radera okända filer automatiskt,
- ignorera hela `docs/`,
- ignorera lockfiles,
- lägga credentials i `.gitignore` och tro att problemet är löst om de redan är commit:ade,
- commit:a `node_modules`,
- behålla gamla ZIP-kopior i repo,
- skapa backup folders i stället för Git history.

## 44. Exit-kriterier för SB-22

SB-22 är klart när:

- filklassificering definierats,
- high/low-confidence cleanup definierats,
- `.gitignore` baseline definierats,
- `.dockerignore` baseline definierats,
- secrets/archives/generated handling definierats,
- ZIP/GitHub/release hygiene gates definierats,
- merge-safe ignore generation definierats,
- validator/scanner finns.

---

## Source: `docs/github-actions-baseline.md`

# System Builder – GitHub Actions-baslinje

## 1. Syfte

System Builder ska kunna etablera en enkel, säker och relevant GitHub Actions-baslinje för projekt som använder GitHub.

Baslinjen ska ge reproducerbar verifiering av de kontroller som faktiskt krävs för projektet, exempelvis build, test, lint, typecheck, schema validation och packaging checks. Målet är inte maximal CI-komplexitet utan minsta pipeline som ger tillräcklig evidens.

## 2. Grundprincip

> CI ska automatisera projektets verkliga verifieringskontrakt, inte introducera en separat uppsättning regler.

Kommandon i CI ska så långt möjligt vara samma som utvecklare och System Builder kör lokalt.

## 3. När CI ska etableras

För GitHub-baserade projekt ska CI normalt skapas när projektet innehåller kod, build/test är del av done criteria, PR används för leverans, release byggs från GitHub eller schema/contract validation är viktig. För rena dokumentprojekt kan en enklare validation workflow räcka.

## 4. Standardtriggers

Normal baseline är `pull_request` och `push` mot explicit default branch. Undvik push på alla branches utan behov. PR kan vara primär gate och default branch verifieras efter merge.

## 5. Workflow separation

Föredra få tydliga workflows, typiskt `ci.yml` och senare `release.yml`. CI verifierar source och PR. Release/deployment-side effects ska normalt inte ligga i vanlig PR-CI.

## 6. Job design

Små projekt kan ha ett `validate`-jobb. Större projekt kan dela backend, frontend, integration, container eller security endast när det förbättrar feedbacktid, parallellism, felsökning eller isolation.

## 7. Required checks

CI ska härledas från test strategy och development contract. React/TypeScript använder typiskt locked install, lint, typecheck, tests och build. Java/Maven använder setup Java och `verify`. Python använder canonical dependency install och projektets validators/tests.

## 8. Lockfile enforcement

CI ska använda projektets låsta dependency state, exempelvis `npm ci`, `pnpm install --frozen-lockfile`, wrapper-baserad Maven/Gradle och canonical Python dependency setup. CI ska inte tyst uppdatera lockfiles.

## 9. Runtime versions

Java-, Node-, Python- och package-manager-versioner ska vara explicita eller härledas från canonical project configuration. Undvik flytande `latest` när reproducerbarhet är viktig.

## 10. Caching

Caching får användas när det minskar CI-tid och cache key kopplas till dependency state. Cache får inte ersätta korrekt installation eller skapa dold state.

## 11. Permissions

Vanlig CI ska använda minsta permissions, normalt `contents: read`. Lägg bara till write/id-token permissions när ett specifikt jobb behöver dem.

## 12. Secrets och fork PRs

Grund-CI bör vara secret-free. Secret-dependent integration tests ska separeras eller skyddas så att fork PRs inte får otillåten access. Secrets ska ligga i GitHub Secrets/environments och aldrig i workflow YAML eller logs.

## 13. Third-party actions

Använd etablerade actions med explicit version/pinning enligt projektpolicy. Undvik okända actions med breda permissions och actions för triviala shellkommandon.

## 14. CI/local parity

Komplex verifieringslogik ska helst ligga i repository scripts. Exempel: `./scripts/ci.sh`, `./mvnw verify`, `pnpm ci`. Workflow YAML ska vara tunn orchestration.

## 15. Required kontra optional checks

Markera vilka checks som är required. Required CI-failure blockerar completion. Informational checks som coverage trend får vara non-blocking om projektet beslutat det.

## 16. Baseline failure

Om CI är röd före ändringen ska baseline dokumenteras. Ett gammalt fel får inte tillskrivas ny kod, men det kan blockera om säker verifiering annars inte är möjlig.

## 17. Nytt CI-fel

Om aktuell ändring orsakar required failure gäller:

```text
CI FAIL
→ active step remains incomplete
→ repair becomes next action
→ do not continue to next DEV-step
```

## 18. Database och integration

Använd service container, Testcontainers eller relevant testmiljö. PostgreSQL-specifikt beteende ska vid behov verifieras mot PostgreSQL, inte ersättas av en annan databas av bekvämlighet.

## 19. Container verification

Om Docker är del av delivery contract bör CI kunna verifiera image build och vid relevant risk startup/health. Detta kan ligga i eget jobb.

## 20. Schema och dokumentkontrakt

CI ska köra canonical validators från repositoryt. Regler ska inte dupliceras i workflow YAML. Dokumentvalidering används bara när ett faktiskt strukturellt kontrakt finns.

## 21. Security i CI

Dependency audit, secret scanning eller SAST kan ingå när projektets risk kräver det. CI-baslinjen ersätter inte specialistgranskning.

## 22. Artifacts och coverage

Ladda upp artifacts endast när de behövs för felsökning eller release. Coverage är observability och ska inte få en generell 100 %-gate.

## 23. Concurrency, timeout och paths filters

Concurrency kan avbryta stale runs när det är lämpligt. Jobs bör ha rimliga timeouts. `paths` filters används endast när det är säkert att förändringar verkligen inte påverkar checks.

## 24. Matrix och monorepo

Matrix används endast för verkligt stödda runtime-/OS-/DB-varianter. Monorepo får använda affected-package-logik men cross-cutting checks får inte tappas bort.

## 25. Stabil naming

Workflow-, job- och checknamn ska vara stabila eftersom branch protection kan referera till dem.

## 26. Runners

GitHub-hosted runner är rimlig default när kraven tillåter det. Self-hosted används bara när intern åtkomst, specialhårdvara eller policy kräver det.

## 27. Generated files

Om generated files medvetet versioneras ska CI kunna verifiera att regeneration inte skapar diff. Annars ska generated output normalt inte commit:as.

## 28. CREATE / CHANGE / IMPROVE

CREATE etablerar CI tidigt när skeleton och verifieringskommandon finns. CHANGE uppdaterar CI om nya runtime/test/migration targets introduceras. IMPROVE får förbättra CI men inte sänka required verification utan explicit beslut.

## 29. Release separation

Release workflow definieras separat. PR-CI ska normalt inte skapa GitHub Release, deploya production eller bumpa releaseversion.

## 30. Baseline workflow

En generell baseline innehåller explicit trigger, `contents: read`, checkout, explicit runtime setup, canonical verify command och timeout.

## 31. Workflow validation

Efter att CI skapas ska System Builder minst verifiera YAML parse, triggers, least-privilege permissions, expected commands och paths. När GitHub finns tillgängligt används verkligt workflow-resultat också som evidens.

## 32. Anti-patterns

Undvik `permissions: write-all`, secrets i workflow YAML, `curl | sh` utan starkt skäl, duplicerad testlogik, release side effects i PR-CI, matrix explosion, osäkra path filters, flytande runtimes utan policy och completion trots röd required CI.

## 33. Exit-kriterier för SB-23

SB-23 är klart när trigger-policy, required/optional checks, runtime/lockfile/caching, permissions/secrets/fork-regler, CI/local parity, failure/blocker-regler, CREATE/CHANGE/IMPROVE-regler samt baseline workflow template och validator finns.
