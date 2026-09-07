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
