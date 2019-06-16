from jiezi_admin import views
from django.urls import path


urlpatterns = [
    path('admin_home', views.admin_home, name='admin_home'),
    path('update_entry', views.update_entry, name='update_entry'),
    path('update_media', views.update_media, name='update_media'),
    path('media_update_status', views.media_update_status, name='media_update_status'),
]
