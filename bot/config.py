from dotenv import load_dotenv
from os import getenv
from pytz import timezone
import os


load_dotenv ()
DEBUG = bool(int(getenv('DEBUG')))


class Config:
    if DEBUG:
        token = getenv ("TOKEN_TEST")
        google_table_id = os.getenv('GOOGLE_TABLE_ID_TEST')
        admin_group_id = -1001669708234
    else:
        token = getenv ("TOKEN")
        google_table_id = os.getenv('GOOGLE_TABLE_ID')
        admin_group_id = int(os.getenv('ADMIN_GROUP_ID'))

    db_url = getenv('DB_URL')
    tz = timezone('Asia/Tashkent')
    day_form = '%d.%m'
    date_form = '%d.%m.%Y'
    datetime_form = '%d.%m.%Y %H:%M'
    time_form = '%H:%M'

    google_key_path = os.path.join ('data', 'cred.json')
    data_path = 'data'
