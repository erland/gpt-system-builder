#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, yaml

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('file'); a=ap.parse_args(); p=Path(a.file)
    try: data=yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception as e:
        print('FAIL: YAML parse:',e); return 1
    errs=[]
    on=data.get('on',data.get(True))
    if not isinstance(on,dict): errs.append('missing mapping: on')
    else:
        if 'pull_request' not in on: errs.append('missing pull_request trigger')
        push=on.get('push')
        if not isinstance(push,dict) or not push.get('branches'): errs.append('push trigger must target explicit branch(es)')
    perms=data.get('permissions')
    if not isinstance(perms,dict): errs.append('explicit permissions mapping required')
    elif perms.get('contents')!='read': errs.append('baseline should use contents: read')
    jobs=data.get('jobs')
    if not isinstance(jobs,dict) or not jobs: errs.append('at least one job required')
    else:
        checkout=verify=timeout=False
        for job in jobs.values():
            if not isinstance(job,dict): continue
            timeout=timeout or bool(job.get('timeout-minutes'))
            for step in job.get('steps',[]):
                if not isinstance(step,dict): continue
                checkout=checkout or str(step.get('uses','')).startswith('actions/checkout@')
                verify=verify or ('run' in step)
        if not checkout: errs.append('actions/checkout step missing')
        if not verify: errs.append('verification run step missing')
        if not timeout: errs.append('job timeout missing')
    text=p.read_text(encoding='utf-8')
    for f in ['permissions: write-all','curl | sh']:
        if f in text: errs.append(f'forbidden pattern: {f}')
    if errs:
        print('FAIL'); [print('-',e) for e in errs]; return 1
    print('PASS: GitHub Actions baseline valid'); return 0
if __name__=='__main__': sys.exit(main())
