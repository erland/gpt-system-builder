#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("root")
    a=ap.parse_args()
    root=Path(a.root)
    k=root/"knowledge"
    errs=[]

    if not (k/"README.md").exists():
        errs.append("knowledge/README.md missing")

    md_files=sorted(p for p in k.glob("*.md") if p.name!="README.md")
    if not md_files:
        errs.append("no Knowledge files")

    for p in md_files:
        text=p.read_text(encoding="utf-8")
        m=re.search(r"^Class:\s*(reference|example)\s*$", text, re.M)
        if not m:
            errs.append(f"{p.name}: Class must be reference/example")

    readme=(k/"README.md").read_text(encoding="utf-8") if (k/"README.md").exists() else ""
    for p in md_files:
        if f"`{p.name}`" not in readme:
            errs.append(f"{p.name}: missing from Knowledge index")

    # Critical runtime phrases must have canonical docs outside Knowledge.
    canonical=root/"docs"
    checks={
        "one-step": "next-step-state-machine.md",
        "release": "release-readiness-standard.md",
        "github": "github-mode.md",
        "zip": "zip-mode.md",
    }
    for _, fname in checks.items():
        if not (canonical/fname).exists():
            errs.append(f"canonical runtime file missing: docs/{fname}")

    if errs:
        print("FAIL")
        for e in errs: print("-",e)
        return 1

    print(f"PASS: Knowledge architecture valid ({len(md_files)} reference files)")
    return 0

if __name__=="__main__":
    sys.exit(main())
