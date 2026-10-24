"""
Master Seeding Script: 3,600 Authentic, Real Questions across 36 Subjects.
Populates:
1. Local SQLite database (testmybrain default)
2. Remote Supabase PostgreSQL database (production)

Exact Requirements:
- Exactly 36 subjects (100% matched with Supabase subject catalog)
- Exactly 100 authentic questions per subject (34 Easy, 33 Medium, 33 Hard)
- Exactly 4 realistic options per question (shuffled to randomize correct answer position)
- Educational step-by-step logic explanations for every question
- Total Questions = 3,600
- Total Choices = 14,400
- NO demo questions, NO dummy options ("Option A", etc.)
"""
import os
import sys
import random
import time
import django

# Set up Django environment for Local SQLite
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testmybrain.settings")
django.setup()

from django.db import transaction, connection
from quiz.models import Subject as DjangoSubject, Question as DjangoQuestion, Choice as DjangoChoice

# Import all question generators from questions_bank
from scripts.questions_bank.sciences import (
    get_mathematics_questions,
    get_physics_questions,
    get_chemistry_questions,
    get_biology_questions,
)
from scripts.questions_bank.engineering_it import (
    get_ai_emerging_tech_questions,
    get_data_analytics_questions,
    get_statistics_questions,
    get_web_designing_questions,
    get_cyber_safety_questions,
    get_office_tools_questions,
)
from scripts.questions_bank.entrance_exams import (
    get_upsc_preparation_questions,
    get_jee_preparation_questions,
    get_neet_preparation_questions,
    get_gate_preparation_questions,
)
from scripts.questions_bank.humanities import (
    get_history_questions,
    get_geography_questions,
    get_political_science_questions,
    get_sociology_questions,
    get_languages_questions,
)
from scripts.questions_bank.governance_law import (
    get_public_policy_questions,
    get_public_administration_questions,
    get_administrative_law_questions,
    get_legal_constitutional_questions,
    get_government_schemes_questions,
)
from scripts.questions_bank.business_management import (
    get_project_management_questions,
    get_finance_accounting_questions,
    get_human_resource_management_questions,
    get_procurement_gem_questions,
    get_digital_governance_questions,
)
from scripts.questions_bank.competencies_skills import (
    get_leadership_self_leadership_questions,
    get_communication_skills_questions,
    get_behavioural_competencies_questions,
    get_functional_competencies_questions,
    get_domain_specific_competencies_questions,
    get_health_safety_questions,
    get_railways_questions,
)

# Complete mapping of all 36 subjects to their generator functions
SUBJECT_GENERATOR_MAP = [
    # Sciences (4)
    ("Mathematics", get_mathematics_questions),
    ("Physics", get_physics_questions),
    ("Chemistry", get_chemistry_questions),
    ("Biology", get_biology_questions),

    # Engineering & IT (6)
    ("Artificial Intelligence & Emerging Technologies", get_ai_emerging_tech_questions),
    ("Data & Data Analytics", get_data_analytics_questions),
    ("Statistics and data-related learning", get_statistics_questions),
    ("Web designing", get_web_designing_questions),
    ("Cyber/Digital Safety", get_cyber_safety_questions),
    ("Office/IT productivity tools", get_office_tools_questions),

    # Entrance Exams (4)
    ("UPSC Preparation", get_upsc_preparation_questions),
    ("JEE Preparation", get_jee_preparation_questions),
    ("NEET Preparation", get_neet_preparation_questions),
    ("GATE Preparation", get_gate_preparation_questions),

    # Humanities (5)
    ("History", get_history_questions),
    ("Geography", get_geography_questions),
    ("Political Science", get_political_science_questions),
    ("Sociology", get_sociology_questions),
    ("Languages", get_languages_questions),

    # Governance & Law (5)
    ("Public Policy", get_public_policy_questions),
    ("Public Administration", get_public_administration_questions),
    ("Administrative Law", get_administrative_law_questions),
    ("Legal & Constitutional topics", get_legal_constitutional_questions),
    ("Government schemes and programmes", get_government_schemes_questions),

    # Business & Management (5)
    ("Project Management", get_project_management_questions),
    ("Finance & Accounting", get_finance_accounting_questions),
    ("Human Resource Management", get_human_resource_management_questions),
    ("Procurement & GeM", get_procurement_gem_questions),
    ("Digital Governance", get_digital_governance_questions),

    # Competencies & Specialized Operations (7)
    ("Leadership & Self Leadership", get_leadership_self_leadership_questions),
    ("Communication Skills", get_communication_skills_questions),
    ("Behavioural competencies", get_behavioural_competencies_questions),
    ("Functional competencies", get_functional_competencies_questions),
    ("Domain-specific competencies", get_domain_specific_competencies_questions),
    ("Health & Safety", get_health_safety_questions),
    ("Railways", get_railways_questions),
]

def seed_local():
    print("\n" + "=" * 70)
    print("STEP 1: SEEDING LOCAL SQLITE DATABASE")
    print("=" * 70)
    start_time = time.time()
    
    rnd = random.Random(42)

    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM quiz_contest_questions;")
        DjangoChoice.objects.all().delete()
        DjangoQuestion.objects.all().delete()

        # Align Local Subject records to match the 36 exact names
        exact_names = set(sub_name for sub_name, _ in SUBJECT_GENERATOR_MAP)
        DjangoSubject.objects.exclude(name__in=exact_names).delete()

        total_q_created = 0
        total_c_created = 0

        for idx, (sub_name, gen_func) in enumerate(SUBJECT_GENERATOR_MAP, 1):
            subject_obj, _ = DjangoSubject.objects.get_or_create(name=sub_name)
            questions_data = gen_func()
            assert len(questions_data) == 100, f"{sub_name} does not have 100 questions!"

            q_instances = []
            q_choices_map = []

            for q_dict in questions_data:
                q_inst = DjangoQuestion(
                    text=q_dict["text"],
                    subject=subject_obj,
                    difficulty=q_dict["difficulty"],
                    explanation=q_dict.get("explanation", "")
                )
                q_instances.append(q_inst)

                # Shuffle choices so the correct answer is randomly distributed
                shuffled_choices = list(q_dict["choices"])
                rnd.shuffle(shuffled_choices)
                q_choices_map.append(shuffled_choices)

            # Bulk create questions
            created_questions = DjangoQuestion.objects.bulk_create(q_instances)

            # Prepare choices
            choice_instances = []
            for q_obj, choices_list in zip(created_questions, q_choices_map):
                for choice_text, is_correct in choices_list:
                    choice_instances.append(DjangoChoice(
                        question=q_obj,
                        text=choice_text,
                        is_correct=is_correct
                    ))

            # Bulk create choices
            DjangoChoice.objects.bulk_create(choice_instances)

            total_q_created += len(created_questions)
            total_c_created += len(choice_instances)

            print(f"[{idx:02d}/36] Local: '{sub_name}' -> 100 Qs, 400 Choices")

    elapsed = time.time() - start_time
    print(f"\nLocal SQLite Seeding Complete in {elapsed:.2f}s!")
    print(f"  Subjects in Local DB : {DjangoSubject.objects.count()} (Target: 36)")
    print(f"  Questions in Local DB: {DjangoQuestion.objects.count()} (Target: 3600)")
    print(f"  Choices in Local DB  : {DjangoChoice.objects.count()} (Target: 14400)")


def seed_supabase():
    print("\n" + "=" * 70)
    print("STEP 2: SEEDING REMOTE SUPABASE POSTGRESQL DATABASE")
    print("=" * 70)
    start_time = time.time()

    import dj_database_url
    import psycopg2
    from psycopg2.extras import execute_values

    SUPABASE_URL = "postgresql://postgres.uhvafwnceynvcvhdiapl:%21%21T3%3FeZpdDVCrhZ@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres?sslmode=require"
    cfg = dj_database_url.parse(SUPABASE_URL)

    conn = psycopg2.connect(
        dbname=cfg["NAME"],
        user=cfg["USER"],
        password=cfg["PASSWORD"],
        host=cfg["HOST"],
        port=cfg["PORT"],
        sslmode="require",
    )
    conn.autocommit = False
    cur = conn.cursor()

    try:
        # Clear existing questions & choices from Supabase
        print("Clearing old data from Supabase...")
        cur.execute("DELETE FROM quiz_contest_questions;")
        cur.execute("DELETE FROM quiz_choice;")
        cur.execute("DELETE FROM quiz_question;")
        conn.commit()
        print("Cleared old data.")

        # Fetch existing subjects from Supabase
        cur.execute("SELECT id, name FROM quiz_subject;")
        supabase_subjects = {row[1]: row[0] for row in cur.fetchall()}
        print(f"Found {len(supabase_subjects)} subjects in Supabase.")

        # Ensure all 36 subjects exist in Supabase
        for sub_name, _ in SUBJECT_GENERATOR_MAP:
            if sub_name not in supabase_subjects:
                cur.execute("INSERT INTO quiz_subject (name) VALUES (%s) RETURNING id;", (sub_name,))
                new_id = cur.fetchone()[0]
                supabase_subjects[sub_name] = new_id
                print(f"Created missing subject in Supabase: {sub_name} (ID: {new_id})")
        conn.commit()

        rnd = random.Random(42)
        total_q_remote = 0
        total_c_remote = 0

        for idx, (sub_name, gen_func) in enumerate(SUBJECT_GENERATOR_MAP, 1):
            sub_id = supabase_subjects[sub_name]
            questions_data = gen_func()
            assert len(questions_data) == 100, f"{sub_name} does not have 100 questions!"

            # Insert questions for this subject in a batch
            q_records = [
                (q["text"], sub_id, q["difficulty"], q.get("explanation", ""))
                for q in questions_data
            ]
            
            cur.execute("""
                INSERT INTO quiz_question (text, subject_id, difficulty, explanation)
                VALUES """ + ",".join(["(%s, %s, %s, %s)"] * len(q_records)) + """
                RETURNING id;
            """, [item for sublist in q_records for item in sublist])
            
            created_q_ids = [row[0] for row in cur.fetchall()]

            # Prepare choices
            c_records = []
            for q_id, q_dict in zip(created_q_ids, questions_data):
                shuffled_choices = list(q_dict["choices"])
                rnd.shuffle(shuffled_choices)
                for choice_text, is_correct in shuffled_choices:
                    c_records.append((choice_text, is_correct, q_id))

            # Batch insert choices
            execute_values(
                cur,
                "INSERT INTO quiz_choice (text, is_correct, question_id) VALUES %s;",
                c_records
            )

            conn.commit()
            total_q_remote += len(created_q_ids)
            total_c_remote += len(c_records)
            print(f"[{idx:02d}/36] Supabase: '{sub_name}' (ID: {sub_id}) -> 100 Qs, 400 Choices")

        elapsed = time.time() - start_time
        print(f"\nSupabase Seeding Complete in {elapsed:.2f}s!")

        cur.execute("SELECT count(*) FROM quiz_subject;")
        remote_subs = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM quiz_question;")
        remote_qs = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM quiz_choice;")
        remote_cs = cur.fetchone()[0]

        print(f"  Subjects in Supabase : {remote_subs} (Target: 36)")
        print(f"  Questions in Supabase: {remote_qs} (Target: 3600)")
        print(f"  Choices in Supabase  : {remote_cs} (Target: 14400)")

    except Exception as e:
        conn.rollback()
        print(f"ERROR during Supabase seeding: {e}")
        raise e
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    print("=" * 70)
    print("STARTING FULL DATABASE SEEDING (3,600 REAL QUESTIONS, 36 SUBJECTS)")
    print("=" * 70)
    
    seed_local()
    seed_supabase()
    
    print("\n" + "=" * 70)
    print("ALL 36 SUBJECTS SUCCESSFULLY SEEDED IN BOTH LOCAL AND SUPABASE!")
    print("=" * 70)
