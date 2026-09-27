#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, yaml

def tag_version(tag):
    if not isinstance(tag,str) or not tag.startswith("v") or len(tag)<2:
        raise ValueError("invalid release tag")
    return tag[1:]

def evaluate(case):
    i=case["input"]
    actual={}
    if i.get("readme_present") and not i.get("readme_matches_current_state"):
        actual.update({"reconciliation":"fail","action":"update_readme","release_ready":False})
        return actual

    actual["reconciliation"]="pass"
    actual["action"]="none"
    version=tag_version(i["release_tag"])
    actual["artifact_version"]=version

    owner=i.get("version_owner")
    secondary=i.get("secondary_version")
    if owner=="tag":
        consistent = secondary in (None, version)
    elif owner=="ecosystem":
        consistent = secondary == version
    else:
        consistent = False

    actual["version_consistent"]=consistent
    actual["release_ready"]=bool(consistent)
    return actual

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--scenario",required=True)
    args=ap.parse_args()
    data=yaml.safe_load(Path(args.scenario).read_text(encoding="utf-8"))
    errors=[]
    for case in data.get("cases",[]):
        actual=evaluate(case)
        for key,value in case["expected"].items():
            if actual.get(key)!=value:
                errors.append(f'{case["id"]}: {key} expected={value!r} actual={actual.get(key)!r}')
    if errors:
        print("FAIL")
        for e in errors:
            print("-",e)
        return 1
    print(f'PASS: README/release-version policy ({len(data.get("cases",[]))} cases)')
    return 0

if __name__=="__main__":
    sys.exit(main())
