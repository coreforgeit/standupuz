from django.db import models
from django.contrib.postgres.fields import ArrayField


# Ивенты
class Event(models.Model):
    id = models.AutoField ('ID', primary_key=True)
    created_at = models.DateTimeField ('Создана', auto_created=True)
    title = models.CharField ('Название', max_length=255)
    event_date = models.DateField ('Дата', null=True, blank=True)
    event_time = models.TimeField ('Время', null=True, blank=True)
    text = models.TextField ('Текст', null=True, blank=True)
    entities = ArrayField (base_field=models.CharField(255), verbose_name='Сущности', null=True, blank=True)
    photo_id = models.CharField ('Фото', null=True, blank=True)
    is_active = models.BooleanField ('Активен', default=True)

    def __str__(self):
        return f"<Event({self.id}>"

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        db_table = 'events'
        managed = False


# тарифы ивентов
class Option(models.Model):
    id = models.AutoField ('ID', primary_key=True)
    event_id = models.IntegerField ('ID ивента')
    name = models.CharField ('Название', max_length=255)
    empty_place = models.IntegerField ('Осталось мест', null=True, blank=True)
    all_place = models.IntegerField ('Всего мест', null=True, blank=True)
    cell = models.CharField ('Ячейка', null=True, blank=True)
    price = models.IntegerField ('Стоимость', null=True, blank=True)

    def __str__(self):
        return f"<Option({self.id}>"

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        db_table = 'options'
        managed = False
