# System Builder – Status

## Övergripande status
**CHANGE IN PROGRESS – SB-58**

## Ny förändringsserie

GitHub Pages-stöd för statiska PWA/webbappar:

- **SB-58** – canonical GitHub Pages deployment profile,
- **SB-59** – static PWA/base-path/routing/service-worker configuration,
- **SB-60** – GitHub Pages Actions workflow och regression coverage.

## Aktivt steg

SB-58 implementerar profilen `github-pages-static-pwa`.

Profilen ska väljas när applikationen är en publik statisk browser-only app utan backend/server-side secrets. Den ska inte väljas för intern/känslig information, server-side auth, backendberoende funktionalitet eller klientbundlade secrets.

Canonical deployment rules, CREATE routing och runtime projections uppdateras i detta steg.

## Nästa åtgärd

Verifiera SB-58 med full required CI. Därefter är SB-59 nästa steg.
