from django.urls import path
from . import views

urlpatterns = [
    # deprecated
    path('temporary_access/<int:access_id>', views.temporary_access),
]