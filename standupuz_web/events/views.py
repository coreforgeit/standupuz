from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from datetime import datetime, date, time

from .models import Event, Option
from .data import days_of_week
from .utils import get_photo_url

import os
import logging

day_str_format = '%d/%m'
time_str_format = '%H:%M'


# новые заказы
def new_orders_view(request: HttpRequest):
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('request.META')
    for i in request.META:
        print(i)

    events = Event.objects.filter(is_active=True).all()
    print(f'len {len(events)}')
    card_data = []
    for event in events:
        option = Option.objects.filter(event_id=event.id).order_by('price').first()
        empty_options = Option.objects.filter(event_id=event.id, empty_place__gt=0).all()
        print(len(empty_options))

        price = str(option.price) if option else '0'
        event: Event
        event_date: date = event.event_date
        event_time: time = event.event_time
        card_data.append({
            'photo_path': get_photo_url(event.photo_id),
            'places': 1 if empty_options else 0,
            'date_str': event_date.strftime(day_str_format),
            'time_str': event_time.strftime(time_str_format),
            'day_str': days_of_week.get(event_date.weekday(), ''),
            'place': 'Steam Bar',
            'min_amount': f'{price[:-3]} {price[-3:]}' if len(price) > 3 else price,
            'description':
                '🔥Стендап в пабе Понаехали🍻\n\nОтмечаем праздники и приглашаем всех провести веселый, '
                'летний вечер вторника с иностранным стендапером Денисом Комовым!\n\nОткрытый микрофон - '
                'это горнило юмора, основа комедии, зачатие шуток, это база. Профессиональные и начинающие '
                'артисты приходят сюда проверить новый материал, себя и просто повеселиться!\n\n'
                'Это настоящий андерграунд в баре! Приглашайте друзей, мы будем рады всем!🤗',
         }
        )

    # context = {'cards': {'card_data': card_data}}
    context = {'cards': card_data}
    return render(request, 'index_affiche.html', context)


def orders_view(request: HttpRequest):

    context = {}
    return render(request, 'index_about.html', context)
