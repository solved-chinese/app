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
    path('C<dddd:character_pk>/', views.learning_character, name='learning_character'),# reverse by {% url 'learning_character' 1 %}

]

