# E2E Scenario – CHANGE on existing system

Existing system: **Counter Service**.

Current behavior:
- `increment(value)` adds 1.
- `reset()` returns 0.
- unit tests are green.

Requested CHANGE:
- add a new `decrement(value)` operation that subtracts 1,
- preserve existing increment/reset behavior,
- update current-state functional specification,
- record change history,
- create a change plan,
- implement exactly one DEV step and stop.

Eval goal:
baseline → change request → impact analysis → current-state spec update → plan → one implementation step → regression → state → complete ZIP.
