from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
import django.contrib.auth.views as auth_views

from .forms import UserSignupForm, UserUpdateForm
from classroom.forms import StudentForm, TeacherForm


def role_signup(request, role_form_class, role):
    if request.method == 'POST':
        user_form = UserSignupForm(data=request.POST)
        role_form = role_form_class(data=request.POST)
        if user_form.is_valid() and role_form.is_valid():
            user = user_form.save()
            setattr(user, f'is_{role}', True)
            user.save()

            role = role_form.save(commit=False)
            role.user = user
            role.save()

            login(request, user)
            return redirect('index')
    else:
        user_form = UserSignupForm()
        role_form = role_form_class()

    context = {'forms': [user_form, role_form], 'role': role}
    return render(request, 'accounts/role_signup.html', context)


def student_signup(request):
    return role_signup(request, StudentForm, 'student')


def teacher_signup(request):
    return role_signup(request, TeacherForm, 'teacher')


@login_required
def profile(request):
    if request.user.is_student:
        role_form_class = StudentForm
        role = request.user.student
    elif request.user.is_teacher:
        role_form_class = TeacherForm
        role = request.user.teacher
    else:
        raise Exception("User must be either student or teacher")

    success=False
    if request.method == 'POST':
        user_form = UserUpdateForm(instance=request.user, data=request.POST)
        role_form = role_form_class(instance=role, data=request.POST)
        if user_form.is_valid() and role_form.is_valid():
            user_form.save()
            role_form.save()
            success = True
    else:
        user_form = UserUpdateForm(instance=request.user)
        role_form = role_form_class(instance=role)

    context = {'forms': [user_form, role_form], 'success' : success}
    return render(request, 'accounts/profile.html', context)


class Login(auth_views.LoginView):
    template_name = 'accounts/login.html'


class Logout(auth_views.LogoutView):
    template_name = 'accounts/logged_out.html'


class ChangePassword(auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'


class DoneChangePassword(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/done_change_password.html'


@login_required
def staff_panel(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('profile'))

    return render(request, 'accounts/staff_panel.html')
