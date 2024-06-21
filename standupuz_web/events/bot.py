from django.test import TestCase

import telebot
import os

from standupuz_web.settings import BASE_DIR, TOKEN_BOT, MEDIA_ROOT

bot = telebot.TeleBot(TOKEN_BOT, parse_mode='html')


# скачивает фото
def download_file(file_id: str, file_path: str) -> None:
    # file_path = os.path.join (MEDIA_ROOT, f'{file_id}.jpg')
    file_info = bot.get_file (file_id)
    photo_file = bot.download_file (file_info.file_path)

    with open (file_path, 'wb') as new_file:
        new_file.write (photo_file)
