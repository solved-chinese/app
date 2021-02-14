from django.urls import path
from . import views, API_views

urlpatterns = [
    path('<int:set_pk>',
         views.LearningView.as_view(),
         name='learn_set'),
    path('assignment/<int:set_pk>',
         views.AssignmentView.as_view(),
         name='assignment'),

    path('api/<int:set_pk>',
         API_views.LearningAPIView.as_view()),
    path('api/assignment/<int:set_pk>',
         API_views.AssignmentAPIView.as_view()),
]
