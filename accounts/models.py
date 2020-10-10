from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # info
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=255)

    is_guest = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)

    def get_display_name(self):
        if self.is_guest:
            return 'Guest'
        elif self.first_name and self.first_name != 'None':
            return self.first_name
        else:
            return self.username
