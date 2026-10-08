#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import yaml
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "execution-profile.schema.json"
EXAMPLE = ROOT / "examples" / "execution-profile.example.yaml"

def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    example = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    validator.validate(example)

    if example["source_mode"] == "github" and example.get("repository_authority") is not True:
        raise SystemExit("FAIL: GitHub execution profile must preserve repository authority")

    invalid = copy.deepcopy(example)
    invalid["status"] = "blocked"
    invalid["selected_profile"] = "github_first"
    try:
        validator.validate(invalid)
    except ValidationError:
        pass
    else:
        raise SystemExit("FAIL: blocked routing decision accepted a selected profile")

    invalid = copy.deepcopy(example)
    invalid["selected_profile"] = "unknown_profile"
    try:
        validator.validate(invalid)
    except ValidationError:
        pass
    else:
        raise SystemExit("FAIL: unknown execution profile was accepted")

    print("PASS: execution profile contract and example are valid")
    return 0

if __name__ == "__main__":
    sys.exit(main())
