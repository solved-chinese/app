from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views, CRUD_views

"""
@api {GET} /search search 
@apiGroup index
@apiIgnore TODO

@apiParam   {String}  str    the string to be searched
"""

urlpatterns = [
    path('profile/', views.profile, name="profile"),
    path('staff_panel/', views.staff_panel, name="staff_panel"),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('alt_profile/', views.alt_profile, name='alt_profile'),

    path('manage_library/<int:set_id>', views.manage_library, name='manage_library'),
    path('manage_library/', views.manage_library, name='manage_library'),


    path('user_character_tag/',
         CRUD_views.UserCharacterTagList.as_view(),
         name='user_character_tag_list'),
    path('user_character_tag/<int:pk>',
         CRUD_views.UserCharacterTagDetail.as_view(),
         name='user_character_tag_detail'),
    path('user_character/',
         CRUD_views.UserCharacterList.as_view(),
         name='user_character_list'),
    path('user_character/<int:pk>',
         CRUD_views.UserCharacterDetail.as_view(),
         name='user_character_detail'),
    path('my_user/',
         CRUD_views.MyUserDetail.as_view(),
         name='my_user_detail'),
]
