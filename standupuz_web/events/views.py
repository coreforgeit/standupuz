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
from .utils import get_photo_url
from standupuz_web.settings import DAY_STR_FORMAT, TIME_STR_FORMAT


def build_card(ev: Event) -> dict:
    option = Option.objects.filter(event_id=ev.id).order_by('price').first()
    has_places = Option.objects.filter(event_id=ev.id, empty_place__gt=0).exists()
    price_str = str(option.price) if option else '0'

    tg_link = ev.ticket_url if ev.ticket_url else f'https://t.me/standupuz_bot?start={ev.id}'

    return {
        'event_id':   ev.id,
        'title':   ev.title,
        'photo_path': get_photo_url(ev.id),
        'places':     1 if has_places else 0,
        'date_str':   ev.event_date.strftime(DAY_STR_FORMAT),
        'time_str':   ev.event_time.strftime(TIME_STR_FORMAT),
        'day_str':    days_of_week.get(ev.event_date.weekday(), ''),
        'place':      ev.club or '',
        'min_amount': f'{price_str[:-3]} {price_str[-3:]}' if len(price_str) > 3 else price_str,
        'description': ev.text.replace('\n', '<br>'),
        'tg_link':    tg_link,
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
            card = build_card(ev)
            return Response(card, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class InfoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        info = Info.objects.get(id=1)
        return Response({'phone': info.phone, 'text': info.text,})


# мобильная о мероприятии

# def event_mob_view(request: HttpRequest, event_id):
#     event = Event.objects.filter(id=event_id).first()
#     info = Info.objects.get(id=1)
#     empty_options = Option.objects.filter(event_id=event.id, empty_place__gt=0).all()
#     card = {
#         'photo_path': get_photo_url(event.id),
#         'places': 1 if empty_options else 0,
#         'description': event.text.replace('\n', '<br>'),
#         'tg_link': f'https://t.me/standupuz_bot?start={event.id}',
#          }
#     context = {'card': card, 'phone': info.phone}
#     return render(request, 'index_affiche_mob.html', context)

