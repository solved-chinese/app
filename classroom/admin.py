from django.contrib import admin
from .models import Student, Teacher, Class, Assignment
from django.utils.html import format_html
from accounts.admin import RemoveTestersFilter, \
    RemoveTestersRelatedOnlyFieldListFilter


class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'in_class', 'total_study_duration']
    list_filter = (RemoveTestersFilter,)


admin.site.register(Student, StudentAdmin)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'school')
    list_filter = (RemoveTestersFilter,)


admin.site.register(Teacher, TeacherAdmin)


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('detail', 'class_name', 'teacher_name')
    list_display_links = None
    list_filter = (RemoveTestersFilter,)

    def class_name(self, obj):
        return format_html('<a href={}>{}</a>',
                           obj.in_class.get_absolute_url(),
                           obj.in_class.name)
    class_name.short_description = 'class'

    def teacher_name(self, obj):
        return obj.in_class.teacher.display_name
    teacher_name.short_description = 'teacher'

    def detail(self, obj):
        return format_html('<a href={}>{}</a>',
                           obj.get_absolute_url(),
                           obj.name)
    detail.short_description = 'name'


admin.site.register(Assignment, AssignmentAdmin)


class ClassAdmin(admin.ModelAdmin):

    list_display = ('detail', 'teacher_display_name', 'student_count')
    list_display_links = None
    list_filter = (
        ('teacher', RemoveTestersRelatedOnlyFieldListFilter),
    )

    def teacher_display_name(self, obj):
        return obj.teacher.display_name
    teacher_display_name.short_description = 'teacher'

    def detail(self, obj):
        return format_html('<a href={}>{}</a>',
                           obj.get_absolute_url(),
                           obj.name)
    detail.short_description = 'name'


admin.site.register(Class, ClassAdmin)
