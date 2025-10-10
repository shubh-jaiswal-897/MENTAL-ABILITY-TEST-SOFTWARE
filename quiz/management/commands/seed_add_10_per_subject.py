from django.core.management.base import BaseCommand
import random


class Command(BaseCommand):
    help = 'Add 10 generated multiple-choice questions per Subject (no web scraping).'

    def handle(self, *args, **options):
        from quiz.models import Subject, Question, Choice

        subjects = Subject.objects.all()
        if not subjects:
            self.stdout.write(self.style.WARNING('No subjects found. Create subjects first.'))
            return

        for subject in subjects:
            created = 0
            base_idx = Question.objects.filter(subject=subject).count() + 1
            for i in range(10):
                q_text = f"{subject.name} Generated Question {base_idx + i}"
                q, q_created = Question.objects.get_or_create(text=q_text, subject=subject)
                if q_created:
                    # generate 4 choices; first one will be the correct by convention, shuffle later
                    opts = [
                        f"{subject.name} option A for question {base_idx + i}",
                        f"{subject.name} option B for question {base_idx + i}",
                        f"{subject.name} option C for question {base_idx + i}",
                        f"{subject.name} option D for question {base_idx + i}",
                    ]
                    correct_index = random.randrange(4)
                    for idx, text in enumerate(opts):
                        Choice.objects.create(question=q, text=text, is_correct=(idx == correct_index))
                    created += 1

            total = Question.objects.filter(subject=subject).count()
            self.stdout.write(self.style.SUCCESS(f"Subject '{subject.name}': added {created} generated questions (now {total})."))

        self.stdout.write(self.style.SUCCESS('Generated seeding complete.'))
