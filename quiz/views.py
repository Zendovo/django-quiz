from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, CreateView
from django.http import HttpResponseNotFound

from .models import Quiz, Question

# Create your views here.
class QuizListView(ListView):
    model = Quiz


class QuizAttemptView(View):
    model = Quiz
    
    def get(self, request, *args, **kwargs):
        quiz_id = kwargs['id']# get the id

        quiz = Quiz.objects.filter(pk=quiz_id)

        if not quiz.exists():
            return HttpResponseNotFound('Quiz not found')
        quiz = quiz[0]
        
        questions = Question.objects.filter(quiz=quiz)

        return render(request, 'quiz/attempt.html', { 'quiz': quiz, 'questions': questions, })

