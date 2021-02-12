from django.contrib import admin
from .models import Student, Teacher, Class, Assignment


@admin.register(Student, Teacher, Class, Assignment)
class ClassroomAdmin(admin.ModelAdmin):
    pass
