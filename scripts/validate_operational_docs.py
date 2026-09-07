#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys

SECTIONS = {
    "configuration": ["Overview","Runtime variables","Secrets","Defaults","Environment-specific behavior","External services","Validation / startup behavior","Example configuration"],
    "installation": ["Prerequisites","Obtain/build artifact","Configure runtime","External services","Database setup/migrations","Start/deploy","Verify installation","Upgrade","Uninstall/remove"],
    "operations": ["Service overview","Health","Logs","Start / stop / restart","Redeploy / upgrade","Database operations","Backup / restore","Migrations","Rollback","Troubleshooting","Known operational limitations"],
}

SECRET_VALUE_PATTERNS = [
    re.compile(r"(?i)(password|token|secret|private[_ -]?key)\s*[:=]\s*(?!<secret>|\.\.\.|-)([A-Za-z0-9+/=_-]{12,})")
]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("kind", choices=SECTIONS)
    ap.add_argument("file")
    a=ap.parse_args()
    t=Path(a.file).read_text(encoding="utf-8")
    errs=[]
    for h in SECTIONS[a.kind]:
        if not re.search(rf"^##\s+{re.escape(h)}$", t, re.M):
            errs.append(f"missing section: {h}")

    for pat in SECRET_VALUE_PATTERNS:
        m=pat.search(t)
        if m:
            errs.append("possible real secret value in documentation")
            break

    if a.kind=="configuration":
        if "| Variable | Required | Secret | Default | Description |" not in t:
            errs.append("runtime variable table header missing")
    if a.kind=="installation" and "Verify installation" in t:
        if not re.search(r"health|verify|smoke|HTTP 200", t, re.I):
            errs.append("installation verification lacks observable check")
    if a.kind=="operations" and "Rollback" in t:
        if not re.search(r"previous|restore|rollback", t, re.I):
            errs.append("operations lacks rollback/recovery language")

    if errs:
        print("FAIL")
        for e in errs: print("-",e)
        return 1
    print(f"PASS: {a.kind} documentation valid")
    return 0

if __name__=="__main__":
    sys.exit(main())
