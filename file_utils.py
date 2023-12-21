import time
from os import listdir, path
from config import LOCAL_DIR, TIME_WATCH

file_storage = {}


def watch_files():
    while True:
        for file_name in listdir(LOCAL_DIR):
            if file_name not in file_storage.keys():
                file_storage[file_name] = path.getmtime(LOCAL_DIR + file_name)
            elif file_storage[file_name] < path.getmtime(LOCAL_DIR + file_name):
                print('файл изменился')

        time.sleep(float(TIME_WATCH))


watch_files()