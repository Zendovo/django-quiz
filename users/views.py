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
from quiz.helpers import calculate_score

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

        score = calculate_score(attempt)

        return render(request, 'users/prev_attempts_detail.html', {'attempt': attempt, 'score': score})
