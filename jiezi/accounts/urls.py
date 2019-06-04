from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views

"""
@api {GET} /search search 
@apiGroup index
@apiIgnore TODO

@apiParam   {String}  str             the string to be searched
"""

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('alt_profile/', views.alt_profile, name='alt_profile'),

    path('manage_library/', views.manage_library, name='manage_library'),

    path('add_set/', views.add_set),
    path('delete_set/', views.delete_set),
    path('get_available_sets/', views.get_available_sets),
    path('delete_character/', views.delete_character),

    path('sessionid', views.sessionid),
    path('test', views.test)
]