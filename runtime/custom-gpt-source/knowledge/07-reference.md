# System Builder Knowledge Bundle

Class: reference

---

## Source: `knowledge/technology-patterns.md`

# Technology Patterns

Class: reference

Generella utgångspunkter:

- föredra enkel arkitektur före distribuerad komplexitet,
- modular monolith är ofta ett bra default för små/medelstora system,
- använd external PostgreSQL för relationsdata när SQL-transaktioner behövs,
- håll web/API-services stateless där praktiskt,
- använd Docker/OCI som packaging när målmiljön är containerbaserad,
- använd characterization tests före riskfylld legacy-refaktorering,
- använd spike/PoC när teknisk osäkerhet är större än implementationen.

Detta är referensvägledning. Canonical beslut styrs av `docs/architecture-standard.md`, `docs/risk-feasibility-standard.md` och deploymentstandarderna.

---

## Source: `knowledge/platform-reference.md`

# Platform Reference

Class: reference

## GitHub

Repository, branch, pull request, commit och CI används som delivery state när GitHub-läge är valt. Canonical regler finns i `docs/github-mode.md`.

## Docker

Docker/OCI används som packagingform. Canonical regler finns i `docs/docker-baseline.md`.

## Coolify

Coolify kan köra app containers och separata databastjänster. Canonical målprofil finns i `docs/coolify-profile.md`. Produktdetaljer som kan ändras över tid ska verifieras mot aktuell dokumentation.

## PostgreSQL

Relationsdatabas körs normalt separat från app image. Migrations hör till applikationens releasecontract.

## Generic container platform

Anta inte plattformsspecifika capabilities utan verifiering. Beskriv image, config, secrets, health, persistence och rollout explicit.

---

## Source: `knowledge/terminology.md`

# Terminology

Class: reference

- **current-state document** – dokument som beskriver nuvarande avsett system.
- **work series** – sammanhängande CREATE-, CHANGE- eller IMPROVE-arbete.
- **selected step** – det DEV-step som är låst för aktuell körning.
- **blocker** – förhållande som gör fortsatt arbete osäkert eller omöjligt.
- **completion evidence** – verifierbart underlag som visar att ett steg är klart.
- **acceptance** – bedömning av systemets beteende mot krav/acceptance criteria.
- **release readiness** – helhetsbedömning om en version kan släppas.
- **packaging** – hur en körbar leverans byggs.
- **deployment** – hur leveransen placeras och körs i målmiljö.
- **reference knowledge** – stödmaterial som inte ensamt styr critical runtime behavior.
