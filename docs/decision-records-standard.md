# System Builder – ADR och produktbeslut

## Syfte
System Builder skiljer mellan current-state-dokument och historiska beslut. `architecture.md` och `functional-specification.md` beskriver aktuellt läge; ADR och produktbeslut bevarar rationale och historik.

## Architecture Decision Records
Skapa ADR för betydande arkitekturval som påverkar struktur, dataägarskap, säkerhet, integrationer, deployment eller viktiga trade-offs.

Skapa normalt inte ADR för triviala dependency-versioner, lokala refaktoreringar eller rena kodstilsval.

### Format
Varje ADR ska innehålla:
- ID och titel
- status
- datum
- context
- decision
- alternatives considered
- rationale
- consequences
- references
- supersedes / superseded by

Status: `Proposed`, `Accepted`, `Superseded`, `Rejected`.

Filnamn: `docs/architecture-decisions/ADR-001-<slug>.md`.

När ett accepterat ADR påverkar current state ska `docs/architecture.md` uppdateras. Ett superseded ADR ska bevaras och länka till ersättande ADR.

## Produktbeslut
`docs/product-decisions.md` används för viktiga funktionella eller produktmässiga beslut som behöver historik men inte är arkitekturbeslut.

Exempel:
- varför en funktion exkluderas från MVP,
- varför en viss roll krävs,
- varför ett användarflöde förenklas.

Varje produktbeslut ska normalt innehålla:
- ID (`PD-001`)
- status
- datum
- context
- decision
- rationale
- consequences
- affected requirements/use cases
- supersedes / superseded by

## CHANGE-regel
Vid större CHANGE:
1. change request beskriver behovet,
2. impact analysis beskriver påverkan,
3. ADR/produktbeslut bevarar viktiga vägval,
4. current-state spec/architecture uppdateras till det nya läget.

Historiska artefakter får aldrig bli den enda platsen där current state framgår.

## Small-project-regel
Skapa decision records selektivt. Små projekt behöver inte ADR eller produktbeslut för triviala implementation details.

## Exit-kriterier
- ADR-kontrakt definierat
- produktbeslutskontrakt definierat
- current-state/history-separation explicit
- superseded-regler definierade
- mallar och exempel finns
- strukturell validering finns
