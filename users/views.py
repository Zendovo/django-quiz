from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.http import HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from quiz.models import *

# Create your views here.


class RegisterView(View):
    form_class = RegisterForm
    template_name = "registration/sign_up.html"

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class LoginRedirectView(View):

    def get(self, request):
        if request.user.is_staff and request.user.groups.filter(name="Quiz Master").exists():
            return redirect('admin:index')

        return redirect('quiz-list-view')


@method_decorator(login_required, name='dispatch')
class PrevAttemptsView(View):

    def get(self, request):
        attempts = Attempt.objects.filter(attempter=request.user)
        return render(request, 'users/prev_attempts.html', {'attempts': attempts})


@method_decorator(login_required, name='dispatch')
class PrevAttemptDetailView(View):

    def get(self, request, *args, **kwargs):
        attempt_id = kwargs['id']
        attempt = Attempt.objects.filter(id=attempt_id, attempter=request.user)

        if not attempt.exists():
            return HttpResponseNotFound('Attempt ID invalid')
        attempt = attempt[0]

        score = 0
        for answer in attempt.answers.all():
            question = answer.question

            if question.question_type == 'SCQ':
                selected = answer.selected_options.all()
                if len(selected) == 0:
                    continue

                selected = selected[0]
                if selected.option.answer:
                    score += question.positive_marking
                else:
                    score -= question.negative_marking

            elif question.question_type == 'MCQ':
                selected = answer.selected_options.all()
                correct_opts = question.options.filter(answer=True)

                neg = 0
                for option in selected:
                    if option.option.answer == False:
                        score -= question.negative_marking
                        neg = 1
                        break

                if neg:
                    continue

                if len(selected) == len(correct_opts):
                    score += question.positive_marking

            elif question.question_type == 'NUM':
                if not answer.num_answer is None:
                    if answer.num_answer == question.num_answer:
                        score += question.positive_marking
                    else:
                        score -= question.negative_marking

            else:
                if not answer.bool_answer is None:
                    if answer.bool_answer == question.bool_answer:
                        score += question.positive_marking
                    else:
                        score -= question.negative_marking

        return render(request, 'users/prev_attempts_detail.html', {'attempt': attempt, 'score': score})
