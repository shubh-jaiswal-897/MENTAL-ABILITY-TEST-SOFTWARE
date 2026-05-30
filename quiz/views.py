from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice, ContactSubmission, TestAttempt, Subject
from .forms import ContactForm
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import random
import json
from django.db.models import Avg, Count

def index(request):
    # Home page: do not show the full question list here.
    # Keep this page as a landing area; questions are available on the Revision page.
    return render(request, 'quiz/index.html')


def revision(request):
    """Show all questions for revision/study (linked in the navbar).

    Supports:
    - subject filter via GET param `subject` (subject id)
    - free-text search via GET param `q` (matches question text)
    - pagination via GET param `page` (25 items per page)
    """
    from django.core.paginator import Paginator
    from django.db.models import Q
    from .models import Subject

    # Base queryset with prefetching
    qs = Question.objects.select_related('subject').prefetch_related('choices').all()

    # Subject filter
    subjects = Subject.objects.all()
    subject_id = request.GET.get('subject')
    if subject_id:
        try:
            qs = qs.filter(subject_id=int(subject_id))
        except Exception:
            pass

    # Search filter
    search_q = request.GET.get('q', '').strip()
    if search_q:
        qs = qs.filter(text__icontains=search_q)

    # No pagination, show all
    return render(request, 'quiz/revision.html', {
        'questions': qs,
        'subjects': subjects,
        'selected_subject': subject_id,
        'search_query': search_q,
    })


def take_quiz(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        try:
            choice_id = int(request.POST.get('choice'))
            choice = question.choices.get(pk=choice_id)
        except Exception:
            return render(request, 'quiz/quiz.html', {'question': question, 'error': 'Please select an option.'})

        correct = choice.is_correct
        return redirect(reverse('quiz:result', args=[question.pk, int(correct)]))

    # shuffle choices for display
    choices = list(question.choices.all())
    random.shuffle(choices)
    return render(request, 'quiz/quiz.html', {'question': question, 'shuffled_choices': choices})


def result(request, pk, correct):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'quiz/result.html', {'question': question, 'correct': bool(int(correct))})


def signup(request):
    """Allow new users to sign up using Django's built-in UserCreationForm."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz:index')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.ip_address = request.META.get("REMOTE_ADDR")
            submission.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('quiz:contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


@login_required
def test_session(request):
    """
    Handles the lifecycle of a test session.
    Includes initialization, question navigation, timing, scoring, and result persistence.
    """
    import logging
    logger = logging.getLogger(__name__)

    # Ensure user is authenticated (decorator already enforces, but keep guard for safety)
    if not request.user.is_authenticated:
        return redirect('login')

    # Start a new test session
    if 'action' in request.GET and request.GET['action'] == 'start':
        subject_ids = request.GET.getlist('subjects')
        limit = request.GET.get('limit')
        if not subject_ids:
            return render(request, 'test_session.html', {
                'error': 'Please select at least one subject.',
                'subjects': Subject.objects.all()
            })
        qs_qs = Question.objects.filter(subject_id__in=subject_ids)
        qs_ids = list(qs_qs.values_list('id', flat=True))

        # Apply limit
        try:
            limit_val = int(limit)
            if limit_val > 0:
                qs_ids = qs_ids[:limit_val]
        except Exception:
            qs_ids = qs_ids[:10]

        if not qs_ids:
            return render(request, 'test_session.html', {'error': 'No questions available.'})

        random.shuffle(qs_ids)
        request.session['test_qs'] = qs_ids
        request.session['test_subjects'] = ','.join([str(s) for s in subject_ids])
        request.session['test_index'] = 0
        request.session['test_score'] = 0
        request.session['test_start'] = timezone.now().timestamp()
        request.session['test_duration'] = len(qs_ids) * 20  # 20 seconds per question
        return redirect('quiz:test_session')

    # Retrieve session data
    qs = request.session.get('test_qs')
    if not qs:
        subjects = Subject.objects.all()
        return render(request, 'test_session.html', {'subjects': subjects})

    start_ts = request.session.get('test_start')
    if start_ts is None:
        return render(request, 'test_session.html', {'error': 'Session not initialized.'})

    elapsed_seconds = timezone.now().timestamp() - float(start_ts)
    duration_seconds = int(request.session.get('test_duration', 3 * 60))
    remaining_seconds = int(duration_seconds - elapsed_seconds)
    if remaining_seconds <= 0:
        return redirect('quiz:test_result')

    index = int(request.session.get('test_index', 0))

    # POST: process answer / navigation
    if request.method == 'POST':
        # Re‑calculate elapsed to protect against late submissions
        elapsed_seconds = timezone.now().timestamp() - float(start_ts)
        if elapsed_seconds >= duration_seconds:
            # Time expired – finalize attempt with current score
            attempt = TestAttempt.objects.create(
                user=request.user,
                started_at=timezone.datetime.fromtimestamp(float(start_ts)),
                finished_at=timezone.now(),
                score=int(request.session.get('test_score', 0)),
                total=len(qs),
                subjects=request.session.get('test_subjects', ''),
                questions=','.join([str(x) for x in qs]),
            )
            return redirect('quiz:test_result')

        # Record selected choice
        try:
            selected = int(request.POST.get('choice'))
        except Exception:
            selected = None

        if index >= len(qs):
            return redirect('quiz:test_result')
        qid = qs[index]
        answers = request.session.get('test_answers', {})
        answers[str(qid)] = selected
        request.session['test_answers'] = answers

        action = request.POST.get('action', 'next')
        if action == 'end':
            # Compute final score
            score = 0
            answers = request.session.get('test_answers', {})
            for qid_str, choice_id in answers.items():
                if choice_id:
                    try:
                        q = Question.objects.get(pk=int(qid_str))
                        choice = q.choices.get(pk=choice_id)
                        if choice.is_correct:
                            score += 1
                    except Exception:
                        pass
            request.session['test_score'] = score
            # Persist attempt
            attempt = TestAttempt.objects.create(
                user=request.user,
                started_at=timezone.datetime.fromtimestamp(float(start_ts)),
                finished_at=timezone.now(),
                score=score,
                total=len(qs),
                subjects=request.session.get('test_subjects', ''),
                questions=','.join([str(x) for x in qs]),
            )
            return redirect('quiz:test_result')
        elif action == 'previous':
            index -= 1
        else:
            index += 1

        request.session['test_index'] = index
        if index >= len(qs):
            # Finalize test
            score = 0
            answers = request.session.get('test_answers', {})
            for qid_str, choice_id in answers.items():
                if choice_id:
                    try:
                        q = Question.objects.get(pk=int(qid_str))
                        choice = q.choices.get(pk=choice_id)
                        if choice.is_correct:
                            score += 1
                    except Exception:
                        pass
            request.session['test_score'] = score
            attempt = TestAttempt.objects.create(
                user=request.user,
                started_at=timezone.datetime.fromtimestamp(float(start_ts)),
                finished_at=timezone.now(),
                score=score,
                total=len(qs),
                subjects=request.session.get('test_subjects', ''),
                questions=','.join([str(x) for x in qs]),
            )
            return redirect('quiz:test_result')
        elif index < 0:
            index = 0
            request.session['test_index'] = 0
        return redirect('quiz:test_session')

    # GET: render current question
    index = int(request.session.get('test_index', 0))
    if index >= len(qs):
        # Final calculation (same as above)
        score = 0
        answers = request.session.get('test_answers', {})
        for qid_str, choice_id in answers.items():
            if choice_id:
                try:
                    q = Question.objects.get(pk=int(qid_str))
                    choice = q.choices.get(pk=choice_id)
                    if choice.is_correct:
                        score += 1
                except Exception:
                    pass
        request.session['test_score'] = score
        attempt = TestAttempt.objects.create(
            user=request.user,
            started_at=timezone.datetime.fromtimestamp(float(start_ts)),
            finished_at=timezone.now(),
            score=score,
            total=len(qs),
            subjects=request.session.get('test_subjects', ''),
            questions=','.join([str(x) for x in qs]),
        )
        return redirect('quiz:test_result')

    qid = qs[index]
    question = Question.objects.get(pk=qid)
    choices = list(question.choices.all())
    random.shuffle(choices)
    answers = request.session.get('test_answers', {})
    selected_choice = answers.get(str(qid))
    return render(request, 'test_session.html', {
        'question': question,
        'shuffled_choices': choices,
        'index': index + 1,
        'total': len(qs),
        'remaining_seconds': remaining_seconds,
        'selected_choice': selected_choice,
    })
def test_result(request):
    score = int(request.session.get('test_score', 0))
    qs = request.session.get('test_qs', [])
    total = len(qs)
    # marks: correct=1, wrong=0
    marks = score
    max_marks = total
    percentage = 0
    if max_marks > 0:
        percentage = round((marks / max_marks) * 100, 2)
    # clear session keys (including duration)
    for k in ['test_qs', 'test_index', 'test_score', 'test_start', 'test_duration', 'test_subjects', 'test_answers']:
        request.session.pop(k, None)
    return render(request, 'test_session_result.html', {
        'score': score,
        'total': total,
        'marks': marks,
        'max_marks': max_marks,
        'percentage': percentage,
    })


@login_required
def dashboard(request):
    attempts = TestAttempt.objects.filter(user=request.user).order_by('-started_at')
    total_attempts = attempts.count()
    avg_score = 0
    subject_avg = {}
    recommendations = []
    scores_over_time = []

    if total_attempts > 0:
        avg_score = attempts.aggregate(Avg('score'))['score__avg'] or 0
        avg_score = round((avg_score / attempts.first().total * 100) if attempts.first().total > 0 else 0, 2)

        # Get subject name mapping
        subject_name_map = {str(sub.id): sub.name for sub in Subject.objects.all()}

        # Subject-wise performance
        subject_scores = {}
        for attempt in attempts:
            subjects_list = [s.strip() for s in attempt.subjects.split(',') if s.strip()] if attempt.subjects else []
            score_perc = (attempt.score / attempt.total * 100) if attempt.total > 0 else 0
            for sub in subjects_list:
                subject_name = subject_name_map.get(sub, sub)  # Use name if available, else ID
                if subject_name in subject_scores:
                    subject_scores[subject_name]['count'] += 1
                    subject_scores[subject_name]['total_score'] += score_perc
                else:
                    subject_scores[subject_name] = {'count': 1, 'total_score': score_perc}

        subject_avg = {sub: round(data['total_score'] / data['count'], 2) for sub, data in subject_scores.items()}

        # Recommendations: subjects with average below 60%
        recommendations = [sub for sub, avg in subject_avg.items() if avg < 60]

        # Scores over time (last 10 attempts)
        scores_over_time = [
            {
                'date': attempt.started_at.strftime('%Y-%m-%d'),
                'score': (attempt.score / attempt.total * 100) if attempt.total > 0 else 0
            }
            for attempt in attempts[:10]
        ]

    # Convert subject IDs to names for display in recent activity
    recent_attempts = []
    subject_name_map = {str(sub.id): sub.name for sub in Subject.objects.all()}
    for attempt in attempts[:5]:
        attempt_copy = attempt
        subjects_list = [s.strip() for s in attempt.subjects.split(',') if s.strip()] if attempt.subjects else []
        subject_names = [subject_name_map.get(sub, sub) for sub in subjects_list]
        attempt_copy.subject_names = ', '.join(subject_names)
        recent_attempts.append(attempt_copy)

    context = {
        'total_attempts': total_attempts,
        'avg_score': avg_score,
        'subject_avg': subject_avg,
        'recommendations': recommendations,
        'scores_over_time': json.dumps(scores_over_time),  # Convert to JSON for JavaScript
        'attempts': recent_attempts,  # Pass recent attempts with subject names
    }
    return render(request, 'dashboard.html', context)
