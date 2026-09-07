# System Builder – Instruction-adherence evals

## Syfte

Instruction-adherence evals verifierar att både Chat ZIP och Custom GPT följer samma canonical behavior.

## Behavioral coverage

Sviten ska minst täcka:

- mode selection för CREATE/CHANGE/IMPROVE,
- ett steg per normal körning,
- source/state före chat memory,
- blocker/failure före nästa plansteg,
- REPAIR,
- ZIP complete-output,
- GitHub PR reuse,
- no-false-pass,
- release readiness,
- Docker/Coolify invariants,
- Knowledge som reference,
- proportionerliga frågor och complexity.

## Evalformat

Varje YAML-case har:

- `id`
- `title`
- `category`
- `severity`
- `prompt`
- `expected`
- `forbidden`

Ett live-case PASS:ar när expected behavior observeras och forbidden behavior uteblir.

## Static contract evals

Static evals kontrollerar att distributionsinstruktionerna faktiskt bär kärnkontraktet.

De använder **semantiska alternativgrupper**, inte exakt samma fras i båda distributionerna. Varje grupp innehåller flera formuleringar där minst en måste hittas.

Det förhindrar att komprimering till Custom GPT eller annan formulering i Chat ZIP skapar falska FAIL.

## Live evals

Static adherence ersätter inte live behavior-evals. Samma cases ska senare kunna köras mot faktisk runtime och bedömas med scorecard.

## Critical failures

Följande är release-blocking:

- flera development steps trots vanlig “Gör nästa steg”,
- false PASS,
- ignored blocker/failed verification,
- chat memory över faktisk source,
- partial ZIP som default,
- ny PR per DEV-step i samma work series,
- PostgreSQL inbyggd i canonical app image.

## Exit-kriterier

SB-33 är klart när:
- minst 15 behavioral cases finns,
- minst 7 critical cases finns,
- static evals kan köras mot båda distributioner,
- samma kärnkontrakt passerar i båda,
- live scorecard-format finns.
