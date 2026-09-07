# System Builder – Kravspårbarhet

## Syfte

`.system-builder/traceability.yaml` är den canonical maskinläsbara spårbarhetskällan mellan krav, acceptance criteria, development steps och verifiering.

Den kompletterar människolästa dokument men duplicerar inte kravtext.

## Huvudrelation

```text
FR/NFR
  ↓
AC
  ↓
DEV
  ↓
TEST
```

Relationerna får vara många-till-många där det behövs.

## Canonical regler

- Full kravtext finns i `docs/functional-specification.md`.
- `traceability.yaml` använder stabila ID:n och status.
- Krav som ska implementeras får normalt inte sakna development steps.
- `must`-krav får inte betraktas som verifierade utan verifieringsreferens.
- `verified` kräver att refererade verifieringar faktiskt har status `passed`.
- Referenser måste peka på existerande objekt.
- Krav↔development-step-relationer ska vara konsistenta i båda riktningarna när båda sektionerna används.
- `identified`, `deferred` och `cancelled` får sakna implementation eftersom de ännu inte ingår i aktiv leverans.

## Statusmodell för krav

- `identified`
- `specified`
- `planned`
- `in_progress`
- `implemented`
- `verified`
- `deferred`
- `cancelled`

## Prioritet

- `must`
- `should`
- `could`

`out of scope` ska normalt inte representeras som aktivt krav i traceability; det hör hemma i functional specification eller change request.

## Orphan requirements

Ett krav betraktas som orphan när det förväntas genomföras men saknar koppling till development step.

System Builder ska kunna flagga detta före release readiness.

## Release readiness

Minst följande ska kunna upptäckas maskinellt:

- `must`-krav som inte nått avsedd status,
- verifierade krav utan passerad verifiering,
- orphan requirements,
- referenser till saknade development steps, tests eller acceptance criteria.

## Small-project-regel

För små projekt kan `traceability.yaml` utelämnas om:

- kravmängden är liten,
- kopplingarna mellan krav, plansteg och verifiering är uppenbara,
- formell spårbarhet inte tillför reell nytta.

Om filen finns gäller dock kontraktet fullt ut.

## Validering

```bash
python scripts/validate_traceability.py \
  --file .system-builder/traceability.yaml \
  --schema schemas/traceability.schema.json
```

Negativ fixture:

```bash
python scripts/validate_traceability.py \
  --file examples/traceability.invalid.yaml \
  --schema schemas/traceability.schema.json \
  --expect-invalid
```
