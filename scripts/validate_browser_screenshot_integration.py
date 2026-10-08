#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import yaml
from jsonschema import Draft202012Validator, ValidationError, FormatChecker

ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/"schemas"/"browser-screenshot-evidence.schema.json"
EXAMPLE=ROOT/"examples"/"browser-screenshot-evidence.example.yaml"
RUNTIME=ROOT/"runtime"/"runtime-contract.json"
POLICY=ROOT/"docs"/"browser-screenshot-integration.md"

def main()->int:
    schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
    example=yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    validator=Draft202012Validator(schema, format_checker=FormatChecker())
    validator.validate(example)

    runtime=json.loads(RUNTIME.read_text(encoding="utf-8"))
    policy=runtime.get("capabilities",{}).get("browser_screenshot",{})
    if policy.get("requirement")!="optional":
        raise SystemExit("FAIL: Browser Screenshot must remain optional")
    if policy.get("default_preset")!="desktop":
        raise SystemExit("FAIL: Browser Screenshot default preset must be desktop")
    if policy.get("screenshot_is_functional_verification") is not False:
        raise SystemExit("FAIL: screenshot must not count as functional verification")
    if policy.get("extra_viewports_policy")!="only_when_requirement_risk_or_user_justifies":
        raise SystemExit("FAIL: extra screenshot viewports must be demand-driven")
    if policy.get("public_http_url_required") is not True:
        raise SystemExit("FAIL: Browser Screenshot must require a public HTTP(S) URL")
    if policy.get("supported_presets")!=["desktop","tablet","mobile"]:
        raise SystemExit("FAIL: Browser Screenshot live preset set mismatch")
    if policy.get("custom_viewport_supported") is not True:
        raise SystemExit("FAIL: Browser Screenshot must preserve custom viewport support")
    if policy.get("full_page_supported") is not True:
        raise SystemExit("FAIL: Browser Screenshot must preserve fullPage support")

    text=POLICY.read_text(encoding="utf-8").lower()
    for marker in ("desktop", "tablet", "mobile", "custom", "fullpage", "public", "playwright", "functional"):
        if marker not in text:
            raise SystemExit(f"FAIL: Browser Screenshot policy missing marker: {marker}")

    invalid=copy.deepcopy(example)
    invalid["functional_verification"]=True
    try:
        validator.validate(invalid)
    except ValidationError:
        pass
    else:
        raise SystemExit("FAIL: screenshot incorrectly accepted as functional verification")

    print("PASS: Browser Screenshot evidence and visual-only policy are valid")
    return 0

if __name__=="__main__":
    sys.exit(main())
