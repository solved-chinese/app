from django.test import TestCase, Client
from rest_framework.reverse import reverse

from jiezi.tests.utils import create_student, create_teacher


class ClassroomTest(TestCase):
    def setUp(self):
        self.teacher = create_teacher()
        self.teacher_client = Client()
        self.teacher_client.force_login(self.teacher.user)
        self.student = create_student()
        self.student_client = Client()
        self.student_client.force_login(self.student.user)

    def test_classroom(self):
        # have the teacher create a class
        response = self.teacher_client.post(reverse('create_class'),
                                                    {'name': 'test_class_name'})
        self.assertEqual(self.teacher.classes.count(), 1)
        class_object = self.teacher.classes.first()
        self.assertRedirects(response, reverse('class_detail',
                                               args=[class_object.pk]))
        # class_list contains the created class
        response = self.teacher_client.get(reverse('list_class'))
        self.assertContains(response, 'test_class_name')
        # have a student join this class
        response = self.student_client.get(
            reverse('join_class', args=[class_object.uuid.hex]))
        self.assertContains(response, 'test_teacher_name')
        self.assertContains(response, 'test_class_name')
        response = self.student_client.post(
            reverse('join_class', args=[class_object.uuid.hex]))
        self.assertRedirects(response, reverse('index'))
        # the teacher sees the student in this class
        response = self.teacher_client.get(
            reverse('class_detail', args=[class_object.pk]))
        self.assertContains(response, 'test_student_name')
