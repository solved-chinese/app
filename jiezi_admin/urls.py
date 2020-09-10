from jiezi_admin import views
from django.urls import path


urlpatterns = [
    path('update_entry', views.update_entry, name='update_entry'),
    path('update_character_animated_stroke_order_image',
         views.update_character_animated_stroke_order_image,
         name='update_character_animated_stroke_order_image'),
    path('update_radical_mnemonic_image',
         views.update_radical_mnemonic_image,
         name='update_radical_mnemonic_image'),
    path('task/<slug:task_id>/', views.task_info, name='task_info'),
    path('kill_task/', views.kill_task, name='kill_task'),
]
