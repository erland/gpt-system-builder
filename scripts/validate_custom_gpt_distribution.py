#!/usr/bin/env python3
import argparse,zipfile,yaml,sys
CORE=["one safe development step","actual current source","never report an unrun check as pass","complete project zip","reuse active pr","postgresql server must not be embedded","ready_with_warnings"]
CORE_ALTERNATIVES=[("knowledge is reference material","knowledge is reference")]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("zipfile"); a=ap.parse_args(); errs=[]
    with zipfile.ZipFile(a.zipfile,"r") as z:
        bad=z.testzip()
        if bad: errs.append(f"corrupt member: {bad}")
        names=set(z.namelist())
        for req in ["README.md","instructions.txt","custom-gpt.yaml"]:
            if req not in names: errs.append(f"missing {req}")
        k=[n for n in names if n.startswith("knowledge/") and n.endswith(".md")]
        if not k: errs.append("no Knowledge files")
        if len(k)>20: errs.append(f"too many Knowledge files: {len(k)}")
        text=z.read("instructions.txt").decode("utf-8")
        low=text.lower()
        if len(text)>8000: errs.append(f"instructions exceed 8000 chars: {len(text)}")
        if len(text)<4000: errs.append("instructions unexpectedly short")
        for phrase in CORE:
            if phrase not in low: errs.append(f"missing core phrase: {phrase}")
        for alternatives in CORE_ALTERNATIVES:
            if not any(phrase in low for phrase in alternatives): errs.append("missing core knowledge-reference rule")
        data=yaml.safe_load(z.read("custom-gpt.yaml").decode("utf-8"))
        if data.get("distribution")!="custom_gpt": errs.append("wrong distribution")
        if data.get("instruction_characters")!=len(text): errs.append("instruction char count mismatch")
        cp=data.get("capability_parity",{})
        if cp.get("capability_aware_execution")!="reduced": errs.append("Custom GPT capability-aware parity must be reduced")
        if cp.get("companion_integrations")!="not_guaranteed": errs.append("Custom GPT companion integration support must be explicitly non-guaranteed")
        if cp.get("core_safety_invariants_preserved") is not True: errs.append("Custom GPT must preserve core safety invariants")
        b=data.get("behavior_contract",{})
        if b.get("one_completed_step_per_run_default") is not True: errs.append("one-step behavior missing")
        if b.get("critical_behavior_in_knowledge_only") is not False: errs.append("critical behavior must not be Knowledge-only")
    if errs:
        print("FAIL")
        for e in errs: print("-",e)
        return 1
    print(f"PASS: Custom GPT distribution valid ({len(text)} instruction chars, {len(k)} Knowledge files)")
    return 0
if __name__=="__main__": sys.exit(main())
