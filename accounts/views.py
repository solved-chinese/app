from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import django.contrib.auth.views as auth_views
from django.shortcuts import render, redirect
from django.core.mail import mail_managers

from jiezi.settings import DEBUG
from classroom.forms import StudentForm, TeacherForm
from .forms import UserSignupForm, UserUpdateForm


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

    success = False
    if request.method == 'POST':
        user_form = UserUpdateForm(instance=request.user, data=request.POST)
        role_form = role_form_class(instance=role, data=request.POST)
        if user_form.is_valid() and role_form.is_valid():
            user_form.save()
            role_form.save()
            success = True
        else:
            # there seems to be a problem with request.user being Lazy that
            # causes request.user to be out of date in template rendering
            # when form is not valid
            request.user.refresh_from_db()
    else:
        user_form = UserUpdateForm(instance=request.user)
        role_form = role_form_class(instance=role)

    context = {'forms': [user_form, role_form], 'success': success}
    return render(request, 'accounts/profile.html', context)


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

            if not DEBUG and role == 'teacher':
                mail_managers(
                    f'New teacher registration',
                    f'user: {repr(user)} \n email: {user.email}\n '
                    f'school {role.school}',
                    fail_silently=True
                )
            login(request, user)
            return redirect('index')
    else:
        user_form = UserSignupForm()
        role_form = role_form_class()

    context = {'forms': [user_form, role_form], 'role': role}
    return render(request, 'accounts/role_signup.html', context)


def signup(request):
    return render(request, "accounts/signup.html")


def student_signup(request):
    return role_signup(request, StudentForm, 'student')


def teacher_signup(request):
    return role_signup(request, TeacherForm, 'teacher')


class Login(auth_views.LoginView):
    template_name = 'accounts/login.html'


class Logout(auth_views.LogoutView):
    next_page = 'index'


class ChangePassword(auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'


class DoneChangePassword(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/done_change_password.html'


class PasswordReset(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'
    html_email_template_name = 'emails/password_reset_email.html'


class PasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'


class PasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/done_change_password.html'
