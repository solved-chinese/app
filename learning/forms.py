from django import forms
from .models import ReviewManager, Ability
from content.reviews import *


class ReviewManagerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = ReviewManager
        exclude = ['monitored_abilities']
