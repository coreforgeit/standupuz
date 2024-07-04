from django.db import models
from django.contrib.postgres.fields import ArrayField


# Ивенты
class Event(models.Model):
    id = models.AutoField ('ID', primary_key=True)
    created_at = models.DateTimeField ('Создана', auto_created=True)
    title = models.CharField ('Название', max_length=255, null=True, blank=True)
    club = models.CharField ('Локация', max_length=255, null=True, blank=True)
    event_date = models.DateField ('Дата', null=True, blank=True)
    event_time = models.TimeField ('Время', null=True, blank=True)
    text = models.TextField ('Текст', null=True, blank=True)
    entities = ArrayField (base_field=models.CharField(255), verbose_name='Сущности', null=True, blank=True)
    photo_id = models.CharField ('Фото', null=True, blank=True)
    is_active = models.BooleanField ('Активен', default=True)
    text_1 = models.TextField('Текст 1', null=True, blank=True)
    text_2 = models.TextField('Текст 2', null=True, blank=True)
    text_3 = models.TextField('Текст 3', null=True, blank=True)

    def __str__(self):
        return f"<Event({self.title})>"

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
        return f"<Option({self.name})>"

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        db_table = 'options'
        managed = False


# инфо
class Info(models.Model):
    id = models.AutoField ('ID', primary_key=True)
    phone = models.CharField('Телефон', max_length=255)
    text = models.TextField('Текст', null=True, blank=True)

    def __str__(self):
        return f"<Info({self.id})>"

    class Meta:
        verbose_name = 'Инфо'
        verbose_name_plural = 'Инфо'
        db_table = 'site_info'
        managed = False


# инфо бот
class InfoBot(models.Model):
    id = models.AutoField ('ID', primary_key=True)
    text_1 = models.TextField('Текст 1', null=True, blank=True)
    text_2 = models.TextField('Текст 2', null=True, blank=True)
    text_3 = models.TextField('Текст 3', null=True, blank=True)

    def __str__(self):
        return f"<InfoBot({self.id})>"

    class Meta:
        verbose_name = 'Основные тексты для бота'
        verbose_name_plural = 'Основные тексты для бота'
        db_table = 'bot_info'
        managed = False


# пользователи
class User(models.Model):
    id = models.AutoField ('ID', primary_key=True)
    user_id = models.IntegerField ('ID пользователя')
    full_name = models.CharField ('Имя', max_length=255, null=True, blank=True)
    username = models.CharField ('Юзернейм', max_length=255, null=True, blank=True)
    last_visit = models.DateTimeField ('Последний визит', null=True, blank=True)
    phone = models.CharField ('Телефон', max_length=255, null=True, blank=True)

    def __str__(self):
        return f"<User({self.user_id})>"

    class Meta:
        verbose_name = 'Пользователь (бот)'
        verbose_name_plural = 'Пользователи (бот)'
        db_table = 'users'
        managed = False
