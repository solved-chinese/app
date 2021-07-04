from django.urls import path

from . import CRUD_views


urlpatterns = [
    path('user', CRUD_views.UserDetail.as_view(), name='user-detail'),
]