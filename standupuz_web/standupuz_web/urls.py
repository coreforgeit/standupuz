from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from standupuz_web import settings
from events.views import new_orders_view, orders_view

urlpatterns = [
    path('', new_orders_view, name='events'),
    path('events/', new_orders_view, name='events'),
    path('about/', orders_view, name='about'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
