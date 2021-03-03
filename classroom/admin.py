from django.contrib import admin
from django.utils.html import format_html

from .models import Class, Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('detail', 'class_name', 'teacher_name')
    list_display_links = None

    def class_name(self, obj):
        return format_html('<a href={}>{}</a>',
                           obj.klass.get_absolute_url(),
                           obj.klass.name)
    class_name.short_description = 'class'

    def teacher_name(self, obj):
        return obj.klass.teacher.display_name
    teacher_name.short_description = 'teacher'

    def detail(self, obj):
        return format_html('<a href={}>{}</a>',
                           obj.get_absolute_url(),
                           obj.name)
    detail.short_description = 'name'


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('detail', 'teacher_display_name', 'student_count')
    list_display_links = None

    def teacher_display_name(self, obj):
        return obj.teacher.display_name
    teacher_display_name.short_description = 'teacher'

    def detail(self, obj):
        return format_html('<a href={}>{}</a>',
                           obj.get_absolute_url(),
                           obj.name)
    detail.short_description = 'name'
