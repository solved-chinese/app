from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'display_name', 'email')
        help_texts = {
            'username': 'This is used for login only. '
                        'It can never be changed after signup.',
        }


class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = ('username', 'display_name', 'email')
        help_texts = {
            'username': 'Readonly. This is used for login.',
            'email': "Your email is used for resetting password and receiving"
                     " notifications",
        }

    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return instance.username
        else:
            raise Exception('Cannot use this form unbounded')
