#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "runtime" / "distribution-registry.yaml"
PROJECT = ROOT / "gpt-project.yaml"
CONTRACT = ROOT / "runtime" / "runtime-contract.json"

def main() -> int:
    errors = []
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    project = yaml.safe_load(PROJECT.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    active = registry.get("active_targets", [])
    if len(active) != len(set(active)):
        errors.append("duplicate active targets in distribution registry")
    expected = project.get("build", {}).get("targets", [])
    if active != expected:
        errors.append(f"registry active_targets != build.targets: {active!r} != {expected!r}")
    planned = project.get("runtimes", {}).get("planned", [])
    if set(active) != set(planned):
        errors.append("active distribution targets must match planned runtimes")
    targets = registry.get("targets", {})
    patterns = []
    for runtime in active:
        cfg = targets.get(runtime)
        if not cfg:
            errors.append(f"missing registry target: {runtime}")
            continue
        pattern = cfg.get("artifact_pattern")
        if not pattern or "{version}" not in pattern:
            errors.append(f"{runtime}: artifact_pattern must contain {{version}}")
        else:
            patterns.append(pattern)
        for field in ("builder", "validator"):
            command = cfg.get(field)
            if not isinstance(command, list) or not command:
                errors.append(f"{runtime}: {field} command missing")
                continue
            for rel in [x for x in command if isinstance(x, str) and x.startswith("scripts/")]:
                if not (ROOT / rel).is_file():
                    errors.append(f"{runtime}: referenced script missing: {rel}")
        runtime_cfg = contract.get("runtime_compatibility", {}).get(runtime, {})
        if runtime_cfg.get("status") != "implemented":
            errors.append(f"{runtime}: active runtime must be implemented in runtime contract")
    if len(patterns) != len(set(patterns)):
        errors.append("distribution artifact patterns must be unique")
    hygiene = registry.get("hygiene", {})
    if not hygiene.get("generated_roots"):
        errors.append("hygiene.generated_roots missing")
    if not hygiene.get("forbidden_runtime_projection_paths"):
        errors.append("hygiene.forbidden_runtime_projection_paths missing")
    if errors:
        print("FAIL")
        for error in errors:
            print("-", error)
        return 1
    print("PASS: distribution registry is synchronized with project and runtime contract")
    return 0

if __name__ == "__main__":
    sys.exit(main())
