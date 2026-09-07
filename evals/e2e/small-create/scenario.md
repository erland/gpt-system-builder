# E2E Scenario – Small CREATE

Build **Tiny Status API**, a deliberately small Python 3.12+ HTTP service.

Must:
- `GET /health` → 200 + `{"status":"ok"}`
- `GET /message` → 200 + configurable message
- default message `Hello`
- no database
- local development target

Eval goal: blank idea → spec → architecture → plan → first implementation step → verification → resumable state.
