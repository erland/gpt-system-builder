# Development Plan – CR-001

## DEV-001 – Add decrement behavior

### Objective
Implement FR-003 without changing FR-001 or FR-002.

### Scope
Add `decrement(value)` and its unit test.

### Prerequisites
- Baseline increment/reset tests pass.
- CR-001 impact analysis complete.
- Functional specification updated.

### Implementation / touched parts
- `src/counter_service/counter.py`
- `tests/test_counter.py`

### Verification
`python -m unittest discover -s tests -v`

### Done criteria
- AC-003 passes.
- Existing AC-001 and AC-002 continue to pass.

### Dependencies
None.

## DEV-002 – Final change acceptance review

### Objective
Confirm current-state docs, regression and release readiness for CR-001.

### Prerequisites
DEV-001 complete.

### Verification
Review functional spec and full test suite.

### Done criteria
Change is ready for acceptance.

### Dependencies
DEV-001.
