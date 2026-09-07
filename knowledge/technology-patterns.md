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
