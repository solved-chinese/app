from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect

from accounts.forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    if request.GET.get('endsession', False):
        request.session['is_learning'] = False

    return render(request, 'accounts/profile.html')


@login_required
def staff_panel(request):
    if request.GET.get('endsession', False):
        request.session['is_learning'] = False

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('profile'))

    return render(request, 'accounts/staff_panel.html')


@login_required
def alt_profile(request):
    if request.method == 'POST':
        currentUser = request.user
        currentUser.email = request.POST.get("email")
        currentUser.first_name = request.POST.get("first_name")
        currentUser.last_name = request.POST.get("last_name")
        currentUser.save()
        return HttpResponseRedirect(reverse('profile'))
    else:
        return render(request, 'accounts/profile.html')
