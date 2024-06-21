from django.contrib import admin

from .models import Event, Option


@admin.register(Event)
class ViewAdminProfile(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'event_time']
    # list_filter = ['status', 'city_id']
    # ordering = ['-last_activity']

    # def city_str(self, obj):
    #     return maps.cities_dict.get (obj.city_id, 'н/д')
    #
    # city_str.short_description = 'Город'


@admin.register(Option)
class ViewAdminProfile(admin.ModelAdmin):
    list_display = ['event_name', 'name', 'empty_place', 'price']
    # list_display = ['name', 'empty_place', 'price']

    def event_name(self, obj):
        # print(obj.event_id)
        event = Event.objects.filter(id=obj.event_id).first()
        return event.title if event else str(obj.event_id)

    event_name.short_description = 'Ивент'
