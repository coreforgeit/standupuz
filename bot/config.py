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

    admin_group_id = int(os.getenv('ADMIN_GROUP_ID'))

    tz = timezone('Asia/Tashkent')
    day_form = '%d.%m'
    datetime_form = '%d.%m.%Y %H:%M'
    time_form = '%H:%M'

    google_key_path = os.path.join ('data', 'cred.json')
    google_table_id = os.getenv('GOOGLE_TABLE_ID')
    data_path = 'data'
