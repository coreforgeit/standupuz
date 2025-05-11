from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Event, Option, Info, InfoBot, User, LogError


@admin.register(Event)
class ViewAdminEvent(ModelAdmin):
    list_display = ['title', 'event_date', 'event_time']
    readonly_fields = ['entities', 'created_at', 'photo_id']


@admin.register(Option)
class ViewAdminOption(ModelAdmin):
    list_display = ['name', 'event_name', 'empty_place', 'price']

    def event_name(self, obj):
        event = Event.objects.filter(id=obj.event_id).first()
        return event.title if event else str(obj.event_id)

    event_name.short_description = 'Ивент'


@admin.register(User)
class ViewAdminUser(ModelAdmin):
    list_display = ['full_name', 'username', 'phone', 'last_visit']
    ordering = ['-last_visit']
    readonly_fields = ['last_visit', 'user_id', 'full_name', 'username']


@admin.register(Info)
class ViewAdminInfo(ModelAdmin):
    list_display = ['text', 'phone']


@admin.register(InfoBot)
class ViewAdminInfoBot(ModelAdmin):
    list_display = ['text_1', 'text_2', 'text_3']


@admin.register(LogError)
class ErrorJournalAdmin(ModelAdmin):
    list_display = ("id", "created_at", "user_id", "message", "comment")
    search_fields = ("user_id", "message", "traceback")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "user_id", "traceback", "message")

