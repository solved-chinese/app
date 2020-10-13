from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

from content.models import CharacterSet
from learning.models import StudentCharacter, StudentCharacterTag
from jiezi.utils.mixins import IsTeacherMixin
from .models import Class


class FilterInClass(IsTeacherMixin, TemplateView):
    template_name = "utils/table_renderer.html"

    def get_context_data(self, **kwargs):
        teacher = self.request.user.teacher
        class_object = get_object_or_404(Class, pk=kwargs.get('pk', None))
        if class_object.teacher != teacher:
            raise PermissionError('You are not the owner of this class.')
        cset_pk = self.request.GET.get('cset_pk', None)
        cset = get_object_or_404(CharacterSet, pk=cset_pk)
        labels = ['student name', 'cset_added']
        objects = []
        for index, student in enumerate(class_object.students.all()):
            object = [student.display_name,
                      StudentCharacterTag.objects.filter(
                          student=student, character_set=cset).exists()]
            state = StudentCharacter.of(student, cset=cset). \
                get_states_count_dict()
            for key, value in state.items():
                if index == 0:
                    labels.append(key)
                object.append(value)
            objects.append(object)

        return {'header': f'stats of class {class_object.name} on '
                          f'CharacterSet {cset.name}',
                'labels': labels,
                'objects': objects}



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

    def get_context_data(self, **kwargs):
        content = super().get_context_data()
        content['csets'] = CharacterSet.objects.all()
        return content


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
