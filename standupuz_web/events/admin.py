from django.contrib import admin

from .models import Event, Option, Info, InfoBot, User


@admin.register(Event)
class ViewAdminEvent(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'event_time']


@admin.register(Option)
class ViewAdminOption(admin.ModelAdmin):
    list_display = ['name', 'event_name', 'empty_place', 'price']

    def event_name(self, obj):
        event = Event.objects.filter(id=obj.event_id).first()
        return event.title if event else str(obj.event_id)

    event_name.short_description = 'Ивент'


@admin.register(User)
class ViewAdminUser(admin.ModelAdmin):
    list_display = ['full_name', 'username', 'phone', 'last_visit']
    ordering = ['-last_visit']


@admin.register(Info)
class ViewAdminInfo(admin.ModelAdmin):
    list_display = ['text', 'phone']


@admin.register(InfoBot)
class ViewAdminInfoBot(admin.ModelAdmin):
    list_display = ['text_1', 'text_2', 'text_3']
