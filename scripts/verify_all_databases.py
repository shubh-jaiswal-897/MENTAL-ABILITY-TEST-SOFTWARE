import os
import sys
import django
from django.db.models import Count

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testmybrain.settings')
django.setup()

from quiz.models import Subject, Question, Choice
import dj_database_url
import psycopg2

def verify_local():
    print("=" * 60)
    print("VERIFYING LOCAL SQLITE DATABASE")
    print("=" * 60)
    subjects = Subject.objects.all().order_by('name')
    print(f"Total Subjects: {subjects.count()}")
    assert subjects.count() == 36, f"Expected 36 subjects, got {subjects.count()}"

    total_q = Question.objects.count()
    total_c = Choice.objects.count()
    print(f"Total Questions: {total_q} (Expected: 3600)")
    print(f"Total Choices: {total_c} (Expected: 14400)")
    assert total_q == 3600, f"Expected 3600 questions, got {total_q}"
    assert total_c == 14400, f"Expected 14400 choices, got {total_c}"

    for idx, s in enumerate(subjects, 1):
        qs = s.questions.all()
        q_count = qs.count()
        easy = qs.filter(difficulty='EASY').count()
        med = qs.filter(difficulty='MEDIUM').count()
        hard = qs.filter(difficulty='HARD').count()
        assert q_count == 100, f"{s.name} has {q_count} questions"
        assert easy == 34 and med == 33 and hard == 33, f"{s.name}: Easy={easy}, Med={med}, Hard={hard}"
        
        # Check choices for questions
        q_ids = list(qs.values_list('id', flat=True))
        choices = Choice.objects.filter(question_id__in=q_ids)
        assert choices.count() == 400, f"{s.name} choices={choices.count()}"
        print(f"[{idx:02d}/36] OK - {s.name:<45} | Easy: {easy}, Med: {med}, Hard: {hard} | Choices: {choices.count()}")

    # Check for any dummy choice text
    dummy_choices = Choice.objects.filter(text__iregex=r'^(option [abcd]|dummy|choice [1234])$').count()
    print(f"\nDummy choice check: {dummy_choices} found.")
    assert dummy_choices == 0

    print("LOCAL SQLITE: 100% PERFECT!\n")

def verify_supabase():
    print("=" * 60)
    print("VERIFYING SUPABASE POSTGRESQL DATABASE")
    print("=" * 60)
    raw_url = os.environ.get('DATABASE_URL')
    if not raw_url:
        raw_url = "postgresql://postgres.uhvafwnceynvcvhdiapl:%21%21T3%3FeZpdDVCrhZ@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres?sslmode=require"
    
    cfg = dj_database_url.parse(raw_url)
    conn = psycopg2.connect(
        dbname=cfg['NAME'],
        user=cfg['USER'],
        password=cfg['PASSWORD'],
        host=cfg['HOST'],
        port=cfg['PORT'],
        sslmode='require'
    )
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM quiz_subject;")
    sub_count = cur.fetchone()[0]
    print(f"Total Subjects: {sub_count}")
    assert sub_count == 36, f"Expected 36 subjects, got {sub_count}"

    cur.execute("SELECT count(*) FROM quiz_question;")
    q_count = cur.fetchone()[0]
    print(f"Total Questions: {q_count} (Expected: 3600)")
    assert q_count == 3600, f"Expected 3600 questions, got {q_count}"

    cur.execute("SELECT count(*) FROM quiz_choice;")
    c_count = cur.fetchone()[0]
    print(f"Total Choices: {c_count} (Expected: 14400)")
    assert c_count == 14400, f"Expected 14400 choices, got {c_count}"

    cur.execute("""
        SELECT s.id, s.name,
               count(q.id) as total_q,
               count(case when q.difficulty = 'EASY' then 1 end) as easy_q,
               count(case when q.difficulty = 'MEDIUM' then 1 end) as med_q,
               count(case when q.difficulty = 'HARD' then 1 end) as hard_q
        FROM quiz_subject s
        LEFT JOIN quiz_question q ON s.id = q.subject_id
        GROUP BY s.id, s.name
        ORDER BY s.name;
    """)
    rows = cur.fetchall()
    for idx, (sid, name, t_q, e_q, m_q, h_q) in enumerate(rows, 1):
        assert t_q == 100, f"{name}: total {t_q}"
        assert e_q == 34 and m_q == 33 and h_q == 33, f"{name}: E={e_q}, M={m_q}, H={h_q}"
        print(f"[{idx:02d}/36] OK - {name:<45} | Easy: {e_q}, Med: {m_q}, Hard: {h_q}")

    cur.execute("""
        SELECT count(*) FROM quiz_choice
        WHERE lower(text) IN ('option a', 'option b', 'option c', 'option d', 'dummy', 'choice 1');
    """)
    dummy_choices = cur.fetchone()[0]
    print(f"\nDummy choice check: {dummy_choices} found.")
    assert dummy_choices == 0

    conn.close()
    print("SUPABASE POSTGRESQL: 100% PERFECT!\n")

if __name__ == '__main__':
    verify_local()
    verify_supabase()
    print("ALL VERIFICATIONS PASSED SUCCESSFULLY!")
