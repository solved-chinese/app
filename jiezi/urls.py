import posixpath

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from jiezi import views, settings


urlpatterns = [
    # celery progress app
    path('celery-progress/', include('celery_progress.urls')),
    # rest framework api
    path('api_auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path("select2/", include("django_select2.urls")),

    # app urls
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('content/', include('content.urls')),

    # front-page urls
    path('index/', views.index, name="index"),
    path('', RedirectView.as_view(url='admin')),
    path('about_us/', views.about_us, name="about_us"),

    path('api_root/', views.api_root),

    path('learning/', include('frontend.urls')),

    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),
]
if settings.DEBUG:
    # if DEBUG, redirect media according to settings
    def serve(request, path):
        path = posixpath.normpath(path).lstrip('/')
        return redirect(f'{settings.MEDIA_REDIRECT}{path}')
    if settings.MEDIA_REDIRECT is None:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    else:
        urlpatterns.append(re_path(r'^media/(?P<path>.*)$', serve))
urlpatterns += staticfiles_urlpatterns()
