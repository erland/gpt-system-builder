#!/usr/bin/env python3
from pathlib import Path
import argparse,yaml,re,sys

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("workflow")
    ap.add_argument("entrypoint")
    a=ap.parse_args()
    errs=[]

    wf=Path(a.workflow)
    ep=Path(a.entrypoint)

    if not wf.exists(): errs.append("workflow missing")
    if not ep.exists(): errs.append("entrypoint missing")

    if wf.exists():
        text=wf.read_text(encoding="utf-8")
        data=yaml.safe_load(text)
        trigger=data.get("on", data.get(True))
        if not isinstance(trigger,dict):
            errs.append("workflow trigger missing")
        else:
            if "pull_request" not in trigger: errs.append("pull_request trigger missing")
            push=trigger.get("push")
            branches=(push or {}).get("branches",[]) if isinstance(push,dict) else []
            if "main" not in branches: errs.append("push main trigger missing")
        if data.get("permissions",{}).get("contents")!="read":
            errs.append("contents: read missing")
        for phrase in ["actions/checkout@v4","actions/setup-python@v5","bash scripts/ci-project.sh"]:
            if phrase not in text: errs.append(f"workflow missing {phrase}")
        if "write-all" in text: errs.append("unsafe write-all")
        if re.search(r"curl\\s+.*\\|\\s*(ba)?sh",text):
            errs.append("unsafe curl|sh")

    if ep.exists():
        t=ep.read_text(encoding="utf-8")
        required=[
            "build_chat_runtime_zip.py",
            "build_custom_gpt_distribution.py",
            "validate_chat_runtime_zip.py",
            "validate_custom_gpt_distribution.py",
            "run_static_instruction_evals.py",
            "validate_runtime_parity.py",
            "run_e2e_small_create_eval.py",
            "run_e2e_existing_change_eval.py",
            "run_e2e_docker_coolify_eval.py",
            "scan_repository_hygiene.py",
        ]
        for x in required:
            if x not in t: errs.append(f"entrypoint missing {x}")
        if "dist-ci" not in t:
            errs.append("fresh CI distribution directory missing")
        build_pos=t.find("build_chat_runtime_zip.py")
        parity_pos=t.find("validate_runtime_parity.py")
        if build_pos < 0 or parity_pos < 0 or build_pos > parity_pos:
            errs.append("distribution build must precede parity validation")

    if errs:
        print("FAIL")
        for e in errs: print("-",e)
        return 1

    print("PASS: System Builder project CI valid")
    return 0

if __name__=="__main__":
    sys.exit(main())
