#!/usr/bin/env python3
from pathlib import Path
import argparse, zipfile, yaml, sys
FILES=[
"runtime/canonical-instructions.md","runtime/runtime-manifest.yaml",
"docs/create-mode.md","docs/change-mode.md","docs/improve-mode.md","docs/next-step-state-machine.md",
"docs/zip-mode.md","docs/github-mode.md","docs/release-readiness-standard.md",
"docs/functional-specification-standard.md","docs/architecture-standard.md","docs/decision-records-standard.md",
"docs/development-plan-standard.md","docs/risk-feasibility-standard.md","docs/test-verification-standard.md",
"docs/security-baseline.md","docs/project-complexity.md","docs/document-state-architecture.md",
"docs/deployment-packaging-patterns.md","docs/docker-baseline.md","docs/coolify-profile.md",
"docs/configuration-installation-operations-standard.md","docs/repository-hygiene.md",
"docs/github-actions-baseline.md","docs/knowledge-architecture.md","knowledge/README.md",
"knowledge/technology-patterns.md","knowledge/platform-reference.md","knowledge/terminology.md",
"schemas/project.schema.json","schemas/work-status.schema.json","schemas/traceability.schema.json",
"schemas/deployment-profile.schema.json"]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--project-root",required=True); ap.add_argument("--output",required=True); a=ap.parse_args()
    root=Path(a.project_root); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    manifest={"name":"System Builder","distribution":"chat_zip","version":(root/"VERSION").read_text().strip(),
      "entrypoint":"runtime/canonical-instructions.md","runtime_manifest":"runtime/runtime-manifest.yaml",
      "knowledge_index":"knowledge/README.md",
      "behavior_contract":{"one_completed_step_per_run_default":True,"source_state_over_chat_memory":True,
      "critical_behavior_in_knowledge_only":False,"false_pass_forbidden":True,"zip_mode":True,"github_mode":True},
      "included_files":sorted(["README.md"]+FILES)}
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.md","# System Builder – Chat ZIP Runtime\n\nEntry point: `runtime/canonical-instructions.md`\n")
        z.writestr("chat-runtime-manifest.yaml",yaml.safe_dump(manifest,sort_keys=False,allow_unicode=True))
        for rel in FILES:
            p=root/rel
            if not p.exists(): raise FileNotFoundError(rel)
            z.write(p,rel)
    print(out); return 0
if __name__=="__main__": sys.exit(main())
