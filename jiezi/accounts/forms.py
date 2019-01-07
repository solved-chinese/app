from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from accounts.models import User

class SignUpForm(UserCreationForm):
    grade = forms.IntegerField(help_text="enter grade")

    def clean_grade(self):
        data = self.cleaned_data['grade']
        if data < 0:
            raise ValidationError('grade >= 0 ')
        return data

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'grade')