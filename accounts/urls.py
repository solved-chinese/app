
from django.urls import path

from . import views, CRUD_views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('student_signup/', views.student_signup, name='student_signup'),
    path('teacher_signup/', views.teacher_signup, name='teacher_signup'),

    path('profile/', views.profile, name="profile"),

    path('password_change_done/', views.DoneChangePassword.as_view(),
         name='password_change_done'),
    path('change_password/', views.ChangePassword.as_view(),
         name='change_password'),
    path('password_reset/', views.PasswordReset.as_view(),
         name='password_reset'),
    path('password_reset_done/', views.PasswordResetDone.as_view(),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         views.PasswordResetConfirm.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/', views.PasswordResetComplete.as_view(),
         name='password_reset_complete'),

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('user', CRUD_views.UserDetail.as_view(), name='user-detail'),
]