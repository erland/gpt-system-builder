# System Builder – Project CI

System Builder-projektets CI verifierar själva GPT-projektet och båda distributionerna.

## Required gate

På pull request och push till `main` körs:

1. state/schema validators,
2. canonical artifact validators,
3. fresh build av Chat ZIP,
4. fresh build av Custom GPT,
5. distributionsvalidators,
6. static instruction-adherence,
7. runtime parity,
8. E2E CREATE,
9. E2E CHANGE,
10. E2E Docker/Coolify,
11. repository hygiene.

## Fresh-build-regel

Parity och distributions-evals måste alltid använda ZIP-filer som byggts i samma CI-körning. Checked-in eller gamla `dist/`-artefakter får inte vara underlag för PASS.

## Permissions

Ordinarie CI använder `contents: read` och kräver inga release-secrets.

## No false pass

Live Coolify-verifiering får vara `pending` när ingen riktig målmiljö finns. Den får aldrig fabriceras som PASS.

## Release separation

PR-CI publicerar ingenting. Separat release-build definieras i SB-39.
