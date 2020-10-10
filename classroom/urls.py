from django.urls import path
from classroom import views


urlpatterns = [
    path('manage_library/<int:set_id>', views.manage_library,
         name='manage_library'),
    path('manage_library/', views.manage_library, name='manage_library'),
]
