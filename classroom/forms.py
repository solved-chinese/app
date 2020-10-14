from django import forms
from .models import Teacher, Student


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['school', 'school_description', 'wechat_id']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = []
