from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render

def signup(request):
    return render(request, 'accounts/signup.html')
class Login(LoginView):
    template_name = 'accounts/login.html'