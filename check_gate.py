import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testmybrain.settings')
django.setup()

from quiz.models import Subject, Question, Choice

print('Subjects:', list(Subject.objects.values_list('name', flat=True)))
gate_subj = Subject.objects.filter(name='GATE').first()
if gate_subj:
    print('GATE questions:', Question.objects.filter(subject=gate_subj).count())
    print('GATE choices:', Choice.objects.filter(question__subject=gate_subj).count())
else:
    print('GATE subject not found')
