#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys

REQ = [
    "Profile","Application","Database","Runtime configuration","Domain / proxy / TLS",
    "Health","Persistence","Migrations","Build / deploy","Verification",
    "Troubleshooting","Live verification status"
]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("file")
    a=ap.parse_args()
    t=Path(a.file).read_text(encoding="utf-8")
    errs=[]

    for h in REQ:
        if not re.search(rf"^##\s+{re.escape(h)}$", t, re.M):
            errs.append(f"missing section: {h}")

    if not re.search(r"^## Profile$\n\ncoolify-external-postgresql\s*$", t, re.M):
        errs.append("profile must be coolify-external-postgresql")

    low=t.lower()
    required_concepts = [
        "external postgresql",
        "coolify",
        "reverse proxy owner: coolify",
        "tls owner: coolify",
        "bind address: `0.0.0.0`",
        "public exposure: no",
    ]
    for concept in required_concepts:
        if concept not in low:
            errs.append(f"missing Coolify baseline concept: {concept}")

    if re.search(r"(?i)postgresql.*(?:inside|embedded|in app image)", t):
        errs.append("PostgreSQL must not be embedded in app image")

    m=re.search(r"^## Live verification status$\n\n(verified|pending)\s*$", t, re.M)
    if not m:
        errs.append("live verification status must be verified/pending")

    if errs:
        print("FAIL")
        for e in errs:
            print("-",e)
        return 1

    print("PASS: Coolify deployment profile valid")
    return 0

if __name__=="__main__":
    sys.exit(main())
