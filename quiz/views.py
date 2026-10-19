import os
import re
import uuid
import random
import json
from datetime import timedelta, datetime, timezone as dt_timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.conf import settings
from .models import Question, Choice, ContactSubmission, TestAttempt, Subject, UserProfile, Contest, GoodieItem, UserGoodieRedemption, StudyMaterial, Exam, ExamQuestion
from .forms import ContactForm
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Count
from django.db import transaction

def _evaluate_test_answers(answers):
    """Calculate score and XP earned based on user answers."""
    score = 0
    xp_earned = 0
    for qid_str, choice_id in answers.items():
        if choice_id:
            try:
                q = Question.objects.get(pk=int(qid_str))
                choice = q.choices.get(pk=int(choice_id))
                if choice.is_correct:
                    score += 1
                    if q.difficulty == Question.EASY:
                        xp_earned += 1
                    elif q.difficulty == Question.MEDIUM:
                        xp_earned += 2
                    elif q.difficulty == Question.HARD:
                        xp_earned += 3
                    else:
                        xp_earned += 1
            except Exception:
                pass
    return score, xp_earned

def debug_db(request):
    import traceback
    from django.http import HttpResponse
    from django.db import connection
    try:
        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
        return HttpResponse(f"Connection successful! Result: {result}", content_type="text/plain")
    except Exception as e:
        tb = traceback.format_exc()
        return HttpResponse(f"Error connecting to database:\n{e}\n\nTraceback:\n{tb}", content_type="text/plain", status=500)

def take_quiz(request, pk):
    question = get_object_or_404(Question, pk=pk)
    choices = list(question.choices.all())
    random.shuffle(choices)
    if request.method == 'POST':
        try:
            choice_id = int(request.POST.get('choice'))
            choice = question.choices.get(pk=choice_id)
        except Exception:
            return render(request, 'quiz/quiz.html', {'question': question, 'shuffled_choices': choices, 'error': 'Please select an option.'})

        correct = choice.is_correct
        return redirect(reverse('quiz:result', args=[question.pk, int(correct)]))

    return render(request, 'quiz/quiz.html', {'question': question, 'shuffled_choices': choices})


def result(request, pk, correct):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'quiz/result.html', {'question': question, 'correct': bool(int(correct))})


def signup(request):
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

def get_or_create_user_profile(user):
    if not user.is_authenticated:
        return None
    profile, created = UserProfile.objects.get_or_create(user=user)
    today = timezone.now().date()
    if profile.last_active_date is None:
        profile.streak_count = 1
        profile.last_active_date = today
        profile.save()
    elif profile.last_active_date < today:
        if profile.last_active_date == today - timedelta(days=1):
            profile.streak_count += 1
        else:
            profile.streak_count = 1
        profile.last_active_date = today
        profile.save()
    return profile


def get_daily_challenge_question():
    """
    Deterministically selects today's Daily Challenge question based on UTC/local calendar day.
    Automatically rotates to a fresh question every 24 hours at midnight.
    """
    today = timezone.now().date()
    day_seed = today.year * 10000 + today.timetuple().tm_yday
    questions = list(Question.objects.select_related('subject').all().order_by('id'))
    if not questions:
        return None
    return questions[day_seed % len(questions)]


def index(request):
    """Home landing page with LeetCode style Daily Challenge and user stats."""
    profile = get_or_create_user_profile(request.user) if request.user.is_authenticated else None
    daily_question = get_daily_challenge_question()

    subjects = Subject.objects.annotate(q_count=Count('questions'))
    total_questions = Question.objects.count()

    context = {
        'profile': profile,
        'daily_question': daily_question,
        'subjects': subjects,
        'total_questions': total_questions,
    }
    return render(request, 'home.html', context)


def revision(request):
    """Show all questions for revision/study with difficulty filter."""
    from django.db.models import Q

    qs = Question.objects.select_related('subject').prefetch_related('choices').all()

    subjects = Subject.objects.all()
    subject_id = request.GET.get('subject')
    if subject_id:
        try:
            qs = qs.filter(subject_id=int(subject_id))
        except Exception:
            pass

    difficulty = request.GET.get('difficulty')
    if difficulty in ['EASY', 'MEDIUM', 'HARD']:
        qs = qs.filter(difficulty=difficulty)

    search_q = request.GET.get('q', '').strip()
    if search_q:
        qs = qs.filter(text__icontains=search_q)

    profile = get_or_create_user_profile(request.user) if request.user.is_authenticated else None

    return render(request, 'quiz/revision.html', {
        'questions': qs,
        'subjects': subjects,
        'selected_subject': subject_id,
        'selected_difficulty': difficulty,
        'search_query': search_q,
        'profile': profile,
    })


@login_required
def daily_challenge(request):
    """Direct shortcut view to launch today's Daily Challenge test session."""
    daily_q = get_daily_challenge_question()
    if not daily_q:
        messages.error(request, "No questions available for Daily Challenge.")
        return redirect('quiz:index')

    # Set up session for single question daily challenge
    request.session['test_qs'] = [daily_q.id]
    request.session['test_subjects'] = daily_q.subject.name if daily_q.subject else 'General'
    request.session['test_index'] = 0
    request.session['test_score'] = 0
    request.session['test_start'] = timezone.now().timestamp()
    request.session['test_duration'] = 60  # 60s timer for daily challenge
    request.session['is_daily_challenge'] = True

    return redirect('quiz:test_session')


def _build_session_question_breakdown(qs, answers):
    """
    Builds a detailed question-by-question breakdown including all choices,
    highlighting the user's selected choice vs the correct choice.
    """
    breakdown = []
    questions = Question.objects.filter(pk__in=qs).select_related('subject').prefetch_related('choices')
    q_map = {q.id: q for q in questions}

    for idx, qid in enumerate(qs, start=1):
        try:
            q_pk = int(qid)
        except (ValueError, TypeError):
            continue

        q = q_map.get(q_pk)
        if not q:
            continue

        selected_choice_id = str(answers.get(str(qid), answers.get(q_pk, '')))
        choices_list = []
        user_choice_obj = None
        correct_choice_obj = None

        for c in q.choices.all():
            is_sel = (str(c.id) == selected_choice_id)
            if c.is_correct:
                correct_choice_obj = c
            if is_sel:
                user_choice_obj = c

            choices_list.append({
                'id': c.id,
                'text': c.text,
                'is_correct': c.is_correct,
                'is_selected': is_sel,
            })

        if user_choice_obj:
            status = 'CORRECT' if user_choice_obj.is_correct else 'INCORRECT'
        else:
            status = 'SKIPPED'

        breakdown.append({
            'num': idx,
            'id': q.id,
            'text': q.text,
            'difficulty': q.get_difficulty_display(),
            'difficulty_code': q.difficulty,
            'subject_name': q.subject.name if q.subject else 'General Aptitude',
            'choices': choices_list,
            'status': status,
            'user_choice': user_choice_obj.text if user_choice_obj else None,
            'correct_choice': correct_choice_obj.text if correct_choice_obj else None,
            'explanation': q.explanation,
        })

    return breakdown


def _finish_test_session(request, start_ts, qs):
    """Calculates scores, updates XP, records attempt, saves result to session, and redirects to test_result."""
    answers = request.session.get('test_answers', {})
    score, xp_earned = _evaluate_test_answers(answers)
    is_daily = request.session.get('is_daily_challenge', False)
    if is_daily:
        xp_earned *= 2

    question_breakdown = _build_session_question_breakdown(qs, answers)

    if request.user.is_authenticated:
        profile = get_or_create_user_profile(request.user)
        profile.total_xp += xp_earned
        profile.solved_questions_count += score
        profile.save()

        start_dt = datetime.fromtimestamp(float(start_ts), tz=dt_timezone.utc)
        TestAttempt.objects.create(
            user=request.user,
            started_at=start_dt,
            finished_at=timezone.now(),
            score=score,
            total=len(qs),
            subjects=request.session.get('test_subjects', ''),
            questions=','.join([str(x) for x in qs]),
        )

    total = len(qs)
    percentage = round((score / total * 100), 2) if total > 0 else 0
    request.session['last_test_result'] = {
        'score': score,
        'total': total,
        'marks': score,
        'max_marks': total,
        'percentage': percentage,
        'xp_earned': xp_earned,
        'is_daily_challenge': is_daily,
        'question_breakdown': question_breakdown,
    }

    for k in ['test_qs', 'test_index', 'test_score', 'test_start', 'test_duration', 'test_subjects', 'test_answers', 'is_daily_challenge']:
        request.session.pop(k, None)

    return redirect('quiz:test_result')


@login_required
def test_session(request):
    """
    LeetCode-Style Quiz Arena test session.
    """
    profile = get_or_create_user_profile(request.user)

    # Start a new test session
    if 'action' in request.GET and request.GET['action'] == 'start':
        subject_ids = request.GET.getlist('subjects')
        limit = request.GET.get('limit')
        if not subject_ids:
            return render(request, 'test_session.html', {
                'error': 'Please select at least one subject.',
                'subjects': Subject.objects.all(),
                'profile': profile,
            })
        qs_qs = Question.objects.filter(subject_id__in=subject_ids)
        qs_ids = list(qs_qs.values_list('id', flat=True))

        try:
            limit_val = int(limit)
            if limit_val > 0:
                qs_ids = qs_ids[:limit_val]
        except Exception:
            qs_ids = qs_ids[:10]

        if not qs_ids:
            return render(request, 'test_session.html', {'error': 'No questions available.', 'profile': profile})

        random.shuffle(qs_ids)
        request.session['test_qs'] = qs_ids
        request.session['test_subjects'] = ','.join([str(s) for s in subject_ids])
        request.session['test_index'] = 0
        request.session['test_score'] = 0
        request.session['test_start'] = timezone.now().timestamp()
        request.session['test_duration'] = len(qs_ids) * 30  # 30s per question
        request.session['is_daily_challenge'] = False
        return redirect('quiz:test_session')

    qs = request.session.get('test_qs')
    if not qs:
        subjects = Subject.objects.all()
        return render(request, 'test_session.html', {'subjects': subjects, 'profile': profile})

    start_ts = request.session.get('test_start')
    if start_ts is None:
        return render(request, 'test_session.html', {'error': 'Session not initialized.', 'profile': profile})

    elapsed_seconds = timezone.now().timestamp() - float(start_ts)
    duration_seconds = int(request.session.get('test_duration', 3 * 60))
    remaining_seconds = int(duration_seconds - elapsed_seconds)

    if remaining_seconds <= 0:
        return _finish_test_session(request, start_ts, qs)

    index = int(request.session.get('test_index', 0))

    if request.method == 'POST':
        action = request.POST.get('action', 'next')
        if elapsed_seconds >= duration_seconds or action == 'end':
            return _finish_test_session(request, start_ts, qs)

        try:
            selected = int(request.POST.get('choice'))
        except Exception:
            selected = None

        if index < len(qs):
            qid = qs[index]
            answers = request.session.get('test_answers', {})
            answers[str(qid)] = selected
            request.session['test_answers'] = answers
            request.session.modified = True

        if action == 'previous':
            index -= 1
            request.session['test_index'] = max(0, index)
            return redirect('quiz:test_session')
        elif action == 'next':
            index += 1
            request.session['test_index'] = index

        if index >= len(qs):
            return _finish_test_session(request, start_ts, qs)

        return redirect('quiz:test_session')

    # GET: render current question arena
    index = int(request.session.get('test_index', 0))
    if index >= len(qs):
        return redirect('quiz:test_result')

    qid = qs[index]
    question = Question.objects.select_related('subject').prefetch_related('choices').get(pk=qid)
    choices = list(question.choices.all())
    seed_key = f"{start_ts}_{qid}"
    rng = random.Random(seed_key)
    rng.shuffle(choices)

    answers = request.session.get('test_answers', {})
    selected_choice = answers.get(str(qid))

    is_daily = request.session.get('is_daily_challenge', False)

    return render(request, 'test_session.html', {
        'question': question,
        'shuffled_choices': choices,
        'index': index + 1,
        'total': len(qs),
        'remaining_seconds': remaining_seconds,
        'selected_choice': selected_choice,
        'profile': profile,
        'is_daily_challenge': is_daily,
    })


def test_result(request):
    result_data = dict(request.session.get('last_test_result', {}))
    profile = get_or_create_user_profile(request.user) if request.user.is_authenticated else None
    if not result_data:
        score = int(request.session.get('test_score', 0))
        qs = request.session.get('test_qs', [])
        total = len(qs)
        percentage = round((score / total * 100), 2) if total > 0 else 0
        result_data = {
            'score': score,
            'total': total,
            'marks': score,
            'max_marks': total,
            'percentage': percentage,
            'xp_earned': 0,
            'is_daily_challenge': False,
        }
    result_data['profile'] = profile
    return render(request, 'test_session_result.html', result_data)


@login_required
def dashboard(request):
    profile = get_or_create_user_profile(request.user)
    attempts = TestAttempt.objects.filter(user=request.user).order_by('-started_at')
    total_attempts = attempts.count()
    avg_score = 0
    subject_avg = {}
    recommendations = []
    scores_over_time = []

    subject_scores = {}

    if total_attempts > 0:
        perc_list = [(attempt.score / attempt.total * 100) for attempt in attempts if attempt.total > 0]
        avg_score = round(sum(perc_list) / len(perc_list), 2) if perc_list else 0

        subject_name_map = {str(sub.id): sub.name for sub in Subject.objects.all()}

        for attempt in attempts:
            subjects_list = [s.strip() for s in attempt.subjects.split(',') if s.strip()] if attempt.subjects else []
            score_perc = (attempt.score / attempt.total * 100) if attempt.total > 0 else 0
            for sub in subjects_list:
                subject_name = subject_name_map.get(sub, sub)
                if subject_name in subject_scores:
                    subject_scores[subject_name]['count'] += 1
                    subject_scores[subject_name]['total_score'] += score_perc
                else:
                    subject_scores[subject_name] = {'count': 1, 'total_score': score_perc}

    # Calculate AI Exam Stats
    from .models import Exam
    ai_exams = Exam.objects.filter(user=request.user, completed_at__isnull=False)
    ai_total_attempts = ai_exams.count()
    ai_avg_score = 0
    if ai_total_attempts > 0:
        ai_perc_list = [(exam.score / exam.total * 100) for exam in ai_exams if exam.total > 0]
        ai_avg_score = round(sum(ai_perc_list) / len(ai_perc_list), 2) if ai_perc_list else 0
        
        # Add AI Exams to subject accuracy
        for exam in ai_exams:
            subject_name = f"{exam.material.title} (AI)"
            score_perc = (exam.score / exam.total * 100) if exam.total > 0 else 0
            if subject_name in subject_scores:
                subject_scores[subject_name]['count'] += 1
                subject_scores[subject_name]['total_score'] += score_perc
            else:
                subject_scores[subject_name] = {'count': 1, 'total_score': score_perc}

    # Calculate final averages and recommendations
    subject_avg = {sub: round(data['total_score'] / data['count'], 2) for sub, data in subject_scores.items()}
    recommendations = [sub for sub, avg in subject_avg.items() if avg < 60]

    # Combine TestAttempts and AI Exams for the chart
    combined_scores = []
    for attempt in attempts:
        combined_scores.append({
            'date': attempt.started_at,
            'label': attempt.started_at.strftime('%Y-%m-%d (Arena)'),
            'score': round((attempt.score / attempt.total * 100), 1) if attempt.total > 0 else 0
        })
    for exam in ai_exams:
        combined_scores.append({
            'date': exam.completed_at,
            'label': exam.completed_at.strftime('%Y-%m-%d (AI Exam)'),
            'score': round((exam.score / exam.total * 100), 1) if exam.total > 0 else 0
        })
        
    # Sort by date descending and take last 10, then reverse for chronological graph
    combined_scores.sort(key=lambda x: x['date'], reverse=True)
    combined_scores = combined_scores[:10]
    
    scores_over_time = []
    for item in combined_scores:
        scores_over_time.append({
            'date': item['label'],
            'score': item['score']
        })

    # Generate LeetCode-Style Heatmap activity data for past 60 days
    today = timezone.now().date()
    heatmap_data = []
    attempt_date_counts = {}
    for attempt in attempts:
        attempt_date = attempt.started_at.date().strftime('%Y-%m-%d')
        attempt_date_counts[attempt_date] = attempt_date_counts.get(attempt_date, 0) + 1

    for i in range(59, -1, -1):
        day_date = today - timedelta(days=i)
        day_str = day_date.strftime('%Y-%m-%d')
        count = attempt_date_counts.get(day_str, 0)
        heatmap_data.append({
            'date': day_str,
            'count': count,
            'level': min(count, 4)  # 0 to 4 intensity level
        })

    recent_attempts = []
    subject_name_map = {str(sub.id): sub.name for sub in Subject.objects.all()}
    for attempt in attempts[:5]:
        attempt_copy = attempt
        subjects_list = [s.strip() for s in attempt.subjects.split(',') if s.strip()] if attempt.subjects else []
        subject_names = [subject_name_map.get(sub, sub) for sub in subjects_list]
        attempt_copy.subject_names = ', '.join(subject_names)
        recent_attempts.append(attempt_copy)

    # Calculate AI Exam Stats
    from .models import Exam
    ai_exams = Exam.objects.filter(user=request.user, completed_at__isnull=False)
    ai_total_attempts = ai_exams.count()
    ai_avg_score = 0
    if ai_total_attempts > 0:
        ai_perc_list = [(exam.score / exam.total * 100) for exam in ai_exams if exam.total > 0]
        ai_avg_score = round(sum(ai_perc_list) / len(ai_perc_list), 2) if ai_perc_list else 0

    context = {
        'profile': profile,
        'total_attempts': total_attempts,
        'avg_score': avg_score,
        'subject_avg': subject_avg,
        'recommendations': recommendations,
        'scores_over_time': json.dumps(scores_over_time),
        'attempts': recent_attempts,
        'heatmap_data': json.dumps(heatmap_data),
        'ai_total_attempts': ai_total_attempts,
        'ai_avg_score': ai_avg_score,
    }
    return render(request, 'dashboard.html', context)


def contests(request):
    """View Weekly & Monthly Contests and Live Leaderboards."""
    profile = get_or_create_user_profile(request.user) if request.user.is_authenticated else None
    
    weekly_contests = Contest.objects.filter(contest_type=Contest.WEEKLY)
    monthly_contests = Contest.objects.filter(contest_type=Contest.MONTHLY)

    # Top User Leaderboard based on total XP
    leaderboard = UserProfile.objects.select_related('user').order_by('-total_xp', '-solved_questions_count')[:10]

    context = {
        'profile': profile,
        'weekly_contests': weekly_contests,
        'monthly_contests': monthly_contests,
        'leaderboard': leaderboard,
    }
    return render(request, 'quiz/contests.html', context)


@login_required
def join_contest(request, pk):
    """Start a specific Contest session."""
    contest = get_object_or_404(Contest, pk=pk)
    qs_ids = list(contest.questions.values_list('id', flat=True))

    if not qs_ids:
        # Fallback to general questions if contest has none assigned
        qs_ids = list(Question.objects.values_list('id', flat=True)[:10])

    random.shuffle(qs_ids)
    request.session['test_qs'] = qs_ids
    request.session['test_subjects'] = contest.title
    request.session['test_index'] = 0
    request.session['test_score'] = 0
    request.session['test_start'] = timezone.now().timestamp()
    request.session['test_duration'] = contest.duration_minutes * 60
    request.session['is_daily_challenge'] = False

    messages.success(request, f"Joined {contest.title}! Good luck!")
    return redirect('quiz:test_session')


from .services import extract_text_from_file, generate_mcqs_from_text

def goodies(request):
    """Goodies Rewards Store where users redeem XP / Goodies Coins for physical rewards."""
    profile = get_or_create_user_profile(request.user) if request.user.is_authenticated else None
    goodies_list = GoodieItem.objects.all()

    user_redemptions = []
    if request.user.is_authenticated:
        user_redemptions = UserGoodieRedemption.objects.filter(user=request.user).select_related('goodie')

    context = {
        'profile': profile,
        'goodies': goodies_list,
        'redemptions': user_redemptions,
        'user_redemptions': user_redemptions,
    }
    return render(request, 'quiz/goodies.html', context)

@login_required
def study_material(request):
    """Study Material page where users upload and manage documents."""
    materials = StudyMaterial.objects.filter(user=request.user).order_by('-uploaded_at')
    profile = get_or_create_user_profile(request.user)
    
    current_provider = request.session.get('ai_provider', 'auto')
    session_key = request.session.get('ai_api_key', '')
    masked_key = f"{session_key[:4]}...{session_key[-4:]}" if len(session_key) > 8 else ("Configured" if session_key else "")
    
    has_env_gemini = bool(os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY'))
    has_env_groq = bool(os.environ.get('GROQ_API_KEY'))
    has_env_openai = bool(os.environ.get('OPENAI_API_KEY'))

    context = {
        'materials': materials,
        'profile': profile,
        'current_provider': current_provider,
        'masked_key': masked_key,
        'has_env_gemini': has_env_gemini,
        'has_env_groq': has_env_groq,
        'has_env_openai': has_env_openai,
    }
    return render(request, 'quiz/study_material.html', context)


@login_required
def save_ai_settings(request):
    """Save user AI provider and optional API key in session."""
    if request.method == 'POST':
        provider = request.POST.get('provider', 'auto')
        api_key = request.POST.get('api_key', '').strip()
        clear_key = request.POST.get('clear_key')

        request.session['ai_provider'] = provider
        if clear_key == '1':
            request.session.pop('ai_api_key', None)
            messages.info(request, "Custom API key cleared. Using default/system AI.")
        elif api_key:
            request.session['ai_api_key'] = api_key
            messages.success(request, f"API key configured for {provider.upper()}! AI generation will use this key.")
        else:
            messages.info(request, f"AI generation mode set to: {provider.upper()}.")
            
    return redirect('quiz:study_material')


@login_required
def get_presigned_url(request):
    """Generate a presigned S3/Supabase URL for direct-to-cloud upload if configured."""
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid method'}, status=405)
        
    file_name = request.GET.get('file_name')
    content_type = request.GET.get('content_type')
    
    if not file_name or not content_type:
        return JsonResponse({'error': 'Missing file_name or content_type'}, status=400)
        
    s3_endpoint = os.environ.get('AWS_S3_ENDPOINT_URL')
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'study-materials')
    
    if not all([s3_endpoint, access_key, secret_key]):
        # Let frontend know to use direct multipart upload
        return JsonResponse({'error': 'Cloud storage not configured', 'use_direct_upload': True}, status=200)
        
    try:
        from botocore.config import Config
        s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=s3_endpoint,
            region_name='us-east-1',
            config=Config(signature_version='s3v4')
        )
        
        unique_filename = f"{request.user.id}_{uuid.uuid4().hex[:8]}_{file_name}"
        
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': unique_filename,
                'ContentType': content_type
            },
            ExpiresIn=3600
        )
        
        if "supabase.co" in s3_endpoint:
            base = s3_endpoint.split('/s3')[0]
            public_url = f"{base}/object/public/{bucket_name}/{unique_filename}"
        else:
            public_url = f"{s3_endpoint}/{bucket_name}/{unique_filename}"
            
        return JsonResponse({
            'presigned_url': presigned_url,
            'file_url': public_url
        })
    except Exception as e:
        return JsonResponse({'error': str(e), 'use_direct_upload': True}, status=500)


@login_required
def upload_study_material(request):
    """
    Handles file upload, cloud URL linking, or text note creation.
    Saves files locally or caches extracted text in DB for instant, reliable AI exam generation.
    """
    if request.method == 'POST':
        try:
            upload_tab = request.POST.get('upload_tab', 'file').strip()
            title = request.POST.get('title', '').strip()
            file_obj = request.FILES.get('file')
            file_url = request.POST.get('file_url', '').strip()
            notes = request.POST.get('notes', '').strip()
            
            final_file_url = None
            extracted_text = ""

            # 1. Pasted text notes
            if upload_tab == 'notes' or (notes and not file_obj and not file_url):
                if not notes or len(notes.strip()) < 15:
                    messages.error(request, "Please enter at least 15 characters of study notes to generate an AI exam.")
                    return redirect('quiz:study_material')
                extracted_text = notes.strip()
                if not title:
                    title = f"Notes - {notes[:30]}..."
                import uuid
                from django.core.files.storage import default_storage
                from django.core.files.base import ContentFile
                unique_filename = f"{request.user.id}_{uuid.uuid4().hex[:8]}_notes.txt"
                save_rel_path = os.path.join('study_material', unique_filename)
                try:
                    saved_name = default_storage.save(save_rel_path, ContentFile(notes.encode('utf-8')))
                    final_file_url = f"{settings.MEDIA_URL}{saved_name}".replace('\\', '/')
                except Exception as save_err:
                    logger.warning(f"Could not save notes to disk: {save_err}")
                    final_file_url = f"/media/study_material/{unique_filename}"

            # 2. External URL
            elif upload_tab == 'url' or (file_url and not file_obj):
                if not file_url:
                    messages.error(request, "Please enter a valid document URL.")
                    return redirect('quiz:study_material')
                final_file_url = file_url
                if not title:
                    title = "Study Resource"
                try:
                    from .services import extract_text_from_file
                    extracted_text = extract_text_from_file(file_url)
                except Exception as ex:
                    logger.warning(f"URL extraction warning: {ex}")

                if not extracted_text or len(extracted_text.strip()) < 15:
                    messages.error(
                        request,
                        "Could not extract sufficient readable text from the provided URL. "
                        "Please verify the URL is public, accessible, and points to a document with text content."
                    )
                    return redirect('quiz:study_material')

            # 3. Direct file upload
            else:
                if not file_obj:
                    messages.error(request, "Please choose a document file (PDF, DOCX, TXT) to upload.")
                    return redirect('quiz:study_material')

                ext = os.path.splitext(file_obj.name)[1].lower()
                allowed = ['.pdf', '.docx', '.txt', '.md', '.doc']
                if ext not in allowed:
                    messages.error(request, f"Unsupported file type ({ext}). Please upload a PDF, DOCX, or TXT file.")
                    return redirect('quiz:study_material')

                if file_obj.size > 25 * 1024 * 1024:
                    messages.error(request, "File size exceeds 25MB limit. Please choose a smaller file.")
                    return redirect('quiz:study_material')

                if not title:
                    title = os.path.splitext(file_obj.name)[0].replace('_', ' ').replace('-', ' ').title()

                # Extract text in memory first
                try:
                    from .services import extract_text_from_file_object, extract_text_via_gemini_multimodal
                    extracted_text = extract_text_from_file_object(file_obj, file_obj.name)

                    # Multimodal fallback for scanned PDFs if Gemini API key exists
                    if (not extracted_text or len(extracted_text.strip()) < 20) and ext == '.pdf':
                        api_key = request.session.get('ai_api_key') or os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
                        if api_key:
                            file_obj.seek(0)
                            mm_text = extract_text_via_gemini_multimodal(file_obj.read(), api_key)
                            if mm_text and len(mm_text.strip()) >= 20:
                                extracted_text = mm_text
                            file_obj.seek(0)
                except Exception as ex:
                    logger.warning(f"In-memory extraction warning: {ex}")

                # Reject files that contain no readable text layers
                if not extracted_text or len(extracted_text.strip()) < 20:
                    messages.error(
                        request,
                        f"Could not extract sufficient readable text from '{file_obj.name}'. "
                        "This file appears to be a scanned image or photo PDF without a selectable text layer. "
                        "Please upload a document with readable text (PDF, Word DOCX, TXT), or paste your study notes directly in the 'Notes' tab."
                    )
                    return redirect('quiz:study_material')

                # Safely attempt to persist to default_storage if writable
                import uuid
                from django.core.files.storage import default_storage
                safe_basename = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', file_obj.name)
                unique_filename = f"{request.user.id}_{uuid.uuid4().hex[:8]}_{safe_basename}"
                save_rel_path = os.path.join('study_material', unique_filename)
                try:
                    saved_name = default_storage.save(save_rel_path, file_obj)
                    final_file_url = f"{settings.MEDIA_URL}{saved_name}".replace('\\', '/')
                except Exception as save_err:
                    logger.warning(f"Could not save file to disk (e.g. serverless read-only filesystem): {save_err}")
                    final_file_url = f"/media/study_material/{unique_filename}"

            if (final_file_url or extracted_text) and title:
                StudyMaterial.objects.create(
                    user=request.user,
                    title=title,
                    file_url=final_file_url,
                    extracted_text=extracted_text
                )
                
                profile = get_or_create_user_profile(request.user)
                profile.total_xp += 5
                profile.save()
                
                messages.success(request, f"'{title}' uploaded successfully! You earned +5 XP.")
            else:
                messages.error(request, "Please provide a document title and select a file or paste study notes.")
        except Exception as e:
            logger.exception("Error in upload_study_material: %s", e)
            messages.error(request, f"Upload error: {str(e)}")
            
    return redirect('quiz:study_material')


@login_required
def delete_study_material(request, material_id):
    if request.method == 'POST':
        try:
            material = get_object_or_404(StudyMaterial, id=material_id, user=request.user)
            # Safely delete local file if present
            if material.file_url:
                if material.file_url.startswith(settings.MEDIA_URL) or material.file_url.startswith('/media/'):
                    rel_path = material.file_url.replace(settings.MEDIA_URL, '').lstrip('/')
                    full_path = os.path.join(settings.MEDIA_ROOT, rel_path)
                    if os.path.exists(full_path):
                        try:
                            os.remove(full_path)
                        except Exception:
                            pass
            material.delete()
            messages.success(request, "Study material deleted successfully.")
        except Exception as e:
            logger.exception("Error deleting study material: %s", e)
            messages.error(request, f"Error deleting study material: {str(e)}")
    return redirect('quiz:study_material')


@login_required
def start_ai_exam(request, material_id):
    try:
        material = get_object_or_404(StudyMaterial, id=material_id, user=request.user)
        
        # Question count (1 - 100)
        try:
            num_questions = int(request.GET.get('num_questions', 5))
            if num_questions > 100:
                num_questions = 100
            elif num_questions < 1:
                num_questions = 1
        except ValueError:
            num_questions = 5
            
        provider = request.GET.get('provider') or request.session.get('ai_provider')
        api_key = request.GET.get('api_key') or request.session.get('ai_api_key')
        
        # Extract or use cached text
        text = material.extracted_text
        if not text:
            if material.file_url:
                text = extract_text_from_file(material.file_url)
                if text:
                    # Cache in DB so future exam generation is instant
                    material.extracted_text = text
                    material.save(update_fields=['extracted_text'])
            
        if not text or len(text.strip()) < 15:
            messages.error(
                request,
                f"Could not extract sufficient readable text from '{material.title}'. "
                "This document appears to be empty or a scanned image without selectable text. "
                "Please delete it and upload a digital PDF/Word document, or paste your study notes in the Notes tab."
            )
            return redirect('quiz:study_material')
            
        mcqs, error_msg, engine_used = generate_mcqs_from_text(
            text=text,
            title=material.title,
            num_questions=num_questions,
            api_key=api_key,
            provider=provider
        )
        
        if not mcqs:
            messages.error(request, f"Failed to generate questions: {error_msg}")
            return redirect('quiz:study_material')
            
        # Create Exam
        exam = Exam.objects.create(material=material, user=request.user, total=len(mcqs))
        
        for q in mcqs:
            # Clean and sanitize choices and correct choice
            corr_choice = 'A'
            raw_c = str(q.get('correct_choice', 'A')).strip().upper()
            for ch in raw_c:
                if ch in ('A', 'B', 'C', 'D'):
                    corr_choice = ch
                    break

            ExamQuestion.objects.create(
                exam=exam,
                question_text=str(q.get('question_text', '')).strip(),
                choice_a=str(q.get('choice_a', '')).strip(),
                choice_b=str(q.get('choice_b', '')).strip(),
                choice_c=str(q.get('choice_c', '')).strip(),
                choice_d=str(q.get('choice_d', '')).strip(),
                correct_choice=corr_choice,
                explanation=str(q.get('explanation', '')).strip()
            )
            
        messages.success(request, f"Exam generated successfully ({len(mcqs)} questions via {engine_used})! Best of luck.")
        return redirect('quiz:take_ai_exam', exam_id=exam.id)
    except Exception as e:
        logger.exception("Error in start_ai_exam: %s", e)
        messages.error(request, f"An error occurred while generating the exam: {str(e)}")
        return redirect('quiz:study_material')

@login_required
def take_ai_exam(request, exam_id):
    try:
        exam = get_object_or_404(Exam, id=exam_id, user=request.user)
        if exam.completed_at:
            messages.info(request, "You have already completed this exam.")
            return redirect('quiz:study_material')
            
        questions = exam.questions.all()
        return render(request, 'quiz/take_ai_exam.html', {'exam': exam, 'questions': questions})
    except Exception as e:
        logger.exception("Error in take_ai_exam: %s", e)
        messages.error(request, f"Error loading exam: {str(e)}")
        return redirect('quiz:study_material')

@login_required
def submit_ai_exam(request, exam_id):
    try:
        if request.method != 'POST':
            return redirect('quiz:study_material')
            
        exam = get_object_or_404(Exam, id=exam_id, user=request.user)
        if exam.completed_at:
            return redirect('quiz:study_material')
            
        score = 0
        for q in exam.questions.all():
            ans = request.POST.get(f'question_{q.id}')
            if ans:
                q.user_answer = ans.strip().upper()
                q.save()
                if q.user_answer == q.correct_choice.strip().upper():
                    score += 1
                    
        exam.score = score
        exam.completed_at = timezone.now()
        exam.save()
        
        # Award XP for AI practice (e.g., 10 XP per correct)
        if hasattr(request.user, 'profile'):
            request.user.profile.total_xp += (score * 10)
            request.user.profile.save()
            
        messages.success(request, f"Exam completed! You scored {score} / {exam.total}.")
        return render(request, 'quiz/ai_exam_result.html', {'exam': exam})
    except Exception as e:
        logger.exception("Error in submit_ai_exam: %s", e)
        messages.error(request, f"Error submitting exam: {str(e)}")
        return redirect('quiz:study_material')



@login_required
def redeem_goodie(request, pk):
    """Initiates goodie redemption flow by checking prerequisites and redirecting to address checkout."""
    goodie = get_object_or_404(GoodieItem, pk=pk)
    profile = get_or_create_user_profile(request.user)

    if goodie.stock <= 0:
        messages.error(request, f"Sorry, {goodie.name} is currently out of stock!")
        return redirect('quiz:goodies')
    elif profile.total_xp < goodie.coin_cost:
        messages.error(request, f"Insufficient XP! You need {goodie.coin_cost} XP to redeem {goodie.name}. Current XP: {profile.total_xp}.")
        return redirect('quiz:goodies')

    return redirect('quiz:redeem_address', pk=pk)


@login_required
def redeem_address(request, pk):
    """Checkout page to enter shipping address and complete goodie order redemption."""
    goodie = get_object_or_404(GoodieItem, pk=pk)
    profile = get_or_create_user_profile(request.user)

    if goodie.stock <= 0:
        messages.error(request, f"Sorry, {goodie.name} is currently out of stock!")
        return redirect('quiz:goodies')
    if profile.total_xp < goodie.coin_cost:
        messages.error(request, f"Insufficient XP! You need {goodie.coin_cost} XP to redeem {goodie.name}. Current XP: {profile.total_xp}.")
        return redirect('quiz:goodies')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        shipping_address = request.POST.get('shipping_address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()

        if not full_name or not phone_number or not shipping_address or not city or not pincode:
            messages.error(request, "Please fill in all required shipping address fields.")
            return render(request, 'quiz/redeem_address.html', {
                'goodie': goodie,
                'profile': profile,
                'remaining_xp': profile.total_xp - goodie.coin_cost,
                'full_name': full_name,
                'phone_number': phone_number,
                'shipping_address': shipping_address,
                'city': city,
                'state': state,
                'pincode': pincode,
            })

        with transaction.atomic():
            g_locked = GoodieItem.objects.select_for_update().get(pk=pk)
            prof_locked = UserProfile.objects.select_for_update().get(user=request.user)

            if g_locked.stock <= 0:
                messages.error(request, f"Sorry, {g_locked.name} is out of stock!")
                return redirect('quiz:goodies')
            if prof_locked.total_xp < g_locked.coin_cost:
                messages.error(request, "Insufficient XP coins to complete redemption!")
                return redirect('quiz:goodies')

            prof_locked.total_xp -= g_locked.coin_cost
            prof_locked.save()

            g_locked.stock -= 1
            g_locked.save()

            order = UserGoodieRedemption.objects.create(
                user=request.user,
                goodie=g_locked,
                full_name=full_name,
                phone_number=phone_number,
                shipping_address=shipping_address,
                city=city,
                state=state,
                pincode=pincode,
                status="Pending Processing"
            )

            messages.success(request, f"🎉 Order #{order.id} Placed Successfully! Your reward '{goodie.name}' is being processed for shipping.")
            return redirect('quiz:goodies')

    context = {
        'goodie': goodie,
        'profile': profile,
        'remaining_xp': profile.total_xp - goodie.coin_cost,
        'full_name': request.user.get_full_name() or request.user.username,
    }
    return render(request, 'quiz/redeem_address.html', context)


