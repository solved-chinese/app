from learning import views
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
    path('search/', views.search),

    path('C<dddd:character_pk>/', views.display_character, name='display_character'),
    path('getAudio/', views.getAudio),

    path('try_me/', views.try_me, name='try_me'),
    path('start_learning/', views.start_learning),
    path('status<slug:session_key>/', views.learning_process),

    path('get_radical/', views.get_radical),
    path('get_character/', views.get_character),

    path('radical/<int:pk>', views.RadicalDetail.as_view(),
         name='radical_detail'),
    path('character/<int:pk>', views.CharacterDetail.as_view(),
         name='character_detail'),
    path('character_set/<int:pk>', views.CharacterSetDetail.as_view(),
         name='character_set_detail'),
]