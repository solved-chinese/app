from learning import views
from learning import CRUD_views
from django.urls import path


urlpatterns = [
    path('report/', views.report, name='report'),

    path('try_me/', views.try_me, name='try_me'),
    path('start_learning/', views.StartLearning.as_view, name='start_learning'),
    path('', views.Learning.as_view, name='continue_learning'),

    path('student_character_tag/',
         CRUD_views.StudentCharacterTagList.as_view(),
         name='student_character_tag_list'),
    path('student_character_tag/<int:pk>',
         CRUD_views.StudentCharacterTagDetail.as_view(),
         name='student_character_tag_detail'),
    path('student_character/',
         CRUD_views.StudentCharacterList.as_view(),
         name='student_character_list'),
    path('student_character/<int:pk>',
         CRUD_views.StudentCharacterDetail.as_view(),
         name='student_character_detail'),
]
