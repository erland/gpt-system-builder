#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys
REQ=["Target profile","Release artifact","Runtime","Configuration","Persistence","Migration strategy","Health / readiness","Proxy / TLS / domain","External services","Packaging verification","Deployment verification","Rollback / restore","Operations ownership"]
PROFILES={"local-development","docker-standalone","docker-external-postgresql","coolify-external-postgresql","generic-container-platform","kubernetes-basic"}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("file"); a=ap.parse_args()
    t=Path(a.file).read_text(encoding="utf-8"); errs=[]
    for h in REQ:
        if not re.search(rf"^##\s+{re.escape(h)}$",t,re.M): errs.append(f"missing section: {h}")
    m=re.search(r"^## Target profile$\n\n([a-z0-9-]+)\s*$",t,re.M)
    if not m: errs.append("target profile value missing")
    elif m.group(1) not in PROFILES: errs.append(f"unsupported target profile: {m.group(1)}")
    if m and m.group(1)=="coolify-external-postgresql":
        low=t.lower()
        for concept in ["external postgresql","coolify","health"]:
            if concept not in low: errs.append(f"coolify profile missing concept: {concept}")
    if errs:
        print("FAIL"); [print("-",e) for e in errs]; return 1
    print("PASS: deployment/packaging plan valid"); return 0
if __name__=="__main__": sys.exit(main())
