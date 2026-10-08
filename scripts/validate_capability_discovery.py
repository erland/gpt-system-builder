#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import sys
import yaml
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "capability-discovery.schema.json"
EXAMPLE = ROOT / "examples" / "capability-discovery.example.yaml"

def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def load_schema():
    import json
    return json.loads(SCHEMA.read_text(encoding="utf-8"))

def main() -> int:
    validator = Draft202012Validator(load_schema())
    example = load_yaml(EXAMPLE)
    validator.validate(example)

    ids = [item["id"] for item in example["capabilities"]]
    if len(ids) != len(set(ids)):
        raise SystemExit("FAIL: duplicate capability ids in discovery example")

    blocked = [c["id"] for c in example["capabilities"] if c["outcome"] == "blocked"]
    degraded = [c["id"] for c in example["capabilities"] if c["outcome"] == "degraded"]
    summary = example["summary"]
    if bool(blocked) != summary["blocked"]:
        raise SystemExit("FAIL: blocked summary does not match capability outcomes")
    if bool(degraded) != summary["degraded"]:
        raise SystemExit("FAIL: degraded summary does not match capability outcomes")
    if sorted(blocked) != sorted(summary.get("blocking_capabilities", [])):
        raise SystemExit("FAIL: blocking_capabilities summary mismatch")
    if sorted(degraded) != sorted(summary.get("degraded_capabilities", [])):
        raise SystemExit("FAIL: degraded_capabilities summary mismatch")

    invalid = copy.deepcopy(example)
    invalid["capabilities"][0]["availability"] = "assumed"
    try:
        validator.validate(invalid)
    except ValidationError:
        pass
    else:
        raise SystemExit("FAIL: invalid discovery availability was accepted")

    print("PASS: capability discovery contract and example are valid")
    return 0

if __name__ == "__main__":
    sys.exit(main())
