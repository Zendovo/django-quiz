from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView
from django.http import HttpResponseNotFound, HttpResponseBadRequest

from .models import *

# Create your views here.
class QuizListView(ListView):
    model = Quiz


class QuizAttemptView(View):
    model = Quiz
    
    def get(self, request, *args, **kwargs):
        quiz_id = kwargs['id']
        quiz = Quiz.objects.filter(pk=quiz_id)

        if not quiz.exists():
            return HttpResponseNotFound('Quiz not found')
        quiz = quiz[0]
        
        questions = Question.objects.filter(quiz=quiz)

        return render(request, 'quiz/attempt.html', { 'quiz': quiz, 'questions': questions, })

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
        for question in questions:
            selected_opt_id = data[f'{question.id}'][0]
            selected = Option.objects.filter(question=question, id=selected_opt_id)
            if not selected.exists():
                return HttpResponseBadRequest('Bad Request')
            selected = selected[0]

            if selected_opt_id is not None:
                Answer.objects.create(attempt=attempt, question=question, selected=selected)
            else:
                Answer.objects.create(attempt=attempt, question=question)

        return redirect('quiz-list-view')


