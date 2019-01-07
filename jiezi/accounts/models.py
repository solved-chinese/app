from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    raw_password = models.CharField(max_length=128, default='THIS_IS_NOT_RECORDED')
    grade = models.IntegerField(default=0)