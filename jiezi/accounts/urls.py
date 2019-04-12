from accounts import views
from django.urls import path
from django.contrib.auth import views as auth_views


"""
@api {POST} /accounts/get_available_sets Get available sets
@apiDescription Get available sets to add
@apiGroup accounts

@apiSuccess {Object[]} set
@apiSuccess {string}   set.name      the name of the set to display
@apiSuccess {Number}   set.id        the id to send back if the set is added
"""
"""
@api {POST} /accounts/add_set Add set
@apiGroup accounts

@apiParam   {Number}   set_id        the id of the set to be added
""""""
@api {POST} /accounts/delete_character Delete character
@apiGroup accounts

@apiParam   {Number}   character_id  the Jiezi id of the character
@apiParam   {Number}   set_id        the id of the set for the character to be deleted from, -1 if delete from all sets
""""""
@api {POST} /accounts/delete_set Delete set
@apiGroup accounts

@apiParam   {Number}  set_id          the id of the set to be deleted from
@apiParam   {Boolean} is_delete_characters  false will not delete the characters in this set, even if they don't belong to any sets 
""""""
@api {GET} /search search (TODO) 
@apiGroup index

@apiParam   {String}  str             the string to be searched
"""

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('manage_stack/', views.manage_stack, name='manage_stack'),
]