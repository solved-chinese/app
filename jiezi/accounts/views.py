from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.forms import *
from learning.models import CharacterSet, Character, Radical

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # why? this seems to create the user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user.save()
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


def manage_stack_new_set_modal(request):
    sets = []
    for set in CharacterSet.objects.all():
        if not request.user.user_character_tags.filter(name=set.name):
            sets.append(set)
    return render(request, 'accounts/manage_stack_new_character.html', {'sets': sets})


@login_required
def manage_stack(request):
    return render(request, 'accounts/manage_stack.html')