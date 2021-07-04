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
]
urlpatterns += router.urls
