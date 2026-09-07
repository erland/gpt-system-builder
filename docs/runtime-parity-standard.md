# System Builder – Runtime parity

Chat ZIP och Custom GPT är två distributionsformer av samma System Builder. De får skilja i komprimering och Knowledge-paketering, men inte i kärnbeteende.

Core parity omfattar: CREATE/CHANGE/IMPROVE, ett steg per nästa-steg-körning, source/state före chat memory, blocker/failure/REPAIR, no-false-pass, komplett ZIP, GitHub PR-reuse, CREATE/CHANGE/IMPROVE-semantik, Docker/Coolify/PostgreSQL-regler, operations docs, release readiness, Knowledge-gräns och fråga-endast-vid-verkligt-beslut.

Båda distributionsmanifesten ska dessutom uttrycka samma behavior contract:
- one completed step per run default
- source state over chat memory
- critical behavior not Knowledge-only
- false pass forbidden
- ZIP mode
- GitHub mode

Parity bedöms semantiskt med alternativgrupper, inte exakt textmatchning. Alla definierade parity-dimensioner ska passera innan SB-37 markeras klar.
