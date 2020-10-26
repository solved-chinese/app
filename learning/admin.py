from django.contrib import admin

from .models import StudentCharacter, StudentCharacterTag, Report
from .learning_process import LearningProcess

admin.register(StudentCharacter)
admin.register(StudentCharacterTag)
admin.register(LearningProcess)
admin.register(Report)
