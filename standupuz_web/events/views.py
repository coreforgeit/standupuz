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


 # path('api/event/', views.EventsListAPIView.as_view(), name='api-event-list'),
 #    path('api/event/<int:event_id>/', views.EventDetailAPIView.as_view(), name='api-event-detail'),
def build_card(ev: Event) -> dict:
    option = Option.objects.filter(event_id=ev.id).order_by('price').first()
    has_places = Option.objects.filter(event_id=ev.id, empty_place__gt=0).exists()
    price_str = str(option.price) if option else '0'

    return {
        'event_id':   ev.id,
        'photo_path': get_photo_url(ev.photo_id),
        'places':     1 if has_places else 0,
        'date_str':   ev.event_date.strftime(day_str_format),
        'time_str':   ev.event_time.strftime(time_str_format),
        'day_str':    days_of_week.get(ev.event_date.weekday(), ''),
        'place':      ev.club or '',
        'min_amount': f'{price_str[:-3]} {price_str[-3:]}' if len(price_str) > 3 else price_str,
        'description': ev.text.replace('\n', '<br>'),
        'tg_link':    f'https://t.me/standupuz_bot?start={ev.id}',
    }

class EventsListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(is_active=True).order_by('event_date')
        cards = [build_card(ev) for ev in events]
        return Response({'cards': cards}, status=status.HTTP_200_OK)


class EventDetailAPIView(APIView):
    def get(self, request, event_id, *args, **kwargs):
        try:
            ev = Event.objects.get(pk=event_id, is_active=True)
        except Event.DoesNotExist:
            return Response({'detail': 'Event not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        card = build_card(ev)
        return Response(card, status=status.HTTP_200_OK)



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
