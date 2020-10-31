from django.core.management.base import BaseCommand, CommandError

from accounts.models import User
from classroom.models import Teacher, Student, Class
from uuid import uuid4


class Command(BaseCommand):
    student_index = 0
    teacher_index = 0

    def _create_student(self, id=None):
        if id is None:
            self.student_index += 1
            username = f"test_s_{self.student_index}"
        else:
            username = f"test_s_{id}"
        password = "test"
        User.objects.filter(username=username).delete()
        user = User.objects.create_user(username, password=password,
                                        is_student=True)
        return Student.of(user)

    def _create_teacher(self, id=None):
        if id is None:
            self.teacher_index += 1
            username = f"test_t_{self.teacher_index}"
        else:
            username = f"test_t_{id}"
        password = "test"
        User.objects.filter(username=username).delete()
        user = User.objects.create_user(username, password=password,
                                        is_teacher=True)
        return Teacher.of(user)

    def handle(self, *args, **options):
        self.student_index = 0
        self.teacher_index = 0
        for id in 'abcde':
            self._create_student(id)
            self._create_teacher(id)
        for i in range(2):
            teacher = self._create_teacher()
            for j in range(2):
                in_class = Class.objects.create(
                    teacher=teacher,
                    name=f"test_class_{uuid4().hex[:5]}"
                )
                for k in range(2):
                    student = self._create_student()
                    student.join_class(in_class)
