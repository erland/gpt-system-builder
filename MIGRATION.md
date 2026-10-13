# Migrering till GPT Byggaren v1.6.21

Källa: System Builder 1.3.2.

- Canonical System Builder-instruktion bevaras oförändrad i `runtime/canonical-instructions.md` och speglas i `src/instructions/system.md`.
- Ursprunglig projektprofil sparas som `gpt-project.legacy.yaml`.
- Ny `gpt-project.yaml` använder GPT Byggarens build-schema.
- De fem nya distributionsmålen ersätter Custom GPT: Chat ZIP, Claude Project, Claude Skills, OpenCode och ChatGPT Plugin.
- Originalets egna filer, tester, schema och utvecklingsdokumentation bibehålls.
- Ny runtime kräver förmågekontroll: GitHub, körmiljö, beständig state och deployment är inte garanterade av enbart paketering.
- Ingen ändring har gjorts direkt i GitHub.

## CI reconciliation for v1.4.1

Distribution targets now come exclusively from `gpt-project.yaml#build_system.targets`: project, chat, claude_project, claude_skills, opencode, plugin. The version 2 registry is a checked mirror. `scripts/ci-migrated.sh` and GitHub Actions use the canonical `build_distributions.py` and `validate_distributions.py`; historical custom-GPT distribution code is retained only as migration evidence and is no longer invoked by CI/release. Local structural tests are not evidence of installed platform behavior.
