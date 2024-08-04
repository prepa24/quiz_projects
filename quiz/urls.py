from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.start_quiz, name='start_quiz'),
    path('question/', views.question, name='question'),
    path('submit/', views.submit_answer, name='submit_answer'),
    path('results/', views.results, name='results'),
    path('time_up/', views.time_up, name='time_up'),
    path('check_time/', views.check_time, name='check_time'),
]
