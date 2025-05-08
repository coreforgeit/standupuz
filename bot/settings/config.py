from pytz import timezone
import os


class Config:
    debug = bool(int(os.getenv('DEBUG')))

    if debug:
        token = os.getenv ("TOKEN_TEST")
        google_table_id = os.getenv('GOOGLE_TABLE_ID_TEST')
        admin_group_id = -1001669708234
        photo_default = 'AgACAgIAAxkBAAIZ_2gUuLrNeqcp3rrc4EVFQ4TqQ6xeAAI58DEbRdSpSOA0drmJIeU3AQADAgADeAADNgQ'

    else:
        token = os.getenv ("TOKEN")
        google_table_id = os.getenv('GOOGLE_TABLE_ID')
        admin_group_id = int(os.getenv('ADMIN_GROUP_ID'))
        photo_default = 'AgACAgIAAxkBAAMDZJLz5wR0skvRu9z8XLdrFaYsz80AAvzOMRuk6phIPY914z_9bZoBAAMCAANtAAMvBA'

    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('POSTGRES_DB')
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_url = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT')

    # db_url = getenv('DB_URL')
    tz = timezone('Asia/Tashkent')
    day_form = '%d.%m'
    date_form = '%d.%m.%Y'
    datetime_form = '%d.%m.%Y %H:%M'
    time_form = '%H:%M'

    data_path = 'data'
    google_key_path = os.path.join (data_path, 'cred.json')
    photo_path = os.path.join (data_path, 'photo')


conf: Config = Config()
