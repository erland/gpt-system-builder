#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
import yaml

ROOT=Path(__file__).resolve().parents[1]

def main() -> int:
    errors=[]
    version=(ROOT/"VERSION").read_text(encoding="utf-8").strip()
    project=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    status=yaml.safe_load((ROOT/"project-status.yaml").read_text(encoding="utf-8"))
    readiness=yaml.safe_load((ROOT/"evals/final-release-readiness.yaml").read_text(encoding="utf-8"))
    runtime=json.loads((ROOT/"runtime/runtime-contract.json").read_text(encoding="utf-8"))
    registry=yaml.safe_load((ROOT/"runtime/distribution-registry.yaml").read_text(encoding="utf-8"))

    candidate=readiness.get("release_candidate",{})
    if version!="1.0.0-rc.2":
        errors.append(f"VERSION must be 1.0.0-rc.2, got {version}")
    if candidate.get("version")!=version:
        errors.append("readiness release candidate version does not match VERSION")
    if candidate.get("tag")!=f"v{version}":
        errors.append("readiness release candidate tag does not match VERSION")
    if candidate.get("reproducible_from_tag") is not True:
        errors.append("release candidate must be reproducible from tag")

    release=project.get("release",{})
    if release.get("candidate_version")!=version:
        errors.append("gpt-project release candidate_version mismatch")
    if release.get("candidate_tag")!=f"v{version}":
        errors.append("gpt-project release candidate_tag mismatch")
    if release.get("runtime_count")!=4:
        errors.append("release runtime_count must be 4")

    expected=["chat_zip","custom_gpt","claude_projects","opencode"]
    if registry.get("active_targets")!=expected:
        errors.append("distribution registry active targets mismatch")
    compat=runtime.get("runtime_compatibility",{})
    for target in expected:
        if compat.get(target,{}).get("status")!="implemented":
            errors.append(f"{target} is not implemented")
    plugin=compat.get("openai_plugin",{})
    if plugin.get("status")!="not_planned" or plugin.get("target")!="reduced":
        errors.append("OpenAI Plugin decision must remain explicit not_planned/reduced")

    if readiness.get("blockers"):
        errors.append("release readiness blockers present")
    if readiness.get("required_gates_passed")!=readiness.get("required_gates_total"):
        errors.append("release readiness gate count mismatch")
    if readiness.get("decision") not in {"READY","READY_WITH_WARNINGS"}:
        errors.append("release readiness is not releasable")

    progress=status.get("progress",{})
    if progress.get("last_completed_step")!=49:
        errors.append("project status must complete SB-49")
    if "SB-49" not in progress.get("completed_step_ids",[]):
        errors.append("SB-49 missing from completed step ids")

    if errors:
        print("FAIL")
        for error in errors: print("-",error)
        return 1
    print(f"PASS: release candidate v{version} is internally consistent across four runtimes")
    return 0

if __name__=="__main__":
    sys.exit(main())
