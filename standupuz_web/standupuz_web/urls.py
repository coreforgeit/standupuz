from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static

from standupuz_web import settings
from events import views

urlpatterns = [
    path('api/event/', views.EventsListAPIView.as_view(), name='api-event-list'),
    path('api/event/<int:event_id>/', views.EventDetailAPIView.as_view(), name='api-event-detail'),
    path('api/info/', views.InfoAPIView.as_view(), name='api-info'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
