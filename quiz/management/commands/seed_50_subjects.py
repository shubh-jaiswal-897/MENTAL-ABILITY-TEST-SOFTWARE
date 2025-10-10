from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Ensure up to 50 questions per Subject exist, each with 4 choices.'

    def handle(self, *args, **options):
        from quiz.models import Subject, Question, Choice

        subjects = Subject.objects.all()
        if not subjects:
            self.stdout.write(self.style.WARNING('No subjects found. Create subjects first.'))
            return

        for subject in subjects:
            created_count = 0
            for i in range(1, 51):
                text = f"{subject.name} Question {i}"
                q, created = Question.objects.get_or_create(text=text, subject=subject)
                if created:
                    Choice.objects.create(question=q, text='Option A', is_correct=True)
                    Choice.objects.create(question=q, text='Option B', is_correct=False)
                    Choice.objects.create(question=q, text='Option C', is_correct=False)
                    Choice.objects.create(question=q, text='Option D', is_correct=False)
                    created_count += 1
            total = Question.objects.filter(subject=subject).count()
            self.stdout.write(self.style.SUCCESS(
                f"Subject '{subject.name}': ensured {total} questions (created {created_count})."
            ))

        self.stdout.write(self.style.SUCCESS('Seeding complete.'))
