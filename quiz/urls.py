from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'quiz'

from . import ai_chat

urlpatterns = [
    path('', views.index, name='index'),
    path('debug-db/', views.debug_db, name='debug_db'),
    path('question/<int:pk>/', views.take_quiz, name='take_quiz'),
    path('result/<int:pk>/<int:correct>/', views.result, name='result'),
    path('accounts/signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('revision/', views.revision, name='revision'),
    path('test-session/', login_required(views.test_session), name='test_session'),
    path('daily-challenge/', login_required(views.daily_challenge), name='daily_challenge'),
    path('test-result/', login_required(views.test_result), name='test_result'),
    path('dashboard/', login_required(views.dashboard), name='dashboard'),
    path('contests/', views.contests, name='contests'),
    path('join-contest/<int:pk>/', login_required(views.join_contest), name='join_contest'),
    path('study-material/', login_required(views.study_material), name='study_material'),
    path('study-material/upload/', login_required(views.upload_study_material), name='upload_study_material'),
    path('study-material/delete/<int:material_id>/', login_required(views.delete_study_material), name='delete_study_material'),
    path('study-material/exam/start/<int:material_id>/', login_required(views.start_ai_exam), name='start_ai_exam'),
    path('study-material/exam/<int:exam_id>/', login_required(views.take_ai_exam), name='take_ai_exam'),
    path('study-material/exam/<int:exam_id>/submit/', login_required(views.submit_ai_exam), name='submit_ai_exam'),
    path('goodies/', views.goodies, name='goodies'),
    path('redeem-goodie/<int:pk>/', login_required(views.redeem_goodie), name='redeem_goodie'),
    path('goodies/redeem/<int:pk>/address/', login_required(views.redeem_address), name='redeem_address'),
    path('ai-chat/', ai_chat.ollama_chat_view, name='ai_chat'),
    path('ai-chat/models/', ai_chat.ollama_models_view, name='ai_models'),
]

