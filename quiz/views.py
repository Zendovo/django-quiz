from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import *


@method_decorator(login_required, name='dispatch')
class QuizListView(ListView):
    model = Quiz


@method_decorator(login_required, name='dispatch')
class QuizAttemptView(View):
    model = Quiz

    def get(self, request, *args, **kwargs):
        quiz_id = kwargs['id']
        quiz = Quiz.objects.filter(pk=quiz_id)

        if not quiz.exists():
            return HttpResponseNotFound('Quiz not found')
        quiz = quiz[0]

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

        attempt = Attempt.objects.create(quiz=quiz, attempter=request.user)

        questions = Question.objects.filter(quiz=quiz)

        scq = questions.filter(question_type='SCQ')
        mcq = questions.filter(question_type='MCQ')
        num = questions.filter(question_type='NUM')
        bool = questions.filter(question_type='BOOL')

        for question in scq:
            selected_opt_id = data[f'{question.id}'][0]
            selected = Option.objects.filter(
                question=question, id=selected_opt_id)
            if not selected.exists():
                return HttpResponseBadRequest('Bad Request')
            selected = selected[0]

            answer = Answer.objects.create(attempt=attempt, question=question)
            if selected_opt_id is not None:
                SelectedOptions.objects.create(answer=answer, option=selected)

        for question in mcq:
            options = Option.objects.filter(question=question)
            answer = Answer.objects.create(attempt=attempt, question=question)
            for opt_id in data[f'{question.id}']:
                option = options.filter(id=int(opt_id))

                if option.exists():
                    SelectedOptions.objects.create(answer=answer, option=option[0])

        for question in num:
            answer = Answer.objects.create(attempt=attempt, question=question)
            try:
                input = int(data[f'{question.id}'][0])
                answer.num_answer = input
                answer.save()
            except ValueError:
                pass

        for question in bool:
            answer = Answer.objects.create(attempt=attempt, question=question)
            input = data[f'{question.id}'][0]

            if input == '1':
                answer.bool_answer = True
            elif input == '0':
                answer.bool_answer = False

        return redirect('quiz-list-view')
