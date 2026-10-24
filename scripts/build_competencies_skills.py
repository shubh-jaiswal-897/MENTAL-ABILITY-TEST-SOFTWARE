"""
Generates scripts/questions_bank/competencies_skills.py
Compiling:
1. Leadership & Self Leadership
2. Communication Skills
3. Behavioural competencies
4. Functional competencies
5. Domain-specific competencies
6. Health & Safety
7. Railways
"""
import os
import sys

# Ensure scripts dir is on sys.path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

import data_leadership as ld
import data_comm_skills as cs
import data_behavioural_comp as bc
import data_functional_comp as fc
import data_domain_comp as dc
import data_health_safety as hs
import data_railways as rl

def format_qs(name, easy_list, med_list, hard_list):
    lines = []
    lines.append(f"def get_{name}_questions():")
    lines.append("    qs = []")
    lines.append(f"    raw_easy = {repr(easy_list)}")
    lines.append("    for q, ca, wa, exp in raw_easy:")
    lines.append('        qs.append(make_q(q, ca, wa, "EASY", exp))')
    lines.append(f"    raw_med = {repr(med_list)}")
    lines.append("    for q, ca, wa, exp in raw_med:")
    lines.append('        qs.append(make_q(q, ca, wa, "MEDIUM", exp))')
    lines.append(f"    raw_hard = {repr(hard_list)}")
    lines.append("    for q, ca, wa, exp in raw_hard:")
    lines.append('        qs.append(make_q(q, ca, wa, "HARD", exp))')
    lines.append("    return qs\n")
    return "\n".join(lines)

def build():
    out_path = os.path.join(scripts_dir, "questions_bank", "competencies_skills.py")
    
    header = '''"""
Module: competencies_skills.py
Contains 100 authentic questions each (34 Easy, 33 Medium, 33 Hard) for:
1. Leadership & Self Leadership
2. Communication Skills
3. Behavioural competencies
4. Functional competencies
5. Domain-specific competencies
6. Health & Safety
7. Railways
"""
from scripts.question_helpers import make_q

'''
    funcs = [
        format_qs("leadership_self_leadership", ld.lead_easy, ld.lead_med, ld.lead_hard),
        format_qs("communication_skills", cs.comm_easy, cs.comm_med, cs.comm_hard),
        format_qs("behavioural_competencies", bc.beh_easy, bc.beh_med, bc.beh_hard),
        format_qs("functional_competencies", fc.func_easy, fc.func_med, fc.func_hard),
        format_qs("domain_specific_competencies", dc.dom_easy, dc.dom_med, dc.dom_hard),
        format_qs("health_safety", hs.hs_easy, hs.hs_med, hs.hs_hard),
        format_qs("railways", rl.rail_easy, rl.rail_med, rl.rail_hard),
    ]
    
    content = header + "\n".join(funcs)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated {out_path} ({len(content)} chars)")

if __name__ == "__main__":
    build()
