from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group

from .forms import RegisterForm

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
