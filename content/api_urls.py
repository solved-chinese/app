from content import CRUD_views, API_views
from django.urls import path

urlpatterns = [
    path('search/', API_views.SearchAPIView.as_view(), name='search'),

    path('radical/<int:pk>', CRUD_views.RadicalDetail.as_view(),
         name='radical-detail'),
    path('character/<int:pk>', CRUD_views.CharacterDetail.as_view(),
         name='character-detail'),
    path('word/<int:pk>', CRUD_views.WordDetail.as_view(),
         name='word-detail'),
    path('word_set/<int:pk>', CRUD_views.WordSetDetail.as_view(),
         name='wordset-detail'),
    path('word_set', CRUD_views.WordSetList.as_view(),
         name='wordset-list'),

    path('question/<int:pk>', API_views.QuestionView.as_view()),

    path('linked_field_autocomplete',
         API_views.LinkedFieldAutocomplete.as_view(),
         name='linked_field_autocomplete'),
]
