from django import forms

from mptt.forms import TreeNodeChoiceField

from .models import Teacher, Student, Assignment
from content.models import WordSet


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = []


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = []


class AssignmentCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.klass = kwargs.pop('klass')
        super().__init__(*args, **kwargs)
        self.fields['wordset'] = TreeNodeChoiceField(
            queryset=WordSet.objects.exclude(
                assignment__klass=self.klass),
            widget=forms.RadioSelect()
        )

    class Meta:
        model = Assignment
        fields = ['wordset']
