from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from jiezi.utils.mixins import IsTeacherMixin
from .models import Class


class ClassDetail(IsTeacherMixin, DetailView):
    model = Class
    template_name = "classroom/class_detail.html"

    def test_func(self):
        if not super().test_func():
            return False
        if self.get_object().teacher != self.request.user.teacher:
            raise PermissionError('You are not the owner of this class.')
        else:
            return True


class ClassCreate(IsTeacherMixin, CreateView):
    template_name = "classroom/class_create.html"
    model = Class
    fields = ['name']

    def form_valid(self, form):
        form.instance.teacher = self.request.user.teacher
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('class_detail', args=[self.object.pk])


class ClassList(IsTeacherMixin, ListView):
    template_name = "classroom/class_list.html"

    def get_queryset(self):
        return Class.objects.filter(teacher=self.request.user.teacher)
