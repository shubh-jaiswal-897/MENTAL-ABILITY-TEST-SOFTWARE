"""
Builds scripts/questions_bank/humanities.py with 100 questions each for:
1. History
2. Geography
3. Political Science
4. Sociology
5. Languages
"""
import os
import sys

def build():
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions_bank", "humanities.py")

    from scripts.data_history import hist_easy, hist_med, hist_hard
    from scripts.data_geo import geo_easy, geo_med, geo_hard
    from scripts.data_pol_sci import pol_sci_easy, pol_sci_med, pol_sci_hard
    from scripts.data_sociology import soc_easy, soc_med, soc_hard
    from scripts.data_languages import lang_easy, lang_med, lang_hard

    subjects_code = [
        ("history", hist_easy, hist_med, hist_hard),
        ("geography", geo_easy, geo_med, geo_hard),
        ("political_science", pol_sci_easy, pol_sci_med, pol_sci_hard),
        ("sociology", soc_easy, soc_med, soc_hard),
        ("languages", lang_easy, lang_med, lang_hard),
    ]

    with open(out_path, "w", encoding="utf-8") as f:
        f.write('"""\nModule: humanities.py\nGenerates 100 authentic questions (34 Easy, 33 Medium, 33 Hard) for:\n1. History\n2. Geography\n3. Political Science\n4. Sociology\n5. Languages\n"""\n')
        f.write('from scripts.question_helpers import make_q\n\n')

        for func_sub, e, m, h in subjects_code:
            f.write(f"def get_{func_sub}_questions():\n")
            f.write("    qs = []\n")
            
            f.write(f"    raw_easy = {repr(e)}\n")
            f.write('    for q, ca, wa, exp in raw_easy:\n')
            f.write('        qs.append(make_q(q, ca, wa, "EASY", exp))\n\n')

            f.write(f"    raw_med = {repr(m)}\n")
            f.write('    for q, ca, wa, exp in raw_med:\n')
            f.write('        qs.append(make_q(q, ca, wa, "MEDIUM", exp))\n\n')

            f.write(f"    raw_hard = {repr(h)}\n")
            f.write('    for q, ca, wa, exp in raw_hard:\n')
            f.write('        qs.append(make_q(q, ca, wa, "HARD", exp))\n\n')

            f.write("    return qs\n\n")

    print(f"Successfully generated {out_path} with 5 subjects (500 questions)!")

if __name__ == "__main__":
    build()
