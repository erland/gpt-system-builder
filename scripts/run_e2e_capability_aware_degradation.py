#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sys
import yaml

ROOT=Path(__file__).resolve().parents[1]
SCENARIO=ROOT/"evals"/"e2e"/"capability-aware-degradation"/"scenario.yaml"
RUNTIME=ROOT/"runtime"/"runtime-contract.json"
PARITY=ROOT/"evals"/"runtime-parity-contract.yaml"

def choose_profile(source_mode, available, required):
    available=set(available)
    missing=[c for c in required if c not in available]
    if missing:
        return None, True
    if source_mode=="github":
        return "github_first", False
    if source_mode in ("zip","workspace") and {"filesystem.read","filesystem.write","code_execution","persistent_state"}.issubset(available):
        return "zip_local", False
    return "degraded_manual", False

def main()->int:
    data=yaml.safe_load(SCENARIO.read_text(encoding="utf-8"))
    runtime=json.loads(RUNTIME.read_text(encoding="utf-8"))
    parity=yaml.safe_load(PARITY.read_text(encoding="utf-8"))
    routing=runtime["capabilities"]["routing"]

    if routing["selection_rule"]!="simplest_profile_that_satisfies_required_capabilities":
        raise SystemExit("FAIL: routing selection rule mismatch")
    if runtime["capabilities"]["agent_workspace"]["github_policy"]!="prefer_github_actions_when_sufficient":
        raise SystemExit("FAIL: GitHub Actions-first Agent Workspace policy missing")
    if runtime["capabilities"]["pwa_preview"]["requirement"]!="optional":
        raise SystemExit("FAIL: PWA Preview must remain optional")
    if runtime["capabilities"]["browser_screenshot"]["requirement"]!="optional":
        raise SystemExit("FAIL: Browser Screenshot must remain optional")

    seen=set()
    companions={"companion.agent_workspace","companion.pwa_preview","companion.browser_screenshot"}
    for scenario in data["scenarios"]:
        sid=scenario["id"]
        if sid in seen:
            raise SystemExit(f"FAIL: duplicate scenario id {sid}")
        seen.add(sid)

        if "variants" in scenario:
            for variant in scenario["variants"]:
                if variant["expected"].get("optional_capability_blocks") is not False:
                    raise SystemExit(f"FAIL: {sid} optional companion capability may not block")
            continue

        available=scenario.get("available", [])
        required=scenario.get("required", [])
        profile, blocked=choose_profile(scenario["source_mode"], available, required)
        expected=scenario["expected"]

        if "profile" in expected and profile!=expected["profile"]:
            raise SystemExit(f"FAIL: {sid} expected profile {expected['profile']} got {profile}")
        if "selected_profile" in expected and profile!=expected["selected_profile"]:
            raise SystemExit(f"FAIL: {sid} selected profile mismatch")
        if "blocked" in expected and blocked is not expected["blocked"]:
            raise SystemExit(f"FAIL: {sid} blocked mismatch")
        if expected.get("use_agent_workspace") is False and profile=="hybrid_github_external_execution":
            raise SystemExit(f"FAIL: {sid} used Agent Workspace redundantly")
        if expected.get("companion_plugins_required") is False and any(c in required for c in companions):
            raise SystemExit(f"FAIL: {sid} incorrectly requires companion plugins")
        if expected.get("false_pass") is False and blocked is False and any(c not in available for c in required):
            raise SystemExit(f"FAIL: {sid} would allow false PASS")

    active=set(parity["runtime_policy"]["active"])
    required_runtimes={"chat_zip","custom_gpt","claude_projects","opencode","openai_plugin"}
    if active!=required_runtimes:
        raise SystemExit(f"FAIL: active runtime parity set mismatch: {sorted(active)}")

    plugin=parity["runtime_policy"]["reduced_runtime_requirements"]["openai_plugin"]
    if "no false PASS for unrun verification" not in plugin["must_preserve"]:
        raise SystemExit("FAIL: OpenAI Plugin must preserve no-false-PASS")

    print(f"PASS: capability-aware degradation scenarios ({len(seen)} scenarios)")
    return 0

if __name__=="__main__":
    sys.exit(main())
