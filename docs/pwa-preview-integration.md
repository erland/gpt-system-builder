# PWA Preview integration

## Syfte

PWA Preview är en **optional preview/review backend** för System Builder. Den används för att göra en redan byggd statisk webbartifact eller PWA tillgänglig via en temporär HTTPS-URL för review, visuell kontroll eller vidare handoff.

PWA Preview är inte en build backend, inte en ersättning för funktionella browser-test och inte produktionsdeployment.

## Applicerbarhet

Använd endast när artifacten är statisk och självständig nog att serveras som preview, exempelvis:

- statisk webbapp,
- byggd React/Vite-app,
- PWA,
- annan frontend-output utan required server-side runtime.

Använd inte PWA Preview som normal väg för:

- backend/API-tjänster,
- system som kräver server-side sessions,
- runtime-secrets som inte kan exponeras i klienten,
- databeroende serverfunktionalitet,
- känslig/intern data när publik temporär preview inte är lämplig.

## Source contract

Live PWA Preview tar en HTTPS-URL till en komprimerad statisk artifact:

- ZIP, eller
- tar.gz.

System Builder ska därför först ha en faktisk byggd artifact och en HTTPS source URL.

Möjliga source-vägar:

- befintlig HTTPS artifact URL,
- signed temporary artifact URL från Agent Workspace när build-artifact faktiskt behövs,
- annan säker HTTPS artifact source som användaren/projektet redan har.

Starta inte Agent Workspace enbart för att skapa en preview om en billigare eller redan existerande artifact URL finns. I GitHub source mode ska GitHub Actions fortsatt användas för build/test när den räcker; Agent Workspace används endast när artifact-handoff eller annan required capability motiverar extra execution-kostnad.

## Artifact gate

Skapa preview först när den artifact som ska visas har relevant build/verifieringsevidens.

Preview av en artifact bevisar endast att PWA Preview kunde packa upp och servera den. Status `READY` betyder inte automatiskt:

- funktionella browser-test PASS,
- offline/PWA behavior PASS,
- accessibility PASS,
- deployment readiness,
- release readiness,
- production deployment PASS.

## Preview lifecycle

Live backend stöder:

- create från HTTPS source URL,
- list/get,
- update av en befintlig preview med ny source URL och samma preview URL,
- extend av TTL,
- delete.

Regler:

1. använd kortast praktiska lifetime inom live-backendens tillåtna intervall, för närvarande 5–1440 minuter,
2. återanvänd/update samma preview för samma work series när stabil URL är värdefull,
3. extend endast när review faktiskt behöver mer tid,
4. delete när preview inte längre behövs och explicit cleanup är praktiskt,
5. låt annars hostens TTL städa upp temporär preview.

## Evidence

Registrera preview som separat review/deployment-like evidence med minst:

- backend: `pwa_preview`,
- source artifact identity eller checksum,
- preview id,
- preview URL,
- status,
- expiry,
- purpose.

Preview-evidence får aldrig ersätta required build/test/browser evidence.

## Handoff från Agent Workspace

När Agent Workspace har producerat en relevant statisk artifact och live capabilities erbjuder signed HTTPS download link:

1. build artifact endast om den behövs,
2. skapa kortlivad signed download link,
3. skicka länken direkt till PWA Preview,
4. skapa eller uppdatera preview,
5. destruera Agent Workspace efter handoff,
6. behåll endast preview metadata/evidens.

Detta är en artifact-handoff, inte skäl att använda Agent Workspace när GitHub Actions eller annan source redan ger en användbar artifact URL.

## Fallback

Om PWA Preview saknas eller inte svarar:

- fortsätt utan preview när preview är optional,
- behåll build/test-verifiering oförändrad,
- använd annan befintlig deployment/preview-väg om projektet redan har en,
- rapportera preview som unavailable/deferred när den faktiskt krävdes för review,
- rapportera aldrig preview som PASS om den inte skapades.
