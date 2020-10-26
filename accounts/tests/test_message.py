from django.test import TestCase, Client
from rest_framework.reverse import reverse

from jiezi.tests.utils import create_student, create_teacher
from ..models import User, Message


class MessageTest(TestCase):
    def setUp(self):
        self.user = create_teacher().user
        self.client.force_login(self.user)

    def test(self):
        msg_1 = self.user.notify("subject1", "content1")
        msg_2 = self.user.notify("subject2", "content2")
        self.assertEqual(Message.of(self.user).count(), 2)
        self.assertEqual(self.user.unread_message_count, 2)
        # test list works
        response = self.client.get(reverse('message_list'))
        self.assertContains(response, 'subject1')
        self.assertContains(response, 'subject2')
        # test detail reads the msg
        response = self.client.get(reverse('message_detail', args=[msg_1.pk]))
        self.assertContains(response, 'content1')
        self.assertEqual(Message.of(self.user).count(), 2)
        self.assertEqual(self.user.unread_message_count, 1)
        # test read
        msg_2.read()
        self.assertEqual(Message.of(self.user).count(), 2)
        self.assertEqual(self.user.unread_message_count, 0)
