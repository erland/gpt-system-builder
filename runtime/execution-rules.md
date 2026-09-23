# System Builder – Deterministic execution rules

## 1. Syfte

Detta är en kort first-hop decision procedure för nästa säkra exekveringsåtgärd. Använd den före längre resonemang när work-status och faktisk source är tillgängliga.

## 2. Grundregel

Läs först faktisk source/repository/ZIP och validera att machine state fortfarande stämmer.

Om `.system-builder/work-status.yaml` innehåller `execution.next_action`, använd det som en stark hint — men bara om det inte motsägs av aktuell source, blockerare eller verification evidence.

## 3. SELECT decision table

Utvärdera i denna ordning och välj första matchande rad:

| Villkor | Nästa åtgärd |
| --- | --- |
| Aktiv blockerare finns | `unblock` |
| Required verification har FAIL/BLOCKED | `repair` |
| Source/state drift eller inkonsistens finns | `repair` |
| Aktivt selected/in-progress steg finns och implementation är inte färdig | `implement` |
| Aktivt steg är implementerat men required verification saknas/pending | `verify` eller `await_verification` |
| Required verification PASS för oförändrad implementation revision och completion återstår | `complete` |
| Dependency saknas för nästa plansteg | slutför dependency/unblock |
| Inga aktiva problem och ett säkert plansteg återstår | `implement` första säkra incomplete steg |
| Inga development steps återstår | `release` / readiness |
| Ingen säker åtgärd kan härledas | `assess` och stoppa före mutation |

Använd aldrig bara `current + 1`.

## 4. GitHub action transitions

### IMPLEMENT

```text
READ CURRENT PR/BRANCH
→ IMPLEMENT ONE STEP
→ LOCAL VERIFY
→ COMMIT IMPLEMENTATION
→ PUSH
→ if remote CI required: STOP with await_verification
```

### VERIFY / REPAIR

```text
CI pending → await_verification
CI failed → repair same active step
CI passed → complete
```

### COMPLETE

```text
NO IMPLEMENTATION CHANGE
→ bind PASS to verified implementation SHA
→ mark step completed
→ calculate next
→ completion-only commit
→ lightweight completion validation
→ STOP
```

Om completion-committen innehåller verifieringsrelevant source är den inte completion-only och full verification krävs igen.

## 5. ZIP action transitions

### IMPLEMENT

```text
READ ZIP/STATE
→ IMPLEMENT ONE STEP
→ FULL REQUIRED VERIFY
```

### COMPLETE

Om all required verification kan köras och PASS:
```text
completion transition
→ lightweight state validation
→ package complete ZIP
→ verify ZIP
→ STOP
```

Om extern required verification saknas:
```text
keep incomplete
→ record pending verification
→ package resumable checkpoint
→ STOP
```

## 6. Backward compatibility

Äldre work-status utan `execution` eller `completion` är giltig. Härled nästa åtgärd med decision table ovan. Kräv inte migration bara för att hints saknas.

## 7. Safety override

Hints är inte source of truth framför faktisk evidens. Om `execution.next_action` säger `implement` men CI har FAIL, blockerare finns eller source drift upptäcks ska den hint ignoreras och state repareras.

## 8. Stop rule

Efter en completed development step eller en explicit repair/unblock-action: rapportera outcome och nästa rekommenderade åtgärd, sedan stoppa. Starta inte nästa development step automatiskt.
