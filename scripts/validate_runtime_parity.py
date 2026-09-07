#!/usr/bin/env python3
from pathlib import Path
import argparse,zipfile,yaml,json,sys
def load(path,kind):
    with zipfile.ZipFile(path) as z:
        if kind=="chat":
            text=z.read("runtime/canonical-instructions.md").decode(); mf=yaml.safe_load(z.read("chat-runtime-manifest.yaml").decode())
        else:
            text=z.read("instructions.txt").decode(); mf=yaml.safe_load(z.read("custom-gpt.yaml").decode())
        return text.lower(),mf.get("behavior_contract",{})
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--contract",required=True); ap.add_argument("--chat",required=True); ap.add_argument("--custom",required=True); ap.add_argument("--json",action="store_true"); a=ap.parse_args()
    c=yaml.safe_load(Path(a.contract).read_text()); ct,cm=load(a.chat,"chat"); ut,um=load(a.custom,"custom")
    errs=[]; rows=[]
    for d in c["dimensions"]:
        def ok(txt): return all(any(alt.lower() in txt for alt in grp) for grp in d["groups"])
        co,uo=ok(ct),ok(ut); parity=co and uo
        rows.append({"id":d["id"],"name":d["name"],"severity":d["severity"],"chat":"pass" if co else "fail","custom":"pass" if uo else "fail","parity":"pass" if parity else "fail"})
        if not parity: errs.append(f"{d['id']} parity fail")
    for k,v in c["manifest_rules"].items():
        if cm.get(k)!=v: errs.append(f"chat manifest {k} mismatch")
        if um.get(k)!=v: errs.append(f"custom manifest {k} mismatch")
    crit=sum(1 for x in rows if x["severity"]=="critical" and x["parity"]=="fail")
    out={"result":"PASS" if not errs else "FAIL","dimensions":len(rows),"passed":sum(x["parity"]=="pass" for x in rows),"critical_failures":crit,"manifest_rules":len(c["manifest_rules"]),"rows":rows,"errors":errs}
    print(json.dumps(out,indent=2) if a.json else f"{out['result']}: {out['passed']}/{out['dimensions']} parity, critical={crit}")
    return 0 if not errs else 1
if __name__=="__main__": sys.exit(main())
