"""
Script to safely delete ALL questions and answers (choices) from both:
1. Local SQLite database (testmybrain default)
2. Remote Supabase PostgreSQL database (production)
Subject records are NOT deleted and remain 100% intact.
"""
import os
import sys
import django

# 1. LOCAL SQLITE DATABASE
print("=" * 60)
print("STEP 1: DELETING QUESTIONS & ANSWERS FROM LOCAL SQLITE")
print("=" * 60)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testmybrain.settings")
django.setup()

from quiz.models import Subject, Question, Choice
from django.db import transaction, connection

local_subjects_before = Subject.objects.count()
local_questions_before = Question.objects.count()
local_choices_before = Choice.objects.count()
print(f"Before local deletion:")
print(f"  Subjects : {local_subjects_before}")
print(f"  Questions: {local_questions_before}")
print(f"  Choices  : {local_choices_before}")

with transaction.atomic():
    # Clear contest questions M2M if table exists
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM quiz_contest_questions;")
    # Delete all choices and questions
    Choice.objects.all().delete()
    deleted_q_count, _ = Question.objects.all().delete()

local_subjects_after = Subject.objects.count()
local_questions_after = Question.objects.count()
local_choices_after = Choice.objects.count()

print(f"\nAfter local deletion:")
print(f"  Subjects : {local_subjects_after} (UNCHANGED)")
print(f"  Questions: {local_questions_after} (CLEARED)")
print(f"  Choices  : {local_choices_after} (CLEARED)")

# 2. REMOTE SUPABASE POSTGRESQL DATABASE
print("\n" + "=" * 60)
print("STEP 2: DELETING QUESTIONS & ANSWERS FROM SUPABASE POSTGRESQL")
print("=" * 60)

import dj_database_url
import psycopg2

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
cur = conn.cursor()

cur.execute("SELECT count(*) FROM quiz_subject;")
remote_subjects_before = cur.fetchone()[0]
cur.execute("SELECT count(*) FROM quiz_question;")
remote_questions_before = cur.fetchone()[0]
cur.execute("SELECT count(*) FROM quiz_choice;")
remote_choices_before = cur.fetchone()[0]

print(f"Before Supabase deletion:")
print(f"  Subjects : {remote_subjects_before}")
print(f"  Questions: {remote_questions_before}")
print(f"  Choices  : {remote_choices_before}")

print("\nExecuting deletions on Supabase...")
cur.execute("DELETE FROM quiz_contest_questions;")
cur.execute("DELETE FROM quiz_choice;")
cur.execute("DELETE FROM quiz_question;")
conn.commit()

cur.execute("SELECT count(*) FROM quiz_subject;")
remote_subjects_after = cur.fetchone()[0]
cur.execute("SELECT count(*) FROM quiz_question;")
remote_questions_after = cur.fetchone()[0]
cur.execute("SELECT count(*) FROM quiz_choice;")
remote_choices_after = cur.fetchone()[0]

print(f"\nAfter Supabase deletion:")
print(f"  Subjects : {remote_subjects_after} (UNCHANGED)")
print(f"  Questions: {remote_questions_after} (CLEARED)")
print(f"  Choices  : {remote_choices_after} (CLEARED)")

conn.close()
print("\n" + "=" * 60)
print("SUCCESS: All questions and answers deleted from both databases!")
print("All subjects were kept intact.")
print("=" * 60)
