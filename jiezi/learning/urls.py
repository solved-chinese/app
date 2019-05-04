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
    path('C<dddd:character_pk>/', views.display_character, name='display_character'),  # reverse by {% url 'display_character' 1 %}
    path('load_from_excel', views.load_from_excel),
    # path('start_learning<int:minutes_to_learn>', views.start_learning, name='start_learning'),
]