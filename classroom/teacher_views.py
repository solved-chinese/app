from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from jiezi.utils.mixins import TeacherOnlyMixin
from .forms import AssignmentCreateForm
from .models import Class, Student, Assignment


class ClassDetailView(TeacherOnlyMixin, DetailView):
    model = Class
    template_name = "classroom/class_detail.html"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        if not super().test_func():
            return False
        if self.get_object().teacher != self.request.user.teacher:
            raise PermissionError('You are not the owner of this class.')
        return True

    def get_context_data(self, **kwargs):
        content = super().get_context_data()
        return content


class StudentRemoveView(TeacherOnlyMixin, View):
    def post(self, request):
        student_pk = request.POST.get('student_pk', 0)
        student = get_object_or_404(Student, pk=student_pk)
        in_class = student.klass
        if not in_class or in_class.teacher != request.user.teacher:
            raise PermissionError("This student isn't in your class")
        student.quit_class()
        return redirect('class_detail', pk=in_class.pk)


class ClassDeleteView(TeacherOnlyMixin, View):
    def post(self, request):
        class_pk = request.POST.get('class_pk', 0)
        klass = get_object_or_404(Class, pk=class_pk)
        if klass.teacher != request.user.teacher:
            raise PermissionError("The class doesn't belong to you")
        klass.delete()
        return redirect('class_list')


class ClassCreateView(TeacherOnlyMixin, CreateView):
    template_name = "classroom/class_create.html"
    model = Class
    fields = ['name']

    def form_valid(self, form):
        form.instance.teacher = self.request.user.teacher
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('class_detail', args=[self.object.pk])


class ClassListView(TeacherOnlyMixin, ListView):
    template_name = "classroom/class_list.html"

    def get_queryset(self):
        return Class.objects.filter(teacher=self.request.user.teacher)


class AssignmentCreateView(TeacherOnlyMixin, CreateView):
    template_name = "classroom/assignment_create.html"
    model = Assignment
    form_class = AssignmentCreateForm

    def form_valid(self, form):
        form.instance.klass = self.klass
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['klass'] = self.klass
        return kwargs

    def get_success_url(self):
        return reverse('assignment_detail', args=[self.object.pk])

    def test_func(self):
        if not super().test_func():
            return False
        self.klass = get_object_or_404(Class, pk=self.kwargs['class_pk'])
        if self.klass.teacher != self.request.user.teacher:
            raise PermissionError('You are not the owner of this class.')
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AssignmentDetailView(TeacherOnlyMixin, DetailView):
    model = Assignment
    template_name = "classroom/assignment_detail.html"

    def test_func(self):
        if self.request.user.is_staff and self.request.method == 'GET':
            return True
        if not super().test_func():
            return False
        if self.get_object().klass.teacher != self.request.user.teacher:
            raise PermissionError('You are not the owner of this class.')
        else:
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(self.object.get_stats())
        return context


class AssignmentDeleteView(TeacherOnlyMixin, View):
    def post(self, request):
        assignment_pk = request.POST.get('assignment_pk', 0)
        assignment = get_object_or_404(Assignment, pk=assignment_pk)
        in_class = assignment.klass
        if in_class.teacher != request.user.teacher:
            raise PermissionError("The class doesn't belong to you")
        assignment.delete()
        return redirect('class_detail', pk=in_class.pk)
