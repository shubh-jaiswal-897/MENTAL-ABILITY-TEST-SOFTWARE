from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:pk>/', views.take_quiz, name='take_quiz'),
    path('result/<int:pk>/<int:correct>/', views.result, name='result'),
    path('accounts/signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('revision/', views.revision, name='revision'),
    path('test-session/', login_required(views.test_session), name='test_session'),
    path('test-result/', login_required(views.test_result), name='test_result'),
    path('dashboard/', login_required(views.dashboard), name='dashboard'),
]
