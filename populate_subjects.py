import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testmybrain.settings')
django.setup()

from quiz.models import Subject, Question, Choice
from django.db import transaction

subjects_list = [
    "Artificial Intelligence & Emerging Technologies",
    "Data & Data Analytics",
    "Digital Governance",
    "Finance & Accounting",
    "Human Resource Management",
    "Project Management",
    "Leadership & Self Leadership",
    "Communication Skills",
    "Public Policy",
    "Administrative Law",
    "Cyber/Digital Safety",
    "Legal & Constitutional topics",
    "Behavioural competencies",
    "Functional competencies",
    "Domain-specific competencies",
    "Languages",
    "Health & Safety",
    "Railways",
    "Government schemes and programmes",
    "Office/IT productivity tools",
    "Procurement & GeM",
    "Statistics and data-related learning"
]

@transaction.atomic
def populate_db():
    print("Starting database population...")
    for sub_name in subjects_list:
        subject, created = Subject.objects.get_or_create(name=sub_name)
        if created:
            print(f"Created new subject: {sub_name}")
        else:
            print(f"Subject already exists: {sub_name}")
            
        # Check how many questions it already has
        existing_count = subject.questions.count()
        if existing_count >= 100:
            print(f"Subject {sub_name} already has {existing_count} questions. Skipping.")
            continue
            
        needed_questions = 100 - existing_count
        
        # We distribute difficulties
        levels = [Question.EASY, Question.MEDIUM, Question.HARD]
        
        questions_to_create = []
        for i in range(needed_questions):
            diff = levels[i % 3]
            q_num = existing_count + i + 1
            text = f"Sample question {q_num} for {sub_name} ({diff.lower()} level)."
            exp = f"This is a detailed explanation for question {q_num} of {sub_name}."
            
            q = Question.objects.create(
                text=text,
                subject=subject,
                difficulty=diff,
                explanation=exp
            )
            
            # Create 4 choices for the question
            Choice.objects.create(question=q, text=f"Option A for Q{q_num}", is_correct=True)
            Choice.objects.create(question=q, text=f"Option B for Q{q_num}", is_correct=False)
            Choice.objects.create(question=q, text=f"Option C for Q{q_num}", is_correct=False)
            Choice.objects.create(question=q, text=f"Option D for Q{q_num}", is_correct=False)
            
        print(f"Added {needed_questions} placeholder questions to {sub_name}.")

if __name__ == '__main__':
    populate_db()
    print("Done populating.")
