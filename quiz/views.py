from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import ListView, CreateView
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
import urllib

from .models import *


@method_decorator(login_required, name='dispatch')
class QuizListView(ListView):
    model = Quiz


@method_decorator(login_required, name='dispatch')
class QuizPasswordView(View):

    def get(self, request, *args, **kwargs):
        quiz_id = kwargs['id']
        quiz = Quiz.objects.filter(pk=quiz_id)

        if not quiz.exists():
            return HttpResponseNotFound('Quiz not found')
        quiz = quiz[0]

        if quiz.password is None:
            return redirect('quiz-attempt-view', id=quiz_id)

        return render(request, 'quiz/password.html', {})

    def post(self, request, *args, **kwargs):
        quiz_id = kwargs['id']
        quiz = Quiz.objects.filter(pk=quiz_id)

        if not quiz.exists():
            return HttpResponseNotFound('Quiz not found')
        quiz = quiz[0]

        data = request.POST

        password = data.get('password', None)
        if password is None:
            return HttpResponseBadRequest('No Password')
        
        if check_password(password, quiz.password):
            return redirect(f"/quiz/{quiz_id}/?{urllib.parse.urlencode({'ph': make_password(password, salt='test')})}")

        return HttpResponseBadRequest('No Password')


@method_decorator(login_required, name='dispatch')
class QuizAttemptView(View):

    def get(self, request, *args, **kwargs):
        quiz_id = kwargs['id']
        quiz = Quiz.objects.filter(pk=quiz_id)

        if not quiz.exists():
            return HttpResponseNotFound('Quiz not found')
        quiz = quiz[0]

        if not quiz.password is None:
            if quiz.password != request.GET.get('ph', None):
                return redirect('quiz-password-view', id=quiz_id)

        questions = Question.objects.filter(quiz=quiz)

        scq = questions.filter(question_type='SCQ')
        mcq = questions.filter(question_type='MCQ')
        num = questions.filter(question_type='NUM')
        bool = questions.filter(question_type='BOOL')

        return render(request, 'quiz/attempt.html', {'quiz': quiz, 'questions': {'scq': scq, 'mcq': mcq, 'num': num, 'bool': bool}, })

    def post(self, request, *args, **kwargs):
        print(request.POST)
        data = request.POST

        quiz_id = kwargs['id']
        quiz = Quiz.objects.filter(pk=quiz_id)

        if not quiz.exists():
            return HttpResponseNotFound('Quiz not found')
        quiz = quiz[0]

        if not quiz.password is None:
            if quiz.password != request.GET.get('ph', None):
                redirect('quiz-password-view', id=quiz_id)

        attempt = Attempt.objects.create(quiz=quiz, attempter=request.user)

        questions = Question.objects.filter(quiz=quiz)

        scq = questions.filter(question_type='SCQ')
        mcq = questions.filter(question_type='MCQ')
        num = questions.filter(question_type='NUM')
        bool = questions.filter(question_type='BOOL')

        for question in scq:
            answer = Answer.objects.create(attempt=attempt, question=question)

            selected_opt_id = data.get(f'{question.id}'[0], None)
            selected = Option.objects.filter(
                question=question, id=selected_opt_id)
            if not selected.exists():
                return HttpResponseBadRequest('Bad Request')
            selected = selected[0]

            if selected_opt_id is not None:
                SelectedOptions.objects.create(answer=answer, option=selected)

        for question in mcq:
            options = Option.objects.filter(question=question)
            answer = Answer.objects.create(attempt=attempt, question=question)

            for option in options:
                print(data.get(f'{question.id}-{option.id}', None))
                tt = data.get(f'{question.id}-{option.id}', None)
                if not tt is None:
                    SelectedOptions.objects.create(
                        answer=answer, option=option)

        for question in num:
            answer = Answer.objects.create(attempt=attempt, question=question)
            tt = data.get(f'{question.id}', None)
            input = int(tt[0])

            if not input is None:
                answer.num_answer = input
                answer.save()

        for question in bool:
            answer = Answer.objects.create(attempt=attempt, question=question)
            input = data.get(f'{question.id}', ['None'])[0]

            if input == '1':
                answer.bool_answer = True
            elif input == '0':
                answer.bool_answer = False
            answer.save()

        return redirect('quiz-list-view')
