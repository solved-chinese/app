from django.urls import path
from classroom import views


urlpatterns = [
    # path('student/join_class', views.join_class, name='join_class'),

    path('teacher/class_detail/<int:pk>', views.ClassDetail.as_view(),
         name='class_detail'),
    path('teacher/create_class', views.ClassCreate.as_view(),
         name='create_class'),
    path('teacher/list_class', views.ClassList.as_view(),
         name='list_class'),
]
