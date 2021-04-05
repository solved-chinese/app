from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

from jiezi.utils.mixins import StudentOnlyMixin
from .models import Class, Student
from learning.models import LearningProcess


class JoinClassView(StudentOnlyMixin, View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.student = Student.of(request.user)

    def get(self, request, *args, **kwargs):
        if self.student.klass:
            messages.add_message(
                request,
                messages.ERROR,
                f'You are already in "{self.student.klass.name}" '
                f'by "{self.student.klass.teacher.display_name}" and cannot '
                f'join a new class'
            )
            return redirect('index')
        return render(request, 'classroom/join_class.html')

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code', '').strip().upper()
        try:
            klass = Class.objects.get(code__iexact=code)
        except Class.DoesNotExist:
            messages.add_message(
                request,
                messages.ERROR,
                f'Class not found with code {code}'
            )
            return render(request, 'classroom/join_class.html')
        messages.add_message(
            request,
            messages.SUCCESS,
            f'You are already in "{self.student.klass.name} '
            f'by "{self.student.klass.teacher.display_name}'
        )
        self.student.join_class(klass)
        return redirect('index')


class StudentDashboardView(StudentOnlyMixin, View):
    def get(self, request):
        student = Student.of(request.user)
        if student.klass is None:
            return redirect('join_class')
        assignments = student.klass.assignments.all()
        processes = [LearningProcess.of(request.user, assignment.wordset)
                     for assignment in assignments]
        return render(
            request, 'student_index.html',
            {'processes': processes}
        )
