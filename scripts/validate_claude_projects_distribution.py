#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import zipfile

CORE_MARKERS = [
    "## 3. One-step rule",
    "actual current source and repository/project state",
    "Never report an unrun check as PASS",
    "ZIP is a first-class source/delivery mode",
    "GitHub is a first-class source mode",
]

REQUIRED = {
    "README.md",
    "project-instructions.md",
    "runtime-contract.json",
    "compatibility.md",
    "knowledge/README.md",
    "knowledge/technology-patterns.md",
    "knowledge/platform-reference.md",
    "knowledge/terminology.md",
}

FORBIDDEN_PREFIXES = (
    ".system-builder/",
    "evals/",
    "tests/",
    "scripts/",
    ".github/",
)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("zipfile")
    args = ap.parse_args()
    errors = []

    with zipfile.ZipFile(args.zipfile, "r") as zf:
        bad = zf.testzip()
        if bad:
            errors.append(f"corrupt member: {bad}")

        names = set(zf.namelist())
        for req in sorted(REQUIRED):
            if req not in names:
                errors.append(f"missing {req}")

        for name in names:
            if name.startswith(FORBIDDEN_PREFIXES):
                errors.append(f"development-only file leaked into Claude distribution: {name}")

        if "project-instructions.md" in names:
            text = zf.read("project-instructions.md").decode("utf-8")
            for marker in CORE_MARKERS:
                if marker not in text:
                    errors.append(f"missing canonical behavior marker: {marker}")

        if "runtime-contract.json" in names:
            contract = json.loads(zf.read("runtime-contract.json").decode("utf-8"))
            cfg = contract.get("runtime_compatibility", {}).get("claude_projects", {})
            if cfg.get("status") != "implemented":
                errors.append("Claude Projects status must be implemented")
            if cfg.get("target") != "reduced":
                errors.append("Claude Projects target must be reduced")
            state = contract.get("workspace_state", {}).get("state", {})
            if state.get("authority") != "workspace_file":
                errors.append("workspace-file state authority must be preserved")

        if "compatibility.md" in names:
            compat = zf.read("compatibility.md").decode("utf-8").lower()
            for phrase in ["reduced parity", "must not assume", "unrun verification"]:
                if phrase not in compat:
                    errors.append(f"compatibility limitation missing: {phrase}")

    if errors:
        print("FAIL")
        for error in errors:
            print("-", error)
        return 1

    print("PASS: Claude Projects distribution valid with explicit reduced parity")
    return 0

if __name__ == "__main__":
    sys.exit(main())
