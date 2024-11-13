import telebot

from standupuz_web.settings import TOKEN_BOT

bot = telebot.TeleBot(TOKEN_BOT, parse_mode='html')


# скачивает фото
def download_file(file_id: str, file_path: str) -> None:
    file_info = bot.get_file (file_id)
    photo_file = bot.download_file (file_info.file_path)

    with open (file_path, 'wb') as new_file:
        new_file.write (photo_file)
