from django.urls import path
from classroom import CRUD_views


urlpatterns = [
    path('assignment/',
         CRUD_views.AssignmentCreate.as_view(),
         name='assignment-create'),
    path('assignment/<int:pk>',
         CRUD_views.AssignmentDetail.as_view(),
         name='assignment-detail'),
    path('class/',
         CRUD_views.ClassCreate.as_view(),
         name='class-create'),
    path('class/<int:pk>',
         CRUD_views.ClassDetail.as_view(),
         name='class-detail'),
]
