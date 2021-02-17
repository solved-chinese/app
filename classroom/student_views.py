from django.views import View
from django.shortcuts import get_object_or_404, render, redirect

from jiezi.utils.mixins import StudentOnlyMixin
from .models import Class
from learning.models import LearningProcess


class JoinClassView(StudentOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        student = self.request.user.student
        class_object = get_object_or_404(Class, uuid=kwargs['uuid'])
        context = {}
        if student.klass:
            context['msg'] = f"You are already in {student.klass}, " \
                             f"so you can't join another class"
        else:
            context['class'] = str(class_object)
        return render(request, 'classroom/join_class.html', context)

    def post(self, request, *args, **kwargs):
        student = self.request.user.student
        klass = get_object_or_404(Class, uuid=kwargs['uuid'])
        student.join_class(klass)
        return redirect('index')


class StudentDashboardView(StudentOnlyMixin, View):
    def get(self, request):
        if request.user.student.klass is None:
            return render(
                request, 'utils/simple_response.html',
                {'content': "Join a class with the link from your teacher."}
            )
        assignments = request.user.student.klass.assignments.all()
        processes = [LearningProcess.of(request.user, assignment.wordset)
                     for assignment in assignments]
        return render(
            request, 'student_index.html',
            {'processes': processes}
        )
