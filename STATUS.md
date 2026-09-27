# System Builder – Status

## Övergripande status
**CHANGE IN PROGRESS – SB-58 complete, SB-59 next**

## Senast slutförda steg
### SB-58 – GitHub Pages deployment profile

SB-58 är verifierad med full required CI för revision `8173a90224ced69e44763261cd1d81fcaf69ae15` och är completed.

System Builder har nu canonical deploymentprofilen `github-pages-static-pwa` för publika statiska browser-only appar som:

- byggs till statiska filer,
- inte kräver backend/server-side runtime,
- inte kräver server-side secrets/auth,
- får exponeras publikt.

Profilen ska inte väljas för intern/känslig information, backendberoende funktionalitet eller klientbundlade secrets. Om publik exponering är ett verkligt verksamhets-/säkerhetsval ska användaren tillfrågas.

Canonical deployment rules, CREATE-routing och runtimeprojektioner är uppdaterade. Custom GPT-instruktionen är fortsatt inom 8 000-teckensgränsen.

## Aktiv förändringsserie

Återstående:

- **SB-59** – static PWA/base-path/routing/service-worker configuration,
- **SB-60** – GitHub Pages workflow och regression coverage.

## Nästa åtgärd

Implementera SB-59 på samma PR.
