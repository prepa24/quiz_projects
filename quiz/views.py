# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, QuizConfig, QuizHistory, QuizSettings
import random, time
from django.utils.translation import gettext as _
from django.contrib.auth.models import User



def home(request):
    return render(request, 'quiz/start.html')

def start_quiz(request):
    try:
        config = QuizConfig.objects.first()
        total_questions = config.num_questions
    except QuizConfig.DoesNotExist:
        total_questions = 50

    all_questions = list(Question.objects.all())
    
    if len(all_questions) < total_questions:
        return render(request, 'quiz/error.html', {'message': 'Not enough questions in the database.'})
    
    quiz_settings = QuizSettings.objects.first()
    time_limit = quiz_settings.time_limit if quiz_settings else 10

    request.session['time_limit'] = time_limit * 60
    request.session['start_time'] = time.time()  # Save current time as start time
    
    # Debogaj pou verifye si start_time byen sove
    print("Start Time Saved:", request.session['start_time'])

    selected_questions = random.sample(all_questions, total_questions)
    request.session['questions'] = [q.id for q in selected_questions]
    request.session['current'] = 0
    request.session['answers'] = {}
    request.session['skipped'] = []
    request.session['correct_answers'] = 0
    request.session['incorrect_answers'] = 0
    return redirect('quiz:question')

def question(request):
    questions = request.session.get('questions', [])
    current = request.session.get('current', 0)

    if not questions:
        return redirect('quiz:start_quiz')

    if current >= len(questions):
        return redirect('quiz:results')

    # Check time limit
    start_time = request.session.get('start_time')
    time_limit = request.session.get('time_limit')

    if start_time is None or time_limit is None:
        return redirect('quiz:start_quiz')

    elapsed_time = time.time() - start_time
    remaining_time_seconds = time_limit - int(elapsed_time)

    # Konvèti segonn yo an minit
    remaining_minutes = remaining_time_seconds // 60
    remaining_seconds = remaining_time_seconds % 60

    if remaining_minutes <= 0:
        return redirect('quiz:time_up')

    question_id = questions[current]
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question)
    has_error = request.GET.get('has_error', False)
    
    # Real-time counts
    correct_count = request.session.get('correct_answers', 0)
    incorrect_count = request.session.get('incorrect_answers', 0)
    skipped_count = len(request.session['skipped'])
    
    context = {
        'question': question,
        'answers': answers,
        'has_error': has_error,
        #'remaining_time': remaining_time,
        'remaining_minutes': remaining_minutes,
        'remaining_seconds': remaining_seconds,
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'skipped_count': skipped_count,
    }
    return render(request, 'quiz/question.html', context)

def submit_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_id = request.POST.get('answer')
        
        if not answer_id and 'skip' not in request.POST:
            return redirect(f"{reverse('quiz:question')}?has_error=True")
        
        if answer_id:
            answer = Answer.objects.get(id=answer_id)
            if answer.is_correct:
                request.session['correct_answers'] += 1
            else:
                request.session['incorrect_answers'] += 1
            request.session['answers'][question_id] = answer_id

        if 'skip' in request.POST:
            if question_id not in request.session['skipped']:
                request.session['skipped'].append(question_id)
        else:
            if question_id in request.session['skipped']:
                request.session['skipped'].remove(question_id)

        request.session['current'] += 1

        # Calculate score to determine if user has passed 80% of the questions correctly
        correct_answers = request.session['correct_answers']
        total_questions = len(request.session['questions'])

        score_percentage = (correct_answers / total_questions) * 100

        if score_percentage >= 80:
            return redirect('quiz:results')
        
        # Verify if there are more questions to answer
        if request.session['current'] < len(request.session['questions']):
            return redirect('quiz:question')

        # If there are skipped questions left to answer, redirect to the first skipped question
        if request.session['skipped']:
            next_skipped_question = request.session['skipped'].pop(0)
            request.session['questions'].append(next_skipped_question)
            request.session['current'] -= 1  # Make sure we don't increase the total question count
            return redirect('quiz:question')

        return redirect('quiz:results')

def results(request):
    user = request.user
    if not isinstance(user, User):
        return HttpResponse("User must be logged in to view results.", status=403)

    answers = request.session.get('answers', {})
    questions = request.session.get('questions', [])
    correct_answers = request.session.get('correct_answers', 0)
    skipped = len(request.session.get('skipped', []))
    incorrect_answers = len(answers) - correct_answers
    score_percentage = (correct_answers / len(questions)) * 100 if questions else 0
    passed = score_percentage >= 80

    start_time = request.session.get("start_time")
    end_time = time.time()
    
    # Verifye si start_time egziste avan nou kontinye
    if not start_time:
        print("Error: Start time not found in session.")
        return redirect('quiz:start_quiz')  # Redireksyon si start_time pa jwenn

    total_time_seconds = int(end_time - start_time)

    QuizHistory.objects.create(
        user=user,
        date_taken=timezone.now(),
        passed=passed,
        correct_answers=correct_answers,
        incorrect_answers=incorrect_answers,
        total_time_seconds=total_time_seconds
    )

    context = {
        'total_questions': len(questions),
        'correct': correct_answers,
        'incorrect': incorrect_answers,
        'skipped': skipped,
        'score_percentage': score_percentage,
        'passed': passed,
        'total_time_seconds': total_time_seconds
    }
    return render(request, 'quiz/results.html', context)


@login_required
def history_view(request):
    history = QuizHistory.objects.filter(user=request.user).order_by('-date_taken')
    return render(request, 'quiz/history.html', {'history': history})




def time_up(request):
    answers = request.session.get('answers', {})
    questions = request.session.get('questions', [])
    correct_answers = request.session.get('correct_answers', 0)
    skipped = len(request.session['skipped'])

    incorrect_answers = len(answers) - correct_answers
    score_percentage = (correct_answers / len(questions)) * 100
    passed = score_percentage >= 80

    context = {
        'total_questions': len(questions),
        'correct': correct_answers,
        'incorrect': incorrect_answers,
        'skipped': skipped,
        'score_percentage': score_percentage,
        'passed': passed,
        'time_up': True,
    }
    return render(request, 'quiz/results.html', context)

def check_time(request):
    start_time = request.session.get('start_time')
    time_limit = request.session.get('time_limit')

    if start_time is None or time_limit is None:
        return JsonResponse({'time_up': True})

    elapsed_time = time.time() - start_time
    remaining_time = time_limit - elapsed_time

    if remaining_time <= 0:
        return JsonResponse({'time_up': True})
    
    return JsonResponse({'time_up': False})
