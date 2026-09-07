# Development Plan – Tiny Status API

## DEV-001 – Establish service skeleton and response logic

### Objective
Create project skeleton and testable response logic.

### Scope
Package, response functions, unit tests, README.

### Prerequisites
Functional specification and architecture complete.

### Implementation / touched parts
`src/tiny_status/app.py`, `tests/test_app.py`, `README.md`.

### Verification
`python -m unittest discover -s tests -v`

### Done criteria
AC-001, AC-002 and AC-003 pass.

### Dependencies
None.

## DEV-002 – Add HTTP adapter

### Objective
Expose verified response logic over HTTP.

### Scope
HTTP handler and local smoke test.

### Prerequisites
DEV-001 complete.

### Verification
Unit tests plus local HTTP smoke test.

### Done criteria
Both endpoints work over HTTP.

### Dependencies
DEV-001.
