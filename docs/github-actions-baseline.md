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
