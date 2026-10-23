# Browser Screenshot integration

## Syfte

Browser Screenshot är en **optional visual-evidence backend** för System Builder. Den används först när en körbar publik HTTP(S)-URL redan finns, exempelvis från PWA Preview, GitHub Pages eller annan verifierad deployment/preview.

Screenshot är visuell review-evidens. Den är inte ett funktionellt browser-test och får inte användas som ersättning för Playwright/E2E när sådana tester krävs.

## Live capability

Den aktuella Browser Screenshot-backenden stödjer:

- publik HTTP(S)-URL,
- preset: `desktop`, `tablet`, `mobile`,
- custom `width`/`height`,
- `deviceScaleFactor`,
- `fullPage`,
- timeout.

System Builder ska beskriva capability-semantik, inte hårdkoda en specifik MCP-implementation som enda möjliga backend.

## Standardval

Använd `desktop` som default.

Ta endast extra screenshots för:

- mobile/tablet när krav, risk eller användarens uttryckliga behov motiverar det,
- custom viewport när ett specifikt breakpoint/layoutproblem behöver verifieras,
- fullPage när helsidans visuella struktur faktiskt är relevant.

Undvik mekanisk screenshot-multiplicering.

## Förutsättningar

Screenshot får tas först när:

1. det finns en faktisk publik HTTP(S)-URL,
2. sidan är relevant för aktuellt steg,
3. screenshoten ger nytt visuell evidens och inte bara duplicerar annan verifiering.

Om URL saknas ska Browser Screenshot inte skapa en egen deployment. Använd PWA Preview eller annan befintlig preview/deployment-väg när det är relevant och tillgängligt.

## Evidence

Registrera minst:

- backend: `browser_screenshot`,
- URL,
- viewport/preset,
- fullPage,
- purpose,
- result,
- relation till aktuell source/artifact/preview när känd.

Screenshot-resultat kan stödja:

- visuell layout-review,
- responsive review,
- stakeholder/demo evidence,
- dokumenterad visuell smoke-check.

## Begränsning

En lyckad screenshot betyder endast att sidan kunde laddas tillräckligt för att en bild skapades.

Den bevisar inte automatiskt:

- att användarflöden fungerar,
- att knappar/formulär/API-anrop fungerar,
- att PWA offline/service worker fungerar,
- accessibility PASS,
- release readiness,
- production deployment correctness.

Funktionella browserkrav ska verifieras med faktisk browser/E2E-testning när det krävs.

## Relation till PWA Preview

Typiskt flöde för statisk webb/PWA:

1. build/test via GitHub Actions eller annan billigaste tillräckliga verifieringsväg,
2. optional preview via PWA Preview,
3. optional screenshot av preview-URL för visuell review.

Browser Screenshot ska inte i sig motivera Agent Workspace eller PWA Preview om en användbar publik URL redan finns.

## Fallback

Om Browser Screenshot saknas eller inte svarar:

- fortsätt utan screenshot när visual review är optional,
- behåll funktionell verifiering oförändrad,
- använd befintlig browser-test/e2e-evidens när sådan finns,
- rapportera visual evidence unavailable/deferred om den uttryckligen behövdes,
- rapportera aldrig screenshot som PASS om den inte skapades.

## Funktionell interaktion när live-pluginen stöder det

Utöver skärmbilder kan en ansluten Browser Screenshot-plugin exponera sessioner, navigering, semantisk sidstruktur, klick och textinmatning. Upptäck dessa capabilities vid körning; anta inte att alla installationer har dem.

När det finns stöd och en riktig HTTP(S)-URL ska System Builder för relevanta kritiska UI-flöden kunna:

1. Skapa en kortlivad webbläsarsession och navigera till exakt aktuell preview/deployment.
2. Läsa faktisk sidstruktur och kontrollera att avsedda element existerar.
3. Använda stabila ID- eller data-testid-selektorer när pluginens interaktioner kräver det.
4. Utföra verkliga klick och inmatningar, läsa observerade resultat och kontrollera explicita förväntningar.
5. Dokumentera vilka steg och assertioner som faktiskt kördes, samt stänga sessionen även vid fel.

En sådan kontroll får redovisas som **functional browser smoke PASS** enbart för de verifierade interaktionerna. Skärmbild utan interaktion är **visual-only**. Ett funktionellt smoke-test ersätter inte automatiskt projektets Playwright-regressionssvit, offline/service-worker-tester eller tester av icke observerade flöden. Om pluginen saknar browser-interaktion ska System Builder använda annan faktisk browser-runner eller klassificera kontrollen som unavailable/deferred enligt risk- och completion-reglerna.

Publicera aldrig hemligheter, intern data eller autentiserade testflöden på en oskyddad publik preview.
