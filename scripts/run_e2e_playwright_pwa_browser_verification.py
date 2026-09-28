#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, yaml

def evaluate(case):
    i=case["input"]
    if i.get("browser_test_ran") and i.get("browser_test_failed"):
        return {
            "classification":"project_failure",
            "deferred":False,
            "project_failure":True,
            "allow_development":False,
            "browser_pass":False,
            "ci_fallback":False,
        }

    if not i.get("browser_binary_available") and not i.get("browser_install_possible"):
        if i.get("github_available") and not i.get("ci_version_matches_project"):
            return {
                "classification":"ci_configuration_error",
                "deferred":True,
                "project_failure":False,
                "allow_development":True,
                "browser_pass":False,
                "ci_fallback":False,
            }
        if i.get("pwa_release_critical"):
            return {
                "classification":"release_blocked_browser_evidence",
                "deferred":True,
                "project_failure":False,
                "allow_development":True,
                "browser_pass":False,
                "ci_fallback":bool(i.get("github_available")),
                "release_ready":False,
            }
        return {
            "classification":"environment_limited",
            "deferred":True,
            "project_failure":False,
            "allow_development":True,
            "browser_pass":False,
            "ci_fallback":bool(i.get("github_available")),
        }

    return {
        "classification":"passed",
        "deferred":False,
        "project_failure":False,
        "allow_development":True,
        "browser_pass":True,
        "ci_fallback":False,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--scenario",required=True)
    args=ap.parse_args()
    data=yaml.safe_load(Path(args.scenario).read_text(encoding="utf-8"))
    errors=[]
    for case in data.get("cases",[]):
        actual=evaluate(case)
        for key,value in case["expected"].items():
            if actual.get(key)!=value:
                errors.append(f'{case["id"]}: {key} expected={value!r} actual={actual.get(key)!r}')
    if errors:
        print("FAIL")
        for e in errors:
            print("-",e)
        return 1
    print(f'PASS: Playwright/PWA browser verification policy ({len(data.get("cases",[]))} cases)')
    return 0

if __name__=="__main__":
    sys.exit(main())
