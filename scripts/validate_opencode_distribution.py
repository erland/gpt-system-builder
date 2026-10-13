#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import zipfile

REQUIRED = {
    "README.md",
    "AGENTS.md",
    "opencode.json",
    ".opencode/runtime-contract.json",
    ".opencode/tool-mapping.json",
    ".opencode/tools/README.md",
    "knowledge/README.md",
    "knowledge/technology-patterns.md",
    "knowledge/platform-reference.md",
    "knowledge/terminology.md",
}

CORE_MARKERS = [
    "## 3. One-step rule",
    "actual current source and repository/project state",
    "Never report an unrun check as PASS",
    "ZIP is a first-class source/delivery mode",
    "GitHub is a first-class source mode",
]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("zipfile")
    args = ap.parse_args()
    errors = []

    with zipfile.ZipFile(args.zipfile, "r") as zf:
        bad = zf.testzip()
        if bad:
            errors.append(f"corrupt member: {bad}")
        names = set(zf.namelist())

        for req in sorted(REQUIRED):
            if req not in names:
                errors.append(f"missing {req}")

        if "CLAUDE.md" in names:
            errors.append("CLAUDE.md must not be used as OpenCode fallback")

        custom_tool_files = [
            n for n in names
            if n.startswith(".opencode/tools/")
            and n.endswith((".ts", ".js", ".py", ".sh"))
        ]
        if custom_tool_files:
            errors.append("undeclared custom script-tools generated: " + ", ".join(sorted(custom_tool_files)))

        if "AGENTS.md" in names:
            agents = zf.read("AGENTS.md").decode("utf-8")
            for marker in CORE_MARKERS:
                if marker not in agents:
                    errors.append(f"missing canonical behavior marker: {marker}")

        if "opencode.json" in names:
            config = json.loads(zf.read("opencode.json").decode("utf-8"))
            rules = config.get("permissions", [])
            effects = {(r.get("action"), r.get("resource")): r.get("effect") for r in rules}
            if effects.get(("edit", "*")) != "ask":
                errors.append("edit mutations must require approval")
            if effects.get(("shell", "*")) != "ask":
                errors.append("shell execution must require approval")
            for action in ("read", "glob", "grep"):
                if effects.get((action, "*")) != "allow":
                    errors.append(f"{action} should be allowed")

        if ".opencode/runtime-contract.json" in names:
            snap = json.loads(zf.read(".opencode/runtime-contract.json").decode("utf-8"))
            if snap.get("runtime") != "opencode":
                errors.append("wrong runtime snapshot")
            root = snap.get("project_root", {})
            if root.get("explicit_argument") != "projectRoot" or root.get("default") != ".":
                errors.append("projectRoot contract missing")
            if root.get("runtime_workspace_is_not_target_project") is not True:
                errors.append("runtime/target workspace separation missing")
            cfg = snap.get("canonical_contract", {}).get("runtime_compatibility", {}).get("opencode", {})
            if cfg.get("status") != "implemented":
                errors.append("OpenCode status must be implemented")
            if cfg.get("target") != "equivalent":
                errors.append("OpenCode target must be equivalent")

        if ".opencode/tool-mapping.json" in names:
            mapping = json.loads(zf.read(".opencode/tool-mapping.json").decode("utf-8"))
            tools = mapping.get("tools", {})
            expected = {
                "workspace-read",
                "workspace-write",
                "run-verification",
                "repository-actions",
                "package-project",
            }
            if set(tools) != expected:
                errors.append("tool mapping does not match canonical declared tool set")
            if tools.get("workspace-write", {}).get("approval") != "ask":
                errors.append("workspace-write approval must be ask")
            if tools.get("repository-actions", {}).get("approval") != "ask":
                errors.append("repository-actions approval must be ask")

    if errors:
        print("FAIL")
        for error in errors:
            print("-", error)
        return 1

    print("PASS: OpenCode distribution valid with AGENTS.md, projectRoot separation and approval policy")
    return 0

if __name__ == "__main__":
    sys.exit(main())
