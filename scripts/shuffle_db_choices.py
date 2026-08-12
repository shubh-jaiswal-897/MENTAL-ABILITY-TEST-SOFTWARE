import os
import sys
import random
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testmybrain.settings")
django.setup()

from quiz.models import Question, Choice
from django.db import transaction

def shuffle_all_db_choices():
    print("Randomizing existing choice positions in database...")
    questions = Question.objects.prefetch_related('choices').all()
    updated_choices = []

    with transaction.atomic():
        for q in questions:
            choices = list(q.choices.all())
            if len(choices) > 1:
                data = [(c.text, c.is_correct) for c in choices]
                random.shuffle(data)
                for c, (text, is_correct) in zip(choices, data):
                    c.text = text
                    c.is_correct = is_correct
                    updated_choices.append(c)

        Choice.objects.bulk_update(updated_choices, ['text', 'is_correct'])

    first_correct = 0
    total_q = Question.objects.count()
    for q in Question.objects.prefetch_related('choices').all():
        first_c = q.choices.first()
        if first_c and first_c.is_correct:
            first_correct += 1

    print(f"Successfully rebalanced choices for {len(questions)} questions!")
    print(f"New DB distribution: {first_correct} out of {total_q} questions have correct answer as 1st choice.")

if __name__ == "__main__":
    shuffle_all_db_choices()
