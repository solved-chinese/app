from django import forms

from .models import Teacher, Student, Assignment
from content.models import WordSet


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['school']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = []


class AssignmentCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.klass = kwargs.pop('klass')
        super().__init__(*args, **kwargs)
        self.fields['wordset'] = forms.ModelChoiceField(
            queryset=WordSet.objects.filter(is_done=True)
                .exclude(assignment__klass=self.klass).exclude(words=None),
            widget=forms.RadioSelect()
        )

    class Meta:
        model = Assignment
        fields = ['wordset']
