from rest_framework import routers
from django.urls import path
from classroom import CRUD_views

router = routers.SimpleRouter()
router.register('assignment', CRUD_views.AssignmentViewSet, 'assignment')
router.register('class', CRUD_views.ClassViewSet, 'class')

urlpatterns = [
    path('student/',
         CRUD_views.StudentDetail.as_view(),
         name='student-detail'),
    path('teacher/',
         CRUD_views.TeacherDetail.as_view(),
         name='student-detail'),
]
urlpatterns += router.urls
