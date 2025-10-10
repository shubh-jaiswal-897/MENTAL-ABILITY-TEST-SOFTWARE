from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice, ContactSubmission
from .forms import ContactForm
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import random

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

    # Pagination
    paginator = Paginator(qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Build params string excluding page for pagination links
    params = request.GET.copy()
    if 'page' in params:
        params.pop('page')
    params_str = params.urlencode()
    if params_str:
        params_str = '&' + params_str

    return render(request, 'quiz/revision.html', {
        'questions': page_obj,
        'subjects': subjects,
        'selected_subject': subject_id,
        'search_query': search_q,
        'params': params_str,
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


def test_session(request):
    # Start or continue a test session. Requires login via URL decorator.
    # Session keys used: 'test_qs' (list of question ids), 'test_index', 'test_start', 'test_score'
    if 'action' in request.GET and request.GET['action'] == 'start':
        # initialize session
        subject_ids = request.GET.getlist('subjects')
        limit = request.GET.get('limit')
        if subject_ids:
            qs_qs = Question.objects.filter(subject_id__in=subject_ids)
        else:
            qs_qs = Question.objects.all()
        qs_ids = list(qs_qs.values_list('id', flat=True))

        # apply limit
        try:
            limit_val = int(limit)
            if limit_val > 0:
                qs_ids = qs_ids[:limit_val]
        except Exception:
            # default to 10
            qs_ids = qs_ids[:10]

        if not qs_ids:
            return render(request, 'test_session.html', {'error': 'No questions available.'})

        random.shuffle(qs_ids)

        # limit to 10 questions for a session
        qs_ids = qs_ids[:10]
        request.session['test_qs'] = qs_ids
        # store selected subject names for attempt record
        request.session['test_subjects'] = ','.join([str(s) for s in subject_ids])
        request.session['test_index'] = 0
        request.session['test_score'] = 0
        # store start as epoch seconds (float) to avoid timezone-aware parsing issues
        request.session['test_start'] = timezone.now().timestamp()
        # compute duration: n questions * 20 seconds each
        try:
            duration_seconds = int(len(qs_ids)) * 20
        except Exception:
            duration_seconds = 3 * 60
        request.session['test_duration'] = duration_seconds
        return redirect('quiz:test_session')

    qs = request.session.get('test_qs')
    if not qs:
        # pass available subjects for the start form
        from .models import Subject
        subjects = Subject.objects.all()
        return render(request, 'test_session.html', {'subjects': subjects})

    # check timer (dynamic per-session)
    start_ts = request.session.get('test_start')
    if start_ts is None:
        return render(request, 'test_session.html', {'error': 'Session not initialized.'})

    # calculate elapsed seconds using timestamps (float)
    elapsed_seconds = timezone.now().timestamp() - float(start_ts)
    duration_seconds = int(request.session.get('test_duration', 3 * 60))
    remaining_seconds = int(duration_seconds - elapsed_seconds)
    if remaining_seconds <= 0:
        # time's up -> show result
        return redirect('quiz:test_result')

    index = int(request.session.get('test_index', 0))
    if request.method == 'POST':
        # Recompute elapsed to protect against late POSTs
        elapsed_seconds = timezone.now().timestamp() - float(start_ts)
        if elapsed_seconds >= duration_seconds:
            # time expired; ignore answer and finish
            # persist attempt with score so far
            from .models import TestAttempt
            attempt = TestAttempt.objects.create(
                user=request.user,
                started_at=timezone.datetime.fromtimestamp(float(start_ts)),
                finished_at=timezone.now(),
                score=int(request.session.get('test_score', 0)),
                total=len(qs),
                subjects=request.session.get('test_subjects', ''),
                questions=','.join([str(x) for x in qs])
            )
            return redirect('quiz:test_result')

        # process answer for current question (only if within time)
        try:
            selected = int(request.POST.get('choice'))
        except Exception:
            selected = None

        qid = qs[index]
        question = Question.objects.get(pk=qid)
        if selected:
            try:
                choice = question.choices.get(pk=selected)
                if choice.is_correct:
                    request.session['test_score'] = int(request.session.get('test_score', 0)) + 1
            except Choice.DoesNotExist:
                pass

        # advance
        index += 1
        request.session['test_index'] = index
        if index >= len(qs):
            # persist attempt
            from .models import TestAttempt
            attempt = TestAttempt.objects.create(
                user=request.user,
                started_at=timezone.datetime.fromtimestamp(float(start_ts)),
                finished_at=timezone.now(),
                score=int(request.session.get('test_score', 0)),
                total=len(qs),
                subjects=request.session.get('test_subjects', ''),
                questions=','.join([str(x) for x in qs])
            )
            return redirect('quiz:test_result')
        return redirect('quiz:test_session')

    # GET: show current question
    index = int(request.session.get('test_index', 0))
    qid = qs[index]
    question = Question.objects.get(pk=qid)
    # shuffle choices for this question
    choices = list(question.choices.all())
    random.shuffle(choices)
    return render(request, 'test_session.html', {
        'question': question,
        'shuffled_choices': choices,
        'index': index + 1,
        'total': len(qs),
        'remaining_seconds': remaining_seconds,
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
    for k in ['test_qs', 'test_index', 'test_score', 'test_start', 'test_duration', 'test_subjects']:
        request.session.pop(k, None)
    return render(request, 'test_session_result.html', {
        'score': score,
        'total': total,
        'marks': marks,
        'max_marks': max_marks,
        'percentage': percentage,
    })
