"""
Generates scripts/questions_bank/business_management.py
Compiling:
1. Project Management
2. Finance & Accounting
3. Human Resource Management
4. Procurement & GeM
5. Digital Governance
"""
import os
import sys

# Ensure scripts dir is on sys.path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

import data_project_mgmt as pm
import data_finance_acc as fa
import data_hrm as hr
import data_procurement_gem as gem
import data_digital_gov as dg

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
    out_path = os.path.join(scripts_dir, "questions_bank", "business_management.py")
    
    header = '''"""
Module: business_management.py
Contains 100 authentic questions each (34 Easy, 33 Medium, 33 Hard) for:
1. Project Management
2. Finance & Accounting
3. Human Resource Management
4. Procurement & GeM
5. Digital Governance
"""
from scripts.question_helpers import make_q

'''
    funcs = [
        format_qs("project_management", pm.pm_easy, pm.pm_med, pm.pm_hard),
        format_qs("finance_accounting", fa.fin_easy, fa.fin_med, fa.fin_hard),
        format_qs("human_resource_management", hr.hrm_easy, hr.hrm_med, hr.hrm_hard),
        format_qs("procurement_gem", gem.gem_easy, gem.gem_med, gem.gem_hard),
        format_qs("digital_governance", dg.dg_easy, dg.dg_med, dg.dg_hard),
    ]
    
    content = header + "\n".join(funcs)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated {out_path} ({len(content)} chars)")

if __name__ == "__main__":
    build()
