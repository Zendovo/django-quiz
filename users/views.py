from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.http import HttpResponseNotFound

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


class PrevAttemptsView(View):
    
    def get(self, request):
        attempts = Attempt.objects.filter(attempter=request.user)
        return render(request, 'users/prev_attempts.html', {'attempts': attempts})


class PrevAttemptDetailView(View):
    
    def get(self, request, *args, **kwargs):
        attempt_id = kwargs['id']
        attempt = Attempt.objects.filter(id=attempt_id, attempter=request.user)

        if not attempt.exists():
            return HttpResponseNotFound('Attempt ID invalid')
        attempt = attempt[0]
        return render(request, 'users/prev_attempts_detail.html', {'attempt': attempt})
