from django.contrib.auth.models import UserManager
from uuid import uuid4


class JieziUserManager(UserManager):
    def create_guest_student(self):
        """This doesn't create Student object tho"""
        user = self.create_user(f"test_user_{uuid4().hex}",
                                is_guest=True, is_student=True)
        return user
