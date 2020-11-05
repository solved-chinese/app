from django import forms

from .models import Teacher, Student, Assignment
from content.models import CharacterSet
from learning.fields import ReviewManagerField


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['school', 'school_description', 'wechat_id']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = []


class AssignmentForm(forms.ModelForm):
    review_manager = ReviewManagerField(
        label="Please select what types of review questions you want your "
              "student to encounter in this assignment"
    )

    def __init__(self, *args, **kwargs):
        self.in_class = kwargs.pop('in_class')
        super().__init__(*args, **kwargs)
        self.fields['character_set'] = forms.ModelChoiceField(
            queryset=CharacterSet.objects.exclude(
                assignment__in_class=self.in_class),
            widget=forms.RadioSelect()
        )

    class Meta:
        model = Assignment
        fields = ['character_set', 'review_manager']
