#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

REFERENCES = [
    "runtime/execution-rules.md",
    "docs/create-mode.md",
    "docs/change-mode.md",
    "docs/improve-mode.md",
    "docs/next-step-state-machine.md",
    "docs/completion-verification.md",
    "docs/zip-mode.md",
    "docs/github-mode.md",
    "docs/release-readiness-standard.md",
    "docs/test-verification-standard.md",
    "docs/security-baseline.md",
    "knowledge/technology-patterns.md",
    "knowledge/platform-reference.md",
    "knowledge/terminology.md",
]

ASSETS = [
    "templates/functional-specification-template.md",
    "templates/architecture-template.md",
    "templates/development-plan-template.md",
    "templates/test-strategy-template.md",
    "templates/release-readiness-template.md",
]

README = """# System Builder – OpenAI Plugin Distribution

This is the skills-first OpenAI Plugin distribution for System Builder.

The plugin preserves System Builder's canonical behavior and packages references and
assets needed for system-development work. It is intentionally **host-dependent**:
the plugin package does not itself provision a writable workspace, code execution,
persistent state, or GitHub/repository tools.

When the host provides those capabilities, System Builder should use them. When a
required capability is unavailable, the operation must be blocked or degraded
according to the runtime contract. Never simulate verification or report an unrun
check as PASS.

The canonical project/repository state remains authoritative over chat memory.
"""

COMPATIBILITY = """# OpenAI Plugin compatibility

Compatibility target: **reduced / host-dependent parity**.

## Preserved

- canonical System Builder behavior and operating modes
- one safe development step by default
- source/project state over conversation memory
- no false PASS for unrun verification
- specification, architecture, planning, risk, security and release-readiness workflows
- ZIP and GitHub source-mode semantics when the host exposes the required capabilities

## Host requirements

The plugin requires or conditionally relies on host capabilities for:

- filesystem read/write
- code execution for real build/test/verification work
- persistent workspace/state
- repository/GitHub integration in GitHub source mode
- project packaging in ZIP source mode

The package does not synthesize these abstract API actions as fake local tools.
Use the host's available capabilities. If a required capability is missing, report
that limitation explicitly and follow the declared fallback; do not pretend the
operation ran.
"""

SKILL_HEADER = """---
name: system-builder
description: Develop new and existing software systems from need or change request through specification, architecture, implementation, verification, packaging and release readiness.
metadata:
  source: generated-from-canonical-project
---

## Runtime requirements

- Filesystem read: required.
- Filesystem write: required.
- Code execution: required for implementation verification and deterministic checks.
- Persistent project/workspace state: required.
- Repository/GitHub capability: conditionally required in GitHub source mode.
- Project packaging capability: conditionally required in ZIP source mode.
- If a required capability is unavailable, block or degrade honestly according to the runtime contract.
- Never simulate a deterministic verification result and never report an unrun check as PASS.

## Canonical behavior

"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--output", required=True)
    ap.add_argument("--version", required=True)
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    instruction = root / "runtime" / "canonical-instructions.md"
    contract_path = root / "runtime" / "runtime-contract.json"
    required = [instruction, contract_path] + [root / p for p in REFERENCES + ASSETS]
    missing = [str(p.relative_to(root)) for p in required if not p.is_file()]
    if missing:
        raise FileNotFoundError("missing Plugin source files: " + ", ".join(missing))

    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    plugin_cfg = contract["runtime_compatibility"]["openai_plugin"]
    if plugin_cfg["status"] != "implemented":
        raise ValueError("OpenAI Plugin runtime must be implemented")
    if plugin_cfg["target"] not in {"reduced", "host_dependent"}:
        raise ValueError("OpenAI Plugin target must remain reduced/host-dependent")

    runtime_requirements = {
        "filesystem": {"read": "required", "write": "required"},
        "code_execution": {
            "level": "required",
            "fallback": "block",
            "reason": "Implementation and required verification must be executable rather than prose-only.",
        },
        "persistent_state": {
            "level": "required",
            "authority": ".system-builder/work-status.yaml",
            "fallback": "block",
        },
        "repository": {
            "level": "conditional",
            "condition": "github_source_mode",
            "fallback": "manual",
        },
        "project_packaging": {
            "level": "conditional",
            "condition": "zip_source_mode",
            "fallback": "manual",
        },
    }

    plugin_manifest = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": "system-builder",
        "version": args.version,
        "description": "System Builder skills-first plugin for end-to-end software system development.",
    }

    snapshot = {
        "schema_version": 1,
        "runtime_id": "openai_plugin",
        "role": "peer_distribution",
        "mode": "skills_first",
        "canonical_source": {
            "instructions": "runtime/canonical-instructions.md",
            "contract": "runtime/runtime-contract.json",
        },
        "runtime_requirements": runtime_requirements,
        "tool_projection": {
            "strategy": "host_capability_mapping",
            "mcp_generated": False,
            "declared_tools": contract["tools"]["tools"],
            "note": "Canonical api_action tools are mapped to host capabilities when available; no fake wrappers are generated.",
        },
        "canonical_contract": contract,
    }

    skill_text = SKILL_HEADER + instruction.read_text(encoding="utf-8").strip() + "\n\n"
    skill_text += "## References\n\n"
    for rel in REFERENCES:
        skill_text += f"- Read `references/{Path(rel).name}` when relevant.\n"
    skill_text += "\n## Assets\n\n"
    for rel in ASSETS:
        skill_text += f"- Use `assets/{Path(rel).name}` when that template is useful.\n"

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("plugin.json", json.dumps(plugin_manifest, indent=2) + "\n")
        zf.writestr("README.md", README)
        zf.writestr("compatibility.md", COMPATIBILITY)
        zf.writestr("runtime-contract.json", json.dumps(snapshot, indent=2) + "\n")
        zf.writestr("skills/system-builder/SKILL.md", skill_text)
        for rel in REFERENCES:
            zf.write(root / rel, f"skills/system-builder/references/{Path(rel).name}")
        for rel in ASSETS:
            zf.write(root / rel, f"skills/system-builder/assets/{Path(rel).name}")

    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
