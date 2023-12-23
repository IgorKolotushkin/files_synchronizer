import os
import configparser

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, т.к отсутствует файл .env")
else:
    load_dotenv()

config = configparser.ConfigParser()
config.read('config.ini')

YANDEX_DIR = config['settings']['path_folder_disk']
LOCAL_DIR = config['settings']['path_local_folder']
TIME_WATCH = config['settings']['time_watch']
LOG_PATH = config['settings']['log_file_path']
TOKEN: str = os.getenv("TOKEN")

if not TOKEN:
    exit('Токен не указан')
if not YANDEX_DIR:
    exit("В файле config.ini не указано название папки на Яндекс Диске")
if not LOCAL_DIR:
    exit("В файле config.ini не указан путь к локальной папке")
if not LOG_PATH:
    exit("В файле config.ini не указан путь к папке для хранения логов")
if not TIME_WATCH:
    exit("В файле config.ini не указан период синхронизации")

