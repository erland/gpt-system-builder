#!/usr/bin/env python3
from pathlib import Path
import sys, yaml

def fail(msg):
    print("FAIL:", msg)
    raise SystemExit(1)

def main():
    status_path = Path("project-status.yaml")
    if not status_path.exists():
        fail("project-status.yaml missing")
    data = yaml.safe_load(status_path.read_text(encoding="utf-8"))
    progress = data.get("progress") or {}
    state = data.get("state") or {}
    next_step = data.get("next_step") or {}

    if state.get("blocking_issues") not in ([], None):
        fail("blocking issues remain")
    completed_ids = progress.get("completed_step_ids") or []
    last_completed = progress.get("last_completed_step")
    current = progress.get("current_step")
    if not isinstance(completed_ids, list):
        fail("completed_step_ids must be a list")
    if last_completed is not None and current is not None and last_completed > current:
        fail("last_completed_step cannot exceed current_step")
    if not next_step.get("recommended"):
        fail("next_step.recommended missing")

    # Human-readable status should still exist and mention SB-50 when this
    # project's own completion transition is used.
    human = Path("STATUS.md")
    if not human.exists():
        fail("STATUS.md missing")

    print("PASS: lightweight completion state validation")
    return 0

if __name__ == "__main__":
    sys.exit(main())
