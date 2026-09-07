#!/usr/bin/env python3
from pathlib import Path
import argparse,zipfile,yaml,sys,json
def load_text(path,dist):
    with zipfile.ZipFile(path,"r") as z:
        return z.read("runtime/canonical-instructions.md" if dist=="chat_zip" else "instructions.txt").decode("utf-8")
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--requirements",required=True)
    ap.add_argument("--distribution",choices=["chat_zip","custom_gpt"],required=True)
    ap.add_argument("--artifact",required=True)
    ap.add_argument("--json",action="store_true")
    a=ap.parse_args()
    reqs=yaml.safe_load(Path(a.requirements).read_text(encoding="utf-8"))["requirements"]
    low=load_text(Path(a.artifact),a.distribution).lower(); results=[]
    for req in reqs:
        missing=[]
        for group in req["groups"]:
            if not any(alt.lower() in low for alt in group):
                missing.append(group)
        results.append({"id":req["id"],"severity":req["severity"],"result":"pass" if not missing else "fail","missing_groups":missing})
    fails=[r for r in results if r["result"]=="fail"]
    critical=[r for r in fails if r["severity"]=="critical"]
    result="PASS" if not fails else "FAIL"
    summary={"distribution":a.distribution,"passed":len(results)-len(fails),"total":len(results),"critical_failures":len(critical),"result":result,"results":results}
    if a.json: print(json.dumps(summary,indent=2))
    else:
        print(f"{result}: {a.distribution} {summary['passed']}/{summary['total']}, critical failures={len(critical)}")
        for r in fails: print("-",r["id"],"missing semantic groups:",r["missing_groups"])
    return 0 if result=="PASS" else 1
if __name__=="__main__": sys.exit(main())
