from django.urls import path
from django.contrib.auth import views as auth_views

import learning.CRUD_views
from accounts import views, CRUD_views


urlpatterns = [
    path('profile/', views.profile, name="profile"),
    path('staff_panel/', views.staff_panel, name="staff_panel"),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('alt_profile/', views.alt_profile, name='alt_profile'),

    path('my_user/',
         CRUD_views.MyUserDetail.as_view(),
         name='my_user_detail'),
]
