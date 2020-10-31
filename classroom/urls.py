from django.urls import path
from classroom import teacher_views, student_views


urlpatterns = [
    path('student/join_class/<slug:uuid>', student_views.JoinClass.as_view(),
         name='join_class'),

    path('teacher/class_detail/<int:pk>/filter',
         teacher_views.FilterInClass.as_view(), name='class_detail_filter'),
    path('teacher/class_detail/<int:pk>', teacher_views.ClassDetail.as_view(),
         name='class_detail'),
    path('teacher/assignment_detail/<int:pk>',
         teacher_views.AssignmentDetail.as_view(),
         name='assignment_detail'),
    path('teacher/class_detail/<int:pk>/create_assignment',
         teacher_views.AssignmentCreate.as_view(),
         name='create_assignment'),
    path('teacher/class_detail/<int:pk>/<int:cset_pk>',
         teacher_views.ClassDetail.as_view(), name='class_detail'),
    path('teacher/create_class', teacher_views.ClassCreate.as_view(),
         name='create_class'),
    path('teacher/delete_class', teacher_views.DeleteClass.as_view(),
         name='delete_class'),
    path('teacher/list_class', teacher_views.ClassList.as_view(),
         name='list_class'),
    path('teacher/remove_student/',
         teacher_views.RemoveStudent.as_view(), name='remove_student'),
]
