"""
Generates scripts/questions_bank/governance_law.py
Compiling:
1. Public Policy
2. Public Administration
3. Administrative Law
4. Legal & Constitutional topics
5. Government schemes and programmes
"""
import os
import sys

# Ensure scripts dir is on sys.path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

import data_public_policy as pp
import data_pub_admin as pa
import data_admin_law as al
import data_legal_const as lc
import data_gov_schemes as gs

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
    out_path = os.path.join(scripts_dir, "questions_bank", "governance_law.py")
    
    header = '''"""
Module: governance_law.py
Contains 100 authentic questions each (34 Easy, 33 Medium, 33 Hard) for:
1. Public Policy
2. Public Administration
3. Administrative Law
4. Legal & Constitutional topics
5. Government schemes and programmes
"""
from scripts.question_helpers import make_q

'''
    funcs = [
        format_qs("public_policy", pp.policy_easy, pp.policy_med, pp.policy_hard),
        format_qs("public_administration", pa.admin_easy, pa.admin_med, pa.admin_hard),
        format_qs("administrative_law", al.admin_law_easy, al.admin_law_med, al.admin_law_hard),
        format_qs("legal_constitutional", lc.legal_easy, lc.legal_med, lc.legal_hard),
        format_qs("government_schemes", gs.schemes_easy, gs.schemes_med, gs.schemes_hard),
    ]
    
    content = header + "\n".join(funcs)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated {out_path} ({len(content)} chars)")

if __name__ == "__main__":
    build()
