#!/usr/bin/env python3
from pathlib import Path
import argparse, zipfile, yaml, sys, re

REQUIRED = {
    "README.md",
    "chat-runtime-manifest.yaml",
    "runtime/canonical-instructions.md",
    "runtime/runtime-manifest.yaml",
    "docs/create-mode.md",
    "docs/change-mode.md",
    "docs/improve-mode.md",
    "docs/next-step-state-machine.md",
    "docs/zip-mode.md",
    "docs/github-mode.md",
    "docs/release-readiness-standard.md",
    "knowledge/README.md",
}

FORBIDDEN_PREFIXES = (
    "examples/",
    "tests/",
    ".github/",
    ".system-builder/",
    "dist/",
)
FORBIDDEN_FILES = {
    "project-status.yaml",
    "STATUS.md",
}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("zipfile")
    a=ap.parse_args()
    zp=Path(a.zipfile)
    errs=[]

    with zipfile.ZipFile(zp,"r") as z:
        bad=z.testzip()
        if bad:
            errs.append(f"corrupt member: {bad}")
        names=set(z.namelist())
        missing=sorted(REQUIRED-names)
        if missing:
            errs.append("missing required files: " + ", ".join(missing))

        for n in names:
            if n in FORBIDDEN_FILES:
                errs.append(f"development-only file included: {n}")
            if any(n.startswith(pref) for pref in FORBIDDEN_PREFIXES):
                errs.append(f"development-only path included: {n}")
            if n.endswith(".zip"):
                errs.append(f"nested ZIP included: {n}")

        try:
            manifest=yaml.safe_load(z.read("chat-runtime-manifest.yaml").decode("utf-8"))
        except Exception as e:
            errs.append(f"invalid chat runtime manifest: {e}")
            manifest={}

        if manifest.get("distribution") != "chat_zip":
            errs.append("manifest distribution must be chat_zip")
        if manifest.get("entrypoint") != "runtime/canonical-instructions.md":
            errs.append("manifest entrypoint mismatch")

        text=z.read("runtime/canonical-instructions.md").decode("utf-8")
        for phrase in [
            "one safe development step",
            "actual current source",
            "complete project ZIP",
            "reuse the active PR",
            "Never report an unrun check as PASS",
        ]:
            if phrase not in text:
                errs.append(f"runtime instruction missing core phrase: {phrase}")

    if errs:
        print("FAIL")
        for e in errs: print("-",e)
        return 1

    print(f"PASS: Chat ZIP runtime valid ({len(names)} files)")
    return 0

if __name__=="__main__":
    sys.exit(main())
