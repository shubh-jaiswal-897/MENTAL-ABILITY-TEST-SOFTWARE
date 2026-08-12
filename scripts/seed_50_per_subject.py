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
                # Add four choices; randomize correct choice position
                import random
                choices_list = [
                    ('Option A', True),
                    ('Option B', False),
                    ('Option C', False),
                    ('Option D', False)
                ]
                random.shuffle(choices_list)
                for text_val, corr in choices_list:
                    Choice.objects.create(question=q, text=text_val, is_correct=corr)
                created_count += 1
        total = Question.objects.filter(subject=subject).count()
        print(f"Subject '{subject.name}': ensured {total} questions (created {created_count}).")
    print('Seeding complete.')
