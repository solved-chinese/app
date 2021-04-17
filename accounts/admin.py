from django.db.models import F
from django.utils.html import format_html, format_html_join, mark_safe
from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import User
from classroom.models import Student, Teacher
from jiezi.utils.admins import get_admin_url


def user_linked_display(user):
    if user.is_student:
        student = Student.of(user)
        if student.klass is None:
            return format_html('<a href={}>S:{}</a> orphan',
                               get_admin_url(user),
                               str(student.user))
        return format_html('<a href={}>S:{}</a> '
                           'in <a href={}>C:{}</a> '
                           'by <a href={}>T:{}</a>',
                           get_admin_url(user),
                           str(user),
                           get_admin_url(student.klass),
                           student.klass.name,
                           get_admin_url(student.klass.teacher.user),
                           str(student.klass.teacher.user))
    elif user.is_teacher:
        return format_html('<a href={}>T:{}</a>',
                           get_admin_url(user),
                           str(user))
    else:
        return format_html('<a href={}>{}</a> no role',
                           get_admin_url(user),
                           str(user))


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('role_display',)}),
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('alias', 'display_name', 'email')}),
        ('Solved specific info', {'fields': ('is_student', 'is_teacher')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('role_display',)
    list_display = (user_linked_display, 'email', 'alias', 'last_login')
    list_display_links = None
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',
                   'is_student', 'is_teacher',
                   ('alias', admin.EmptyFieldListFilter))
    list_editable = ('alias',)
    search_fields = ('username', 'alias', 'display_name', 'email')
    list_per_page = 50
    ordering = (F('last_login').desc(nulls_last=True),)

    def role_display(self, user):
        if user.is_teacher:
            teacher = Teacher.of(user)
            classes = format_html_join(
                ', ',
                '<a href={}>{}</a>',
                [(get_admin_url(klass), klass.name)
                 for klass in teacher.classes.all()]
            )
            return format_html('{}<br>Classes: {}',
                               user_linked_display(user), classes)
        return user_linked_display(user)
