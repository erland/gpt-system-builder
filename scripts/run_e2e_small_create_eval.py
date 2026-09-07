#!/usr/bin/env python3
from pathlib import Path
import argparse,subprocess,yaml,zipfile,hashlib,sys,json
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--scenario-root",required=True); a=ap.parse_args()
    base=Path(a.scenario_root); p=base/"generated-project"; errs=[]
    phases=[e["phase"] for e in yaml.safe_load((base/"evaluation-trace.yaml").read_text())["events"]]
    order=["need","scope_and_spec","architecture","development_plan","select_and_lock","implementation","verification","state_update","stop"]
    if phases!=order: errs.append("CREATE phase order invalid")
    req=["README.md",".system-builder/project.yaml",".system-builder/work-status.yaml","docs/functional-specification.md","docs/architecture.md","docs/development-plan.md","src/tiny_status/app.py","tests/test_app.py"]
    for r in req:
        if not (p/r).exists(): errs.append("missing "+r)
    st=yaml.safe_load((p/".system-builder/work-status.yaml").read_text())
    if st.get("completed_steps")!=["DEV-001"]: errs.append("must complete exactly DEV-001")
    if st.get("next_step",{}).get("recommended")!="DEV-002": errs.append("must resume at DEV-002")
    t=subprocess.run([sys.executable,"-m","unittest","discover","-s","tests","-v"],cwd=p,capture_output=True,text=True)
    if t.returncode: errs.append("DEV-001 tests failed")
    out=base/"tiny-status-api-after-dev001.zip"
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
        for f in sorted(p.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts: z.write(f,f.relative_to(p).as_posix())
    with zipfile.ZipFile(out) as z:
        if z.testzip(): errs.append("fixture ZIP corrupt")
        names=set(z.namelist())
        for r in req:
            if r not in names: errs.append("fixture ZIP missing "+r)
    result={"result":"PASS" if not errs else "FAIL","tests":"PASS" if not t.returncode else "FAIL",
            "completed_steps":st.get("completed_steps"),"next_step":st.get("next_step",{}).get("recommended"),
            "zip_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),"errors":errs}
    print(json.dumps(result,indent=2)); return 0 if not errs else 1
if __name__=="__main__": sys.exit(main())
