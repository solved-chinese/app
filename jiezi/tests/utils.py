from uuid import uuid4

from accounts.models import User
from classroom.models import Teacher, Student


def create_teacher():
    user = User.objects.create_user(uuid4().hex, is_teacher=True,
                                    display_name='test_teacher_name')
    return Teacher.of(user)


def create_student():
    user = User.objects.create_user(uuid4().hex, is_student=True,
                                    display_name='test_student_name')
    return Student.of(user)