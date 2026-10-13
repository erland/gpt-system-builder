#!/usr/bin/env python3
"""Validate canonical distribution targets; legacy target IDs are not active."""
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
reg=yaml.safe_load((ROOT/'runtime/distribution-registry.yaml').read_text())
project=yaml.safe_load((ROOT/'gpt-project.yaml').read_text())
expected=project['build_system']['targets']
active=reg['active_targets']
assert reg['schema_version']==2
assert len(active)==len(set(active)) and active==expected,(active,expected)
assert set(active)=={'project','chat','claude_project','claude_skills','opencode','plugin'}
assert all((ROOT/reg[key]).is_file() for key in ('builder','validator'))
assert not any(x in active for x in ('custom_gpt','claude_projects','openai_plugin'))
print('PASS: canonical distribution registry synchronized with gpt-project.yaml')
