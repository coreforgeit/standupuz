from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static

from standupuz_web import settings
from events import views

urlpatterns = [
    path('', views.home_page_redirect, name='home'),
    path('fox/', views.FoxView.as_view(), name='fox'),
    path('events/', views.events_view, name='events'),
    path('event_mob/<int:event_id>/', views.event_mob_view, name='event_mob'),
    # path('event_mob/', views.event_mob_view, name='event_mob'),
    path('about/', views.about_view, name='about'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
