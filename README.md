# System Builder

System Builder är ett GPT-projekt för stegvis systemutveckling från behov eller förändringsönskemål till ett fungerande, verifierat, dokumenterat och paketerat system.

Projektet stödjer nya system och vidareutveckling av befintliga system samt arbetar i ZIP- och GitHub-läge.

## Projektstatus

Primär maskinläsbar status finns i `project-status.yaml`. Mänskligt läsbar status finns i `STATUS.md`.

## Utvecklingsplan

Se `docs/development-plan.md`.

## Aktuellt läge

SB-01–SB-42 är genomförda. Projektet är inne i en runtime-migrering mot GPT Byggaren 1.4.0.

Nästa rekommenderade steg är **SB-43 – Inför plattformsneutrala runtime-kontrakt**.

## Runtime-målbild

Aktiverade eller planerade runtime-distributioner:

- Chat ZIP
- Custom GPT
- Claude Projects
- OpenCode

OpenAI Plugin v1 är bedömd men inte planerad som distribution eftersom System Builders kritiska workspace/state- och repository-tool-flöden inte kan täckas med fullgod parity i nuvarande pluginmodell.

Se `docs/gpt-builder-1.4-runtime-migration.md` för migrationsanalysen.

Dessutom byggs en komplett projekt-ZIP efter varje genomfört utvecklingssteg.
