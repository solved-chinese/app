from django import forms
from .models import Teacher, Student, Assignment
from content.models import CharacterSet
from django.forms import ModelChoiceField


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['school', 'school_description', 'wechat_id']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = []


class AssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        in_class = kwargs.pop('in_class')
        super().__init__(*args, **kwargs)
        self.fields['character_set'] = forms.ModelChoiceField(
            queryset=CharacterSet.objects.exclude(assignment__in_class=in_class))

    class Meta:
        model = Assignment
        fields = ['character_set']
