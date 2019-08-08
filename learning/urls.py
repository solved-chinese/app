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
    path('report/', views.report),
    path('search/', views.search),

    path('C<dddd:character_pk>/', views.display_character, name='display_character'),
    path('getAudio/', views.getAudio),

    path('start_learning/', views.start_learning),
    path('status<slug:session_key>/', views.learning_process),

    path('get_radical/', views.get_radical),
    path('get_character/', views.get_character),
]