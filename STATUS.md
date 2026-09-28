# System Builder – Status

## Övergripande status
**CHANGE IN PROGRESS – SB-67**

## Ny förändringsserie

- **SB-67** – Playwright browser-test fallback för PWA/ZIP,
- **SB-68** – regression coverage.

## Aktivt steg

SB-67 gör browser-verifiering miljötolerant:

- saknad Chromium/WebKit/browser binary i aktuell ZIP/Chat-runtime klassificeras som environment-limited verification,
- all övrig möjlig verifiering körs,
- browserprov registreras som deferred och rapporteras aldrig som PASS utan faktisk körning,
- planen får fortsätta när ingen project failure observerats och riskklassningen tillåter det,
- GitHub-projekt använder normalt en Playwright CI-miljö vars version matchar projektets `@playwright/test`,
- browserprov som faktiskt körs och faller är fortsatt project failure,
- PWA-kritiska browserkontroller ska normalt ha faktisk PASS-evidens före release readiness.

Custom GPT-instruktionen är **7 968 tecken**.

## Nästa åtgärd

Verifiera SB-67 med full required CI.
