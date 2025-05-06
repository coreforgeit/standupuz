from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, date, time

import random
import logging
import json

from .models import Event, Option, Info
from .data import days_of_week
from .utils import get_photo_url, get_photo_url_mob

day_str_format = '%d/%m'
time_str_format = '%H:%M'


class FoxView(APIView):
    def get(self, request, *args, **kwargs):
        logging.warning('rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
        try:
            weird_fox_quotes = [
                "Лиса не хитрая — она просто забыла, что хотела.",
                "Настоящая лиса не крадёт кур. Она их арендует по бартеру.",
                "Если лиса молчит — значит, у неё грузится Windows XP.",
                "Не всякая рыжая в лесу — лиса. Иногда это сбежавший парик.",
                "Лиса знает три пути: к норе, к холодильнику и обратно.",
                "Когда жизнь кидает палки в лапы — лиса делает из них костёр и жарит маршмеллоу.",
                "Лиса не врёт. Она тренирует альтернативные факты.",
                "Одинокая лиса — это просто кошка с дипломом философа.",
                "Лиса идёт одна не потому что гордая, а потому что потерялась.",
                "Настоящая лиса всегда с хвостом. Даже если это скотч."
            ]
            quotes = random.choice(weird_fox_quotes)
            logging.warning(quotes)

            # return Response(json.dumps({"text": quotes}), status=status.HTTP_200_OK)
            return Response({"text": quotes}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"text": str(e)}, status=status.HTTP_200_OK)


def home_page_redirect(request):
    return redirect('events')


# новые заказы
def events_view(request: HttpRequest):
    events = Event.objects.filter(is_active=True).order_by('event_date').all()
    info = Info.objects.get(id=1)
    card_data = []
    for event in events:
        option = Option.objects.filter(event_id=event.id).order_by('price').first()
        empty_options = Option.objects.filter(event_id=event.id, empty_place__gt=0).all()

        price = str(option.price) if option else '0'
        event: Event
        event_date: date = event.event_date
        event_time: time = event.event_time
        photo = get_photo_url(event.photo_id)
        card_data.append({
            'event_id': event.id,
            'photo_path': photo,
            'places': 1 if empty_options else 0,
            'date_str': event_date.strftime(day_str_format),
            'time_str': event_time.strftime(time_str_format),
            'day_str': days_of_week.get(event_date.weekday(), ''),
            'place': event.club or '',
            'min_amount': f'{price[:-3]} {price[-3:]}' if len(price) > 3 else price,
            'description': event.text.replace('\n', '<br>'),
            'tg_link': f'https://t.me/standupuz_bot?start={event.id}',
         }
        )

    context = {
        'cards': card_data,
        'phone': info.phone
    }
    return render(request, 'index_affiche.html', context)


def about_view(request: HttpRequest):
    info = Info.objects.get(id=1)
    context = {
        'phone': info.phone,
        'text': info.text,
    }
    return render(request, 'index_about.html', context)


# мобильная о мероприятии
def event_mob_view(request: HttpRequest, event_id):
    event = Event.objects.filter(id=event_id).first()
    info = Info.objects.get(id=1)
    empty_options = Option.objects.filter(event_id=event.id, empty_place__gt=0).all()
    card = {
        'photo_path': get_photo_url_mob(event.photo_id),
        'places': 1 if empty_options else 0,
        'description': event.text.replace('\n', '<br>'),
        'tg_link': f'https://t.me/standupuz_bot?start={event.id}',
         }
    context = {'card': card, 'phone': info.phone}
    return render(request, 'index_affiche_mob.html', context)
