# System Builder – GitHub Pages static PWA profile

## Syfte

Profilen `github-pages-static-pwa` används för webbapplikationer som kan levereras som en ren statisk site och köras helt i webbläsaren utan egen backend/server-side runtime.

Målet är den enklaste rimliga deploymentformen för publika statiska PWA:er när repositoryt ligger på GitHub.

## När profilen passar

System Builder får härleda profilen när samtliga relevanta villkor är uppfyllda:

- applikationen byggs till statiska HTML/CSS/JS/assets,
- ingen backend eller server-side rendering krävs i drift,
- ingen server-side session state krävs,
- ingen runtime-secret får behöva bäddas in i klienten,
- klienten kan fungera med lokal browser-storage och/eller publika externa API:er,
- publik webbtillgänglighet är förenlig med funktionell scope och informationsklassning,
- GitHub används som source host eller deployment via GitHub är uttryckligen accepterad.

PWA är inte ett absolut krav; samma profil kan användas för annan ren statisk webbapp.

## När profilen inte ska väljas

Välj inte `github-pages-static-pwa` automatiskt när:

- applikationen kräver Java/Quarkus, Node-server, Python-backend eller annan server-side runtime,
- authentication kräver hemligheter eller server-side token exchange,
- klienten skulle behöva innehålla API-nycklar/secrets,
- data eller användningsfall är interna, känsliga eller inte får publiceras öppet,
- server-side access control är ett krav,
- backendpersistens är ett krav som inte kan ersättas av avsedd browser-local storage eller publik extern tjänst,
- deploymentkraven kräver privat nät, intern DNS eller andra miljöegenskaper som Pages inte erbjuder.

Om publikhetskravet är oklart och det är ett verkligt verksamhets-/säkerhetsval ska System Builder fråga användaren.

## Security och information exposure

GitHub Pages ska behandlas som publik webbpublicering som default.

System Builder ska därför:

- inte publicera intern/känslig information,
- inte bygga in secrets i frontend bundle,
- inte anta att privat repository innebär privat Pages-site,
- granska environment-variable-användning så att build-time variabler som hamnar i klientbundle är offentliga,
- dokumentera externa API:ers CORS/auth-behov när sådana används.

## Packaging

Release/deployment artifact är en statisk site bundle. Profilen förutsätter att hela deploybara resultatet kan serveras som statiska filer utan serverprocess.

Canonical build inputs är projektets source, lockfile och explicit build configuration.

Deploymentartifact ska verifieras genom minst:

- production build PASS,
- expected entry document finns,
- statiska assets refereras med korrekt public base path,
- inga secrets eller server-only artifacts ingår,
- PWA manifest/service worker valideras när PWA används.

## URL och base path

GitHub Pages kan publicera antingen under en root/custom domain eller under repository path.

System Builder ska därför behandla public base path som deploymentkonfiguration och inte anta `/`.

För project sites ska default normalt härledas som `/<repository-name>/`. För user/organization site eller verifierad custom domain kan root `/` vara korrekt.

För Vite-baserade appar ska `base` konfigureras från deploymentmålet. Typiskt används `/<repo-name>/` för project site och `/` för user/org site eller custom domain.

Byggverifiering ska kontrollera att genererad `index.html` och statiska assets använder paths som fungerar under vald Pages-base.

## Routing

GitHub Pages är statisk hosting. Server-side rewrite/routing får inte antas finnas.

För SPA måste routingstrategi vara explicit, exempelvis:

- hash routing,
- statiskt kompatibel fallback-strategi,
- eller annan verifierad lösning som fungerar med vald Pages-konfiguration.

System Builder ska inte generera deep links som kräver server-side rewrites utan att lösa deploymentkonsekvensen.

Hash routing är säker default när clean URLs inte är ett krav. History routing får bara användas tillsammans med en konkret statisk fallback/404-strategi som verifierats för projektet.

## PWA manifest och service worker

När appen är en PWA ska:

- `start_url` och `scope` ligga inom appens public base,
- icons och andra manifest-assets fungera under deployment-URL,
- service worker registreras under rätt base path och scope,
- precache/navigation fallback använda built asset paths,
- offline support bara utlovas när den faktiskt implementeras och verifieras.

För project site ska `start_url` och `scope` normalt använda repository-subpathen, inte root.

Om ett PWA-plugin genererar manifest/service worker ska System Builder verifiera plugin-konfigurationen i stället för att duplicera generated filer manuellt.

## Built artifact verification

För Pages/PWA ska production artifact minst verifieras för:

- `index.html` finns i output root,
- inga root-antaganden bryter repository-subpath deployment,
- manifestet refererar giltiga built assets,
- service worker kan registreras inom rätt scope,
- routingstrategin fungerar för vald URL-modell,
- appen kräver ingen server-side runtime efter build.

När en lokal statisk server finns tillgänglig bör built artifact testas under samma base path som Pages kommer använda.

## GitHub Actions

Deployment till Pages ska behandlas som separat deployment-side effect, inte vanlig PR-CI.

Det canonical workflowmönstret definieras i SB-60 och ska använda GitHub Pages-artifact/deploymentmekanism med minsta nödvändiga permissions.

## Custom domain

Custom domain är optional och ska bara konfigureras när användaren uttryckligen vill använda en domän eller projektkraven anger den.

TLS/DNS-verifiering får inte rapporteras som PASS utan faktisk evidens.

## Installation och operations

För en ren statisk Pages-site ska dokumentationen vara proportionell.

Relevant dokumentation omfattar normalt:

- build prerequisites,
- hur Pages deployment aktiveras/körs,
- public URL/base path,
- eventuell custom domain/DNS,
- cache/service-worker update behavior,
- rollback genom tidigare deployment/source revision,
- kända begränsningar för offline/local storage.

Serverdrift, process restart, databasbackup och container health ska inte fabriceras för en deployment som saknar dessa komponenter.

## Selection guide

- statisk publik PWA/webbapp utan backend + GitHub → `github-pages-static-pwa`
- statisk app men intern/känslig → välj annan privat hostinglösning
- backend/API krävs → välj container/service-profil
- server-side auth/secrets krävs → välj backend-capable profil
- deploymentmål uttryckligen annat → följ användarens val

## Anti-patterns

Undvik:

- GitHub Pages för backendberoende app,
- hemliga nycklar i frontend environment/build,
- antagande att Pages är privat,
- hårdkodad root path när repo-site använder subpath,
- service worker/manifest paths som bara fungerar lokalt,
- SPA-routing som förutsätter server rewrites,
- deployment från PR-CI med onödiga write permissions.
