from dotenv import load_dotenv
from os import getenv
from pytz import timezone
import os


load_dotenv ()
DEBUG = bool(int(getenv('DEBUG')))


class Config:
    if DEBUG:
        token = getenv ("TOKEN_TEST")
    else:
        token = getenv ("TOKEN")

    db_url = getenv('DB_URL')

    tz = timezone('Asia/Tashkent')
    day_form = '%d.%m'
    datetime_form = '%d.%m.%Y %H:%M'
    time_form = '%H:%M'

    file_google_path = os.path.join ('data', 'cred.json')
    data_path = 'data'
