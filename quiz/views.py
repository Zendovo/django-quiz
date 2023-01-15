from django.shortcuts import render
from django.views.generic import ListView, CreateView

from .models import Quiz

# Create your views here.
class QuizListView(ListView):
    model = Quiz


class QuizAttemptView(CreateView):
    model = Quiz
    template_name = ".html"

