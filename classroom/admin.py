from django.contrib import admin
from django.utils.html import mark_safe, format_html

from jiezi.utils.admins import ViewOnlyAdminMixin, get_admin_url
from .models import Class, Assignment, Student, Teacher
from accounts.admin import user_linked_display


def class_linked_display(klass):
    user = klass.teacher.user
    return format_html("<a href={}>T:{}</a>'s <a href={}>C:{}</a>",
                       get_admin_url(user),
                       str(user),
                       get_admin_url(klass),
                       klass.name
                       )


def assignment_linked_display(assignment):
    klass = assignment.klass
    user = klass.teacher.user
    return format_html("<a href={}>T:{}</a>'s "
                       "<a href={}>C:{}</a>'s "
                       "<a href={}>A:{}</a>",
                       get_admin_url(user),
                       str(user),
                       get_admin_url(klass),
                       klass.name,
                       get_admin_url(assignment),
                       assignment.name,
                       )


class AssignmentGeneralAdmin(ViewOnlyAdminMixin):
    exclude = ('data',)
    fields = ('detail', 'wordset', 'display_stats', 'published_time')
    readonly_fields = ('detail', 'display_stats', 'published_time')

    def detail(self, assignment):
        return assignment_linked_display(assignment)

    def display_stats(self, assignment):
        stats = assignment.get_stats()
        return mark_safe(','.join(stats.values()))


class AssignmentInlinAdmin(AssignmentGeneralAdmin, admin.StackedInline):
    show_change_link = True
    model = Assignment
    fields = ('detail', 'wordset', 'published_time')
    readonly_fields = ('detail', 'published_time')


@admin.register(Assignment)
class AssignmentAdmin(AssignmentGeneralAdmin, admin.ModelAdmin):
    list_display = (assignment_linked_display,)
    list_display_links = None


class StudentInlineAdmin(admin.StackedInline):
    model = Student
    fields = ('display_student',)
    readonly_fields = ('display_student',)

    def display_student(self, student):
        return user_linked_display(student.user)


@admin.register(Class)
class ClassAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    list_display = (class_linked_display, 'student_count')
    list_display_links = None
    inlines = (AssignmentInlinAdmin, StudentInlineAdmin)
    list_filter = (
        ('teacher__user__alias', admin.EmptyFieldListFilter),
    )

    def lookup_allowed(self, lookup, value):
        return (lookup == 'teacher__user__alias__isempty'
                or super().lookup_allowed(lookup, value))

