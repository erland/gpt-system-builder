# System Builder

System Builder är ett GPT-projekt för stegvis systemutveckling från behov eller förändringsönskemål till ett fungerande, verifierat, dokumenterat, paketerat och releaseklart system.

Projektet stödjer CREATE, CHANGE och IMPROVE och arbetar i både ZIP- och GitHub-läge.

## Projektstatus

Maskinläsbar status finns i `project-status.yaml`. Mänskligt läsbar status finns i `STATUS.md`.

Utvecklingsplan: `docs/development-plan.md`.

## Runtime-distributioner

Fem aktiva runtime-distributioner byggs från samma canonical kontrakt:

- **Chat ZIP**
- **Custom GPT**
- **Claude Projects** – explicit reduced parity
- **OpenCode**
- **OpenAI Plugin** – skills-first och host-dependent/reduced parity

Plugin-distributionen bevarar canonical System Builder-beteende men förutsätter att hosten tillhandahåller nödvändiga capabilities, bland annat filesystem read/write, code execution, persistent workspace/state och GitHub/repository-stöd när GitHub source mode används. Saknas en required capability ska operationen blockeras eller degraderas ärligt; verifiering får aldrig simuleras.

## Centrala arbetssätt

System Builder:

- använder faktisk source/state före chat memory,
- genomför normalt ett verifierbart utvecklingssteg per körning,
- skiljer governing intent från implementation progress,
- gör final documentation reconciliation före release readiness,
- verifierar tekniskt möjliga gates automatiskt även i ZIP-läge,
- stödjer Docker, Coolify, generiska containerplattformar, Kubernetes och GitHub Pages för lämpliga statiska appar/PWA,
- bygger och validerar alla aktiva runtime-distributioner från canonical source.

## GitHub Pages

För publika statiska browser-only appar utan backend/server-side secrets kan System Builder använda profilen `github-pages-static-pwa`.

Profilen omfattar bland annat repository-subpath/public base, Vite/PWA paths, service-worker scope, routingstrategi samt separat Pages-deployment från vanlig PR-CI.

Se `docs/github-pages-profile.md`.

## Build och verifiering

Lokal full CI:

```bash
bash scripts/ci-project.sh
```

Bygg alla distributioner:

```bash
python3 scripts/build_all_distributions.py --output-dir dist --version dev
python3 scripts/validate_all_distributions.py --manifest dist/distribution-build-manifest.json
```

## Dokumentation

README är projektets översikt. Detaljer finns i canonical dokumentation, bland annat:

- `docs/canonical-scope.md`
- `docs/architecture-standard.md`
- `docs/functional-specification-standard.md`
- `docs/deployment-packaging-patterns.md`
- `docs/configuration-installation-operations-standard.md`
- `docs/release-readiness-standard.md`
- `docs/readme-current-state-standard.md`

## Release

Git-taggen är canonical versionskälla för System Builders releaseartefakter. Exempelvis ger taggen `v1.3.0` artifactversion `1.3.0`.

Release-workflowet kör full CI, bygger och validerar alla fem runtime-distributionerna, kör instruction-adherence/runtime-parity och skapar checksummor samt release metadata.

En release innehåller:

- `system-builder-chat-<version>.zip`
- `system-builder-custom-gpt-<version>.zip`
- `system-builder-claude-projects-<version>.zip`
- `system-builder-opencode-<version>.zip`
- `system-builder-plugin-<version>.zip`
- `SHA256SUMS.txt`
- `release-metadata.yaml`
- `distribution-build-manifest.json`

Aktuell canonical version finns i `VERSION`.
