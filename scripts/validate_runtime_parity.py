#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import zipfile
import yaml

ENTRYPOINTS = {
    "chat_zip": "runtime/canonical-instructions.md",
    "custom_gpt": "instructions.txt",
    "claude_projects": "project-instructions.md",
    "opencode": "AGENTS.md",
}

def read_json(zf, name):
    return json.loads(zf.read(name).decode("utf-8"))

def load_runtime(path: Path, runtime: str):
    with zipfile.ZipFile(path) as zf:
        text = zf.read(ENTRYPOINTS[runtime]).decode("utf-8").lower()
        data = {"text": text, "names": set(zf.namelist())}
        if runtime == "chat_zip":
            data["manifest"] = yaml.safe_load(zf.read("chat-runtime-manifest.yaml").decode("utf-8"))
        elif runtime == "custom_gpt":
            data["manifest"] = yaml.safe_load(zf.read("custom-gpt.yaml").decode("utf-8"))
        elif runtime == "claude_projects":
            data["contract"] = read_json(zf, "runtime-contract.json")
            data["compatibility"] = zf.read("compatibility.md").decode("utf-8").lower()
        elif runtime == "opencode":
            snap = read_json(zf, ".opencode/runtime-contract.json")
            data["contract"] = snap["canonical_contract"]
            data["tool_mapping"] = read_json(zf, ".opencode/tool-mapping.json")
            data["config"] = read_json(zf, "opencode.json")
        return data

def text_ok(text, requirement):
    return all(any(alt.lower() in text for alt in group) for group in requirement["groups"])

def expectation_result(runtime, expected, actual):
    if expected == "reduced":
        return "pass" if actual in {"reduced", "equivalent"} else "fail"
    if expected == "equivalent_with_platform_constraints":
        return "pass" if actual in {"equivalent_with_platform_constraints", "equivalent"} else "fail"
    return "pass" if actual == expected else "fail"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--contract",required=True)
    ap.add_argument("--chat",required=True)
    ap.add_argument("--custom",required=True)
    ap.add_argument("--claude",required=True)
    ap.add_argument("--opencode",required=True)
    ap.add_argument("--json",action="store_true")
    a=ap.parse_args()

    contract=yaml.safe_load(Path(a.contract).read_text(encoding="utf-8"))
    artifacts={
        "chat_zip":Path(a.chat),
        "custom_gpt":Path(a.custom),
        "claude_projects":Path(a.claude),
        "opencode":Path(a.opencode),
    }
    runtimes={name:load_runtime(path,name) for name,path in artifacts.items()}
    errors=[]; rows=[]

    # behavior
    for req in contract["dimensions"]["behavior"]["requirements"]:
        for runtime,data in runtimes.items():
            ok=text_ok(data["text"],req)
            rows.append({"dimension":"behavior","id":req["id"],"runtime":runtime,"result":"pass" if ok else "fail"})
            if not ok:
                errors.append(f"behavior {req['id']} missing in {runtime}")

    # canonical contract-derived dimensions
    canonical = runtimes["claude_projects"]["contract"]
    capabilities = canonical["capabilities"]["requirements"]
    cap_actual={
        "chat_zip":"equivalent",
        "custom_gpt":"equivalent_with_platform_constraints",
        "claude_projects":"reduced",
        "opencode":"equivalent",
    }
    for runtime,expected in contract["dimensions"]["capability"]["runtime_expectations"].items():
        actual=cap_actual[runtime]
        result=expectation_result(runtime,expected,actual)
        rows.append({"dimension":"capability","runtime":runtime,"expected":expected,"actual":actual,"result":result})
        if result=="fail": errors.append(f"capability parity mismatch for {runtime}")
    for key,level in contract["dimensions"]["capability"]["canonical_requirements"].items():
        source_key = key
        if key.startswith("filesystem_"):
            sub=key.split("_",1)[1]
            actual=capabilities["filesystem"][sub]
        else:
            actual=capabilities[key]["level"]
        if actual != level:
            errors.append(f"canonical capability {key} expected {level}, got {actual}")

    outputs=canonical["artifacts"]["outputs"]
    for required in contract["dimensions"]["artifact"]["required_outputs"]:
        if outputs.get(required,{}).get("requirement")!="required":
            errors.append(f"required artifact contract missing: {required}")
    for conditional in contract["dimensions"]["artifact"]["conditional_outputs"]:
        if outputs.get(conditional,{}).get("requirement")!="conditional":
            errors.append(f"conditional artifact contract missing: {conditional}")
    for runtime,expected in contract["dimensions"]["artifact"]["runtime_expectations"].items():
        actual=cap_actual[runtime]
        result=expectation_result(runtime,expected,actual)
        rows.append({"dimension":"artifact","runtime":runtime,"expected":expected,"actual":actual,"result":result})
        if result=="fail": errors.append(f"artifact parity mismatch for {runtime}")

    state=canonical["workspace_state"]["state"]
    ws=contract["dimensions"]["workspace_state"]
    if state.get("authority")!=ws["authority"]: errors.append("workspace-state authority mismatch")
    if state.get("conversation_fallback")!=ws["conversation_fallback"]: errors.append("workspace-state conversation fallback mismatch")
    if state.get("path")!=ws["state_path"]: errors.append("workspace-state path mismatch")
    for runtime,expected in ws["runtime_expectations"].items():
        actual=cap_actual[runtime]
        result=expectation_result(runtime,expected,actual)
        rows.append({"dimension":"workspace_state","runtime":runtime,"expected":expected,"actual":actual,"result":result})
        if result=="fail": errors.append(f"workspace_state parity mismatch for {runtime}")

    declared={t["id"] for t in canonical["tools"]["tools"]}
    if declared!=set(contract["dimensions"]["tool"]["declared_tools"]):
        errors.append("canonical declared tool set mismatch")
    required={t["id"] for t in canonical["tools"]["tools"] if t["requirement"]=="required"}
    if not set(contract["dimensions"]["tool"]["required_tools"]).issubset(required):
        errors.append("canonical required tool set mismatch")
    for runtime,expected in contract["dimensions"]["tool"]["runtime_expectations"].items():
        actual=cap_actual[runtime]
        result=expectation_result(runtime,expected,actual)
        rows.append({"dimension":"tool","runtime":runtime,"expected":expected,"actual":actual,"result":result})
        if result=="fail": errors.append(f"tool parity mismatch for {runtime}")

    claude=runtimes["claude_projects"]
    compat=claude["compatibility"]
    for phrase in contract["runtime_policy"]["reduced_runtime_requirements"]["claude_projects"]["must_document_limitations"]:
        if phrase.lower() not in compat:
            errors.append(f"Claude reduced parity limitation not documented: {phrase}")
    for phrase in ["unrun verification","workspace-file authority","canonical behavior"]:
        if phrase not in compat:
            errors.append(f"Claude reduced parity preservation not explicit: {phrase}")

    mapping=runtimes["opencode"]["tool_mapping"].get("tools",{})
    if set(mapping)!=declared:
        errors.append("OpenCode tool mapping does not match canonical tool set")
    if mapping.get("workspace-write",{}).get("approval")!="ask":
        errors.append("OpenCode workspace-write must require approval")
    if mapping.get("repository-actions",{}).get("approval")!="ask":
        errors.append("OpenCode repository-actions must require approval")

    crit_fail=sum(1 for row in rows if row["result"]=="fail" and contract["dimensions"].get(row["dimension"],{}).get("severity")=="critical")
    out={
        "result":"PASS" if not errors else "FAIL",
        "runtimes":list(artifacts),
        "dimensions":["behavior","capability","artifact","workspace_state","tool"],
        "rows":rows,
        "critical_failures":crit_fail,
        "errors":errors,
    }
    if a.json: print(json.dumps(out,indent=2))
    else:
        print(f"{out['result']}: {len(out['runtimes'])} runtimes across {len(out['dimensions'])} parity dimensions, critical={crit_fail}")
        for error in errors: print("-",error)
    return 0 if not errors else 1

if __name__=="__main__":
    sys.exit(main())
