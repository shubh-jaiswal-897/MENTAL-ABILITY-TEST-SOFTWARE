"""Seed up to 50 questions per Subject with 4 choices each.
This is a one-off script to run with the workspace Python: 
python scripts/seed_50_per_subject.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testmybrain.settings')
django.setup()

from quiz.models import Subject, Question, Choice

subjects = list(Subject.objects.all())
if not subjects:
    print('No subjects found. Create subjects first (e.g., via admin).')
else:
    for subject in subjects:
        created_count = 0
        for i in range(1, 51):
            text = f"{subject.name} Question {i}"
            q, created = Question.objects.get_or_create(text=text, subject=subject)
            if created:
                # Add four choices; mark Option A as correct
                Choice.objects.create(question=q, text='Option A', is_correct=True)
                Choice.objects.create(question=q, text='Option B', is_correct=False)
                Choice.objects.create(question=q, text='Option C', is_correct=False)
                Choice.objects.create(question=q, text='Option D', is_correct=False)
                created_count += 1
        total = Question.objects.filter(subject=subject).count()
        print(f"Subject '{subject.name}': ensured {total} questions (created {created_count}).")
    print('Seeding complete.')
