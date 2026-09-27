#!/usr/bin/env python3
from pathlib import Path
import sys, yaml

ROOT=Path(__file__).resolve().parents[1]
workflow=ROOT/"templates/github-pages-deploy-template.yml"
profile=ROOT/"docs/github-pages-profile.md"
errors=[]

try:
    data=yaml.safe_load(workflow.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"FAIL: cannot parse Pages workflow: {exc}")
    sys.exit(1)

permissions=data.get("permissions",{})
for key,value in {"contents":"read","pages":"write","id-token":"write"}.items():
    if permissions.get(key)!=value:
        errors.append(f"workflow permission {key} must be {value}")

jobs=data.get("jobs",{})
build=jobs.get("build",{})
deploy=jobs.get("deploy",{})
build_text=workflow.read_text(encoding="utf-8")
for token in ["actions/configure-pages@","actions/upload-pages-artifact@","actions/deploy-pages@"]:
    if token not in build_text:
        errors.append(f"missing {token}")
if deploy.get("needs")!="build":
    errors.append("deploy job must depend on build")
env=deploy.get("environment",{})
if env.get("name")!="github-pages":
    errors.append("deploy environment must be github-pages")
if "pull_request" in str(data.get(True,{}) or data.get("on",{})):
    errors.append("Pages deployment template must not deploy on pull_request")

profile_text=profile.read_text(encoding="utf-8").lower()
for phrase in [
    "separat deployment-side effect",
    "repository-subpath",
    "hash routing",
    "server-side secrets",
]:
    if phrase.lower() not in profile_text:
        errors.append(f"profile missing rule: {phrase}")

if errors:
    print("FAIL")
    for e in errors:
        print("-",e)
    sys.exit(1)
print("PASS: GitHub Pages profile/workflow contract")
