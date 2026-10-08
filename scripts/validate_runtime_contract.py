#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / 'runtime' / 'runtime-contract.json'
SCHEMAS = {
    'behavior': ROOT / 'schemas' / 'behavior-contract.schema.json',
    'capabilities': ROOT / 'schemas' / 'capability-contract.schema.json',
    'artifacts': ROOT / 'schemas' / 'artifact-contract.schema.json',
    'workspace_state': ROOT / 'schemas' / 'workspace-state-contract.schema.json',
    'tools': ROOT / 'schemas' / 'tool-contract.schema.json',
}

def load_json(path: Path):
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)

def validate_component(name: str, value: dict) -> None:
    Draft202012Validator(load_json(SCHEMAS[name])).validate(value)

def main() -> int:
    contract = load_json(CONTRACT)
    if contract.get('schema_version') != 1:
        raise SystemExit('FAIL: runtime contract schema_version must be 1')
    if contract.get('runtime_id') != 'system-builder':
        raise SystemExit('FAIL: runtime_id must be system-builder')
    for name in SCHEMAS:
        if name not in contract:
            raise SystemExit(f'FAIL: missing runtime contract component: {name}')
        validate_component(name, contract[name])
    discovery = contract['capabilities'].get('discovery', {})
    for key in ('result_schema', 'canonical_reference'):
        rel = discovery.get(key)
        if not rel or not (ROOT / rel).is_file():
            raise SystemExit(f'FAIL: capability discovery {key} missing or unreadable: {rel}')
    routing = contract['capabilities'].get('routing', {})
    for key in ('decision_schema', 'canonical_reference'):
        rel = routing.get(key)
        if not rel or not (ROOT / rel).is_file():
            raise SystemExit(f'FAIL: execution routing {key} missing or unreadable: {rel}')
    if routing.get('selection_rule') != 'simplest_profile_that_satisfies_required_capabilities':
        raise SystemExit('FAIL: execution routing selection rule mismatch')
    agent_workspace = contract['capabilities'].get('agent_workspace', {})
    for key in ('canonical_reference', 'evidence_schema'):
        rel = agent_workspace.get(key)
        if not rel or not (ROOT / rel).is_file():
            raise SystemExit(f'FAIL: Agent Workspace {key} missing or unreadable: {rel}')
    pwa_preview = contract['capabilities'].get('pwa_preview', {})
    for key in ('canonical_reference', 'evidence_schema'):
        rel = pwa_preview.get(key)
        if not rel or not (ROOT / rel).is_file():
            raise SystemExit(f'FAIL: PWA Preview {key} missing or unreadable: {rel}')
    browser_screenshot = contract['capabilities'].get('browser_screenshot', {})
    for key in ('canonical_reference', 'evidence_schema'):
        rel = browser_screenshot.get(key)
        if not rel or not (ROOT / rel).is_file():
            raise SystemExit(f'FAIL: Browser Screenshot {key} missing or unreadable: {rel}')
    if browser_screenshot.get('default_preset') != 'desktop':
        raise SystemExit('FAIL: Browser Screenshot default preset must be desktop')
    if browser_screenshot.get('screenshot_is_functional_verification') is not False:
        raise SystemExit('FAIL: Browser Screenshot cannot count as functional verification')
    if pwa_preview.get('preview_is_functional_verification') is not False:
        raise SystemExit('FAIL: PWA Preview cannot count as functional verification')
    if pwa_preview.get('preview_is_production_deployment') is not False:
        raise SystemExit('FAIL: PWA Preview cannot count as production deployment')
    if agent_workspace.get('github_policy') != 'prefer_github_actions_when_sufficient':
        raise SystemExit('FAIL: Agent Workspace must prefer GitHub Actions when sufficient')
    if agent_workspace.get('redundant_execution_forbidden') is not True:
        raise SystemExit('FAIL: redundant Agent Workspace execution must be forbidden')
    instruction_path = ROOT / contract['behavior']['canonical_instruction']
    if not instruction_path.is_file():
        raise SystemExit(f'FAIL: canonical instruction missing: {instruction_path.relative_to(ROOT)}')
    instruction = instruction_path.read_text(encoding='utf-8')
    missing = [m for m in contract['behavior']['required_markers'] if m not in instruction]
    if missing:
        raise SystemExit('FAIL: canonical behavior markers missing: ' + ', '.join(missing))
    state = contract['workspace_state']['state']
    if state['authority'] != 'workspace_file' or state.get('conversation_fallback'):
        raise SystemExit('FAIL: workspace state must be authoritative with no conversation fallback')
    tool_ids = [tool['id'] for tool in contract['tools']['tools']]
    if len(tool_ids) != len(set(tool_ids)):
        raise SystemExit('FAIL: duplicate tool ids')
    required_tools = {tool['id'] for tool in contract['tools']['tools'] if tool['requirement'] == 'required'}
    if not {'workspace-read', 'workspace-write', 'run-verification'}.issubset(required_tools):
        raise SystemExit('FAIL: critical required tools are missing')
    invalid = copy.deepcopy(contract['capabilities'])
    invalid.pop('requirements')
    try:
        validate_component('capabilities', invalid)
    except ValidationError:
        pass
    else:
        raise SystemExit('FAIL: invalid capability contract was not rejected')
    active = {name for name, cfg in contract['runtime_compatibility'].items() if cfg['status'] in {'implemented', 'planned'}}
    expected = {'chat_zip', 'custom_gpt', 'claude_projects', 'opencode', 'openai_plugin'}
    if active != expected:
        raise SystemExit(f'FAIL: unexpected active runtime set: {sorted(active)}')
    print('PASS: platform-neutral runtime contract is valid')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
