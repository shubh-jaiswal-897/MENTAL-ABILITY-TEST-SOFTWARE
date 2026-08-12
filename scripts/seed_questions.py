import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testmybrain.settings")
django.setup()

from quiz.models import Subject, Question, Choice

def seed():
    print("Seeding LeetCode-style Questions and Subjects...")

    subjects_data = {
        "Logical Reasoning": [
            {
                "text": "If ALL GATORS ARE REPTILES and ALL REPTILES ARE ANIMALS, then which statement is 100% true?",
                "difficulty": Question.EASY,
                "explanation": "Syllogism rule: Gators ⊂ Reptiles ⊂ Animals. Therefore, all Gators are transitively Animals.",
                "choices": [
                    ("All Gators are Animals", True),
                    ("All Animals are Gators", False),
                    ("Some Reptiles are not Animals", False),
                    ("No Gators are Animals", False),
                ]
            },
            {
                "text": "Find the missing number in series: 2, 6, 12, 20, 30, ?",
                "difficulty": Question.MEDIUM,
                "explanation": "The differences between consecutive terms are +4, +6, +8, +10. Next difference is +12, so 30 + 12 = 42.",
                "choices": [
                    ("42", True),
                    ("40", False),
                    ("36", False),
                    ("44", False),
                ]
            },
            {
                "text": "A is the brother of B. B is the sister of C. C is the father of D. How is A related to D?",
                "difficulty": Question.MEDIUM,
                "explanation": "C is D's father. A is C's brother. Father's brother is Uncle.",
                "choices": [
                    ("Uncle", True),
                    ("Father", False),
                    ("Brother", False),
                    ("Grandfather", False),
                ]
            },
            {
                "text": "In a certain code, 'LEET' is written as '12-5-5-20'. How is 'CODE' written?",
                "difficulty": Question.EASY,
                "explanation": "Each letter is represented by its 1-indexed alphabetical position: C=3, O=15, D=4, E=5.",
                "choices": [
                    ("3-15-4-5", True),
                    ("3-14-4-5", False),
                    ("4-15-3-5", False),
                    ("3-15-5-4", False),
                ]
            }
        ],
        "Quantitative Aptitude": [
            {
                "text": "A train 150 meters long passes a telegraph pole in 12 seconds. What is the speed of the train in km/h?",
                "difficulty": Question.MEDIUM,
                "explanation": "Speed = Distance / Time = 150m / 12s = 12.5 m/s. Convert to km/h: 12.5 * (18/5) = 45 km/h.",
                "choices": [
                    ("45 km/h", True),
                    ("50 km/h", False),
                    ("40 km/h", False),
                    ("60 km/h", False),
                ]
            },
            {
                "text": "If 12 men can complete a work in 20 days, how many days will 15 men take to complete the same work?",
                "difficulty": Question.EASY,
                "explanation": "Man-days formula: M1 * D1 = M2 * D2 => 12 * 20 = 15 * D2 => 240 = 15 * D2 => D2 = 16 days.",
                "choices": [
                    ("16 days", True),
                    ("15 days", False),
                    ("18 days", False),
                    ("20 days", False),
                ]
            },
            {
                "text": "What is the probability of getting a sum of 7 when rolling two fair 6-sided dice?",
                "difficulty": Question.HARD,
                "explanation": "Total outcomes = 36. Favorable outcomes for sum 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) -> 6 outcomes. Probability = 6/36 = 1/6.",
                "choices": [
                    ("1/6", True),
                    ("1/12", False),
                    ("5/36", False),
                    ("1/4", False),
                ]
            }
        ],
        "Verbal & Analogies": [
            {
                "text": "Select the word that is synonymous with 'EPHEMERAL':",
                "difficulty": Question.MEDIUM,
                "explanation": "'Ephemeral' means lasting for a very short time (transitory or fleeting).",
                "choices": [
                    ("Transient", True),
                    ("Eternal", False),
                    ("Substantial", False),
                    ("Rigid", False),
                ]
            },
            {
                "text": "Complete the analogy: ARCHITECT : BUILDING :: SCULPTOR : ?",
                "difficulty": Question.EASY,
                "explanation": "An architect designs and builds a building; a sculptor creates a statue.",
                "choices": [
                    ("Statue", True),
                    ("Museum", False),
                    ("Chisel", False),
                    ("Painting", False),
                ]
            }
        ],
        "Pattern Recognition": [
            {
                "text": "Look at this series: 80, 10, 70, 15, 60, 20, ? What number should come next?",
                "difficulty": Question.HARD,
                "explanation": "Alternating series: Series 1 (-10): 80, 70, 60, [50]. Series 2 (+5): 10, 15, 20. The next number belongs to Series 1 -> 50.",
                "choices": [
                    ("50", True),
                    ("25", False),
                    ("30", False),
                    ("55", False),
                ]
            }
        ]
    }

    for sub_name, questions in subjects_data.items():
        subject, _ = Subject.objects.get_or_create(name=sub_name)
        for q_data in questions:
            q, created = Question.objects.get_or_create(
                text=q_data["text"],
                defaults={
                    "subject": subject,
                    "difficulty": q_data["difficulty"],
                    "explanation": q_data["explanation"]
                }
            )
            if not created:
                q.subject = subject
                q.difficulty = q_data["difficulty"]
                q.explanation = q_data["explanation"]
                q.save()
            
            # recreate choices
            choices_list = list(q_data["choices"])
            import random
            random.shuffle(choices_list)
            for choice_text, is_corr in choices_list:
                Choice.objects.create(question=q, text=choice_text, is_correct=is_corr)

    print("Seeding complete! Total Questions:", Question.objects.count())

if __name__ == "__main__":
    seed()
