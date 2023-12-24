import os

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, т.к отсутствует файл .env")
else:
    load_dotenv()


YANDEX_DIR: str = os.getenv("YANDEX_DIR")
LOCAL_DIR: str = os.getenv("LOCAL_DIR")
TIME_WATCH: str = os.getenv("TIME_WATCH")
LOG_PATH: str = os.getenv("LOG_PATH")
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

