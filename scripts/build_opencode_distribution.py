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

README = """# System Builder – OpenCode Distribution

This package is an OpenCode workspace runtime for System Builder.

## Usage

1. Extract the ZIP into a dedicated OpenCode workspace.
2. Open the workspace root in OpenCode.
3. OpenCode V2 loads root `AGENTS.md` as project instructions.
4. Place the software project to work on in a subdirectory such as `project/`,
   or use another explicit relative `projectRoot`.
5. The System Builder runtime workspace and the target software project are
   separate concepts. The runtime ZIP does not itself represent the target
   project's canonical state.
6. `.opencode/runtime-contract.json` is a generated adapter snapshot.
7. `.opencode/tool-mapping.json` maps canonical tool capabilities to OpenCode
   built-ins. No undeclared custom script-tools are generated.
8. `opencode.json` requires approval for mutations and shell execution.

Generated adapter files are runtime projections, never canonical source.
"""

TOOL_README = """# OpenCode tools

System Builder currently declares abstract runtime capabilities rather than
concrete script-tools. Therefore this distribution intentionally generates no
custom TypeScript tool wrappers.

The effective mapping is recorded in `../tool-mapping.json`:

- workspace-read -> read / glob / grep
- workspace-write -> edit / write / apply_patch
- run-verification -> shell, with approval
- repository-actions -> shell-based Git/GitHub operations, with approval
- package-project -> shell-based project packaging, with approval

If concrete canonical script-tools are added later, only those declared tools
may be projected into this directory.
"""

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    instruction_path = root / "runtime" / "canonical-instructions.md"
    contract_path = root / "runtime" / "runtime-contract.json"
    execution_rules = root / "runtime" / "execution-rules.md"\n    required = [instruction_path, execution_rules, contract_path] + [root / p for p in KNOWLEDGE_FILES]
    missing = [str(p.relative_to(root)) for p in required if not p.is_file()]
    if missing:
        raise FileNotFoundError("missing OpenCode source files: " + ", ".join(missing))

    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    opencode_cfg = contract["runtime_compatibility"]["opencode"]
    if opencode_cfg["target"] != "equivalent":
        raise ValueError("OpenCode target must be equivalent")

    snapshot = {
        "schema_version": 1,
        "runtime": "opencode",
        "role": "peer_distribution",
        "mode": "opencode_workspace",
        "canonical_source": {
            "instructions": "runtime/canonical-instructions.md",
            "contract": "runtime/runtime-contract.json",
        },
        "generated_projection": {
            "instructions": "AGENTS.md",
            "runtime_contract": ".opencode/runtime-contract.json",
            "knowledge": "knowledge/",
            "config": "opencode.json",
            "tools": ".opencode/tools/",
        },
        "project_root": {
            "explicit_argument": "projectRoot",
            "default": ".",
            "runtime_workspace_is_not_target_project": True,
        },
        "tool_policy": {
            "custom_script_tools": [],
            "reason": "No concrete script tools are declared in the canonical tool contract.",
            "mapping_file": ".opencode/tool-mapping.json",
        },
        "canonical_contract": contract,
    }

    tool_mapping = {
        "schema_version": 1,
        "projectRoot": {
            "type": "relative_path",
            "default": ".",
            "description": "Target project relative to the OpenCode runtime workspace.",
        },
        "tools": {
            "workspace-read": {
                "canonical_requirement": "required",
                "opencode_tools": ["read", "glob", "grep"],
                "mutating": False,
            },
            "workspace-write": {
                "canonical_requirement": "required",
                "opencode_tools": ["edit", "write", "apply_patch"],
                "mutating": True,
                "approval": "ask",
            },
            "run-verification": {
                "canonical_requirement": "required",
                "opencode_tools": ["shell"],
                "mutating": False,
                "approval": "ask",
            },
            "repository-actions": {
                "canonical_requirement": "recommended",
                "opencode_tools": ["shell"],
                "mutating": True,
                "approval": "ask",
            },
            "package-project": {
                "canonical_requirement": "recommended",
                "opencode_tools": ["shell"],
                "mutating": False,
                "approval": "ask",
            },
        },
    }

    config = {
        "$schema": "https://opencode.ai/config.json",
        "permissions": [
            {"action": "read", "resource": "*", "effect": "allow"},
            {"action": "glob", "resource": "*", "effect": "allow"},
            {"action": "grep", "resource": "*", "effect": "allow"},
            {"action": "webfetch", "resource": "*", "effect": "allow"},
            {"action": "websearch", "resource": "*", "effect": "allow"},
            {"action": "question", "resource": "*", "effect": "allow"},
            {"action": "edit", "resource": "*", "effect": "ask"},
            {"action": "shell", "resource": "*", "effect": "ask"},
            {"action": "external_directory", "resource": "*", "effect": "ask"},
        ],
    }

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("README.md", README)
        zf.writestr("AGENTS.md", instruction_path.read_text(encoding="utf-8"))\n        zf.write(execution_rules, "runtime/execution-rules.md")
        zf.writestr("opencode.json", json.dumps(config, indent=2) + "\n")
        zf.writestr(".opencode/runtime-contract.json", json.dumps(snapshot, indent=2) + "\n")
        zf.writestr(".opencode/tool-mapping.json", json.dumps(tool_mapping, indent=2) + "\n")
        zf.writestr(".opencode/tools/README.md", TOOL_README)
        for rel in KNOWLEDGE_FILES:
            zf.write(root / rel, rel)

    print(output)
    return 0

if __name__ == "__main__":
    sys.exit(main())
