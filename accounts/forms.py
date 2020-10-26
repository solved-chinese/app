from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class UserSignupForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Must contain at least 4 characters.",
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    class Meta:
        model = User
        fields = ('username', 'display_name', 'email')
        help_texts = {
            'username': 'Used for login and as a unique identifier of your '
                        'account. You won’t be able to change it later, '
                        'so choose wisely!',
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
            'username': 'This is used for login. You cannot change this.',
        }

    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return instance.username
        else:
            raise Exception('Cannot use this form unbounded')
