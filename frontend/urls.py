from django.urls import re_path, path
from . import views

urlpatterns = [
    path('temporary_access/<int:access_id>',
         views.temporary_access),
    re_path(r'^$', views.index),
    re_path(r'^(?:.*)/?$', views.index)
]