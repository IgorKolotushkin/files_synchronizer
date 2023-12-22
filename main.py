import logging
import time
from os import listdir, path

from config import TOKEN, LOCAL_DIR, YANDEX_DIR, TIME_WATCH
from disk_utils import YandexDisk

logger: logging.Logger = logging.getLogger(__name__)


def get_local_files(local_dir: str):
    file_storage = {}
    for file_name in listdir(local_dir):
        if file_name not in file_storage.keys():
            file_storage[file_name] = path.getmtime(local_dir + file_name)

    return file_storage


def upload_files(local_dir: str, files: set, ydisk: YandexDisk):
    for file in files:
        ydisk.load(f'{local_dir}{file}')


def update_files(file_storage: dict, updated_storage: dict, ydisk: YandexDisk):
    for file in file_storage:
        if file_storage[file] < updated_storage[file]:
            ydisk.reload(f'{LOCAL_DIR}{file}')
            logger.info(f'Файл {file} перезаписан')


def delete_files(files_for_delete: set, file_storage: dict, ydisk: YandexDisk):
    for file in files_for_delete:
        ydisk.delete(file)
        logger.info(f'Файл {file} удален')
        file_storage.pop(file)

    return file_storage


def main():
    ydisk = YandexDisk(TOKEN, YANDEX_DIR)
    file_storage = get_local_files(LOCAL_DIR)
    upload_files(LOCAL_DIR, set(file_storage), ydisk)

    while True:
        updated_storage = get_local_files(LOCAL_DIR)
        if len(updated_storage) > len(file_storage):
            new_files = updated_storage.keys() - file_storage.keys()
            for file in new_files:
                file_storage[file] = path.getmtime(LOCAL_DIR + file)
                ydisk.load(f'{LOCAL_DIR}{file}')

        if len(updated_storage) < len(file_storage):
            files_for_delete = file_storage.keys() - updated_storage.keys()
            file_storage = delete_files(files_for_delete, file_storage, ydisk)
        else:
            update_files(file_storage, updated_storage, ydisk)
            file_storage = updated_storage

        time.sleep(float(TIME_WATCH))


if __name__ == '__main__':
    logging.basicConfig(
        filename='logs.log',
        level=logging.INFO,
        format="%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s",
    )
    main()

