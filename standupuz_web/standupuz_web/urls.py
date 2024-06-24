from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from standupuz_web import settings
from events.views import events_view, about_view

urlpatterns = [
    path('', events_view, name='events'),
    path('events/', events_view, name='events'),
    path('events_mob/', events_view, name='events'),
    path('about/', about_view, name='about'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
