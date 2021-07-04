from content import CRUD_views, views, API_views
from django.urls import path


urlpatterns = [
    path('display/word/<int:pk>', views.WordDisplayView.as_view(),
         name='word_display'),
    path('display/character/<int:pk>', views.CharacterDisplayView.as_view(),
         name='character_display'),
    path('display/radical/<int:pk>', views.RadicalDisplayView.as_view(),
         name='radical_display'),
    path('display/question/<int:question_pk>',
         views.QuestionDisplayView.as_view(),
         name='question_display'),

    path('display/questions_by_set/<slug:set_pk>/<int:question_pk>',
         views.admin_display_question,
         name='admin_question_display'),
    path('display/questions_by_set/<slug:set_pk>',
         views.admin_display_question,
         name='admin_question_display'),

    path('display/wordset/<int:pk>/<int:word_pk>',
         views.SetDisplayView.as_view(),
         name='set_display'),
    path('display/wordset/<int:pk>',
         views.SetDisplayView.as_view(),
         name='set_display'),

    path('review_question_factory/<slug:question_type>/<int:ro_id>',
         views.ReviewQuestionFactoryView.as_view(),
         name='review_question_factory_view'),
    path('show_all_options_toggle',
         views.show_all_options_toggle,
         name='show_all_options_toggle'),
    path('split_wordset/<int:wordset_pk>',
         views.split_set_view,
         name='split_wordset'),
]
