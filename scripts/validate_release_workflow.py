#!/usr/bin/env python3
from pathlib import Path
import argparse, yaml, re, sys

REQUIRED_RUNTIME_MARKERS = [
    "system-builder-chat-$VERSION.zip",
    "system-builder-custom-gpt-$VERSION.zip",
    "system-builder-claude-projects-$VERSION.zip",
    "system-builder-opencode-$VERSION.zip",
]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("workflow")
    ap.add_argument("script")
    a=ap.parse_args()
    errs=[]
    wf=Path(a.workflow)
    sc=Path(a.script)

    if not wf.exists(): errs.append("release workflow missing")
    if not sc.exists(): errs.append("release script missing")

    if wf.exists():
        text=wf.read_text(encoding="utf-8")
        data=yaml.safe_load(text)
        trigger=data.get("on", data.get(True))
        if not isinstance(trigger,dict):
            errs.append("release trigger missing")
        else:
            push=trigger.get("push")
            tags=(push or {}).get("tags",[]) if isinstance(push,dict) else []
            if "v*" not in tags: errs.append("tag trigger v* missing")
            if "workflow_dispatch" not in trigger: errs.append("workflow_dispatch missing")
        if data.get("permissions",{}).get("contents")!="write":
            errs.append("contents: write required for release")
        for phrase in [
            "actions/checkout@v4",
            "actions/setup-python@v5",
            "actions/upload-artifact@v4",
            "bash scripts/build_release.sh",
            "release-artifacts/*",
            "gh release",
        ]:
            if phrase not in text: errs.append(f"workflow missing {phrase}")

    if sc.exists():
        t=sc.read_text(encoding="utf-8")
        required=[
            "bash scripts/ci-project.sh",
            "build_all_distributions.py",
            "validate_all_distributions.py",
            "run_static_instruction_evals.py",
            "validate_runtime_parity.py",
            "distribution-build-manifest.json",
            "SHA256SUMS.txt",
            "release-metadata.yaml",
            "source_of_version",
            "distribution_registry",
            'VERSION="${TAG#v}"'.replace("\\",""),
        ]
        for phrase in required:
            if phrase not in t: errs.append(f"release script missing {phrase}")
        for marker in REQUIRED_RUNTIME_MARKERS:
            if marker not in t: errs.append(f"release script missing runtime artifact marker {marker}")
        for dist in ["chat_zip","custom_gpt","claude_projects","opencode"]:
            if f"--distribution {dist}" not in t:
                errs.append(f"release static eval missing for {dist}")
        for flag in ["--chat","--custom","--claude","--opencode"]:
            if flag not in t: errs.append(f"release parity missing {flag}")
        if re.search(r'VERSION\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+', t):
            errs.append("hardcoded release version found")

    if errs:
        print("FAIL")
        for e in errs: print("-",e)
        return 1
    print("PASS: GitHub Release build valid for four runtime distributions")
    return 0

if __name__=="__main__":
    sys.exit(main())
