from django.urls import path

from accounts import views, CRUD_views


urlpatterns = [
    path('student_signup/', views.student_signup, name='student_signup'),
    path('teacher_signup/', views.teacher_signup, name='teacher_signup'),
    path('password_change_done', views.DoneChangePassword.as_view(),
         name='password_change_done'),
    path('change_password', views.ChangePassword.as_view(),
         name='change_password'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('profile/', views.profile, name="profile"),
    path('staff_panel/', views.staff_panel, name="staff_panel"),

    path('messages/', views.MessageList.as_view(), name='message_list'),
    path('messages/<int:pk>', views.MessageDetail.as_view(),
         name='message_detail'),

    path('my_user/',
         CRUD_views.MyUserDetail.as_view(),
         name='my_user_detail'),
]
