from django.urls import path
from classroom import teacher_views, student_views


urlpatterns = [
    path('student/join_class/<slug:uuid>', student_views.JoinClass.as_view(),
         name='join_class'),

    path('teacher/class_detail/<int:pk>', teacher_views.ClassDetail.as_view(),
         name='class_detail'),
    path('teacher/assignment_detail/<int:pk>',
         teacher_views.AssignmentDetail.as_view(),
         name='assignment_detail'),
    path('teacher/class_detail/<int:pk>/assignment_create',
         teacher_views.AssignmentCreate.as_view(),
         name='assignment_create'),
    path('teacher/assignment_delete/',
         teacher_views.DeleteAssignemtn.as_view(),
         name='assignment_delete'),
    path('teacher/class_detail/<int:pk>/<int:cset_pk>',
         teacher_views.ClassDetail.as_view(), name='class_detail'),
    path('teacher/class_create', teacher_views.ClassCreate.as_view(),
         name='class_create'),
    path('teacher/class_delete', teacher_views.DeleteClass.as_view(),
         name='class_delete'),
    path('teacher/class_list', teacher_views.ClassList.as_view(),
         name='class_list'),
    path('teacher/remove_student/',
         teacher_views.RemoveStudent.as_view(), name='remove_student'),
]
