from django.views import View
from django.shortcuts import get_object_or_404, render, redirect

from jiezi.utils.mixins import IsStudentMixin
from .models import Class


class JoinClass(IsStudentMixin, View):
    def get(self, request, *args, **kwargs):
        student = self.request.user.student
        class_object = get_object_or_404(Class, uuid=kwargs['uuid'])
        context = {}
        if student.in_class:
            context['msg'] = f"You are already in {student.in_class}, " \
                             f"so you can't join another class"
        else:
            context['class'] = str(class_object)
        return render(request, 'classroom/join_class.html', context)

    def post(self, request, *args, **kwargs):
        student = self.request.user.student
        class_object = get_object_or_404(Class, uuid=kwargs['uuid'])
        student.join_class(class_object)
        return redirect('index')
