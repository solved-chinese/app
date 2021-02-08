from django.urls import path
from . import views, API_views

urlpatterns = [
    path('<int:set_pk>',
         views.LearningView.as_view(),
         name='learn_set'),
    path('api/<int:set_pk>',
         API_views.LearningAPIView.as_view()),
]
