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
