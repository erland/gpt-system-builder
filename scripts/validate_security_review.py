#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys

def main():
    p=argparse.ArgumentParser()
    p.add_argument("file")
    a=p.parse_args()
    text=Path(a.file).read_text(encoding="utf-8")
    required=[
        "Context","Authentication","Authorization","Inputs and file handling",
        "Secrets and configuration","Logging and errors","Container / deployment",
        "Security verification","Blockers","Specialist review needed"
    ]
    errs=[]
    for h in required:
        if not re.search(rf"^##\s+{re.escape(h)}$", text, re.M):
            errs.append(f"missing section: {h}")
    # Basic quality signals
    for term in ["server-side","secret","input","deployment"]:
        if term.lower() not in text.lower():
            errs.append(f"missing baseline concept: {term}")
    if errs:
        print("FAIL")
        for e in errs:
            print("-",e)
        return 1
    print("PASS: security baseline structure valid")
    return 0

if __name__=="__main__":
    sys.exit(main())
