#!/usr/bin/env python3
from pathlib import Path
import re, sys, yaml

ROOT=Path(__file__).resolve().parents[1]
readme=ROOT/"README.md"
project=ROOT/"gpt-project.yaml"
version_file=ROOT/"VERSION"
status=ROOT/"project-status.yaml"
errors=[]

if not readme.is_file():
    print("PASS: README not present; reconciliation rule applies when README exists")
    sys.exit(0)

text=readme.read_text(encoding="utf-8")
lower=text.lower()

if project.is_file():
    data=yaml.safe_load(project.read_text(encoding="utf-8")) or {}
    runtimes=((data.get("runtimes") or {}).get("planned") or [])
    names={
        "chat_zip":"Chat ZIP",
        "custom_gpt":"Custom GPT",
        "claude_projects":"Claude Projects",
        "opencode":"OpenCode",
    }
    for runtime in runtimes:
        marker=names.get(runtime)
        if marker and marker.lower() not in lower:
            errors.append(f"README missing active runtime: {marker}")

if version_file.is_file():
    version=version_file.read_text(encoding="utf-8").strip()
    stale=re.findall(r"\b(?:version|versionen|kandidat|releasekandidat)[^\n]{0,50}?v?(\d+\.\d+\.\d+(?:[-.]\w[\w.-]*)?)", text, re.I)
    for claimed in stale:
        if claimed != version:
            errors.append(f"README contains stale version/status claim {claimed}; canonical VERSION is {version}")

if status.is_file():
    data=yaml.safe_load(status.read_text(encoding="utf-8")) or {}
    last=((data.get("progress") or {}).get("last_completed_step"))
    for m in re.finditer(r"SB-01[–-]SB-(\d+)", text):
        if last is not None and int(m.group(1)) < int(last):
            errors.append(f"README progress range ends at SB-{m.group(1)} but project completed through SB-{last}")

for required in ["scripts/ci-project.sh","docs/development-plan.md"]:
    if required not in text:
        errors.append(f"README missing current project entrypoint/reference: {required}")

if errors:
    print("FAIL")
    for e in errors:
        print("-",e)
    sys.exit(1)
print("PASS: README current-state consistency checks")
