#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

KNOWLEDGE_FILES = [
    "knowledge/README.md",
    "knowledge/technology-patterns.md",
    "knowledge/platform-reference.md",
    "knowledge/terminology.md",
]

README = """# System Builder – Claude Projects Distribution

Use `project-instructions.md` as the Claude Project Instructions.

Upload the files under `knowledge/` plus `runtime-contract.json` and
`compatibility.md` to Project Knowledge when practical.

This runtime intentionally has **reduced parity**. The canonical behavior is
preserved, but local command execution, deterministic project verification,
workspace mutation and GitHub write actions cannot be assumed to exist in a
plain Claude Project. When a required capability is unavailable, report that
limitation explicitly and do not claim the corresponding action or verification
as completed.
"""

COMPATIBILITY = """# Claude Projects compatibility

Compatibility target: **reduced parity**.

## Preserved

- CREATE / CHANGE / IMPROVE / PLAN / REPAIR / RELEASE routing
- one safe development step per \"Gör nästa steg\" by default
- source/project state over conversation memory
- functional specification, architecture and development planning
- risk, security, test and release-readiness reasoning
- ZIP-oriented analysis and complete-project delivery when the environment can
  read and return files

## Runtime limitations

A plain Claude Project must not assume these runtime capabilities:

- **local command execution**
- **deterministic project verification**
- **workspace mutation**
- **GitHub write actions**

The runtime therefore has reduced parity, but it must preserve **canonical behavior**.
The project/repository state file remains the **workspace-file authority** for resume.

If a required capability is unavailable, the runtime must degrade honestly:
produce the artifacts it can and explicitly mark **unrun verification** as unrun.
It must never convert missing execution capability into a false PASS.
"""

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    instruction = root / "runtime" / "canonical-instructions.md"
    contract_path = root / "runtime" / "runtime-contract.json"
    execution_rules = root / "runtime" / "execution-rules.md"
    required = [instruction, execution_rules, contract_path] + [root / p for p in KNOWLEDGE_FILES]
    missing = [str(p.relative_to(root)) for p in required if not p.is_file()]
    if missing:
        raise FileNotFoundError("missing Claude Projects source files: " + ", ".join(missing))

    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    claude = contract["runtime_compatibility"]["claude_projects"]
    if claude["target"] != "reduced":
        raise ValueError("Claude Projects must declare reduced compatibility")

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("README.md", README)
        zf.writestr("project-instructions.md", instruction.read_text(encoding="utf-8"))\n        zf.write(execution_rules, "runtime/execution-rules.md")
        zf.writestr("runtime-contract.json", json.dumps(contract, indent=2) + "\n")
        zf.writestr("compatibility.md", COMPATIBILITY)
        for rel in KNOWLEDGE_FILES:
            zf.write(root / rel, rel)

    print(output)
    return 0

if __name__ == "__main__":
    sys.exit(main())
