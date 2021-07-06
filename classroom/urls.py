from rest_framework import routers
from django.urls import path
from classroom import CRUD_views

router = routers.SimpleRouter()
router.register('assignment', CRUD_views.AssignmentViewSet, 'assignment')

urlpatterns = [
    path('class/',
         CRUD_views.ClassCreate.as_view(),
         name='class-create'),
    path('class/<int:pk>',
         CRUD_views.ClassDetail.as_view(),
         name='class-detail'),
    path('student/',
         CRUD_views.StudentDetail.as_view(),
         name='student-detail'),
    path('teacher/',
         CRUD_views.TeacherDetail.as_view(),
         name='student-detail'),
]
urlpatterns += router.urls
