from learning import views
from learning import CRUD_views
from django.urls import path, register_converter


class FourDigitConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value


register_converter(FourDigitConverter, 'dddd')

urlpatterns = [
    path('report/', views.report, name='report'),
    path('search/', views.Search.as_view(), name='search'),

    path('C<dddd:character_pk>/', views.display_character,
         name='display_character'),
    path('getAudio/', views.getAudio),

    path('try_me/', views.try_me, name='try_me'),
    path('start_learning/', views.start_learning),
    path('status<slug:session_key>/', views.learning_process),

    path('radical/', CRUD_views.RadicalList.as_view(),
         name='radical_list'),
    path('radical/<int:pk>', CRUD_views.RadicalDetail.as_view(),
         name='radical_detail'),
    path('character/', CRUD_views.CharacterList.as_view(),
         name='character_list'),
    path('character/<int:pk>', CRUD_views.CharacterDetail.as_view(),
         name='character_detail'),
    path('character_set/', CRUD_views.CharacterSetList.as_view(),
         name='character_set_list'),
    path('character_set/<int:pk>', CRUD_views.CharacterSetDetail.as_view(),
         name='character_set_detail'),
]
