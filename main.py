import time
from os import listdir, path

from config import TOKEN, LOCAL_DIR, YANDEX_DIR, TIME_WATCH
from disk_utils import YandexDisk

file_storage = {}


def main():
    ydisk = YandexDisk(TOKEN, YANDEX_DIR)
    while True:
        files_in_ydisk = ydisk.get_info()
        for file_name in listdir(LOCAL_DIR):

            if file_name not in file_storage.keys():
                file_storage[file_name] = path.getmtime(LOCAL_DIR + file_name)
                ydisk.load(f'{LOCAL_DIR}{file_name}')
            elif file_storage[file_name] < path.getmtime(LOCAL_DIR + file_name):
                file_storage[file_name] = path.getmtime(LOCAL_DIR + file_name)
                ydisk.reload(f'{LOCAL_DIR}{file_name}')
                print(f'файл {file_name} изменился')
            elif file_name not in files_in_ydisk and file_name in file_storage.keys():
                ydisk.delete(file_name)
                file_storage.pop(file_name)
                print(f'файл {file_name} удален')

        time.sleep(float(TIME_WATCH))


if __name__ == '__main__':
    main()

