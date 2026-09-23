# System Builder

System Builder är ett GPT-projekt för stegvis systemutveckling från behov eller förändringsönskemål till ett fungerande, verifierat, dokumenterat och paketerat system.

Projektet stödjer nya system och vidareutveckling av befintliga system samt arbetar i ZIP- och GitHub-läge.

## Projektstatus

Primär maskinläsbar status finns i `project-status.yaml`. Mänskligt läsbar status finns i `STATUS.md`.

## Utvecklingsplan

Se `docs/development-plan.md`.

## Aktuellt läge

SB-01–SB-49 är genomförda. **SB-50** implementerar en completion transition som undviker onödig full CI efter ren statusändring, med bakåtkompatibilitet för äldre System Builder-projekt. SB-50 väntar på full required CI innan steget får klarmarkeras.

Nuvarande version är fortsatt **1.0.0-rc.2** tills nästa releasebeslut tas.

## Runtime-målbild

Fyra runtime-distributioner byggs från samma canonical kontrakt:

- **Chat ZIP** – full chat-distribution.
- **Custom GPT** – motsvarande beteende inom Custom GPT-plattformens begränsningar.
- **Claude Projects** – reduced parity; canonical behavior bevaras men lokal exekvering, workspace-mutation och GitHub-write kan inte antas.
- **OpenCode** – peer runtime med root `AGENTS.md`, explicit `projectRoot`, runtime-contract snapshot och approval för muterande operationer.

OpenAI Plugin v1 är bedömd men inte aktiverad eftersom System Builders kritiska workspace/state- och repository-tool-flöden inte når tillräcklig parity i den modellen.

Se `docs/gpt-builder-1.4-runtime-migration.md` för migrationsanalysen.

## Build och verifiering

`runtime/distribution-registry.yaml` är det gemensamma registret för aktiverade runtimes.

Lokal full CI:

```bash
bash scripts/ci-project.sh
```

Bygg alla distributioner:

```bash
python3 scripts/build_all_distributions.py --output-dir dist --version dev
python3 scripts/validate_all_distributions.py --manifest dist/distribution-build-manifest.json
```

## Release

Git-taggen styr versionsnumret. Aktuell kandidat är `v1.0.0-rc.2`. Releasebygget kör full CI, bygger och validerar alla fyra runtime-distributionerna, kör instruction adherence och runtime parity och skapar checksummor samt release metadata.

En release innehåller:

- `system-builder-chat-<version>.zip`
- `system-builder-custom-gpt-<version>.zip`
- `system-builder-claude-projects-<version>.zip`
- `system-builder-opencode-<version>.zip`
- `SHA256SUMS.txt`
- `release-metadata.yaml`
- `distribution-build-manifest.json`

Dessutom byggs en komplett projekt-ZIP efter genomförda utvecklingssteg när ZIP-leverans används.
