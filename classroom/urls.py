from django.urls import path
from classroom import teacher_views, student_views


urlpatterns = [
    path('student/dashboard',
         student_views.StudentDashboardView.as_view(),
         name='student_dashboard'),
    path('student/join_class/<slug:uuid>',
         student_views.JoinClassView.as_view(),
         name='join_class'),

    path('teacher/class_list',
         teacher_views.ClassListView.as_view(),
         name='class_list'),
    path('teacher/class_detail/<int:pk>',
         teacher_views.ClassDetailView.as_view(),
         name='class_detail'),
    path('teacher/class_create',
         teacher_views.ClassCreateView.as_view(),
         name='class_create'),
    path('teacher/class_delete',
         teacher_views.ClassDeleteView.as_view(),
         name='class_delete'),

    path('teacher/assignment_detail/<int:pk>',
         teacher_views.AssignmentDetailView.as_view(),
         name='assignment_detail'),
    path('teacher/assignment_delete/',
         teacher_views.AssignmentDeleteView.as_view(),
         name='assignment_delete'),
    path('teacher/assignment_create/<int:class_pk>',
         teacher_views.AssignmentCreateView.as_view(),
         name='assignment_create'),

    path('teacher/remove_student/',
         teacher_views.StudentRemoveView.as_view(),
         name='remove_student'),
]
