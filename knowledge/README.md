# System Builder Knowledge

Knowledge är referensmaterial som stödjer System Builder.

Kritiska runtime-regler finns i canonical instruktioner och `docs/`, inte enbart här.

## Klassificering

| File | Purpose | Use when | Class |
|---|---|---|---|
| `technology-patterns.md` | Kort teknisk referens | När implementation/arkitektur behöver generell vägledning | reference |
| `platform-reference.md` | Plattformssammanfattning | När GitHub/Docker/Coolify/PostgreSQL används | reference |
| `terminology.md` | Stabil terminologi | När begrepp behöver tolkas konsekvent | reference |

## Regler

- Knowledge är inte ensam källa för critical behavior.
- Tidskänsliga produkt-/plattformdetaljer ska verifieras när de används.
- Canonical docs uppdateras före Knowledge när regler förändras.
- Custom GPT får använda en kuraterad delmängd av Knowledge.
