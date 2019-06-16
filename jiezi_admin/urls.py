from jiezi_admin import views
from django.urls import path


urlpatterns = [
    path('update_entry', views.update_entry, name='update_entry'),
]
