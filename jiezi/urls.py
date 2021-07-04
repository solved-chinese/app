import posixpath

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from jiezi import views, settings


urlpatterns = [
    # celery progress app
    path("select2/", include("django_select2.urls")),
    path('advanced_filters/', include('advanced_filters.urls')),

    # app urls
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/accounts/', include('accounts.api_urls')),
    path('content/', include('content.urls')),
    path('api/content/', include('content.api_urls')),
    path('api/learning/', include('learning.urls')),
    path('api/classroom/', include('classroom.urls')),

    # front-page urls
    path('index/', views.index, name="index"),
    path('', RedirectView.as_view(url='index')),
    path('dashboard', views.frontend_index(url='frontend_index')),
    path('about_us/', views.about_us, name="about_us"),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),
]
if settings.DEBUG:
    # if DEBUG, redirect media according to settings
    def serve(request, path):
        path = posixpath.normpath(path).lstrip('/')
        return redirect(f'{settings.MEDIA_REDIRECT}{path}')
    if settings.MEDIA_REDIRECT is None:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
    else:
        urlpatterns.append(re_path(r'^media/(?P<path>.*)$', serve))
urlpatterns += staticfiles_urlpatterns()
