from content import views, CRUD_views
from django.urls import path, register_converter


class FourDigitConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value


register_converter(FourDigitConverter, 'dddd')

urlpatterns = [
    path('search/', views.Search.as_view(), name='search'),

    path('update_entry', views.update_entry, name='update_entry'),
    path('update_character_animated_stroke_order_image',
         views.update_character_animated_stroke_order_image,
         name='update_character_animated_stroke_order_image'),
    path('update_radical_mnemonic_image',
         views.update_radical_mnemonic_image,
         name='update_radical_mnemonic_image'),
    path('task/<slug:task_id>/', views.task_info, name='task_info'),
    path('kill_task/', views.kill_task, name='kill_task'),

    path('C<dddd:character_pk>/', views.display_character,
         name='display_character'),
    path('C<dddd:character_pk>/review/<int:review_type>/',
         views.ReviewView.as_view(),
         name='review_character'),

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
