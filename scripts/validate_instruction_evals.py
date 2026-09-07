#!/usr/bin/env python3
from pathlib import Path
import argparse,yaml,sys
REQ=["id","title","category","severity","prompt","expected","forbidden"]
SEV={"critical","high","medium","low"}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("file"); a=ap.parse_args()
    data=yaml.safe_load(Path(a.file).read_text(encoding="utf-8")); errs=[]; cs=data.get("cases",[])
    if len(cs)<15: errs.append("at least 15 cases required")
    ids=set(); critical=0
    for c in cs:
        for k in REQ:
            if k not in c: errs.append(f"{c.get('id','?')}: missing {k}")
        if c.get("id") in ids: errs.append(f"duplicate id: {c.get('id')}")
        ids.add(c.get("id"))
        if c.get("severity") not in SEV: errs.append(f"{c.get('id')}: invalid severity")
        if c.get("severity")=="critical": critical+=1
        if not c.get("expected"): errs.append(f"{c.get('id')}: expected empty")
        if not c.get("forbidden"): errs.append(f"{c.get('id')}: forbidden empty")
    if critical<7: errs.append("at least 7 critical cases required")
    if errs:
        print("FAIL")
        for e in errs: print("-",e)
        return 1
    print(f"PASS: eval suite valid ({len(cs)} cases, {critical} critical)")
    return 0
if __name__=="__main__": sys.exit(main())
