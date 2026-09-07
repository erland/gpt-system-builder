#!/usr/bin/env python3
from pathlib import Path
import argparse, subprocess, yaml, zipfile, hashlib, sys, json

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--scenario-root", required=True)
    a=ap.parse_args()
    base=Path(a.scenario_root)
    project=base/"generated-project"
    errs=[]

    phases=[e["phase"] for e in yaml.safe_load((base/"evaluation-trace.yaml").read_text(encoding="utf-8"))["events"]]
    expected=["read_current_system","baseline","change_request","impact_analysis","update_current_state_spec","change_plan","select_and_lock","implementation","regression_verification","state_update","stop"]
    if phases != expected:
        errs.append("CHANGE phase order invalid")

    req=[
        "docs/functional-specification.md",
        "docs/architecture.md",
        "docs/development-plan.md",
        "docs/changes/CR-001/request.md",
        "docs/changes/CR-001/impact-analysis.md",
        ".system-builder/work-status.yaml",
        "src/counter_service/counter.py",
        "tests/test_counter.py",
    ]
    for rel in req:
        if not (project/rel).exists():
            errs.append("missing "+rel)

    fs=(project/"docs/functional-specification.md").read_text(encoding="utf-8")
    if "FR-003" not in fs or "decrement" not in fs:
        errs.append("current-state functional spec missing new behavior")

    hist=(project/"docs/changes/CR-001/impact-analysis.md").read_text(encoding="utf-8")
    if "baseline" not in hist.lower() or "regression" not in hist.lower():
        errs.append("impact analysis missing baseline/regression")

    status=yaml.safe_load((project/".system-builder/work-status.yaml").read_text(encoding="utf-8"))
    if status.get("completed_steps") != ["DEV-001"]:
        errs.append("exactly DEV-001 must be completed")
    if status.get("next_step",{}).get("recommended") != "DEV-002":
        errs.append("must resume at DEV-002")

    test=subprocess.run([sys.executable,"-m","unittest","discover","-s","tests","-v"],cwd=project,capture_output=True,text=True)
    if test.returncode != 0:
        errs.append("regression tests failed")

    out=base/"counter-service-after-cr001-dev001.zip"
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(project.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                z.write(p,p.relative_to(project).as_posix())
    with zipfile.ZipFile(out) as z:
        if z.testzip():
            errs.append("output ZIP corrupt")
        names=set(z.namelist())
        for rel in req:
            if rel not in names:
                errs.append("output ZIP missing "+rel)

    result={
        "result":"PASS" if not errs else "FAIL",
        "tests":"PASS" if test.returncode==0 else "FAIL",
        "completed_steps":status.get("completed_steps"),
        "next_step":status.get("next_step",{}).get("recommended"),
        "zip_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),
        "errors":errs,
    }
    print(json.dumps(result,indent=2))
    return 0 if not errs else 1

if __name__=="__main__":
    sys.exit(main())
